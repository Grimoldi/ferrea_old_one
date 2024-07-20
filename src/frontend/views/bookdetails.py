
from rest_framework.views import APIView
from django.shortcuts import render, redirect
import os
from backend.views import ReadBook


class BookDetails(APIView):
    '''BookDetails This class handles the request to retrieve details about a single book.

    This class handles the request to retrieve details about a single book.
    The book is identified by its isbn, so the info provided could touch also the single copy of the book.
    '''

    def __init__(self):
        '''__init__ Constructor

        Constructor of the class
        '''
        self._template_path = "../templates/pages"
        self._err_key = "error_msg"
        self._success_key = "success_msg"

    def get(self, request, isbn, data=None, format=None):
        '''get book details

        This method override the get method.
        It simply render the template, adding an error msg if found in session.

        Args:
            request (HTTPRequest): the request object
            isbn (string): isbn of the book to get
            data (dict, optional): optional additional data to be rendered in the page.
            Defaults to None.
            format (string, optional): format of the response to provide (json, xml...). Defaults to None.

        Returns:
            HTTPResponse: the rendering of the template page.
        '''

        view = ReadBook()
        book = view.get(request=request, isbn=isbn)

        template_page = 'book_detail.html'
        template = os.path.join(self._template_path, template_page)

        context = {
            "error_msg": request.session.get(self._err_key, ""),
            "book": book.data["book"],
            "user": request.session["user"],
            "success_msg": request.session.get(self._success_key, ""),
        }

        return render(request, template, context)
