
from rest_framework.views import APIView
from django.shortcuts import render, redirect
import os
from backend.views import ReadBookSearch
from frontend.models import SearchForm


class SearchBook(APIView):
    '''SearchBook This class handles the request to search for a book matching some given criteria.

    This class handles the request to search for a certain book matching user's criteria.
    '''

    def __init__(self):
        '''__init__ Constructor

        Constructor of the class
        '''
        self._template_path = "../templates/pages"
        self._err_key = "error_msg"
        self._success_key = "success_msg"

    def post(self, request, format=None):
        '''post This method handles the request of submission of the form.

        This method override the post method.
        It calls the backend view in order to lookup for the books matching on data db (Neo4J).
        Finally, it redirects to the search page.

        Args:
            request (HTTPRequest): the request object
            format (string, optional): format of the response to provide (json, xml...). Defaults to None.

        Returns:
            HttpResponsePermanentRedirect: to search page.
        '''
        # removing old search results, if present
        has_search_in_session = "search_form_data" in request.session.keys()
        if has_search_in_session:
            request.session.pop("search_form_data")
            try:
                request.session.pop("book_list")
            except Exception as e:
                # if the key is not in request.session, it's not a big problem
                # we should've cancelled it anyways
                # if it's missing it means that previous search found nothing
                pass

        # create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            # saving current inputs in request.session
            request.session["search_form_data"] = {
                "author": request.data["author"],
                "title": request.data["title"],
                "saga": request.data["saga"],
                "status": request.data["status"],
            }

            view = ReadBookSearch()
            book_search_result = view.get(
                request=request,
                username=request.session["user"],
            )
            is_search_successfull = book_search_result.status_code == 200

            if is_search_successfull:
                request.session.pop(self._err_key, "")

                request.session["book_list"] = book_search_result.data

            else:
                request.session[self._err_key] = book_search_result.data[self._err_key]

        else:
            request.session[self._err_key] = "Form is not valid"

        return redirect('/search_book')

    def get(self, request, data=None, format=None):
        '''get This method renders the search page.

        This method override the get method.
        Its function is to graphically renders the page.

        Args:
            request (HTTPRequest): the request object.
            data (dict, optional): optional additional data to be rendered in the page. Defaults to None.
            format (string, optional): format of the response to provide (json, xml...). Defaults to None.

        Returns:
            HTTPResponse: the rendering of the template page.
        '''

        template_page = 'search.html'
        template = os.path.join(self._template_path, template_page)

        context = {
            "error_msg": request.session.get(self._err_key, ""),
            "book_list": request.session.get("book_list", None),
            "form": SearchForm(),
            "user": request.session["user"],
            "success_msg": request.session.get(self._success_key, ""),
        }

        has_already_search_data = "search_form_data" in request.session.keys()
        if has_already_search_data:
            context["form"] = SearchForm(
                data=request.session["search_form_data"]
            )

        return render(request, template, context)
