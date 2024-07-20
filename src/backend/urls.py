
from django.urls import (
    include,
    path,
)

# views for CRUD operations
# create
from .views import (
    CreateBook,
    CreateLibrary,
    CreateHosts,
    CreateVote,

    ReadBook,
    ReadBookLend,
    ReadBookSearch,
    ReadLists,
    ReadSuggestion,
    ReadHistory,

    UpdateAuthor,
    UpdateBook,

    ManageReadUser2Book,  # create + update
    ManageReserveUser2Book,  # create + delete
    ManageUser,  # create + update + read
)

urlpatterns = [
    # CREATE
    # nodes
    path('create_book', CreateBook.as_view(), name="create_book"),
    path('create_library', CreateLibrary.as_view(), name="create_library"),
    path('create_user', ManageUser.as_view(), name="create_user"),
    # relationships
    path('create_hosts',
         CreateHosts.as_view(), name="create_hosts"),
    path('create_read',
         ManageReadUser2Book.as_view(), name="create_read"),
    path('create_reserve',
         ManageReserveUser2Book.as_view(), name="create_reserve"),
    path('create_vote', CreateVote().as_view(), name="create_vote"),

    # READ
    # list
    path('list/', include(
        [
            path('author', ReadLists.as_view(), {
                'listname': 'author'}, name="list_author"),
            path('book', ReadLists.as_view(), {
                'listname': 'book'}, name="list_book"),
            path('library', ReadLists.as_view(), {
                'listname': 'library'}, name="list_library"),
            path('preview', ReadLists.as_view(), {
                'listname': 'preview'}, name="list_preview"),
            path('publisher', ReadLists.as_view(), {
                'listname': 'publisher'}, name="list_publisher"),
            path('saga', ReadLists.as_view(), {
                'listname': 'saga'}, name="list_saga"),
            path('user', ReadLists.as_view(), {
                'listname': 'user'}, name="list_user"),
        ])
    ),
    # read
    path('book/<isbn>', ReadBook.as_view(), name="get_book"),
    path('read_book_lend', ReadBookLend.as_view(), name="read_book_lend"),
    path('read_history/<username>', ReadHistory.as_view(), name="read_history"),
    path('read_suggestion/', include(
        [
            path('author/<username>', ReadSuggestion.as_view(), {
                'what': 'author'}, name="suggest_author"),
            path('book/<username>', ReadSuggestion.as_view(), {
                'what': 'book'}, name="suggest_book"),
        ])
    ),
    path('user/<username>', ManageUser.as_view(), name="get_user"),

    # search
    path('search_book/<username>', ReadBookSearch.as_view(), name="search_book"),

    # UPDATE
    path('update_author', UpdateAuthor.as_view(),
         name="update_author"),
    path('update_book', UpdateBook.as_view(),
         name="update_book"),
    path('update_read', ManageReadUser2Book.as_view(),
         name="update_read"),
    path('update_user', ManageUser.as_view(),
         name="update_user"),

    # DELETE
    path('delete_reserve',
         ManageReserveUser2Book.as_view(), name="delete_reserve"),

]
