
from datetime import datetime
from neomodel import db
from backend.models import (
    Book,
    User,
)

from rest_framework import status
from rest_framework.response import Response


class CreateReserveDao():
    '''CreateReserveDao This class handles the creation of a reserve relationship on data db (Neo4J).

    This class controls how a reserve relationship is created on db.
    (User)-[RESERVE]->(Book)
    The class expose the following methods:

    - create_reserve: to create a new reserve relationship.

    '''

    def __init__(self):
        '''__init__ Constructor

        Constructor of the class
        '''
        pass

    def create_reserve(self, username, barcode, when=None):
        '''create_reserve This method creates the relationship RESERVE between user node and book node.

        This method takes barcode and username as parameters, then it creates the relationship RESERVE.
        Since the user can only have ONE reservation at a time
        on the book, I used neomodel models, since they allow only
        a single relationship of the same between the same pair of nodes

        The status on the book is forced to unavailable since no other
        user can borrow the book

        Args:
            username (string): id of the user.
            barcode (string): id of the book.
            when (datetime.datetime): datetime object to add on the relationship.

        Returns:
            HTTPResponse: dictionary with the result of the operations.
            The body is under the key "msg" or "error_msg".
        '''
        query = (
            "match (b:Book {barcode:$barcode})<-[r:RESERVE]-(u:User) "
            "return count(r)"
        )
        params = {"barcode": str(barcode), }

        try:
            book_s_reservation = db.cypher_query(query, params=params)
            is_book_already_reserved = book_s_reservation[0][0][0] > 0

        except Exception as e:
            data = Response(
                {'error_msg': "Reservation failed", 'det': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            return data

        if not is_book_already_reserved:
            try:
                user_node = User.nodes.get(username__exact=username)
                book_node = Book.nodes.get(barcode__exact=barcode)

                db.begin()
                book_node.status = "Unavailable"
                book_node.is_reservable = False
                book_node.save()
                rel = user_node.reserve.connect(book_node)

                if when is not None:
                    rel.on = when
                db.commit()

                data = Response({'msg': "Reservation done"},
                                status=status.HTTP_200_OK)

            except Exception as e:
                db.rollback()
                data = Response(
                    {'error_msg': "Reservation failed", 'det': str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            data = Response(
                {'error_msg': "Book is already reserved by another user, couldn't reserve it."},
                status=status.HTTP_403_FORBIDDEN
            )

        return data
