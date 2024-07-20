
from library.constants import (
    AUTHORS,
    BOOKS,
    PREVIEWS,
    PUBLISHERS,
    SAGAS,
    LIBRARIES,
    USERS,
)


class ReadConstantsDao():
    '''ReadConstantsDao This class loads the constants calculated at the start of the app.

    This class loads all the constants (book nodes, authors nodes and so on) that are calculated just once.
    It makes them available to other classe though its methods.
    The class expose the following methods:

    - fetch_authors
    - fetch_books
    - fetch_libraries
    - fetch_previews
    - fetch_publishers
    - fetch_sagas
    - fetch_users
    '''

    def __init__(self):
        '''__init__ Constructor

        Constructor of the class
        '''
        pass

    def fetch_authors(self):
        '''fetch_books This method returns all the authors

        This method returns a list of all the authors that belongs to the catalog.
        It basically loads library.constants.AUTHORS and return it.

        Returns:
            list: a list with all the items.
        '''
        return AUTHORS

    def fetch_books(self):
        '''fetch_books This method returns all the books

        This method returns a list of all the book that belongs to the catalog.
        It basically loads library.constants.BOOKS and return it.

        Returns:
            list: a list with all the items.
        '''
        return BOOKS

    def fetch_libraries(self):
        '''fetch_libraries This method returns all the libraries

        This method returns a list of all the libraries that belongs to the library circuit.
        It basically loads library.constants.LIBRARIES and return it.

        Returns:
            list: a list with all the items.
        '''
        return LIBRARIES

    def fetch_previews(self):
        '''fetch_previews This method returns all the authors

        This method returns a list of all the authors that belongs to the catalog.
        It basically loads library.constants.AUTHORS and return it.

        Returns:
            list: a list with all the items.
        '''
        return PREVIEWS

    def fetch_publishers(self):
        '''fetch_publishers This method returns all the publishers

        This method returns a list of all the publishers that belongs to the catalog.
        It basically loads library.constants.PUBLISHERS and return it.

        Returns:
            list: a list with all the items.
        '''
        return PUBLISHERS

    def fetch_sagas(self):
        '''fetch_sagas This method returns all the sagas

        This method returns a list of all the sagas that belongs to the catalog.
        It basically loads library.constants.SAGAS and return it.

        Returns:
            list: a list with all the items.
        '''
        return SAGAS

    def fetch_users(self):
        '''fetch_users This method returns all the users

        This method returns a list of all the users that belongs to the catalog.
        It basically loads library.constants.USERS and return it.

        Returns:
            dict: a dict with all the items.
        '''
        return USERS
