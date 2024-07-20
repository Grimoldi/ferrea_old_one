from neomodel import (
    StructuredNode,
    StringProperty,
    RelationshipTo
)
import sys
from .book import Book
from .saga import Saga
from ._nodeutils import NodeUtils


class Author(StructuredNode, NodeUtils):
    '''Author This class defines the Author node

    This class defines attributes and relationships for an Author node.
    '''

    @property
    def serialize(self):
        '''serialize This method serialize the attributes of the node.

        This public method returns a dictionary of node's attribute from the node.

        Returns:
            dict: serialization of node's attributes.
        '''
        return {
            'node_properties': {
                'author': self.author,
                'author_sort': self.author_sort,
                'portrait': self.portrait,
            }
        }

    @property
    def serialize_connections(self):
        '''serialize_connections This method serialize the relationships of the node.

        This public method returns a dictionary of node's relationships from the node.

        Returns:
            dict: serialization of node's relationships.
        '''
        return [
            {
                'nodes_type': 'Book',
                'nodes_related': self.serialize_relationships(self.wrote.all())
            },
            {
                'nodes_type': 'Saga',
                'nodes_related': self.serialize_relationships(self.serialized.all())
            }
        ]

    author = StringProperty(unique_index=True, required=True)
    author_sort = StringProperty()
    portrait = StringProperty()

    # traverse outgoing relations
    wrote = RelationshipTo(Book, 'WROTE')
    serialized = RelationshipTo(Saga, 'SERIALIZED')
