from neomodel import (
    StructuredNode,
    StringProperty,
    RelationshipTo
)
from ._nodeutils import NodeUtils
from .book import Book


class Publisher(StructuredNode, NodeUtils):
    '''Publisher This class defines the Publisher node

    This class defines attributes and relationships for an Publisher node.
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
                'publishing': self.publishing,
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
                'nodes_related': self.serialize_relationships(self.published.all())
            }
        ]

    publishing = StringProperty(unique_index=True, default='NA')

    # traverse outgoing relations
    published = RelationshipTo(Book, 'PUBLISHED')
