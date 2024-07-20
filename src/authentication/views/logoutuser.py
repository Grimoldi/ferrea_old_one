
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from django.contrib.auth import logout


class LogoutUser(APIView):
    '''LogoutUser This class handles the request to logout user

    This class extends APIView class.
    The class override the following methods:

    - post: try to log a user out

    '''

    def __init__(self):
        '''__init__ Constructor

        Constructor of the class
        '''
        pass

    def post(self, request, format=None):
        '''post This method logout a user from the webapp.

        The method implements the Django logout function.
        It also drops any key related to the user in the request.session

        Args:
            request (HTTPRequest): the request object

            format (string, optional): format of the response to provide (json, xml...). Defaults to None.

        Returns:
            HTTPResponse: dictionary with a message.
            The body is under the key "msg".
        '''

        logout(request)
        user_keys = "user"
        is_user_logged_in_session = user_keys in request.session.keys()
        if is_user_logged_in_session:
            request.session.drop(user_keys)

        return Response(
            {"msg": "User logout successfully"},
            status=status.HTTP_200_OK
        )
