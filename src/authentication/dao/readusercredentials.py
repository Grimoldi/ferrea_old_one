
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class ReadUserCredentials():
    '''ReadUserCredentials This class handles user's authention to backend (MySqlLite)

    This class extends APIView class.
    The class exposes the following method:

    - check_credentials

    '''

    def __init__(self, username, password, request):
        '''__init__ Constructor

        Constructor of the class

        Args:
            username (string): username to be authenticated

            password (string): password of the user

            request (HTTPRequest): the request object
        '''
        self._username = username
        self._password = password
        self._request = request

    def check_credentials(self):
        '''check_credentials This method verify if the user exists and authenticate him

        This method will query the authentication backend (MySqlLite) and verify if the user exists.
        It then tries to authenticate him.
        If everything works just fine, it logs he in.

        Returns:
            HTTPResponse: dictionary with a message.
            The body is under the key "msg" or "error_msg".
        '''
        user = authenticate(
            username=self._username, password=self._password)
        is_user_authenticate = user is not None

        if is_user_authenticate:
            try:
                login(self._request, user)
                data = Response(
                    {
                        "msg": "User authenticated correctly",
                    },
                    status=status.HTTP_200_OK,
                )

            except Exception as e:
                data = Response(
                    {"error_msg": "Unable to login the user due to %s" % e},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
                return data

        else:
            data = Response(
                {"error_msg": "Unable to authenticate user"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return data
