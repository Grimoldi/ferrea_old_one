
from backend.models import (
    Library,
)
from neomodel.contrib.spatial_properties import NeomodelPoint
from neomodel import db

from rest_framework import status
from rest_framework.response import Response


class CreateLibraryDao():
    '''CreateHostsDao This class handles the creation of a library node on data db (Neo4J).

    This class controls how a new library node is created on db.
    (Library)
    The class expose the following methods:

    - create_library: to create a new library node.

    '''

    def __init__(self):
        '''__init__ Constructor

        Constructor of the class
        '''
        pass

    @ db.write_transaction
    def create_library(self, create_info):
        '''create_library This method creates the Library node.

        This method takes a dictionary with creation info, then it creates the node Library.
        create_info dict is expected to be like:
        create_info = {
            name,
            address,
            phone,
            lat,
            lon,
        }

        Args:
            create_info (dict): dictionary with the data.

        Returns:
            HTTPResponse: dictionary with the result of the operations.
            The body is under the key "msg" or "error_msg".
        '''
        name = create_info.get('name', "")
        address = create_info.get('address', "")
        phone = create_info.get('phone', "")
        lat = create_info.get('lat', "")
        lon = create_info.get('lon', "")

        try:
            library = Library(
                name=name,
                address=address,
                location=NeomodelPoint((lon, lat), crs='wgs-84'),
                phone=phone
            ).save()

            data = Response({'msg': "Creation done"},
                            status=status.HTTP_200_OK)

        except Exception as e:
            data = Response(
                {'error_msg': "Creation failed", 'error_msg': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            print(e)

        return data
