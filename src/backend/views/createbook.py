
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from backend.dao import Neo4jDao


class CreateBook(APIView):
    '''CreateBook This class handles the creation of a new book

    This class creates a new copy of the book.
    If the book (isbn) is already present in the catalog, the barcode is increased by 1 (cap to 999)
    Otherwise a new book is created

    Author, Publisher, Saga may be created as well
    '''

    def __init__(self):
        '''__init__ Constructor

        Constructor of the class
        '''
        pass

    def post(self, request, format=None):
        '''post Method to create a new book.

        This public method override the post method.
        It gets the parameters from the post.
        Checks if isbn value is passed.
        Then verify if it is already present in db and choose which method has to be called afterwards:
        - create new book
        - create new copy of a book

        Args:
            request (HTTPRequest): the request object.
            format (string, optional): format of the response to provide (json, xml...). Defaults to None.

        Returns:
            HTTPResponse: data returned from the dao.
        '''

        print(request.data)
        create_info = {
            # book
            'isbn': request.data.get('isbn', None),
            'comments': request.data.get('comments', ''),
            'title': request.data.get('title', ''),
            'pub_format': request.data.get('pub_format', ''),
            'language': request.data.get('language', ''),
            'date_published': request.data.get('date_published', ''),
            'cover': request.data.get('cover', ''),
            # barcode is calculated on the fly

            # author
            'author': request.data.get('author', ''),

            # publisher
            'publishing': request.data.get('publishing', ''),

            # saga
            'series': request.data.get('series', ''),

            # library
            'library': request.data.get('library', None),
        }

        dao = Neo4jDao()
        isbn = create_info["isbn"]
        isbns = dao.fetch_previews()
        isbns = isbns.keys()
        library = create_info["library"]
        libraries = dao.fetch_libraries()

        # checking if isbn is passed
        is_isbn_missing = isbn is None
        is_library_missing = library is None
        is_library_correct = library in libraries
        is_incorrect_request = \
            is_isbn_missing or \
            is_library_missing or \
            not is_library_correct

        if is_incorrect_request:
            return Response(
                {"error_msg": "Isbn is missing or library is not correct from post data"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # checking if isbn is already present in db
        is_book_already_present = isbn in isbns
        dao = Neo4jDao()

        if is_book_already_present:
            return dao.create_book_copy(isbn=isbn, library=library)
        else:
            return dao.create_book(create_info=create_info)
