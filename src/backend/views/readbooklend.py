
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from backend.dao import Neo4jDao


class ReadBookLend(APIView):
    '''ReadBookLend This class handles the get of all books that are currently being read.

    This class is capable of searching all books currently "out" of the catalog on the db.
    It adds also the information about every single copy in the catalog (like the user currently reading it).
    '''

    def get(self, request, format=None):
        '''get This method gets the books.

        Args:
            request (HTTPRequest): the request object.
            format (string, optional): format of the response to provide (json, xml...). Defaults to None.

        Returns:
            HTTPResponse: data returned from the dao.
        '''
        dao = Neo4jDao()

        books_list = dao.read_book_lend()
        is_book_list_successfull = books_list.status_code == 200

        book_lended = list()
        if is_book_list_successfull:
            books_list = books_list.data["books"]
            for book in books_list:
                book_copy = {
                    "cover": book[0]["cover"],
                    "barcode": book[0]["barcode"],
                    "date_publishing": book[0]["date_publishing"],
                    "isbn": book[0]["isbn"],
                    "format": book[0]["format"],
                    "language": book[0]["language"],
                    "title": book[0]["title"],

                    "author": book[1]["author"],

                    "series": book[2]["series"],

                    "library_name": book[3]["name"],
                    "library_address": book[3]["address"],
                    "library_phone": book[3]["phone"],

                    "publisher": book[4]["publisher"],

                    "user_name": book[5]["name"],
                    "user_surname": book[5]["surname"],
                    "username": book[5]["username"],
                }
                book_lended.append(book_copy)

            data = Response({"book": book_lended}, status=status.HTTP_200_OK)
        else:
            data = books_list

        return data
