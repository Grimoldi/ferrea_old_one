
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from external_api.dao import GoogleQuery


class GoogleGetBook(APIView):
    '''GoogleGetBook This class handles the get from Google Book APIs.

    This class is dedicated to get the books from google api endpoint.
    '''

    def __init__(self):
        '''__init__ Constructor

        Constructor of the class
        '''
        pass

    def get(self, request, isbn, format=None):
        '''get This method gets the book from its isbn.

        This method override the get method.
        It will perform a search on the API to find details of the isbn passed as arg.

        Args:
            request (HTTPRequest): the request object.
            isbn (string): isbn of the book.
            format (string, optional): format of the response to provide (json, xml...). Defaults to None.

        Returns:
            HTTPResponse: data returned from the dao.
        '''
        google = GoogleQuery()
        book = google.book_get_by_isbn(isbn=isbn)
        is_found = book.status_code == 200
        is_not_found = book.status_code == 404

        if is_found:
            try:
                return Response(book.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif is_not_found:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({book.data}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
