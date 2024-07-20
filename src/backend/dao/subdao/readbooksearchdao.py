
from neomodel import db

from rest_framework import status
from rest_framework.response import Response


class ReadBookSearchDao():
    '''ReadBookSearchDao This class handles the search on the db for all the Book nodes that match some criteria.

    This class controls how to retrieve all book nodes that match some criteria provided by the user.
    The class expose the following methods:

    - read_book_search
    '''

    def __init__(self):
        '''__init__ Constructor

        Constructor of the class
        '''
        pass

    def read_book_search(self, username, title, author, saga, book_status):
        '''read_book_search This method retrieve a list of book nodes matching the given criteria.

        This method retrieve all book node the match the given criteria.
        The book copies are then sorted by distance between the user and the library and then returned to the caller.
        This is made possible since both user and libraries have a point attribute.

        Args:
            username (string): id of the user.
            title (string): the title (of part of it) of the book.
            author (string): the author (or part of it) that wrote the book.
            saga (string): the saga (or part of it) that the book must belongs.
            book_status (string): if the book has to be searched as currently free or not.

        Returns:
            HTTPResponse: dictionary with the result of the operations.
            The body is under the key "msg" or "error_msg".
        '''

        has_to_be_available = book_status != ""

        query = (
            "MATCH (u:User{username: $username}) "
            "MATCH (a:Author)-[w_rel:WROTE]->(b:Book) "
            "MATCH (b)-[s_rel:BELONGS_TO]->(s:Saga) "
            "MATCH (l:Library)-[h_rel:HOSTS]->(b) "
            "WHERE b.title =~ '.*(?i)' + $title + '.*' "
            "and a.author =~ '.*(?i)' + $author + '.*' "
            "and s.series=~ '.*(?i)' + $saga + '.*' "
        )
        if has_to_be_available:
            query = query + (
                "and (b.is_readble = True "
                "or "
                "b.is_reservable = True) "
            )
        query = query + (
            "return "
            "toInteger(distance(u.location, l.location)) as distance, "
            "l.name as library, "
            "b.isbn as isbn, "
            "b.is_readable as readable, "
            "b.is_reservable as reservable, "
            "b.barcode "
            "order by distance"
        )
        params = {
            'username': username,
            'author': author,
            'saga': saga,
            'title': title,
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
