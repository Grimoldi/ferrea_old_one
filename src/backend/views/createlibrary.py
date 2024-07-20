
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from backend.dao import Neo4jDao


class CreateLibrary(APIView):
    '''CreateLibrary This class handles the creation of a new Library node.

    This class creates a new Library node on the db.
    '''

    def __init__(self):
        '''__init__ Constructor

        Constructor of the class
        '''
        pass

    def post(self, request, format=None):
        '''post Method to create the Library node.

        This public method override the post method.
        It gets from the request the attributes of the node, than calls the appropriate dao.

        Args:
            request (HTTPRequest): the request object.
            format (string, optional): format of the response to provide (json, xml...). Defaults to None.

        Returns:
            HTTPResponse: data returned from the dao.
        '''

        print(request.data)
        create_info = {
            'phone': request.data.get('phone', ''),
            'name': request.data.get('name', ''),
            'address': request.data.get('address', ''),
            'lat': request.data.get('lat', ''),
            'lon': request.data.get('lon', ''),
        }

        dao = Neo4jDao()
        nodes_response = dao.create_library(create_info=create_info)

        return nodes_response
