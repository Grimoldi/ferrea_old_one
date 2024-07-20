
from neomodel import db
from backend.models import (
    Book,
    User,
)

from rest_framework import status
from rest_framework.response import Response


class DeleteReserveDao():
    '''DeleteReserveDao This class handles the deletion of a reserve relationship on data db (Neo4J).

    This class controls how a reserve relationship is delete from db
    (User)-[RESERVE]->(Book)
    The class expose the following methods:

    - delete_reserve

    '''

    def __init__(self):
        '''__init__ Constructor

        Constructor of the class
        '''
        pass

    def delete_reserve(self, username, barcode):
        '''delete_reserve This method deletes the relationship RESERVE between user node and book node.

        This method takes username and barcode as parameters.
        It search for a relationship of type RESERVE between the given user and book, and then drops it.

        Args:
            username (string): id of the user.
            barcode (string): id of the book.

        Returns:
            HTTPResponse: dictionary with the result of the operations.
            The body is under the key "msg" or "error_msg".
        '''

        try:
            db.begin()
            user_node = User.nodes.get(username__exact=username)
            book_node = Book.nodes.get(barcode__exact=barcode)

            user_node.reserve.disconnect(book_node)
            book_node.is_reservable = True
            book_node.save()
            db.commit()

            data = Response({'msg': "Reservation canceled"},
                            status=status.HTTP_200_OK)

        except Exception as e:
            db.rollback()
            data = Response(
                {'msg': "Reservation cancellation failed",
                    'error_msg': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return data
