
from django.shortcuts import render
from django.urls import path, include
from .views import (
    AddBook,
    BookDetails,
    DeleteReserve,
    HomeEndUser,
    HomeLibrarian,
    ListLend,
    Login,
    Logout,
    ReadBook,
    ReserveBook,
    ReturnBook,
    SearchBook,
    UserHistory,
    UserProfile,
)
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView

app_name = 'frontend'

urlpatterns = [
    # get (render login page)
    path('login', Login.as_view(), name="login"),

    # post (make login)
    path('ask_auth', Login.as_view(), name="ask_auth"),

    # get (render home end user page)
    path('home', HomeEndUser.as_view(), name="home"),

    # get (render home page librarian)
    path('librarian', HomeLibrarian.as_view(), name="search_book"),

    # get (render login page after logging user out)
    path('logout', Logout.as_view(), name="logout"),

    # get (render search book page)
    path('search_book', SearchBook.as_view(), name="search_book"),

    # post (send book query)
    path('perform_search', SearchBook.as_view(), name="perform_search"),

    # get (render single book page)
    path('details/<isbn>', BookDetails.as_view(), name="details"),

    # delete (remove reservation)
    path('delete_reservation',
         DeleteReserve.as_view(), name="delete_reservation"),

    # post (make a read)
    path('read', ReadBook.as_view(), name="read"),

    # post (make a reservation)
    path('reserve', ReserveBook.as_view(), name="reserve"),

    # get (render user's books history page)
    path('user_books/<username>', UserHistory.as_view(), name="user_books"),

    # get (render user's profile page)
    path('user_profile/<username>', UserProfile.as_view(), name="user_profile"),

    # post (make change to user profile)
    path('perform_edit', UserProfile.as_view(), name="user_profile"),

    # get (render librarian add book page, isbn or book form)
    path('add_new_book', AddBook.as_view(), name="add_new_book"),

    # post (make a lookup for the isbn or add a book to the library)
    path('perform_book_lookup', AddBook.as_view(), name="perform_book_lookup"),
    path('add_book_to_catalog', AddBook.as_view(), name="add_book_to_catalog"),

    # get (render librarian lend page)
    path('list_lends', ListLend.as_view(), name="list_lends"),

    # post (make the book change flagged as returned)
    path('return_book/', ReturnBook.as_view(), name="return_book"),


    # docs url
    path('docs/openapi-create', get_schema_view(
        title="Library",
        description="API for all things …"
    ), name='openapi-schema'),
    path('docs/openapi/', TemplateView.as_view(
        template_name='pages/openapi.html',
        extra_context={'schema_url': 'frontend:openapi-schema'}
    ), name='swagger-ui'),
    path('docs/sphinx/', include('docs.urls')),

]
