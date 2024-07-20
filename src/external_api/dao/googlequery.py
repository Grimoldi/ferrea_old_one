
from requests import (
    get
)
from rest_framework import status
from rest_framework.response import Response


class GoogleQuery:
    ''' GoogleQuery This class handles the search for a book towards Google apis.

    This class expose the method:
    - book_get_by_isbn
    it search for a book on Google Books api.
    '''

    def __init__(self):
        '''__init__ Constructor

        Constructor of the class
        '''
        self._BASE_URL = "https://www.googleapis.com/books/v1/volumes"

    def book_get_by_isbn(self, isbn):
        '''book_get_by_isbn This method gets the book from Google Book APIs.

        This method performs a search on Google APIs for the isbn passed as argument.

        Args:
            isbn (string): isbn of the book to search.

        Returns:
            HTTPResponse: response with the data found.
        '''
        uri = self._BASE_URL
        headers = {'Content-Type': 'application/json', }
        params = {
            "q": f"isbn:{isbn}",
            "projection": "lite"
        }
        response = get(uri, headers=headers, params=params)
        is_found = response.status_code == 200

        if is_found:
            response_json = response.json()
            try:
                book_id = response_json["items"][0]["id"]

            except Exception as e:
                return Response({}, status=status.HTTP_404_NOT_FOUND)

            uri = f"{self._BASE_URL}/{book_id}"
            response = get(uri, headers=headers)

            try:
                data = response.json()
                return Response(data, status=status.HTTP_200_OK)

            except Exception as e:
                error = f'Issue with request. {str(e)}'
                return Response({"error": error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
