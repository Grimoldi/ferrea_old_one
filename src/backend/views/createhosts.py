from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from backend.dao import Neo4jDao


class CreateHosts(APIView):
    '''CreateHosts This class handles the creation of a new HOSTS relationship.

    This class creates a new HOSTS relationship between a Library node and a Book node.
    '''

    def __init__(self):
        '''__init__ Constructor

        Constructor of the class
        '''
        pass

    def post(self, request, format=None):
        '''post Method to create the HOSTS relationship.

        This public method override the post method.
        It gets from the request the barcode and library info, than calls the appropriate dao.

        Args:
            request (HTTPRequest): the request object.
            format (string, optional): format of the response to provide (json, xml...). Defaults to None.

        Returns:
            HTTPResponse: data returned from the dao.
        '''

        print(request.data)
        create_info = {
            'barcode': request.data.get('barcode', ''),
            'library': request.data.get('library', ''),
        }
        dao = Neo4jDao()

        return dao.create_hosts(create_info=create_info)
