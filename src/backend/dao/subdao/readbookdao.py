
from neomodel import db

from rest_framework import status
from rest_framework.response import Response


class ReadBookDao():
    '''ReadBookDao This class handles the search of a book.

    This class handles the get of a book node with its full connection and details.
    Note that the a full list of copies of the searched book is returned, each with its library.
    The class expose the following methods:

    - read_book
    '''

    def __init__(self):
        '''__init__ Constructor

        Constructor of the class
        '''
        pass

    def read_book(self, isbn):
        '''read_book This method handles the search on the db for a particular isbn.

        The method retrieves all book's node that match the isbn provided.
        Please note that by searching by isbn, more than a single could be matched, so the method
        provide also every library that have a copy of the book.

        Args:
            isbn (string): soft id of the book.

        Returns:
            HTTPResponse: dictionary with the result of the operations.
            The body is under the key "msg" or "error_msg".
        '''
        query = (
            "MATCH (b:Book{isbn: $isbn}) "
            "MATCH (a:Author)-[w_rel:WROTE]->(b) "
            "MATCH (b)-[s_rel:BELONGS_TO]->(s:Saga) "
            "MATCH (l:Library)-[h_rel:HOSTS]->(b) "
            "MATCH (p:Publisher)-[p_rel:PUBLISHED]->(b) "

            "return b, a, s, l, p "
        )
        params = {
            'isbn': isbn,
        }

        try:
            books = db.cypher_query(query, params=params)
            is_something_found = len(books[0]) > 0

            if is_something_found:
                data = Response(
                    {"books": books[0]},
                    status=status.HTTP_200_OK
                )
            else:
                data = Response(
                    {
                        'msg': "Nothing found",
                        "error_msg": "Nothing found"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

        except Exception as e:
            data = Response(
                {'msg': "Unable to search for books", 'error_msg': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return data
