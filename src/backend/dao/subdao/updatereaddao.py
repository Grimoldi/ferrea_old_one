

from rest_framework import status
from rest_framework.response import Response
from neomodel import db
from datetime import datetime


class UpdateReadDao():
    '''UpdateReadDao This class handles any update to READ relationships.

    This class handles how a READ relationship can be modified.
    The update mainly means that the user has returned the book
    The relationship is updated with the .to attribute
    (User)-[READ]->(Book)
    The class expose the following methods:

    - update_read
    '''

    def __init__(self):
        '''__init__ Constructor

        Constructor of the class
        '''
        pass

    def update_read(self, username, barcode, when=None):
        '''update_read This method performs the update of the relationship.

        This method implements the change through querying the data db (Neo4J).

        Args:
            username (string): id of the user.
            barcode (string): id of the book.
            when (datetime.datetime, optional): datetime of when the user return the book. Defaults to None.

        Returns:
            HTTPResponse: dictionary with the result of the operations.
            The body is under the key "msg" or "error_msg".
        '''
        now = datetime.now()
        if when is not None:
            now = when

        query = (
            "MATCH (u:User {username: $username})-[r:READ]->(b:Book {barcode: $barcode}) "
            "SET r.to = $now, "
            "b.is_readable = True "
            "return u, r, b"
        )
        params = {
            "username": username,
            "barcode": barcode,
            "now": now,
        }

        try:
            books_count = db.cypher_query(query, params=params)
            data = Response(
                {'msg': "Update done"},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            data = Response(
                {'msg': "Update failed", 'error_msg': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return data
