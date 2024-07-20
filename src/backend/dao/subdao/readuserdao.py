
from neomodel import db

from rest_framework import status
from rest_framework.response import Response
from .readnodedao import ReadNodeDao


class ReadUserDao():
    '''ReadUserDao This class handles the read of a user node on db

    This class expose a method in order to search on the db for a specific user node.
    This class expose the following methods:

    - read_user
    '''

    def __init__(self):
        '''__init__ Constructor

        Constructor of the class
        '''
        pass

    def read_user(self, username):
        '''read_user This method performs the search

        This method will recieve in input a username and performs the search.

        Args:
            username (string): the username of the user

        Returns:
            HTTPResponse: dictionary of user's read book and its status code.
        '''

        query = (
            "MATCH (u:User {username: $username}) "
            "return u"
        )
        params = {
            'username': username,
        }

        try:
            dao = ReadNodeDao()
            user = dao.fetch_node_details(
                node_info={'node_type': "User", 'node_id': username}
            )

            user['node_properties']. pop("location")
            user = user['node_properties']
            return Response(user, status=status.HTTP_200_OK)

        except Exception as e:
            data = Response(
                {'msg': "Unable to search for user", 'error_msg': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return data
