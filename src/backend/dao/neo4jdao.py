from .subdao import (
    # create dao
    CreateBookCopyDao,
    CreateBookDao,
    CreateHostsDao,
    CreateLibraryDao,
    CreateReadDao,
    CreateReserveDao,
    CreateUserDao,
    CreateVoteDao,

    # read dao
    ReadBookDao,
    ReadBookLendDao,
    ReadBookSearchDao,
    ReadConstantsDao,
    ReadNodeDao,
    ReadSuggestedAuthorsDao,
    ReadSuggestedBooksDao,
    ReadUserDao,
    ReadUsersBooksDao,
    ReadUserHistoryDao,

    # update dao
    UpdateAuthorDao,
    UpdateBookDao,
    UpdateReadDao,
    UpdateUserDao,

    # delete dao
    DeleteReserveDao,
)


class Neo4jDao():
    '''Neo4jDao This class handles all the CRUD operations towards the data backend (Neo4j).

    This class is meant to be the only access point for all request towards the data backend.
    It exposes several method, which infact are only the call of a subclass dedicated to the specific operation.

    Example:
        In order to find a book, it exposes the read_book method, that just init the backend.dao.subdao.ReadBook
        class and return the call to the method exposed by the included class.

    '''

    def __init__(self):
        '''__init__ Constructor

        Constructor of the class.
        Only dao for read constants is instantied since it's the only Dao with more than one specific method
        to be called.
        '''
        self._dao = ReadConstantsDao()

    def create_book(self, create_info):
        '''create_book This method include the class backend.dao.subdao.CreateBookDao

        The method include the class backend.dao.subdao.CreateBookDao and call the create_book method.
        It is meant to create a new book.

        Args:
            create_info (dict): dictionary with the attribute for creation.

        Returns:
            HTTPResponse: object returned from the dao.
        '''
        dao = CreateBookDao()
        return dao.create_book(create_info=create_info)

    def create_book_copy(self, isbn, library):
        '''create_book_copy This method include the class backend.dao.subdao.CreateBookCopyDao

        The method include the class backend.dao.subdao.CreateBookDao and call the create_copy method.
        It is meant to create a new copy

        Args:
            isbn (string): isbn of the book already existing.
            library (string): unique id of the library to which link the new copy.

        Returns:
            HTTPResponse: object returned from the dao.
        '''
        dao = CreateBookCopyDao()
        return dao.create_copy(isbn=isbn, library=library)

    def create_hosts(self, create_info):
        '''create_hosts This method include the class backend.dao.subdao.CreateHostsDao

        The method include the class backend.dao.subdao.CreateHostsDao and call the create_hosts method.
        It is meant to create a new relationship between a library and a book.

        Args:
            create_info (dict): dictionary with the attribute for creation.

        Returns:
            HTTPResponse: object returned from the dao.
        '''
        dao = CreateHostsDao()
        return dao.create_hosts(create_info=create_info)

    def create_library(self, create_info):
        '''create_library This method include the class backend.dao.subdao.CreateLibraryDao

        The method include the class backend.dao.subdao.CreateLibraryDao and call the create_library method.
        It is meant to create a new library.

        Args:
            create_info (dict): dictionary with the attribute for creation.

        Returns:
            HTTPResponse: object returned from the dao.
        '''
        dao = CreateLibraryDao()
        return dao.create_library(create_info=create_info)

    def create_read(self, username, barcode, when):
        '''create_read This method include the class backend.dao.subdao.CreateReadDao

        The method include the class backend.dao.subdao.CreateReadDao and call the create_read method.
        It is meant to create a new relationship between a user and a book.

        Args:
            username (string): id of the user.
            barcode (string): id of the book.
            when (datetime.datetime): datetime attribute to add to the relationship.

        Returns:
            HTTPResponse: object returned from the dao.
        '''
        dao = CreateReadDao()
        return dao.create_read(username=username, barcode=barcode, when=when)

    def create_reserve(self, username, barcode, when):
        '''create_reserve This method include the class backend.dao.subdao.CreateReserveDao

        The method include the class backend.dao.subdao.CreateReserveDao and call the create_reserve method.
        It is meant to create a new relationship between a user and a book.

        Args:
            username (string): id of the user.
            barcode (string): id of the book.
            when (datetime.datetime): datetime attribute to add to the relationship.

        Returns:
            HTTPResponse: object returned from the dao.
        '''
        dao = CreateReserveDao()
        return dao.create_reserve(username=username, barcode=barcode, when=when)

    def create_user(self, create_info):
        '''create_user This method include the class backend.dao.subdao.CreateUserDao

        The method include the class backend.dao.subdao.CreateUserDao and call the create_user method.
        It is meant to create a new user.

        Args:
            create_info (dict): dictionary with the attribute for creation.

        Returns:
            HTTPResponse: object returned from the dao.
        '''
        dao = CreateUserDao()
        return dao.create_user(create_info=create_info)

    def create_vote(self, username, barcode, star):
        '''create_vote This method include the class backend.dao.subdao.CreateVoteDao

        The method include the class backend.dao.subdao.CreateVoteDao and call the create_vote method.
        It is meant to create a new relationship between a user and a book.

        Args:
            username (string): id of the user.
            barcode (string): id of the book.
            star (int): number of star the user wants to give to the book.

        Returns:
            HTTPResponse: object returned from the dao.
        '''
        dao = CreateVoteDao()
        return dao.create_vote(username=username, barcode=barcode, star=star)

    def delete_reserve(self, username, barcode):
        '''delete_reserve This method include the class backend.dao.subdao.DeleteReserveDao

        The method include the class backend.dao.subdao.DeleteReserveDao and call the delete_reserve method.
        It is meant to delete a relationship between a user and a book.

        Args:
            username (string): id of the user.
            barcode (string): id of the book.

        Returns:
            HTTPResponse: object returned from the dao.
        '''
        dao = DeleteReserveDao()
        return dao.delete_reserve(username=username, barcode=barcode)

    def read_book(self, isbn):
        '''read_book This method include the class backend.dao.subdao.ReadBookDao

        The method include the class backend.dao.subdao.ReadBookDao and call the read_book method.
        It is meant to read a book node with its attribute and/or relationships.

        Args:
            isbn (string): soft id of the book.

        Returns:
            HTTPResponse: object returned from the dao.
        '''
        dao = ReadBookDao()
        return dao.read_book(isbn=isbn)

    def read_book_lend(self):
        '''read_book_lend This method include the class backend.dao.subdao.ReadBookLendDao

        The method include the class backend.dao.subdao.ReadBookLendDao and call the read_book_lend method.
        It is meant to read all the book that have yet to be returned to library.

        Returns:
            HTTPResponse: object returned from the dao.
        '''
        dao = ReadBookLendDao()
        return dao.read_book_lend()

    def read_book_search(self, username, title, author, saga, status):
        '''read_book_search This method include the class backend.dao.subdao.ReadBookSearchDao

        The method include the class backend.dao.subdao.ReadBookSearchDao and call the read_book_search method.
        It is meant to query the data db in order to find if there's a match with user's search.

        Args:
            username (string): id of the user
            title (string): attribute of book node
            author (string): attribute of author node
            saga (string): attribute of saga node
            status (string): attribute of book node

        Returns:
            HTTPResponse: object returned from the dao.
        '''
        dao = ReadBookSearchDao()
        return dao.read_book_search(username=username, title=title, author=author, saga=saga, book_status=status)

    def read_suggested_authors(self, username):
        '''read_suggested_authors This method include the class backend.dao.subdao.ReadSuggestedAuthorsDao

        The method include the class backend.dao.subdao.ReadSuggestedAuthorsDao and call the read_suggested_authors method.
        It is meant to query the db in order to find authors with a similarity degree to user's previous reading.

        Args:
            username (string): id of the user.

        Returns:
            HTTPResponse: object returned from the dao.
        '''
        dao = ReadSuggestedAuthorsDao()
        return dao.read_suggested_authors(username=username)

    def read_suggested_books(self, username):
        '''read_suggested_books This method include the class backend.dao.subdao.ReadSuggestedBooksDao

        The method include the class backend.dao.subdao.ReadSuggestedBooksDao and call the read_suggested_books method.
        It is meant to query the db in order to find books with a similarity degree to user's previous reading.

        Args:
            username (string): id of the user.

        Returns:
            HTTPResponse: object returned from the dao.
        '''
        dao = ReadSuggestedBooksDao()
        return dao.read_suggested_books(username=username)

    def read_user(self, username):
        '''read_user This method include the class backend.dao.subdao.ReadUserDao

        The method include the class backend.dao.subdao.ReadUserDao and call the read_user method.
        It is meant to read a user node with its attribute and/or relationships.

        Args:
            username (string): id of the user.

        Returns:
            HTTPResponse: object returned from the dao.
        '''
        dao = ReadUserDao()
        return dao.read_user(username=username)

    def read_users_books(self, username, barcode):
        '''read_user This method include the class backend.dao.subdao.ReadUsersBooksDao

        The method include the class backend.dao.subdao.ReadUsersBooksDao and call the read_users_books method.
        It is meant to read a user node with its attribute and/or relationships.

        Args:
            username (string): id of the user.
            barcode (string): id of the book.

        Returns:
            HTTPResponse: object returned from the dao.
        '''
        dao = ReadUsersBooksDao()
        return dao.read_users_books(username=username, barcode=barcode)

    def read_user_history(self, username):
        '''read_user_history This method include the class backend.dao.subdao.ReadUserHistoryDao

        The method include the class backend.dao.subdao.ReadUserHistoryDao and call the read_history method.
        It is meant to read all books reserved or read by the user.

        Args:
            username (string): id of the user.

        Returns:
            HTTPResponse: object returned from the dao.
        '''
        dao = ReadUserHistoryDao(username=username)
        return dao.read_history()

    def update_author(self, update_info):
        '''update_author This method include the class backend.dao.subdao.UpdateAuthorDao

        The method include the class backend.dao.subdao.UpdateAuthorDao and call the update_author method.
        It is meant to update an author node based on the data provided.

        Args:
            update_info (dict): dictionary with the attribute for update.

        Returns:
            HTTPResponse: object returned from the dao.
        '''
        dao = UpdateAuthorDao()
        return dao.update_author(update_info=update_info)

    def update_book(self, update_info):
        '''update_book This method include the class backend.dao.subdao.UpdateBookDao

        The method include the class backend.dao.subdao.UpdateBookDao and call the update_book method.
        It is meant to update a book node based on the data provided.

        Args:
            update_info (dict): dictionary with the attribute for update.

        Returns:
            HTTPResponse: object returned from the dao.
        '''
        dao = UpdateBookDao()
        return dao.update_book(update_info=update_info)

    def update_read(self, username, barcode, when):
        '''update_read This method include the class backend.dao.subdao.UpdateReadDao

        The method include the class backend.dao.subdao.UpdateReadDao and call the update_read method.
        It is meant to update the relationship between a user and a book, when the book is returned.

        Args:
            username (dict): id of the user.
            barcode (string): id of the book.
            when (datetime.datetime): datetime attribute to add to the relationship.

        Returns:
            HTTPResponse: object returned from the dao.
        '''
        dao = UpdateReadDao()
        return dao.update_read(username=username, barcode=barcode, when=when)

    def update_user(self, update_info):
        '''update_user This method include the class backend.dao.subdao.UpdateUserDao

        The method include the class backend.dao.subdao.UpdateUserDao and call the update_user method.
        It is meant to update a user node based on the data provided.

        Args:
            update_info (dict): dictionary with the attribute for update.

        Returns:
            HTTPResponse: object returned from the dao.
        '''
        dao = UpdateUserDao()
        return dao.update_user(update_info=update_info)

    def fetch_authors(self):
        '''fetch_authors This method include the class backend.dao.subdao.ReadConstantsDao

        This method call the method fetch_authors on the dao instance created on the init of Neo4jDao object.

        Returns:
            HTTPResponse: object returned from the dao.
        '''
        return self._dao.fetch_authors()

    def fetch_books(self):
        '''fetch_books This method include the class backend.dao.subdao.ReadConstantsDao

        This method call the method fetch_books on the dao instance created on the init of Neo4jDao object.

        Returns:
            HTTPResponse: object returned from the dao.
        '''
        return self._dao.fetch_books()

    def fetch_libraries(self):
        '''fetch_libraries This method include the class backend.dao.subdao.ReadConstantsDao

        This method call the method fetch_libraries on the dao instance created on the init of Neo4jDao object.

        Returns:
            HTTPResponse: object returned from the dao.
        '''
        return self._dao.fetch_libraries()

    def fetch_previews(self):
        '''fetch_previews This method include the class backend.dao.subdao.ReadConstantsDao

        This method call the method fetch_previews on the dao instance created on the init of Neo4jDao object.

        Returns:
            HTTPResponse: object returned from the dao.
        '''
        return self._dao.fetch_previews()

    def fetch_publishers(self):
        '''fetch_publishers This method include the class backend.dao.subdao.ReadConstantsDao

        This method call the method fetch_publishers on the dao instance created on the init of Neo4jDao object.

        Returns:
            HTTPResponse: object returned from the dao.
        '''
        return self._dao.fetch_publishers()

    def fetch_sagas(self):
        '''fetch_sagas This method include the class backend.dao.subdao.ReadConstantsDao

        This method call the method fetch_sagas on the dao instance created on the init of Neo4jDao object.

        Returns:
            HTTPResponse: object returned from the dao.
        '''
        return self._dao.fetch_sagas()

    def fetch_users(self):
        '''fetch_users This method include the class backend.dao.subdao.ReadConstantsDao

        This method call the method fetch_users on the dao instance created on the init of Neo4jDao object.

        Returns:
            HTTPResponse: object returned from the dao.
        '''
        return self._dao.fetch_users()
