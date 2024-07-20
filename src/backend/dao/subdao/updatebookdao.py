

from rest_framework import status
from rest_framework.response import Response
from .readnodedao import ReadNodeDao
from neomodel import db
from ._modelentities import MODEL_ENTITIES


class UpdateBookDao():
    '''UpdateBookDao This class handles any update to Book nodes.

    This class handles how a Book node can be modified.
    The class expose the following methods:

    - update_book
    '''

    def __init__(self):
        '''__init__ Constructor

        Constructor of the class
        '''
        self._MODEL_ENTITIES = MODEL_ENTITIES

    @ db.write_transaction
    def update_book(self, update_info):
        '''update_author This method performs the update of the node.

        This method implements the change through querying the data db (Neo4J).
        Update info dict should be:
        {
            barcode: "",
            field: "",
            value: "",
        }
        Args:
            update_info (dict): dictionary with the book id, the field to modify, and the new value.

        Returns:
            HTTPResponse: dictionary with the result of the operations.
            The body is under the key "msg" or "error_msg".
        '''
        barcode = update_info.get('isbn', None)
        value = update_info.get('value', None)
        field = update_info.get('field', None)
        dao = ReadNodeDao()
        try:
            book = dao.filter_nodes(
                node_type=self._MODEL_ENTITIES['Book'],
                search_barcode=barcode
            )[0]
            book.field = value
            book.save()
            data = {'msg': "Update done"}

        except Exception as e:
            data = {'msg': "Update failed", 'error_msg': str(e)}

        return data
