
from rest_framework import status
from rest_framework.response import Response
from neomodel.exceptions import DoesNotExist, MultipleNodesReturned
from backend.models import (
    Author,
    Book,
    Publisher,
    Saga,
    Library,
    User,
)
from ._modelentities import MODEL_ENTITIES
PAGE_LIMIT = 10


class ReadNodeDao():
    '''ReadNodeDao This class handles some utilities for a given label of nodes.

    This class handles some utilities for node search, such a serializer, filter nodes...
    The downfall of it, is that it really works on a single label of nodes.
    The class expose the following methods:

    - filter_nodes
    - count_nodes
    - fetch_nodes
    - fetch_node_details

    Raises:
        MultipleNodesReturned: if the get of a node (that must be with the node id) gets more than a single node.
        node_type.DoesNotExist: if the get of a node (that must be with the node id) gets no nodes.
    '''

    def __init__(self):
        '''__init__ Constructor

        Constructor of the class
        '''
        self.PAGE_LIMIT = PAGE_LIMIT
        self.MODEL_ENTITIES = MODEL_ENTITIES

    def filter_nodes(
        self,
        node_type,
        search_barcode=None,  # book
        search_author=None,  # author
        search_publisher=None,  # publisher
        search_series=None,  # saga
        search_name=None,  # library
        search_username=None  # user
    ):
        '''filter_nodes This method can filter a class of nodes based on an attribute.

        This method is capable of filtering a class of nodes (nodes with the same Label) based on the provided attribute.

        Args:
            node_type (StructuredNode): refer to models. The class of the node to be searched.
            search_barcode (string, optional): the filter for a book node. Defaults to None.
            search_author (string, optional): the filter for an author node. Defaults to None.
            search_publisher (string, optional): the filter for a publisher node. Defaults to None.
            search_series (string, optional): the filter for a saga node. Defaults to None.
            search_name (string, optional): the filter for a library node. Defaults to None.
            search_username (string, optional): the filter for a user node. Defaults to None.

        Returns:
            HTTPResponse: dictionary with the result of the operations.
            The body is under the key "nodes"".
        '''
        node_set = node_type.nodes

        mapping = {
            "Author": [search_author],
            "Book": [search_barcode],
            "Publisher": [search_publisher],
            "Library": [search_name],
            "Saga": [search_series],
            "User": [search_username],
        }

        node_label = node_type.__name__
        fields_list = mapping[node_label]
        is_filter_found = False

        for field in fields_list:
            is_filter_set = field is not None
            if is_filter_set:
                filter_value = field
                is_filter_found = True
                break

        if not is_filter_found:
            data = Response(
                {"error_msg": "Filter not found"},
                status=status.HTTP_400_BAD_REQUEST
            )
            return data

        filtering = {
            "Author": node_set.filter(author__contains=filter_value),
            "Book": node_set.filter(barcode__exact=filter_value),
            "Publisher": node_set.filter(publishing__contains=filter_value),
            "Library": node_set.filter(name__contains=filter_value),
            "Saga": node_set.filter(series__contains=filter_value),
            "User": node_set.filter(username__exact=filter_value),
        }

        data = Response(
            {"nodes": filtering[node_label]},
            status=status.HTTP_200_OK,
        )

        return data

    def count_nodes(self, count_info):
        '''count_nodes This method counts the number of node that match a given criteria.

        This method perform a filter on the data db (Neo4J) that return the counter of the nodes,
        as well as the nodes that matched.
        count_info dict fields:
        {
            'node_type': '',
            'isbn': '',
            'author': '',
            'publisher': '',
        }

        Args:
            count_info (dict): dictionary with the node type and the filter key.

        Returns:
            HTTPResponse: dictionary with the result of the operations.
            The body is under the key "count".
        '''
        count = dict()
        node_type = count_info.get('node_type', None)
        search_isbn = count_info.get('isbn', None)
        search_author = count_info.get('author', None)
        search_publisher = count_info.get('publisher', None)

        node_set = self.filter_nodes(
            self.MODEL_ENTITIES[node_type],
            search_isbn,
            search_author,
            search_publisher
        )
        count['count'] = len(node_set)

        return count

    def fetch_nodes(self, fetch_info):
        '''fetch_nodes This method fetch the nodes matching a given criteria, displaying them in pages.

        This method is similar to filter_nodes, except that it split the results in multiple pages.
        In case of large response, it should be preferred to filter_nodes.

        fetch_info fields:
        {
            'node_type': '',
            'barcode': '',
            'author': '',
            'publishing': '',
            'series': '',
            'name': '',
            'username': '',
            'limit': '',
            'page': '',
        }

        Args:
            fetch_info (dict): dictionary with the node type, the filter attribute and the display options.

        Returns:
            HTTPResponse: dictionary with the result of the operations.
        '''
        node_type = fetch_info.get('node_type', None)
        search_barcode = fetch_info.get('barcode', None)
        search_author = fetch_info.get('author', None)
        search_publisher = fetch_info.get('publishing', None)
        search_series = fetch_info.get('series', None)
        search_name = fetch_info.get('name', None)
        search_username = fetch_info.get('username', None)

        # creating pages of limit passed
        # or PAGE_LIMIT if a limit is not specified
        limit = fetch_info.get('limit', self.PAGE_LIMIT)
        start = ((fetch_info.get('page', 1) - 1) * limit)
        end = start + limit

        node_set = self.filter_nodes(
            node_type=self.MODEL_ENTITIES[node_type],
            search_barcode=search_barcode,
            search_author=search_author,
            search_publisher=search_publisher,
            search_series=search_series,
            search_name=search_name,
            search_username=search_username,
        )

        is_node_set_succesfull = node_set.status_code == 200
        if is_node_set_succesfull:
            # returns a subset of nodes
            fetched_nodes = node_set.data["nodes"][start:end]

            return [node.serialize for node in fetched_nodes]

        else:
            return node_set

    def fetch_node_details(self, node_info):
        '''fetch_node_details This method gets a single node based on its unique id.

        This method is capable of getting a node based on its id.
        If the node found is not unique, a MultipleNodesReturned exception will be raised.
        node_info dict:
        {
            'node_type': '',
            'node_id': '',
        }

        Args:
            node_info (dict): dictionary with the label of the node and its id.

        Raises:
            MultipleNodesReturned: if the get of a node (that must be with the node id) gets more than a single node.
            node_type.DoesNotExist: if the get of a node (that must be with the node id) gets no nodes.

        Returns:
            HTTPResponse: dictionary with the result of the operations.
        '''
        node_type = node_info['node_type']
        node_id = node_info['node_id']
        node_ids = {
            "Author": "author",
            "Book": "barcode",
            "Publisher": "publishing",
            "Library": "name",
            "Saga": "series",
            "User": "username",
        }
        id_search = {
            node_ids[node_type]: node_id
        }
        # the get method returns a node
        # till the node_id provided is unique on the the db
        # if the id is not unique
        # it will raise a MultipleNodesReturned exception
        try:
            node = self.MODEL_ENTITIES[node_type].nodes.get(**id_search)
            node_details = node.serialize

            node_details['node_connections'] = []
            if (hasattr(node, 'serialize_connections')):
                node_details['node_connections'] = node.serialize_connections

        except MultipleNodesReturned:
            raise MultipleNodesReturned

        except (
            Author.DoesNotExist,
            Book.DoesNotExist,
            Library.DoesNotExist,
            Publisher.DoesNotExist,
            Saga.DoesNotExist,
            User.DoesNotExist,
        ):
            raise node_type.DoesNotExist

        except Exception as e:
            node_details = {"error_msg": e}

        return node_details
