
from library.constants import MAX_SUGGESTED
from library.constants import PREVIEWS

from rest_framework import status
from rest_framework.response import Response

from neomodel import db


class ReadSuggestedBooksDao():
    '''ReadSuggestedBooksDao This class handles the lookup for books that match the user's read.

    This class handles the get for the books that some users read.
    These users have some reading in sharing with the user.
    The class expose the following methods:

    - read_suggested_books
    '''

    def __init__(self):
        '''__init__ Constructor

        Constructor of the class
        '''
        pass

    def read_suggested_books(self, username):
        '''read_suggested_books This methods retrieve the books read by other user.

        This method gets from the private method read_suggested_from_db the suggested isbn
        and from PREVIEW builds a list of suggested books.

        Args:
            username (string): id of the user.

        Returns:
            HTTPResponse: dictionary with the result of the operations.
            The body is under the key "suggested_books" or "error_msg".
        '''

        isbns = self._read_suggested_from_db(username)
        is_isbns_successfull = isbns.status_code == 200

        if is_isbns_successfull:
            isbns = isbns.data["suggested_books"]
            suggested_books_list = list()
            for isbn in isbns:
                current_preview = PREVIEWS[isbn]
                suggested_books_list.append(current_preview)

            data = Response({"suggested_books": suggested_books_list},
                            status=status.HTTP_200_OK)
            return data

        else:
            return isbns

    def _read_suggested_from_db(self, username):
        '''_read_suggested_from_db This method performs the query on the data db (Neo4J).

        This private method reads on the db  the first MAX_SUGGESTION books that have been read by other users
        that has read at least a book read by the user.

        eg:
        User A reads books 1, 2, 3
        Looking for users that have read at least a book in [1, 2, 3]
        it returns users B, C, D (the current user is excluded)
        That it looks for book read by B, C, D, returning
            [4, 5] for B,
            [4, 7, 8] for C
            [6, 8] by D
        (books already read by A are excluded)

        It returns a sort list of
        [4, 8, 5]

        Args:
            username (string): id of the user.

        Returns:
            HTTPResponse: dictionary with the result of the operations.
            The body is under the key "suggested_books" or "error_msg".
        '''
        query = (
            # books read by the user
            "MATCH (u1:User {username: $username})-[r1:READ]->(b1:Book) "
            "WITH u1, b1 "

            # user that share at least a book read in common with user
            "OPTIONAL MATCH (u2:User)-[r2:READ]->(b1) "
            "WHERE u1.username <> u2.username "
            "WITH u2, b1 "

            # books read by other users
            "OPTIONAL MATCH (u2)-[r3:READ]->(b2:Book) "
            "WITH "
            "collect(distinct(b1.isbn)) as books_read, "
            "collect(distinct(b2.isbn)) as books "

            # return list of difference between both precedent lists
            "return [n IN books WHERE NOT n IN books_read][0..$max_suggested] as suggested_books"
        )
        params = {
            "username": username,
            "max_suggested": MAX_SUGGESTED,
        }

        try:
            suggested_books = db.cypher_query(query, params=params)
            suggested_books_list = suggested_books[0][0][0]

            data = Response({"suggested_books": suggested_books_list},
                            status=status.HTTP_200_OK)

        except Exception as e:
            data = Response(
                {'msg': "Unable to get suggested books", 'error_msg': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return data
