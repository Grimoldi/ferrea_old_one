from neomodel import (
    StructuredNode,
    StringProperty,
    BooleanProperty,
    IntegerProperty,
    RegexProperty,
    DateTimeProperty,
    RelationshipTo,
    RelationshipFrom,
)
from datetime import datetime
from .saga import Saga
from ._nodeutils import NodeUtils


class Book(StructuredNode, NodeUtils):
    '''Book This class defines the Book node

    This class defines attributes and relationships for a Book node.
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
                'isbn': self.isbn,
                'comments': self.comments,
                'title': self.title,
                'pub_format': self.pub_format,
                'language': self.language,
                'date_published': self.date_published.strftime("%Y"),
                'cover': self.cover,
                'barcode': self.barcode,
                'status': self.status,
                'reservable': self.is_reservable,
                'readable': self.is_readable,
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
                'nodes_type': 'Saga',
                'nodes_related': self.serialize_relationships(self.belongs_to.all())
            },
            {
                'nodes_type': 'Publisher',
                'nodes_related': self.serialize_relationships(self.published.all())
            }
        ]

    isbn_regex = r"^\d{10}$|^\d{13}$"  # isbn is 10 or 13 digits
    STATUS = {'Available': "Available",
              "Unavailable": "Unavailable", "Unbookable": "Unbookable"}

    now = datetime.now()

    isbn = RegexProperty(
        expression=isbn_regex,
        required=True
    )
    comments = StringProperty(default="")
    title = StringProperty(default="")
    title_sort = StringProperty(default="")
    pub_format = StringProperty(default="", db_property="format")
    language = StringProperty(default="ita")
    date_published = DateTimeProperty(default=now)
    cover = StringProperty(default="")
    barcode = StringProperty(unique_index=True)
    status = StringProperty(choices=STATUS, default='Available')
    is_readable = BooleanProperty(default=True)
    is_reservable = BooleanProperty(default=True)

    # traverse outgoing relations
    belongs_to = RelationshipTo(Saga, 'BELONGS_TO')
