
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from backend.dao import Neo4jDao


class ManageUser(APIView):
    '''ManageUser This class handles the creation, update or get of a User node.

    This class creates, updates or gets a User node.
    Please note that it doesn't store the password of the user.
    User is supposed to be already authenticated
    '''

    def post(self, request, format=None):
        '''post This method updates or creates a User node.

        This method gets the parameters from the post, checks if email value is passed.

        If email is already listed, it updates the values on db, otherwise it creates a new user.

        Args:
            request (HTTPRequest): the request object.
            format (string, optional): format of the response to provide (json, xml...). Defaults to None.

        Returns:
            HTTPResponse: data returned from the dao.
        '''

        print(request.data)
        create_info = {
            # user
            'email': request.data.get('email', None),
            'phone': request.data.get('phone', None),
            'address': request.data.get('address', None),
            'city': request.data.get('city', None),
            'role': request.data.get('role', 'User'),
            'name': request.data.get('name', None),
            'surname': request.data.get('surname', None),

            # username is populated in background by the login of the user
            'username': request.data.get("username", None),

            # location and card_number are calculated on the fly
        }

        dao = Neo4jDao()
        email = create_info["email"]
        phone = create_info["phone"]
        address = create_info["address"]
        city = create_info["city"]
        name = create_info["name"]
        surname = create_info["surname"]
        username = create_info["username"]
        usernames = dao.fetch_users().keys()

        # checking if mandatory fields are passed
        is_incorrect_request = \
            email is None or \
            phone is None or \
            address is None or \
            name is None or \
            surname is None or \
            username is None or \
            city is None

        if is_incorrect_request:
            return Response(
                {"error_msg": "Please make sure to pass all the mandatory fields from post data"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # checking if isbn is already present in db
        is_username_already_present = username in usernames

        if is_username_already_present:
            return dao.update_user(update_info=create_info)
        else:
            # return create_user(create_info=create_info)
            return dao.create_user(create_info=create_info)

    def get(self, request, username, format=None):
        '''get This method gets the user from the username.

        This method will perform a search on the db to find details of the user passed as arg.

        Args:
            request (HTTPRequest): the request object.
            username (string): id of the username.
            format (string, optional): format of the response to provide (json, xml...). Defaults to None.
        '''
        dao = Neo4jDao()
        user = dao.read_user(username=username)

        is_user_successfull = user.status_code == 200

        if not is_user_successfull:
            data = user

        else:
            user = user.data

            blacklist_fields = ["role", ]
            for blacklist_field in blacklist_fields:
                user.pop(blacklist_field)

            split_address = user["address"].split(",")
            user["city"] = split_address[0]
            user["address"] = ", ".join(split_address[1:])

            data = Response(
                {"user": user},
                status=status.HTTP_200_OK,
            )

        return data
