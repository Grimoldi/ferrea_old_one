
from rest_framework.views import APIView
from django.shortcuts import render, redirect
import os
from backend.views import ReadBookLend


class ListLend(APIView):
    '''ListLend This class handles the rendering of the lended books for librarians.

    This class handles the graphic rendering of the lends page.
    It calls a views from the backend in order to provide the template all the data needed.
    '''

    def __init__(self):
        '''__init__ Constructor

        Constructor of the class
        '''
        self._template_path = "../templates/pages"
        self._err_key = "error_msg"
        self._success_key = "success_msg"

    def get(self, request, data=None, format=None):
        '''get This method render the page

        This method override the get method.
        It simply render the template, adding an error msg if found in session.

        Args:
            request (HTTPRequest): the request object
            data (dict, optional): optional additional data to be rendered in the page. Defaults to None.
            format (string, optional): format of the response to provide (json, xml...). Defaults to None.

        Returns:
            HTTPResponse: renders the template page
        '''

        view = ReadBookLend()
        book = view.get(request=request)

        template_page = 'lend.html'
        template = os.path.join(self._template_path, template_page)
        context = {"user": request.session["user"], }

        is_lend_search_successfull = book.status_code == 200
        if is_lend_search_successfull:
            request.session.pop(self._err_key, "")

            context["lend_list"] = book.data
            context["success_msg"] = book.data.get(self._success_key, "")

        else:
            request.session[self._err_key] = book.data.get(self._err_key, "")
            context[self._err_key] = request.session.get(self._err_key, "")

        return render(request, template, context)
