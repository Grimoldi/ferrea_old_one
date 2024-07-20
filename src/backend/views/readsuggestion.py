
from rest_framework.views import APIView
from backend.dao import Neo4jDao


class ReadSuggestion(APIView):
    '''ReadSuggestion This class handles the request for a suggestion based on user's books read.

    This class handles the request to retrieve any book or author suggestion given a certain user.
    '''

    def __init__(self):
        '''__init__ Constructor

        Constructor of the class
        '''
        pass

    def get(self, request, username, what, format=None):
        '''get This method gets the suggestion from the user.

        It gets the username from the request and return the suggested list.

        Args:
            request (HTTPRequest): the request object.
            username (string): id of the user.
            what (string): string to map what has to be suggested between book and author.
            format (string, optional): format of the response to provide (json, xml...). Defaults to None.

        Returns:
            HTTPResponse: data returned from the dao.
        '''
        dao = Neo4jDao()
        mapping = {
            "author": dao.read_suggested_authors,
            "book": dao.read_suggested_books,
        }
        suggestion_list = mapping[what](username=username)
        return suggestion_list
