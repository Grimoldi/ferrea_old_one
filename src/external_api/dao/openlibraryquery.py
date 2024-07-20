
from requests import (
    get,
)
from rest_framework import status
from rest_framework.response import Response
import os.path


class OpenLibraryQuery:
    ''' OpenLibraryQuery This class handles the search for a book towards OpenLibrary apis.

    This class expose the method:
    - author_portrait_by_isbn
    it search for a book on OpenLibrary and then look for its author portrait.
    '''

    def __init__(self):
        '''__init__ Constructor

        Constructor of the class
        '''
        self._BASE_AUTHOR_URL = "http://covers.openlibrary.org/a/olid/"
        self._BASE_BOOK_URL = "http://openlibrary.org/api/books"

    def author_portrait_by_isbn(self, isbn):
        '''author_portrait_by_isbn This method gets the author portrait from Open Library APIs.

        This method performs a query towards Open Library APIs in order to find if there is the author portrait.

        Args:
            isbn (string): isbn of the book to search.

        Returns:
            HTTPResponse: response with the data found.
        '''
        authors = self._author_get_by_isbn(isbn=isbn)

        is_author_found = authors.status_code == 200
        if is_author_found:
            authors = authors.data["authors"]
            authors_list = list()

            # checking if portrait exists
            # if it doesn't exists it will throw a 404
            # due to default=false parameter
            for author in authors:
                author_olid = author["olid"]
                img_url = f"{self._BASE_AUTHOR_URL}{author_olid}-M.jpg"
                uri = "%s?default=false" % (img_url)
                response = get(uri)
                is_found = response.status_code != 404

                if is_found:
                    temp_data = {"portrait": img_url, "name": author["name"]}
                    authors_list.append(temp_data)

            return Response(authors_list, status=status.HTTP_200_OK)

        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

    def _author_get_by_isbn(self, isbn):
        '''_author_get_by_isbn This method checks if the book is held in Open Library.

        This method performs a GET towards Open Library APIs in order to find if the book is present.
        If present, it retrieve all authors olid (Open Library ID).

        Args:
            isbn (string): isbn of the book.

        Returns:
            HTTPResponse: response with the data found.
        '''
        # querying open_library to get the book
        uri = self._BASE_BOOK_URL
        headers = {'Content-Type': 'application/json', }
        params = {
            "bibkeys": f"ISBN:{isbn}",
            "jscmd": "details",
            "format": "json",
        }

        response = get(uri, headers=headers, params=params)
        response_json = response.json()
        # from the book obtain its authors
        try:
            authors = response_json[f"ISBN:{isbn}"]["details"]["authors"]
            authors_list = list()
            for author in authors:
                author_olid = author["key"]
                author_olid = os.path.basename(author_olid)
                data = {
                    "olid": author_olid,
                    "name": author["name"]
                }
                authors_list.append(data)
            return Response(
                {'authors': authors_list},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
