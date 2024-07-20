
from neomodel import db
from geopy.geocoders import Nominatim
from neomodel.contrib.spatial_properties import NeomodelPoint

from rest_framework import status
from rest_framework.response import Response


class CreateUserDao():
    '''CreateUserDao This class handles the creation of a user node on data db (Neo4J).

    This class controls how a new user node is created on db.
    (User)
    The class expose the following methods:

    - create_user: to create a new user node.

    '''

    def __init__(self):
        '''__init__ Constructor

        Constructor of the class
        '''
        pass

    def create_user(self, create_info):
        '''create_user This method creates the User node.

        This method takes a dictionary with creation info, then it creates the node User.
        It calculates on the fly the user barcode and geographic coordinates of his address, then creates the node.

        Args:
            create_info (dict): dictionary with the data.

        Returns:
            HTTPResponse: dictionary with the result of the operations.
            The body is under the key "msg" or "error_msg".
        '''
        new_card_nr = self._retrieve_new_card_nr()
        has_card_been_succesfull = new_card_nr.status_code == 200

        address_for_location = "%s, %s" % (
            create_info["city"],
            create_info["address"].capitalize()
        )
        create_info["address"] = address_for_location

        location = self._retrieve_coordinate_from_address(address_for_location)
        has_loc_been_succesfull = location.status_code == 200

        if has_card_been_succesfull and has_loc_been_succesfull:
            create_info["card_number"] = new_card_nr.data
            create_info["lon"] = location.data["lon"]
            create_info["lat"] = location.data["lat"]

            return self._create_user_node(create_info)

        else:
            if not has_card_been_succesfull:
                return Response({
                    "error_msg": "Retrieve of card wasn't successfull",
                    "error_msg": new_card_nr.data
                },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            else:
                return Response({
                    "error_msg": "Retrieve of location wasn't successfull",
                    "error_msg": location.data
                },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

    def _retrieve_new_card_nr(self):
        '''_retrieve_new_card_nr This method find the highest card number above all users.

        This private method gets the last card created and then increase it by 1.

        Returns:
            HTTPResponse: dictionary with the result of the operations.
            The body is under the key "msg" or "error_msg".
        '''
        query = (
            "MATCH (u:User) "
            "return u.card_number "
            "order by u.card_number desc"
        )

        try:
            try:
                greatest_card = db.cypher_query(query)[0][0][0]
            except IndexError:
                greatest_card = 0
            new_card_number = int(greatest_card) + 1
            new_card_number = str(new_card_number).zfill(8)
            data = Response(new_card_number, status=status.HTTP_200_OK)

        except Exception as e:
            data = Response(
                {"error_msg": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return data

    def _retrieve_coordinate_from_address(self, address):
        '''_retrieve_coordinate_from_address This method finds the coordinates of user's address.

        This private method tries to find with geopy module the coordinates of user's address.

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

    def _create_user_node(self, create_info):
        '''_create_user_node This method creates the user node.

        This private method receives the creation info and then perform the creation of the node on db.
        create_info dict is expected to be like
        create_info = {
            email,
            phone,
            address,
            role,
            name,
            surname,
            username,
            card_number,
            lat,
            lon,
        }

        Args:
            create_info (dict): dictionary with the data.

        Returns:
            HTTPResponse: dictionary with the result of the operations.
            The body is under the key "msg" or "error_msg".
        '''
        try:
            email = create_info["email"]
            phone = create_info["phone"]
            address = create_info["address"]
            role = create_info["role"]
            name = create_info["name"]
            surname = create_info["surname"]
            username = create_info["username"]
            card_number = create_info["card_number"]
            lat = create_info["lat"]
            lon = create_info["lon"]

        except Exception as e:
            data = Response(
                {'msg': "Data fetching failed", 'error_msg': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            return data

        try:
            db.begin()
            user = User(
                email=email,
                phone=phone,
                address=address,
                role=role,
                name=name,
                surname=surname,
                username=username,
                card_number=card_number,
                location=NeomodelPoint((lon, lat), crs='wgs-84'),
            ).save()
            db.commit()

            data = Response({'msg': "Creation done"},
                            status=status.HTTP_200_OK)

        except Exception as e:
            db.rollback()
            data = Response(
                {'error_msg': "Creation failed", 'det': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return data
