
from rest_framework.views import APIView
from frontend.models import UserForm
from django.shortcuts import render, redirect
import os
from backend.views import ManageUser


class UserProfile(APIView):
    '''UserProfile This class handles the rendering and the editing of a user profile.

    This class exposes two methods.

    - Get: for rendering of user profile through a form
    - Post: to update the user profile
    '''

    def __init__(self):
        '''__init__ Constructor

        Constructor of the class
        '''
        self._template_path = "../templates/pages"
        self._success_key = "success_msg"
        self._err_key = "error_msg"

    def get(self, request, username, data=None, format=None):
        '''get Get method for rendering of user profile.

        This method overrides the get of the super class.
        Its function is to renders the form with the data fetched from the backend.
        Note that the backend with user data is Neo4j and not MySqlLite.

        Args:
            request (HTTPRequest): the request object.
            data (dict, optional): optional additional data to be rendered in the page. Defaults to None.
            format (dict, optional): format of the response to provide (json, xml...). Defaults to None.

        Returns:
            HTTPResponse: the rendering of the template page.
        '''
        is_same_user = username == request.session["user"]
        if not is_same_user:
            request.session[self._err_key] = "Are you trying to hacking me?"
            return redirect(f'/user_profile/{request.session["user"]}')

        template_page = 'profile.html'
        template = os.path.join(self._template_path, template_page)

        dao = ManageUser()
        user = dao.get(request=request, username=username)
        is_user_successfull = user.status_code == 200

        if is_user_successfull:
            user = user.data["user"]
            context = {
                self._err_key: request.session.get(self._err_key, ""),
                "user": request.session["user"],
                "form": UserForm(data={
                    "username": request.session["user"],
                    "email": user["email"],
                    "name": user["name"],
                    "surname": user["surname"],
                    "address": user["address"],
                    "city": user["city"],
                    "phone": user["phone"],
                    "card_number": user["card_number"],
                })
            }

        return render(request, template, context)

    def post(self, request, format=None):
        '''post This method perform the edit of the profile

        This method override the post method of the super class.
        It calls the backend view to modify the profile according to
        the data passed through the form

        Args:
            request (HTTPRequest): the request object
            format (dict, optional): format of the response to provide (json, xml...). Defaults to None.

        Returns:
            HttpResponsePermanentRedirect: to user's profile page..
        '''

        # create a form instance and populate it with data from the request:
        form = UserForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            view = ManageUser()
            user_update_result = view.post(
                request=request,
            )
            is_update_successfull = user_update_result.status_code == 200

            if is_update_successfull:
                request.session.pop(self._err_key, "")

            else:
                request.session[self._err_key] = user_update_result.data[self._err_key]

        else:
            request.session[self._err_key] = "Form is not valid"

        return redirect(f'/user_profile/{request.session["user"]}')
