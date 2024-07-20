
from datetime import datetime
from neomodel import db

from rest_framework import status
from rest_framework.response import Response


class CreateReadDao():
    '''CreateReadDao This class handles the creation of a read relationship on data db (Neo4J).

    This class controls how a read relationship is created on db.
    (User)-[READ]->(Book)
    The class expose the following methods:

    - create_read: to create a new read relationship.

    '''

    def __init__(self):
        '''__init__ Constructor

        Constructor of the class
        '''
        pass

    def create_read(self, username, barcode, when=None):
        '''create_read This method creates the relationship READ between user node and book node.

        This method takes barcode and username as parameters, then it creates the relationship READ.
        I opted to use a cypher query since Neomodel would allow
        a single relationship of the same type between the same pair of nodes.
        A user can obviously read as many times the same book as he likes.
        Furthermore, I'm able to check that the book hasn't been already reserved by another user.

        Upon reading a book (getting it from the library),
        the reservation must be cancelled (if present).
        I opted here too to use a cypher query, since neomodel doesn't seems
        to support both .has and .get method together
        (get the node by property that has the relationship RESERVE)
        The status of the book is forced to Unavailable since no other user can take it

        Args:
            username (string): id of the user.
            barcode (string): id of the book.
            when (datetime.datetime): datetime object to add on the relationship.

        Returns:
            HTTPResponse: dictionary with the result of the operations.
            The body is under the key "msg" or "error_msg".
        '''

        now = datetime.now().timestamp()
        if when is not None:
            now = when

        query = (
            "MATCH (b:Book {barcode: $barcode}) "
            "MATCH (u:User {username: $username}) "

            # getting eventual reservation done by the user that will be deleted
            "OPTIONAL MATCH (u)-[v:RESERVE]->(b) "

            # getting reservation from other users
            "OPTIONAL MATCH (u2:User)-[r2:RESERVE]->(b) "
            "WHERE u2.username <> u.username "

            # filtering where other reservation do not exists
            "with u, b, v, count(r2) as prev_res "
            "where prev_res=0 "

            # if nodes pass through the filter, create the relationship
            "CREATE (u)-[r:READ]->(b) "
            "SET r.since = $now, "
            "b.status= $status, "
            "b.is_readable= False "
            "DELETE v "
            "return r"
        )
        params = {
            "barcode": str(barcode),
            "username": username,
            "now": now,
            "status": "Unavailable",
        }

        try:
            db.begin()

            # create read relationship
            # remove reserve if existing
            read = db.cypher_query(query, params=params)
            is_read_created = len(read[0]) > 0

            if is_read_created:
                db.commit()

                data = Response(
                    {'msg': "Read done, reservation canceled."},
                    status=status.HTTP_200_OK
                )
            else:
                data = Response(
                    {
                        "error_msg": "Sorry, book has already a reservation from another user."
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )

        except Exception as e:
            db.rollback()
            data = Response(
                {'error_msg': "Read failed.", 'det': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return data
