
from rest_framework.views import APIView
from requests import get
from rest_framework import status
from rest_framework.response import Response
import regex
from django.urls import reverse

from library.constants import (
    MAX_FUZZY_DISTANCE,
)


class SearchBook(APIView):
    '''SearchBook This class handles the search across all external datasource enabled a book given its isbn.

    This class handles the request to find data for a given isbn.
    It searches across all external api registered the details for a given isbn.

    Since Google Book is the best shot to find a book, if isbn is not found on google api it will return a 404.
    '''

    def get(self, request, isbn, format=None):
        '''get This method gets the book from its isbn.

        This method makes a get to the following endpoint:
        - /google/<isbn>
        - /open_library/<isbn>
        if is found on google, it searches on open library for the portrait

        Args:
            request (HTTPRequest): the request object.
            isbn (string): soft id of the book.
            format (string, optional): format of the response to provide (json, xml...). Defaults to None.

        Returns:
            HTTPResponse: data returned from the dao.
        '''
        book_details = dict()
        book_details["isbn"] = isbn

        # search on google api
        google = get(request.build_absolute_uri(
            reverse('google', kwargs={'isbn': isbn})
        ))
        is_found_on_google = google.status_code == 200

        if not is_found_on_google:
            return Response(book_details, status=status.HTTP_404_NOT_FOUND)

        else:
            # search on open library api
            google_book = google.json()
            open_library = get(request.build_absolute_uri(
                reverse('open_library', kwargs={'isbn': isbn})
            ))
            is_found_on_ol = open_library.status_code == 200

            # fill the dictionary returned from endpoint
            google_volume = google_book.get("volumeInfo", dict())
            # mandatory fields:
            try:
                book_details["title"] = google_volume["title"]
                book_details["author"] = google_volume["authors"][0]

            except Exception as e:
                return Response(
                    {"error_msg": "Unable to find title or author key from google"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # optional fields
            book_details["publishing"] = google_volume.get("publisher", "")
            book_details["date_published"] = google_volume.get(
                "publishedDate", "")
            book_covers = google_volume.get("imageLinks", None)
            has_covers = book_covers is not None
            if has_covers:

                has_thumbnail = "small_thumbnail" in book_covers.keys(
                ) or "thumbnail" in book_covers.keys()
                if has_thumbnail:
                    book_details["cover"] = book_covers.get(
                        "thumbnail", "small_thumbnail")
            else:
                book_details["cover"] = ""
            book_details["comments"] = google_volume.get("description", "")
            book_details["language"] = google_volume.get("language", "")
            book_details["format"] = google_volume.get("printType", "")

            book_details["author_portrait"] = ""
            if is_found_on_ol:
                for author in open_library.json():
                    pattern_string = book_details["author"]
                    query_string = author["name"]
                    r = regex.compile(
                        '(%s){e<=%s}' % (pattern_string, MAX_FUZZY_DISTANCE)
                    )
                    fuzzy_result = r.match(query_string)
                    is_author_found = fuzzy_result is not None

                    if is_author_found:
                        book_details["author_portrait"] = author["portrait"]
                        break

            return Response(book_details, status=status.HTTP_200_OK)
