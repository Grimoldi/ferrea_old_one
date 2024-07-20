
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from backend.dao import Neo4jDao


class ReadBook(APIView):
    '''ReadBook This class handles the get of a single book.

    This class is capable of searching a single book on the db.
    It adds also the information about every single copy in the catalog (like the library owning the copies).
    '''

    def get(self, request, isbn, format=None):
        '''get This method gets the book from its isbn.

        This method will perform a search on the db to find details of the isbn passed as arg.

        Args:
            request (HTTPRequest): the request object.
            isbn (string): soft id of the book.
            format (string, optional): format of the response to provide (json, xml...). Defaults to None.

        Returns:
            HTTPResponse: data returned from the dao.
        '''
        dao = Neo4jDao()

        books_list = dao.read_book(isbn)
        is_book_list_successfull = books_list.status_code == 200

        if is_book_list_successfull:
            books_list = books_list.data["books"]

            book = {
                "cover": books_list[0][0]["cover"],
                "comments": books_list[0][0]["comments"],
                "date_publishing": books_list[0][0]["date_publishing"],
                # "is_readable": books_list[0][0]["is_readable"],
                # "is_reservable": books_list[0][0]["is_reservable"],
                "isbn": books_list[0][0]["isbn"],
                "format": books_list[0][0]["format"],
                "language": books_list[0][0]["language"],
                "title": books_list[0][0]["title"],
                # "barcode": books_list[0][0]["barcode"],

                "author": books_list[0][1]["author"],

                "series": books_list[0][2]["series"],

                # "library_name": books_list[0][3]["name"],
                # "library_address": books_list[0][3]["address"],
                # "library_phone": books_list[0][3]["phone"],

                "publisher": books_list[0][4]["publisher"],

                "copy_detail": list(),
            }

            for book_copy in books_list:
                copy_dict = {
                    "is_readable": book_copy[0]["is_readable"],
                    "is_reservable": book_copy[0]["is_reservable"],
                    "barcode": book_copy[0]["barcode"],

                    "library_name": book_copy[3]["name"],
                    "library_address": book_copy[3]["address"],
                    "library_phone": book_copy[3]["phone"],
                }

                book["copy_detail"].append(copy_dict)

            data = Response({"book": book}, status=status.HTTP_200_OK)
        else:
            data = books_list

        return data
