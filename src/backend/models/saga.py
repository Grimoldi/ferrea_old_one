from neomodel import (
    StructuredNode,
    StringProperty,
)
from ._nodeutils import NodeUtils


class Saga(StructuredNode, NodeUtils):
    '''Saga This class defines the Saga node

    This class defines attributes and relationships for an Saga node.
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
                'series': self.series,
            }
        }

    series = StringProperty(unique_index=True, required=True)
