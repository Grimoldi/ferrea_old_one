
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from backend.dao import Neo4jDao


class ReadLists(APIView):
    '''ReadLists This class handles the request to retrieve any list of nodes in the catalog.

    This class handles any request to retrieve anyone of the lists of nodes and relationships on data db (Neo4J).
    An example could be book list, author list, but also preview list (a small list with book and author to be rendered).
    '''

    def get(self, request, listname, format=None):
        '''get This method gets the list from the listname.

        This method will return a list given its listname (book, author, saga...).

        Args:
            request (HTTPRequest): the request object.
            listname (string): the name of the list.
            format (string, optional): format of the response to provide (json, xml...). Defaults to None.

        Returns:
            HTTPResponse: data returned from the dao.
        '''

        dao = Neo4jDao()
        corrispondence = {
            "author": dao.fetch_authors,
            "book": dao.fetch_books,
            "library": dao.fetch_libraries,
            "preview": dao.fetch_previews,
            "publisher": dao.fetch_publishers,
            "saga": dao.fetch_sagas,
            "user": dao.fetch_users,
        }
        nodes = corrispondence[listname]()

        data = Response(
            {
                'response': {
                    'status': 200,
                    'rows': len(nodes),
                    'data': nodes,
                },
            },
            status=status.HTTP_200_OK)
        return data
