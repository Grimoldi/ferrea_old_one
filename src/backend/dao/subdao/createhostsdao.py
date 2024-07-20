
from backend.models import (
    Book,
    Library,
)
from neomodel import db

from rest_framework import status
from rest_framework.response import Response


class CreateHostsDao():
    '''CreateHostsDao This class handles the creation of a host relationship on data db (Neo4J).

    This class controls how a new hosts relationship is created on db.
    (Library)-[HOSTS]->(Book)
    The class expose the following methods:

    - create_hosts: to create a new hosts relationship.

    '''

    def __init__(self):
        '''__init__ Constructor

        Constructor of the class
        '''
        pass

    @ db.write_transaction
    def create_hosts(self, create_info):
        '''create_hosts This method creates the relationship HOSTS between library node and book node.

        This method takes a dictionary with barcode and library name, then it creates the relationship HOSTS.

        Args:
            create_info (dict): dictionary with the barcode and library.

        Returns:
            HTTPResponse: dictionary with the result of the operations.
            The body is under the key "msg" or "error_msg".
        '''
        library = create_info.get('library', "")
        barcode = create_info.get('barcode', "")

        try:
            library = Library.nodes.get(name=library)
            book = Book.nodes.get(barcode=barcode)
            library.hosted.connect(book)

            data = Response({'msg': "Creation done"},
                            status=status.HTTP_200_OK)

        except Exception as e:
            data = Response(
                {'error_msg': "Creation failed", 'error_msg': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return data
