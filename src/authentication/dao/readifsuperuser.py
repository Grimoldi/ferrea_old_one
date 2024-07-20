
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User


class ReadIfSuperuser():
    '''ReadIfSuperuser This class handles the check if the user has superuser (librarian) privileges.

    This class extends APIView class.
    The class exposes the following method:

    - check_if_superuser: this enables to check if a user has superuser (librarian) privileges.
    '''

    def __init__(self, username):
        '''__init__ Constructor

        Constructor of the class

        Args:
            username (string): username to be checked.
        '''
        self._username = username

    def check_if_superuser(self):
        '''check_if_superuser The method uses the class attribute username to retrieve if the user is superuser or not

        This method query the authorization backend (MySqlLite) in order to the check if the user is a librarian.

        Returns:
            HTTPResponse: dictionary of user's read book and its status code.
            The body is under the key "msg" or "error_msg".
        '''
        current_user = User.objects.filter(
            username=self._username)
        is_user_existing = len(current_user) > 0

        if is_user_existing:
            is_superuser = current_user[0].is_superuser
            data = Response(
                {
                    "msg": is_superuser,
                },
                status=status.HTTP_200_OK,
            )

        else:
            data = Response(
                {"error_msg": "Unable to find user"},
                status=status.HTTP_404_NOT_FOUND,
            )
        return data
