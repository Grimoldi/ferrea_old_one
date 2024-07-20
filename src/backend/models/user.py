from neomodel import (
    StructuredNode,
    DateTimeProperty,
    IntegerProperty,
    RegexProperty,
    StringProperty,
    RelationshipTo,
)
from ._userrelationship import (
    DateIntervalRelationship,
    DateRelationship,
    VoteRelationship,
)
from neomodel.contrib.spatial_properties import PointProperty
from .book import Book
from ._nodeutils import NodeUtils


class User(StructuredNode, NodeUtils):
    '''User This class defines the User node

    This class defines attributes and relationships for an User node.
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
                'email': self.email,
                'phone': self.phone,
                'address': self.address,
                'name': self.name,
                'role': self.role,
                'name': self.name,
                'surname': self.surname,
                'location': self.location,
                'card_number': self.card_number,
                'username': self.username,
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
                'nodes_related': self.serialize_relationships(self.reserve.all())
            },
            {
                'nodes_type': 'Book',
                'nodes_related': self.serialize_relationships(self.read.all())
            },
            {
                'nodes_type': 'Book',
                'nodes_related': self.serialize_relationships(self.vote.all())
            }
        ]

    email_regex = r"^[\w|\.|\-]+\@\w+\.(?:\w+\.)?(?:net|it|org|com)$"
    # address_regex = r"\w+\,\s(?:Via|Largo|Viale|Vicolo|Piazza)\s\w+(?:\s|\w)+\d{0,4}"
    address_regex = r".*"
    ROLES = {'Librarian': "Librarian", "User": "User"}

    email = RegexProperty(
        expression=email_regex,
        required=True,
        unique_index=True
    )
    phone = IntegerProperty()
    address = RegexProperty(expression=address_regex)
    role = StringProperty(
        choices=ROLES,
        default='User'
    )
    name = StringProperty(required=True)
    surname = StringProperty(required=True)
    username = StringProperty(required=True, unique_index=True)

    # calculated properties
    card_number = IntegerProperty(
        required=True,
        unique_index=True
    )
    # for points on Earth (lat, long)
    location = PointProperty(
        crs='wgs-84',
        required=True
    )

    # traverse outgoing relations
    reserve = RelationshipTo(
        Book,
        'RESERVE',
        model=DateRelationship
    )
    read = RelationshipTo(
        Book,
        'READ',
        model=DateIntervalRelationship
    )
    vote = RelationshipTo(
        Book,
        'VOTE',
        model=VoteRelationship
    )
