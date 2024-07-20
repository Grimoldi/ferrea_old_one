
from rest_framework.views import APIView
from django.shortcuts import render, redirect
import os
from backend.views import ReadHistory


class UserHistory(APIView):
    '''UserHistory This class handles the rendering of user's history.

    This class handles how the history page should be rendered.
    '''

    def __init__(self):
        '''__init__ Constructor

        Constructor of the class
        '''
        self._template_path = "../templates/pages"
        self._err_key = "error_msg"
        self._success_key = "success_msg"

    def get(self, request, username, data=None, format=None):
        '''get This method renders the get request for user history

        This method overrides the get method.
        It mainly renders the page with the data fetched from the backend.

        Args:
            request (HTTPRequest): the request object.
            username (string): username of the user to retrieve history.
            data (dict, optional): optional additional data to be rendered in the page. Defaults to None.
            format (dict, optional): format of the response to provide (json, xml...). Defaults to None.

        Returns:
            HTTPResponse: the rendering of the template page.
        '''
        is_same_user = username == request.session["user"]
        if not is_same_user:
            request.session[self._err_key] = "Are you trying to hacking me?"
            return redirect('/search_book')

        view = ReadHistory()
        history_list = view.get(request=request, username=username)

        is_history_successfull = history_list.status_code == 200

        context = dict()
        context["user"] = request.session["user"]

        if not is_history_successfull:
            request.session[self._err_key] = history_list.data[self._err_key]

        else:
            context["history"] = history_list.data
            request.session.pop(self._err_key, "")

        template_page = 'user_history.html'
        template = os.path.join(self._template_path, template_page)

        context["error_msg"] = request.session.get(self._err_key, "")
        context["success_msg"] = request.session.get(self._success_key, "")

        return render(request, template, context)
