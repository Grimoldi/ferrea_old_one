
from rest_framework.views import APIView
from django.shortcuts import render, redirect
import os
from backend.views import ManageReserveUser2Book


class ReserveBook(APIView):
    '''ReserveBook This class handles the request to create a new RESERVE relationship.

    This class handles the request to reserve a certain book for the login user.
    '''

    def __init__(self):
        '''__init__ Constructor

        Constructor of the class
        '''
        self._err_key = "error_msg"
        self._success_key = "success_msg"

    def post(self, request, format=None):
        '''post This method handles the request of creation of the reservation.

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
        context = dict()
        context["user"] = request.session["user"]

        user_from_post = request.data["username"]
        barcode_from_post = request.data["barcode"]
        is_same_user = context["user"] == user_from_post

        if not is_same_user:
            context[self._err_key] = "Are you trying to hacking me?"
            request.session[self._err_key] = "Are you trying to hacking me?"
            return redirect('/search_book')

        view = ManageReserveUser2Book()
        book_reserve_result = view.post(
            request=request,
        )
        is_read_successfull = book_reserve_result.status_code == 200

        if is_read_successfull:
            has_previous_error = self._err_key in request.session
            if has_previous_error:
                request.session.pop(self._err_key)

            context[self._success_key] = "Book correctly reserved"
            request.session[self._success_key] = "Book correctly reserved"

        else:
            print(book_reserve_result.data)
            request.session.pop(self._success_key)
            request.session[self._err_key] = book_reserve_result.data[self._err_key]

        return redirect('/search_book')
