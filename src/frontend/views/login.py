
from rest_framework.views import APIView
from frontend.models import LoginForm
from django.shortcuts import render, redirect
import os
from authentication.views import AuthenticateUser


class Login(APIView):
    '''Login This class handles the rendering of the login page and the request to log the user in.

    This class handles two different type of request:
    - the graphical rendering of the login page
    - the submit of the credentials in order to log in
    '''

    def __init__(self):
        '''__init__ Constructor

        Constructor of the class
        '''
        self._template_path = "../templates/pages"
        self._err_key = "error_msg"

    def post(self, request, format=None):
        '''post This method handles the credentials submit.

        This method override the post method.
        Its function is to accept the credentials, check if correct and if the user is an end user or not.
        Based on the results, it could redirect to the following pages:
        - login page (invalid credentials)
        - home page end user (valid credentials, end user type)
        - home page librarian (valid credentials, superuser type)

        Args:
            request (HTTPRequest): the request object
            format (string, optional): format of the response to provide (json, xml...). Defaults to None.

        Returns:
            HttpResponsePermanentRedirect: to home page or back to login page if credentials are incorrect.
        '''
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            view = AuthenticateUser()
            authenticate_to_db = view.post(request)
            read_if_librarian = view.get(request)
            is_login_successfull = authenticate_to_db.status_code == 200
            is_superuser_check_successfull = read_if_librarian.status_code == 200

            is_preliminary_check_successfull = is_login_successfull and is_superuser_check_successfull

            if is_preliminary_check_successfull:
                has_previous_error = self._err_key in request.session
                if has_previous_error:
                    request.session.pop(self._err_key)

                # saving user in current session, in order to access it in the future
                request.session["user"] = request.data["username"]

                is_librarian = read_if_librarian.data["msg"]
                if not is_librarian:

                    return redirect("/home")
                else:
                    return redirect("/librarian")

            else:
                request.session[self._err_key] = "Unable to login due to incorrect credentials"
                request.session["pretend_username"] = request.data["username"]

                return redirect('/login')

    def get(self, request, data=None, format=None):
        '''get This method renders the login page.

        This method override the get method.
        Its function is to graphically renders the page.

        Args:
            request (HTTPRequest): the request object.
            data (dict, optional): optional additional data to be rendered in the page. Defaults to None.
            format (string, optional): format of the response to provide (json, xml...). Defaults to None.

        Returns:
            HTTPResponse: the rendering of the template page.
        '''
        template_page = 'login.html'
        template = os.path.join(self._template_path, template_page)

        context = {
            self._err_key: request.session.get(self._err_key, ""),
            "form": LoginForm(data={
                "username": request.session.get("pretend_username", ""),
            })
        }

        return render(request, template, context)
