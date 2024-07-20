
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from library.constants import PREVIEWS
from backend.dao import Neo4jDao
from datetime import datetime


class ReadHistory(APIView):
    '''ReadHistory This class handles how the user history is searched on db.

    This class handles the retrieve of user book history (book read from date to date, book reserved on date...).
    '''

    def __init__(self):
        '''__init__ Constructor

        Constructor of the class
        '''
        pass

    def get(self, request, username, format=None):
        '''get This method gets the history given a username.

        This method will perform a search on the db to find the book history of a user.

        Args:
            request (HTTPRequest): the request object.
            username (string): id of the user.
            format (string, optional): format of the response to provide (json, xml...). Defaults to None.

        Returns:
            HTTPResponse: data returned from the dao.
        '''
        dao = Neo4jDao()
        history_list = dao.read_user_history(username=username)
        is_history_successfull = history_list.status_code == 200

        user_history = list()
        if not is_history_successfull:
            data = history_list

        else:
            reading_list = history_list.data["reading"]
            reserve_list = history_list.data["reservation"]

            for history in reading_list:
                has_data = history[0] is not None
                if has_data:
                    isbn = history[1]
                    from_date = int(float(history[0]["since"]))
                    from_date_obj = datetime.fromtimestamp(from_date)
                    date_format = "%d/%m/%Y"
                    to_date = history[0].get("to", None)
                    is_to_with_value = to_date is not None

                    history_book = {
                        "book": PREVIEWS[isbn],
                        "from_date": datetime.strftime(from_date_obj, date_format),
                        "type": "reading",
                    }
                    position = 0  # insert on top of the list

                if is_to_with_value:
                    to_date = int(float(to_date))
                    to_date_obj = datetime.fromtimestamp(to_date)
                    history_book["to_date"] = datetime.strftime(
                        to_date_obj, date_format)
                    # insert on bottom of the list
                    position = len(user_history)

                user_history.insert(position, history_book)

            for history in reserve_list:
                has_data = history[0] is not None
                if has_data:
                    isbn = history[1]
                    barcode = history[2]
                    on_date = int(float(history[0]["on"]))
                    on_date_obj = datetime.fromtimestamp(on_date)

                    history_book = {
                        "book": PREVIEWS[isbn],
                        "on_date": datetime.strftime(on_date_obj, date_format),
                        "type": "reserve",
                        "barcode": barcode,
                    }

                    # always insert on top
                    user_history.insert(0, history_book)

            data = Response(
                {"history": user_history},
                status=status.HTTP_200_OK,
            )

        return data
