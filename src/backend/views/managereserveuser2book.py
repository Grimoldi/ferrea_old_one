
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from backend.dao import Neo4jDao
from library.constants import MAX_CONCURRENT_BOOKS_HOLD


class ManageReserveUser2Book(APIView):
    '''ManageReserveUser2Book This class handles the creation or deletion of a RESERVE relationship.

    This class creates or deletes a RESERVE relationship between a User node and a Book node.
    '''

    def _retrieve_params(self, request):
        '''_retrieve_params This method retrieves the params from the request.

        This private method checks if all the requested parameters are passed in the request.
        If not, it returns a 400_BAD_REQUEST.

        Args:
            request (HTTPRequest): the request object.

        Returns:
            HTTPResponse: data check result.
        '''
        self.dao = Neo4jDao()
        print(request.data)
        try:
            infos = {
                # user
                'username': request.data['username'],
                # book
                'barcode': request.data['barcode'],
                # reserve
                'when': request.data.get('when', None),
            }
            data = Response(
                infos, status=status.HTTP_200_OK
            )
        except KeyError as missing_key:
            data = Response(
                {"error_msg": f"Field {missing_key} is missing from post data. Please check"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return data

    def delete(self, request, format=None):
        '''delete Method to delete the RESERVE relationship.

        This public method override the delete method.
        It gets from the request the barcode and username info, than calls the appropriate dao.
        Expected data in request.data are
        {
            username,
            barcode,
        }

        Args:
            request (HTTPRequest): the request object.
            format (string, optional): format of the response to provide (json, xml...). Defaults to None.

        Returns:
            HTTPResponse: data returned from the dao.
        '''
        delete_info = self._retrieve_params(request)
        is_info_successfull = delete_info.status_code == 200
        if is_info_successfull:
            return self.dao.delete_reserve(
                delete_info.data["username"],
                delete_info.data["barcode"],
            )
        else:
            return delete_info

    def post(self, request, format=None):
        '''post Method to create the RESERVE relationship.

        This public method override the post method.
        It gets from the request the barcode and username info, than calls the appropriate dao.
        Expected data in request.data are
        {
            username,
            barcode,
            [when (timestamp, optional)]
        }

        First, it checks if the user is holding more books than permitted
        If not, it creates the read relationship.

        Args:
            request (HTTPRequest): the request object.
            format (string, optional): format of the response to provide (json, xml...). Defaults to None.

        Returns:
            HTTPResponse: data returned from the dao.
        '''
        create_info = self._retrieve_params(request)
        is_info_successfull = create_info.status_code == 200
        if is_info_successfull:
            books_hold = self.dao.read_users_books(
                create_info.data["username"],
                create_info.data["barcode"],
            )
            is_books_count_successfull = books_hold.status_code == 200
            if is_books_count_successfull:
                books_hold_int = (books_hold.data)["count"]
                is_already_at_max = books_hold_int >= MAX_CONCURRENT_BOOKS_HOLD
                if is_already_at_max:
                    data = Response(
                        {"error_msg": f"User is already holding max books: {MAX_CONCURRENT_BOOKS_HOLD}"},
                        status=status.HTTP_401_UNAUTHORIZED
                    )
                    return data
                else:
                    return self.dao.create_reserve(**create_info.data)
            else:
                return books_hold
        else:
            return create_info
