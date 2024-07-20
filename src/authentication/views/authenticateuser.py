
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from authentication.dao import (
    ReadUserCredentials,
    ReadIfSuperuser,
)


class AuthenticateUser(APIView):
    '''AuthenticateUser This class handles the view for user's authention

    This class extends APIView class.
    The class override the following methods:

    - post: try to log a user in
    - get: check if a user is a superuser (librarian)

    '''

    def __init__(self):
        '''__init__ Constructor

        Constructor of the class
        '''
        pass

    def post(self, request, format=None):
        '''post This method verifies if a user has the rights to login.

        This method override the post method of the super class.
        It create an instance of the authentication.dao.ReadUserCredentials class and
        return the result to the caller.
        The authentication is done towards the authentication backend (MySQLLite).

        Args:
            request (HTTPRequest): the request object

            format (string, optional): format of the response to provide (json, xml...). Defaults to None.


        Returns:
            HTTPResponse: object returned from the dao.
        '''
        is_a_key_missing = (
            "username" not in request.data.keys()
            or "password" not in request.data.keys()
        )
        if is_a_key_missing:
            data = Response(
                {"error_msg": "At least a key between 'username' and 'password' is missing"},
                status=status.HTTP_400_BAD_REQUEST
            )
            return data

        username = request.data["username"]
        password = request.data["password"]

        dao = ReadUserCredentials(
            username=username, password=password, request=request)
        return dao.check_credentials()

    def get(self, request, format=None):
        '''get This method verifies if a user has the superuser rights.

        This method override the get method of the super class.
        It create an instance of the authentication.dao.ReadIfSuperuser class and
        return the result to the caller.
        The check is done towards the authentication backend (MySQLLite).

        Args:
            request (HTTPRequest): the request object
            format (string, optional): format of the response to provide (json, xml...). Defaults to None.


        Returns:
            HTTPResponse: object returned from the dao.
        '''
        is_a_key_missing = (
            "username" not in request.data.keys()
        )
        if is_a_key_missing:
            data = Response(
                {"error_msg": "The key 'username' is missing"},
                status=status.HTTP_400_BAD_REQUEST
            )
            return data

        username = request.data["username"]

        dao = ReadIfSuperuser(username=username)

        return dao.check_if_superuser()
