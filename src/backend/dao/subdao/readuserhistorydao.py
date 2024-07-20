
from neomodel import db

from rest_framework import status
from rest_framework.response import Response


class ReadUserHistoryDao():
    '''ReadUserHistoryDao This Dao handles the search of a user history

    This Dao gets all books that the user is reading, has read or had reserved.
    This class expose the following methods:

    - read_history
    '''

    def __init__(self, username):
        '''__init__ Constructor

        Constructor of the class

        Args:
            username (string): username of the user to lookup on db.
        '''
        self.username = username

    def read_history(self):
        '''read_history This method query the db.

        This method performs a MATCH on the db, with OPTIONAL MATCH towards any READ or RESERVE
        relationship linked to the user.

        Returns:
            [HTTPResponse]: dictionary of user's actions and its status code.
        '''

        reservation_history = self._read_reserve_books()
        reading_history = self._read_read_books()

        is_reading_found = reading_history.status_code != 404
        is_reservation_found = reservation_history.status_code != 404
        is_something_found = (
            is_reading_found or
            is_reservation_found
        )
        is_reading_in_error = reading_history.status_code != 200
        is_reservation_in_error = reservation_history.status_code != 200

        if not is_something_found:
            data = Response(
                {
                    'msg': "Nothing found",
                    "error_msg": "Nothing found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        else:
            temp_data = dict()
            if is_reading_in_error:
                data = reading_history

            elif is_reservation_in_error:
                data = reservation_history

            else:
                temp_data = dict()
                if is_reading_found:
                    temp_data["reading"] = reading_history.data["read"]
                else:
                    temp_data["reading"] = list()
                if is_reservation_found:
                    temp_data["reservation"] = reservation_history.data["reserve"]
                else:
                    temp_data["reservation"] = list()

                data = Response(
                    temp_data,
                    status=status.HTTP_200_OK
                )

        return data

    def _read_read_books(self):
        '''_read_read_books This method handles only the search on the db of the books read by the user.

        This private method performs a search on db in order to find
        any book with relationship type READ connected to the user
        passed in the constructor method.

        Returns:
            HTTPRespose: dictionary of user's read book and its status code.
        '''
        query = (
            "MATCH (u:User {username: $username}) "
            "OPTIONAL MATCH (u)-[read_rel:READ]->(b:Book) "

            "return read_rel, b.isbn"
        )
        params = {
            'username': self.username,
        }

        try:
            read_history = db.cypher_query(query, params=params)
            is_something_found = len(read_history[0]) > 0
            if is_something_found:
                data = Response(
                    {'read': read_history[0]},
                    status=status.HTTP_200_OK,
                )
            else:
                data = Response(
                    {
                        'msg': "Nothing found",
                        "error_msg": "Nothing found"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

        except Exception as e:
            data = Response(
                {
                    'msg': "Unable to search for reading history",
                    'error_msg': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return data

    def _read_reserve_books(self):
        '''_read_reserve_books This method handles only the search on the db of the books reserved by the user.

        This private method performs a search on db in order to find
        any book with relationship type RESERVE connected to the user
        passed in the constructor method.

        Returns:
            [HTTPRespose]: dictionary of user's reserved book and its status code.
        '''
        query = (
            "MATCH (u:User {username: $username}) "
            "OPTIONAL MATCH (u)-[res_rel:RESERVE]->(b:Book) "

            "return res_rel, b.isbn, b.barcode"
        )
        params = {
            'username': self.username,
        }

        try:
            reserve_history = db.cypher_query(query, params=params)
            is_something_found = len(reserve_history[0]) > 0
            if is_something_found:
                data = Response(
                    {'reserve': reserve_history[0]},
                    status=status.HTTP_200_OK,
                )
            else:
                data = Response(
                    {
                        'msg': "Nothing found",
                        "error_msg": "Nothing found"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

        except Exception as e:
            data = Response(
                {
                    'msg': "Unable to search for reservation history",
                    'error_msg': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return data
