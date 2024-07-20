
from geopy.geocoders import Nominatim
from neomodel.contrib.spatial_properties import NeomodelPoint
from rest_framework import status
from rest_framework.response import Response
from neomodel import db
from backend.models import (
    User,
)


class UpdateUserDao():
    '''UpdateUserDao This class handles any update to User nodes.

    This class handles how a User node can be modified.
    The class expose the following methods:

    - update_user
    '''

    def __init__(self):
        '''__init__ Constructor

        Constructor of the class
        '''
        pass

    def update_user(self, update_info):
        '''update_author This method performs the update of the node.

        This method implements the change through some call to private methods.
        Updatable data include:
        - address (with coordinates ofc)
        - phone
        - name
        - surname

        Update info dict should be:
        {
            phone,
            name,
            surname,
            username,
            address,
            lat,
            lon,
            email,
        }
        Args:
            update_info (dict): dictionary with the user id and the field to be modified.

        Returns:
            HTTPResponse: dictionary with the result of the operations.
            The body is under the key "msg" or "error_msg".
        '''
        address_for_location = "%s, %s" % (
            update_info["city"],
            update_info["address"].capitalize()
        )
        update_info["address"] = address_for_location
        location = self._retrieve_coordinate_from_address(address_for_location)
        has_loc_been_succesfull = location.status_code == 200

        if has_loc_been_succesfull:
            update_info["lon"] = location.data["lon"]
            update_info["lat"] = location.data["lat"]

            return self._update_user_node(update_info=update_info)

        else:
            return Response({
                "msg": "Retrieve of location wasn't successfull",
                "error_msg": location.data
            },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _retrieve_coordinate_from_address(self, address):
        '''_retrieve_coordinate_from_address This method retrieve the coordinates from user's address.

        This private method retrieves the coordinates from the address though geopy library.
        If the location cannot be retrieved, it returns a 404 status code.
        Format of the address provided will be
        City, Address number

        Args:
            address (string): address of the user.

        Returns:
            HTTPResponse: dictionary with the result of the operations.
            The body is under the key "msg" or "error_msg".
        '''
        geolocator = Nominatim(user_agent="my_geo_coder")
        location = geolocator.geocode(address)
        is_location_found = location is not None
        if is_location_found:
            coordinates = {
                'lat': location.latitude,
                'lon': location.longitude
            }
            data = Response(coordinates, status=status.HTTP_200_OK)
        else:
            data = Response(
                {"error_msg": "Coordinates not found, please verify"},
                status=status.HTTP_404_NOT_FOUND
            )

        return data

    def _update_user_node(self, update_info):
        '''_update_user_node This method performs the update of the node.

        This private method implements the change through querying the data db (Neo4J).
        Updatable data include:
        - address (with coordinates ofc)
        - phone
        - name
        - surname

        Update info dict should be:
        {
            phone,
            name,
            surname,
            username,
            address,
            lat,
            lon,
            email,
        }
        Args:
            update_info (dict): dictionary with the user id and the field to be modified.

        Returns:
            HTTPResponse: dictionary with the result of the operations.
            The body is under the key "msg" or "error_msg".
        '''
        try:
            email = update_info["email"]
            phone = update_info["phone"]
            address = update_info["address"]
            name = update_info["name"]
            surname = update_info["surname"]
            lat = update_info["lat"]
            lon = update_info["lon"]

        except Exception as e:
            data = Response(
                {'msg': "Data fetching failed", 'error_msg': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            return data

        try:
            db.begin()
            user = User.nodes.filter(email__exact=email)[0]
            user.phone = phone
            user.address = address
            user.name = name
            user.surname = surname
            user.location = NeomodelPoint((lon, lat), crs='wgs-84')
            user.save()
            db.commit()

            data = Response({'msg': "Update done"},
                            status=status.HTTP_200_OK)

        except Exception as e:
            db.rollback()
            data = Response(
                {'msg': "Update failed", 'error_msg': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return data
