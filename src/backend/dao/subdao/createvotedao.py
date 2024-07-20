from neomodel import db

from rest_framework import status
from rest_framework.response import Response


class CreateVoteDao():
    '''CreateVoteDao This class handles the creation of a vote relationship on data db (Neo4J).

    This class controls how a new vote relationship is created on db.
    (User)-[VOTE]->(Book)
    The class expose the following methods:

    - create_vote: to create a new vote relationship.

    '''

    def __init__(self):
        '''__init__ Constructor

        Constructor of the class
        '''
        pass

    def create_vote(self, username, barcode, star):
        '''create_vote This method creates the relationship VOTE between user node and book node.

        This method takes username, barcode and start as parameters, then it creates the relationship VOTE.
        The user can vote multiple times the book, but the vote is unique.
        So if he changes his mind and give a different vote, just the "star" attribute must change.

        Args:
            username (string): id of the user.
            barcode (string): id of the book.
            star (int): vote from the user to the book.

        Returns:
            HTTPResponse: dictionary with the result of the operations.
            The body is under the key "msg" or "error_msg".
        '''
        query = (
            "MATCH (u:User {username: $username}) "
            "MATCH (b:Book {barcode: $barcode}) "
            "MERGE (u)-[v:VOTE]->(b) "
            "SET v.star = $star "
            "return u, v, b"
        )
        params = {
            "username": username,
            "barcode": barcode,
            "star": star,
        }

        try:
            books_count = db.cypher_query(query, params=params)

            data = Response({'msg': "Creation done"},
                            status=status.HTTP_200_OK)

        except Exception as e:
            data = Response(
                {'msg': "Creation failed", 'error_msg': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            print(e)

        return data
