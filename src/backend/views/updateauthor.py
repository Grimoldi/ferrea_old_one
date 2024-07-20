
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from backend.dao import Neo4jDao


class UpdateAuthor(APIView):
    '''UpdateAuthor This class handles an Author node has to be updated.

    This class handles how an Author node should be updated.
    '''

    def put(self, request, format=None):
        '''put Method to update the Author node.

        This public method override the put method.
        This method gets the parameters from the put and call the method to update the node on db.

        Args:
            request (HTTPRequest): the request object.
            format (string, optional): format of the response to provide (json, xml...). Defaults to None.

        Returns:
            HTTPResponse: data returned from the dao.
        '''

        print(request.data)
        update_info = {
            'author': request.data.get('author', None),
            'value': request.data.get('value', None),
            'field': request.data.get('field', None),
        }
        is_correctly_set = update_info["author"] is not None \
            and update_info["value"] is not None \
            and update_info["field"] is not None

        # at least a parameter is missing, return 400_BAD_REQUEST
        if not is_correctly_set:
            data = Response(
                {"error_msg": f"At least a field is missing from post data. Please check"},
                status=status.HTTP_400_BAD_REQUEST
            )

            return data

        # return update_author(update_info)
        dao = Neo4jDao()
        return dao.update_author(update_info=update_info)
