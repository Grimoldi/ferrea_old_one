
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime
from neomodel import db


class ReadUsersBooksDao():
    '''ReadUsersBooksDao This class handles the lookup for how many books is user currently holding.

    This class handles the lookup for how many books is the user currently holding.
    Note that for this count both reserved books and books currently in reading (not yet returned.)
    (User)-[READ {to:None}]->(Book)
    (User)-[RESERVE]->(Book)
    Count(READ) + Count(RESERVE)

    This class expose the following methods:

    - read_users_books
    '''

    def __init__(self):
        '''__init__ Constructor

        Constructor of the class
        '''
        pass

    def read_users_books(self, username, barcode):
        '''read_users_books This method returns the number of book being hold by user.

        This method reads on the db how many books the user is currently holding.
        The count is both as reservation and reading (but not yet returned).
        From the count it's excluded the book if the user has made a reservation for it
        and is asking to borrow (read) it.

        eg:
        Bob reseve book 1 and book 2, and is currently reading book 3
        If he wants to read (borrow from library) book 1,
        the count should return 2 and not 3 (he has already asked for book 1),
        in order to convert the reserve relationship into a read relationship

        If he wants to reserve/read book 4, however, the counter should return 3

        Args:
            username (string): id of the user.
            barcode (string): id of the book.

        Returns:
            HTTPResponse: dictionary with the result of the operations.
            The body is under the key "count" or "error_msg".
        '''
        query = (
            "MATCH (u:User {username: $username})-[r]->(b:Book) "
            "where "
            "( "
            "type(r) = $reserve_rel AND b.barcode <> $barcode "
            ") "
            "or ( "
            "type(r) = $read_rel AND r.to IS NULL "
            ") "
            "return count(r)"
        )
        params = {
            "username": username,
            "reserve_rel": "RESERVE",
            "barcode": barcode,
            "read_rel": "READ",
        }

        try:
            books_count = db.cypher_query(query, params=params)
            books_count = books_count[0][0][0]

            data = Response({"count": books_count}, status=status.HTTP_200_OK)

        except Exception as e:
            data = Response(
                {'msg': "Unable to get user's books", 'error_msg': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return data
