
from rest_framework import status
from rest_framework.response import Response

from neomodel import db
from .readnodedao import ReadNodeDao
from ._modelentities import MODEL_ENTITIES


class UpdateAuthorDao():
    '''UpdateAuthorDao This class handles any update to Author nodes.

    This class handles how an Author node can be modified.
    The class expose the following methods:

    - update_author
    '''

    def __init__(self):
        '''__init__ Constructor

        Constructor of the class
        '''
        self.MODEL_ENTITIES = MODEL_ENTITIES

    @ db.write_transaction
    def update_author(self, update_info):
        '''update_author This method performs the update of the node.

        This method implements the change through querying the data db (Neo4J).
        Update info dict should be:
        {
            author: "",
            field: "",
            value: "",
        }
        Args:
            update_info (dict): dictionary with the author id, the field to modify, and the new value.

        Returns:
            HTTPResponse: dictionary with the result of the operations.
            The body is under the key "msg" or "error_msg".
        '''
        author = update_info.get('author', None)
        value = update_info.get('value', None)
        field = update_info.get('field', None)
        dao = ReadNodeDao()
        try:
            author_node = dao.filter_nodes(
                node_type=self.MODEL_ENTITIES['Author'],
                search_author=author
            )[0]
            author_node.field = value
            author_node.save()
            data = Response(
                {'msg': "Update done"},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            data = Response(
                {'msg': "Update failed", 'error_msg': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return data
