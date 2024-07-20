
from django.urls import path, include

from .views.google import GoogleGetBook
from .views.openlibrary import OpenLibraryGetAuthorPortrait
from .views.searchbook import SearchBook

urlpatterns = [
    path('book/<isbn>', SearchBook.as_view(), name="search_book"),

    # direct path to external api for testing
    path('google/<isbn>', GoogleGetBook.as_view(), name="google"),
    path('open_library/<isbn>',
         OpenLibraryGetAuthorPortrait.as_view(), name="open_library"),
]
