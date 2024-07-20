
from rest_framework.views import APIView
from frontend.models import LoginForm
from django.shortcuts import render, redirect
import os
from authentication.views import LogoutUser


class Logout(APIView):
    '''Logout This class handles the logout request.

    This class handles the request to logout the user.
    It returns to the login page.
    '''

    def __init__(self):
        '''__init__ Constructor

        Constructor of the class
        '''

    def get(self, request, format=None):
        '''get This method handles the logout request.

        This method override the get method.

        Args:
            request (HTTPRequest): the request object.
            format (string, optional): format of the response to provide (json, xml...). Defaults to None.

        Returns:
            HttpResponsePermanentRedirect: to login page.
        '''
        view = LogoutUser()
        view.post(request)

        return redirect('/login')
