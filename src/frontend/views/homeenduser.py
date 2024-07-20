
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import render, redirect
import os
from django.contrib.auth.mixins import LoginRequiredMixin
from backend.views import (
    ReadLists,
    ReadSuggestion,
)
from random import choice


class HomeEndUser(LoginRequiredMixin, APIView):
    '''HomeEndUser This class handles the rendering of the HomePage for end user.

    This class handles the graphic rendering of the end user home page.
    It calls several views from the backend in order to provide the template all the data needed.
    '''

    def __init__(self):
        '''__init__ Constructor

        Constructor of the class
        '''
        self._template_path = "../templates/pages"
        self._request = None
        self._username = ""

    def get(self, request, data=None, format=None):
        '''get This method renders the home page.

        This method override the get method.
        Its function is to graphically renders the end user home page.

        Args:
            request (HTTPRequest): the request object.
            data (dict, optional): optional additional data to be rendered in the page. Defaults to None.
            format (string, optional): format of the response to provide (json, xml...). Defaults to None.

        Returns:
            HTTPResponse: the rendering of the template page.
        '''
        self._request = request
        self._username = request.session["user"]

        random_books = self._get_random_book()
        suggested_books = self._get_suggested_books()
        suggested_authors = self._get_suggested_authors()

        template_page = 'home.html'
        template = os.path.join(self._template_path, template_page)
        context = {
            "error_msg": request.session.get("error_msg", ""),
            "rand_books": random_books,
            "sugg_authors": suggested_authors.data,
            "sugg_books": suggested_books.data,
            "user": request.session["user"],
        }

        return render(request, template, context)

    def _get_suggested_books(self):
        '''_get_suggested_books This method retrieve the suggested books to be displayed.

        This private method calls the public method get from the view, in order to retrieve the suggested books.

        Returns:
            HTTPResponse: the reponse from the view.
        '''
        view = ReadSuggestion()
        suggested_book_get = view.get(
            request=self._request,
            username=self._username,
            what="book"
        )

        return suggested_book_get

    def _get_suggested_authors(self):
        '''_get_suggested_authors This method retrieve the suggested authors to be displayed.

        This private method calls the public method get from the view, in order to retrieve the suggested authors.

        Returns:
            HTTPResponse: the reponse from the view.
        '''
        view = ReadSuggestion()
        suggested_author_get = view.get(
            request=self._request,
            username=self._username,
            what="author"
        )

        return suggested_author_get

    def _get_random_book(self):
        '''_get_random_book This method retrieve some random books to be displayed.

        This private method calls the public method get from the view, in order to retrieve a bunch of random books.

        Returns:
            HTTPResponse: the reponse from the view.
        '''
        view = ReadLists()
        book_list = view.get(
            request=self._request,
            listname="preview"
        )
        book_list = book_list.data["response"]["data"]

        book_sublist = list()
        size = len(book_list.keys())
        for index in range(0, 5):
            random_book = choice(list(book_list.values()))
            book_sublist.append(random_book)

        return book_sublist
