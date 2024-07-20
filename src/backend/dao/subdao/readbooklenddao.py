
from neomodel import db

from rest_framework import status
from rest_framework.response import Response


class ReadBookLendDao():
    '''ReadBookLendDao This class handles the search of all book that still have to be returned.

    This class handles the get of all book that have to be still returned.
    Note that reserved books will not be returned as they aren't "out from the library".
    The class expose the following methods:

    - read_book_lend
    '''

    def __init__(self):
        '''__init__ Constructor

        Constructor of the class
        '''
        pass

    def read_book_lend(self):
        '''read_book_lend This method retrieve all book that don't have the attribute "to" on their READ relationship.

        This method retrieves all book the don't have the attribute "to" on their READ relationship.
        The method also return a buch of useful informations, such as the user that is currently holding the book,
        or the library which the book belongs to.

        Returns:
            HTTPResponse: dictionary with the result of the operations.
            The body is under the key "msg" or "error_msg".
        '''

        query = (
            "MATCH (b:Book{is_readable: False}) "
            "MATCH (a:Author)-[w_rel:WROTE]->(b) "
            "MATCH (b)-[s_rel:BELONGS_TO]->(s:Saga) "
            "MATCH (l:Library)-[h_rel:HOSTS]->(b) "
            "MATCH (p:Publisher)-[p_rel:PUBLISHED]->(b) "
            "MATCH (u:User)-[r_rel:READ]->(b) "
            "WHERE NOT EXISTS (r_rel.to) "

            "return b, a, s, l, p, u "
        )

        try:
            books = db.cypher_query(query)
            is_something_found = len(books[0]) > 0

            if is_something_found:
                data = Response(
                    {"books": books[0]},
                    status=status.HTTP_200_OK
                )
            else:
                data = Response(
                    {
                        "error_msg": "Nothing found"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

        except Exception as e:
            print(e)
            data = Response(
                {'error_msg': "Unable to search for books", 'det': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return data
