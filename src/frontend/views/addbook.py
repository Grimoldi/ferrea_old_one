
from rest_framework.views import APIView
from frontend.models import UserForm
from django.shortcuts import render, redirect
import os
from frontend.models import (
    IsbnForm,
    BookForm,
)
from external_api.views import SearchBook
from backend.views import (
    CreateBook,
    ManageUser,
)


class AddBook(APIView):
    '''AddBook This class handles the rendering and the add of a new book (or a new copy)

    This class extends APIView and exposes two methods, overriding the ones
    from the super class.
    Get
        for rendering the page with a form (the form could be of two types depending 
        on what stage of the add we are at)

    Post
        to perform the add on Neo4j backend
    '''

    def __init__(self):
        '''__init__ Constructor

        Constructor of the class
        '''
        self._template_path = "../templates/pages"
        self._success_key = "success_msg"
        self._err_key = "error_msg"

    def get(self, request, data=None, format=None):
        '''get Get method to render the page

        This method overrides the get of the super class.
        Its function is to renders page with the form.
        The form could be 
            - IsbnForm if the librarian is inserting from scratch the isbn
            - BookForm if the librarian has already inserted the isbn and we are rendering
                the data get from external api

        Args:
            request (HTTPRequest): the request object
            data (dict, optional): optional additional data to be rendered in the page. Defaults to None.
            format (dict, optional): format of the response to provide (json, xml...). Defaults to None.

        Returns:
            HTTPResponse: renders the template page
        '''
        template_page = 'add_book.html'
        template = os.path.join(self._template_path, template_page)
        self._context = dict()

        is_isbn_already_searched = "isbn" in request.session.keys()
        if is_isbn_already_searched:
            self._render_book_form(request=request)
        else:
            self._render_isbn_form(request=request)

        if "book" in request.session.keys():
            self._context["book"] = request.session["book"]

        return render(request, template, self._context)

    def post(self, request, format=None):
        '''post This method perform the search of an isbn or the add to db of a copy

        This method overrides the post of the super class.
        Its function is to perform either
            - The look for an isbn through the external api module
            - The add of a book/new copy to Neo4j backend

        Args:
            request (HTTPRequest): the request object

            format (dict, optional): format of the response to provide (json, xml...). Defaults to None.

        Returns:
            HttpResponsePermanentRedirect: to the appropriate page to be rendered.
        '''
        is_isbn_already_searched = "isbn" in request.session.keys()
        if is_isbn_already_searched:
            form = BookForm(request.POST)
            self._add_book_to_library(request=request, form=form)
        else:
            form = IsbnForm(request.POST)
            self._lookup_for_book_data(request=request, form=form)

        return redirect('/add_new_book')

    def _render_isbn_form(self, request):
        '''_render_isbn_form This method fullfill the context with the empty IsbnForm

        This private method fullfill the context attribute in order to be able to render
        the page with just the IsbnForm in order for the librarian to be able to
        search a book from a specific isbn

        Args:
            request (HTTPRequest): the request object
        '''
        self._context = {
            self._err_key: request.session.get(self._err_key, ""),
            "user": request.session["user"],
            "form_isbn": IsbnForm()
        }

    def _render_book_form(self, request):
        '''_render_book_form This method fullfill the context with the BookForm with the data autofetched

        This private method fullfill the context attribute in order to be able to render
        the page with just the BookForm in order for the librarian to be able to
        edit anything if he wants and then add to Neo4j backend.

        Args:
            request (HTTPRequest): the request object.
        '''
        self._context = {
            self._err_key: request.session.get(self._err_key, ""),
            "user": request.session["user"],
            "form_book": BookForm(data={
                "isbn": request.session["book"]["isbn"],
                "title": request.session["book"]["title"],
                "author": request.session["book"]["author"],
                "publishing": request.session["book"]["publishing"],
                "date_published": request.session["book"]["date_published"],
                "language": request.session["book"]["language"],
                "book_format": request.session["book"]["format"],
                "cover": request.session["book"]["cover"],
                "comments": request.session["book"]["comments"],
                "saga": "NA",
            }),
            "cover": request.session["book"]["cover"]
        }

    def _lookup_for_book_data(self, request, form):
        '''_lookup_for_book_data This method will perform the lookup through the external_api module

        This private method will create an instance of the external_api view and then perform a search
        api in order to automatically get book data from external sources.

        Args:
            request (HTTPRequest): the request object.
            form (IsbnForm): the form with the searched isbn
        '''
        if form.is_valid():
            view = SearchBook()
            isbn_search = view.get(request=request, isbn=request.data["isbn"])
            is_get_successfull = isbn_search.status_code == 200

            if is_get_successfull:
                request.session["book"] = isbn_search.data
                request.session["isbn"] = request.data["isbn"]

            else:
                request.session[self._err_key] = isbn_search.data[self._err_key]
        else:
            request.session[self._err_key] = "Form is not valid"

    def _add_book_to_library(self, request, form):
        '''_add_book_to_library This method will add the book to the catalog

        This private method will create an instance of the backend view backend.views.CreateBook
        and then perform a post in order to add the book to the catalog.

        Args:
            request (HTTPRequest): the request object.
            form (IsbnForm): the form with the searched isbn
        '''
        if form.is_valid():
            view = CreateBook()
            book_add = view.post(request=request)
            is_add_successfull = book_add.status_code == 200

            if is_add_successfull:
                request.session[self._success_key] = book_add.data.get(
                    self._success_key, "")
                request.session.pop("book", "")
                request.session.pop("isbn", "")
            else:
                request.session[self._err_key] = book_add.data[self._err_key]
        else:
            request.session[self._err_key] = "Form is not valid"
