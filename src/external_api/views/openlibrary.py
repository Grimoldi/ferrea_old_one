
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from external_api.dao import OpenLibraryQuery


class OpenLibraryGetAuthorPortrait(APIView):
    '''OpenLibraryGetAuthorPortrait This class handles the get from Open Library APIs.

    This class is dedicated to fetch the author portrait from Open Library Public APIs.
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
        openlibrary = OpenLibraryQuery()
        portrait = openlibrary.author_portrait_by_isbn(isbn=isbn)
        is_portrait_found = portrait.status_code != 404
        data = portrait.data

        if is_portrait_found:
            state = status.HTTP_200_OK
        else:
            state = status.HTTP_404_NOT_FOUND
        return Response(data, status=state)
