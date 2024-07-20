
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from backend.dao import Neo4jDao


class ReadBookSearch(APIView):
    '''ReadBookSearch This class handles the search of a book based on given criteria.

    This class handles how a book is searched on the db, given some custom criteria.
    The criteria could include from none to all of the following parameters:
    - author
    - title (of the book)
    - saga (to which the book belongs)
    '''

    def get(self, request, username=None, format=None):
        '''get This method gets the book matching the criteria.

        This method will perform a search on the db to find any book that matches the criteria.
        Expected data in request.data are
        {
            [author (optional)],
            [title (optional)],
            [saga (optional)],
        }


        Args:
            request (HTTPRequest): the request object.
            username (string): id of the user (needed to sort result by distance user/library).
            format (string, optional): format of the response to provide (json, xml...). Defaults to None.

        Returns:
            HTTPResponse: data returned from the dao.
        '''
        is_username_missing = username is None
        if is_username_missing:
            data = Response(
                {"ris": "Unable to perform the search on db",
                    "error_msg": "Username was not provided"},
                status=status.HTTP_400_BAD_REQUEST
            )
            return data

        search_data = {
            'username': username,
            'author': request.data.get('author', ''),
            'title': request.data.get('title', ''),
            'saga': request.data.get('saga', ''),
            'status': request.data.get('status', ''),
        }
        dao = Neo4jDao()

        books_list = dao.read_book_search(**search_data)
        is_book_search_successfull = books_list.status_code == 200

        if is_book_search_successfull:
            previews = dao.fetch_previews()
            books_result = list()

            for book_tupla in books_list.data["books"]:
                isbn = book_tupla[2]

                book_temp = {
                    "title": previews[isbn]["title"],
                    "cover": previews[isbn]["cover"],
                    "series": previews[isbn]["series"],
                    "author": previews[isbn]["author"],
                    "publishing": previews[isbn]["publishing"],
                    "distance": book_tupla[0],
                    "library": book_tupla[1],
                    "isbn": isbn,
                    "readable": book_tupla[3],
                    "reservable": book_tupla[4],
                    "barcode": book_tupla[5],
                }
                books_result.append(book_temp)

            data = Response({"books": books_result}, status=status.HTTP_200_OK)
        else:
            data = books_list

        return data
