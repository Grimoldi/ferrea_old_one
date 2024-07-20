from neomodel import (
    StructuredNode,
    StringProperty,
    RelationshipTo,
)
from neomodel.contrib.spatial_properties import PointProperty
from ._nodeutils import NodeUtils
from .book import Book


class Library(StructuredNode, NodeUtils):
    '''Library This class defines the Library node

    This class defines attributes and relationships for an Library node.
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
                'name': self.name,
                'phone': self.phone,
                'address': self.address
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
                'nodes_related': self.serialize_relationships(self.hosted.all())
            }
        ]

    name = StringProperty(unique_index=True)
    phone = StringProperty()
    address = StringProperty()
    location = PointProperty(crs='wgs-84')  # for points on Earth (lat, long)

    # traverse outgoing relations
    hosted = RelationshipTo(Book, 'HOSTS')
