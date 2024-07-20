
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from backend.dao import Neo4jDao


class CreateVote(APIView):
    '''CreateVote This class handles the creation of a new VOTE relationship

    This class creates a new VOTE relationship between a User node and a Book node.
    '''

    def post(self, request, format=None):
        '''post Method to create the VOTE relationship.

        This public method override the post method.
        It gets from the request the barcode and user info, than calls the appropriate dao.

        Args:
            request (HTTPRequest): the request object.
            format (string, optional): format of the response to provide (json, xml...). Defaults to None.

        Returns:
            HTTPResponse: data returned from the dao.
        '''

        print(request.data)
        create_info = {
            'username': request.data.get("username", None),
            'barcode': request.data.get("barcode", None),
            'star': request.data.get("star", None),
        }

        username = create_info["username"]
        barcode = create_info["barcode"]
        star = create_info["star"]

        # checking if mandatory fields are passed
        is_incorrect_request = \
            username is None or \
            barcode is None or \
            star is None

        if is_incorrect_request:
            return Response(
                {"error_msg": "Please make sure to pass all the mandatory fields from post data"},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            dao = Neo4jDao()
            # return create_vote(**create_info)
            return dao.create_vote(**create_info)
