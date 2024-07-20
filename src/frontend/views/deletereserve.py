
from rest_framework.views import APIView
from django.shortcuts import render, redirect
import os
from backend.views import ManageReserveUser2Book
from .userhistory import UserHistory


class DeleteReserve(APIView):
    '''DeleteReserve This class handles the deletion of a book reservation

    This class expose a delete method in order to cancel a reservation a user
    has made for a particolarly copy.

    Args:
        APIView (APIView): super class
    '''

    def __init__(self):
        '''__init__ Constructor

        Constructor of the class
        '''
        self._err_key = "error_msg"
        self._success_key = "success_msg"

    def delete(self, request, format=None):
        '''delete This method handles the request to remove a reservation

        This method gets from args the barcode and from request.session the user.
        Then performs a call to the backend module in order to remove the reservation
        of the user for the specific copy.

        Args:
            request (HTTPRequest): the request object
            format ([tring, optional): format of the response to provide (json, xml...). 
                Defaults to None.

        Return:
            HttpResponsePermanentRedirect: to the appropriate page to be rendered.
        '''
        context = dict()
        context["user"] = request.session["user"]

        user_from_post = request.data["username"]
        barcode_from_post = request.data["barcode"]
        is_same_user = context["user"] == user_from_post

        if not is_same_user:
            context[self._err_key] = "Are you trying to hacking me?"
            return redirect(f'/user_books/{user_from_post}')

        view = ManageReserveUser2Book()
        book_reservation_cancel = view.delete(
            request=request,
        )
        is_cancel_successfull = book_reservation_cancel.status_code == 200

        if is_cancel_successfull:
            has_previous_error = self._err_key in request.session
            if has_previous_error:
                request.session.pop(self._err_key)

            request.session[self._success_key] = "Reservation correctly canceled"
            context[self._success_key] = "Reservation correctly canceled"

        else:
            request.session.pop(self._success_key)
            request.session[self._err_key] = book_reservation_cancel.data[self._err_key]

        # print(request.path_info)

        view = UserHistory()
        return view.get(request=request, username=request.session["user"])
