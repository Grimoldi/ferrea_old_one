
from neomodel import db
from library.constants import MAX_SUGGESTED

from rest_framework import status
from rest_framework.response import Response


class ReadSuggestedAuthorsDao():
    '''ReadSuggestedAuthorsDao This class handles the lookup for authors that match the user's read.

    This class handles the get for the authors that some users read.
    These users have some reading in sharing with the user.
    The class expose the following methods:

    - read_suggested_authors
    '''

    def __init__(self):
        '''__init__ Constructor

        Constructor of the class
        '''
        pass

    def read_suggested_authors(self, username):
        '''read_suggested_authors This methods retrieve the authors read by other user. 

        This method reads on the db the first MAX_SUGGESTION authors that have been read by other users
        that has read at least a book read by the user.

        eg:
        User A reads books 1, 2, 3 written by A1, B1, C1
        Looking for users that have read at least a book in [1, 2, 3]
        it returns users B, C, D (the current user is excluded)
        That it looks for authors read by B, C, D, returning
            [E1, D1] for B,
            [E1, F1] for C
            [E1, G1, H1] by D
        (authors already read by A are excluded)

        The method finally returns a list of
        [E1, D1, F1]

        Args:
            username (string): id of the user.

        Returns:
            HTTPResponse: dictionary with the result of the operations.
            The body is under the key "authors" or "error_msg".
        '''
        query = (
            # authors read by the user
            "MATCH (u1:User {username: $username})-[r1:READ]->(b1:Book)<-[w1:WROTE]-(a1:Author) "
            "WITH u1, a1, b1 "

            # user that share at least a book read in common with user
            "OPTIONAL MATCH (u2:User)-[r2:READ]->(b1) "
            "WHERE u1.username <> u2.username "
            "WITH u2, a1 "

            # authors read by other users
            "OPTIONAL MATCH (u2)-[r3:READ]->(b2:Book)<-[w2:WROTE]-(a2:Author) "
            "WITH "
            "collect(distinct(a1.author)) as authors_read, "
            "collect(distinct(a2.author)) as authors "

            # return list of difference between both precedent lists
            "return [n IN authors WHERE NOT n IN authors_read][0..$max_suggested] as suggested_authors_list"
        )
        params = {
            "username": username,
            "max_suggested": MAX_SUGGESTED,
        }

        try:
            suggested_authors = db.cypher_query(query, params=params)
            suggested_authors_list = suggested_authors[0][0][0]

            data = Response({"authors": suggested_authors_list},
                            status=status.HTTP_200_OK)

        except Exception as e:
            data = Response(
                {'msg': "Unable to get suggested books", 'error_msg': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return data
