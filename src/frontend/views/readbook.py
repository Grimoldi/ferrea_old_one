
from rest_framework.views import APIView
from django.shortcuts import render, redirect
import os
from backend.views import ManageReadUser2Book


class ReadBook(APIView):
    '''ReadBook This class handles the request to create a new READ relationship.

    This class handles the request to read a certain book from the login user.
    '''

    def __init__(self):
        '''__init__ Constructor

        Constructor of the class
        '''
        self._template_path = "../templates/pages"
        self._err_key = "error_msg"
        self._success_key = "success_msg"

    def post(self, request, format=None):
        '''post This method handles the request of creation of the read.

        This method override the post method.
        Its function is to check that the user received is the same as the logged in user.
        It then calls the backend view in order to create the relationship on data db (Neo4J).
        Finally, it redirects to the search page.

        Args:
            request (HTTPRequest): the request object
            format (string, optional): format of the response to provide (json, xml...). Defaults to None.

        Returns:
            HttpResponsePermanentRedirect: to search page.
        '''

        template_page = 'search.html'
        template = os.path.join(self._template_path, template_page)

        user_from_post = request.data["username"]
        is_same_user = request.session["user"] == user_from_post

        if not is_same_user:
            request.session[self._err_key] = "Are you trying to hacking me?"
            return redirect('/search_book')

        view = ManageReadUser2Book()
        book_read_result = view.post(
            request=request,
        )
        is_read_successfull = book_read_result.status_code == 200

        if is_read_successfull:
            has_previous_error = self._err_key in request.session
            if has_previous_error:
                request.session.pop(self._err_key)

            request.session[self._success_key] = "Book correctly read"

        else:
            request.session.pop(self._success_key)
            request.session[self._err_key] = book_read_result.data[self._err_key]

        return redirect('/search_book')
