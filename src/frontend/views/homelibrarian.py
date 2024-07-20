
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import render, redirect
import os
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeLibrarian(LoginRequiredMixin, APIView):
    '''HomeLibrarian This class handles the rendering of the HomePage for librarian.

    This class handles the graphic rendering of the librarian home page.
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
            request (HTTPRequest): the request object
            data (dict, optional): optional additional data to be rendered in the page. Defaults to None.
            format (string, optional): format of the response to provide (json, xml...). Defaults to None.

        Returns:
            HTTPResponse: renders the template page
        '''
        self._request = request
        self._username = request.session["user"]

        if "book" in request.session.keys():
            request.session.pop("book")
        if "isbn" in request.session.keys():
            request.session.pop("isbn")

        template_page = 'librarian.html'
        template = os.path.join(self._template_path, template_page)
        context = {
            "error_msg": request.session.get("error_msg", ""),
            "user": request.session["user"],
        }

        return render(request, template, context)
