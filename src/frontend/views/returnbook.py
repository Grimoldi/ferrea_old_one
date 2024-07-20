
from rest_framework.views import APIView
from django.shortcuts import render, redirect
import os
from backend.views import ManageReadUser2Book


class ReturnBook(APIView):
    '''ReturnBook This class handles the request to update a READ relationship.

    This class handles the request to return a book to the library.
    '''

    def __init__(self):
        '''__init__ Constructor

        Constructor of the class
        '''
        self._err_key = "error_msg"
        self._success_key = "success_msg"

    def put(self, request, format=None):
        '''post This method handles the request of update of the read.

        This method override the post method.
        It calls the backend view in order to update the relationship on data db (Neo4J).
        Finally, it redirects to the lends page.

        Args:
            request (HTTPRequest): the request object
            format (string, optional): format of the response to provide (json, xml...). Defaults to None.

        Returns:
            HttpResponsePermanentRedirect: to search page.
        '''
        barcode_from_post = request.data["barcode"]

        view = ManageReadUser2Book()
        book_return_result = view.put(
            request=request,
        )
        is_return_successfull = book_return_result.status_code == 200

        if is_return_successfull:
            has_previous_error = self._err_key in request.session
            if has_previous_error:
                request.session.pop(self._err_key)

            request.session[self._success_key] = "Book correctly returned"

        else:
            request.session.pop(self._success_key, "")
            request.session[self._err_key] = book_return_result.data.get(
                self._err_key, "")

        return redirect('/list_lends')
