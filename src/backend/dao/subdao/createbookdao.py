
from rest_framework import status
from rest_framework.response import Response
import regex

from backend.models import (
    Author,
    Book,
    Library,
    Publisher,
    Saga,
)
from .readconstantsdao import ReadConstantsDao
from library.constants import (
    MAX_FUZZY_DISTANCE,
)
from .readnodedao import ReadNodeDao
from datetime import datetime
from neomodel import db


class CreateBookDao():
    '''CreateBookDao This class handles the creation of a book node on data db (Neo4J).

    The class expose the following methods:

    - create_book: to create a new book from scratch.

    '''

    def __init__(self):
        '''__init__ Constructor

        Constructor of the class
        '''
        pass

    def create_book(self, create_info):
        '''create_book This method handles the request to create a new book that doesn't already belongs to libraries.

        This method takes data from the dictionary create_info, search with Fuzzy research if some node is already created
        (e.g. an Author is already present in db), the creates and links all the new nodes.
        Note that no User node is involved.

        Args:
            create_info (dict): dictionary with the data to create all nodes.

        Returns:
            HTTPResponse: dictionary with the result of the operations and its status code.
            The body is under the key "msg" or "error_msg".
        '''
        standard_data = self._standardize_input_data(create_info=create_info)
        is_successful = standard_data.status_code == 200
        if is_successful:
            return self._merge_new_nodes(merge_data_list=standard_data.data["resp"])
        else:
            return Response({
                "error_msg": "Standardize data wasn't successfull",
                "error_msg": standard_data.data
            },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _standardize_input_data(self, create_info):
        '''_standardize_input_data This method tries to find if some nodes are already created on db.

        This private method performs a Fuzzy search to the db in order to find if some node is already created.
        If it finds anything, the result take the place of the data passed to the public method.
        If nothing is found, the data is unchanged.

        Args:
            create_info (dict): dictionary with the data to create all nodes.

        Returns:
            HTTPResponse: dictionary with a list of nodes and its status code.
            [Author, Publisher, Saga, Book, Library]
        '''
        node_list = list()
        keywords = {"Author": "author",
                    "Publisher": "publishing", "Saga": "series"}

        for label in ["Author", "Publisher", "Saga"]:
            # search if any of author, publisher or saga is already present
            element_in_list = self._retrieve_fuzzy_node_from_list(
                node_label=label, filter_keyword=create_info[keywords[label]])
            is_found = element_in_list.status_code == 200

            # if present, append the id of the node to the list
            if is_found:
                element_in_list = element_in_list.data
                dao = ReadNodeDao()
                '''
                node = dao.fetch_nodes(
                    {"node_type": label,  keywords[label]: element_in_list})
                '''
                node = dao.fetch_node_details(node_info={
                    "node_type": label,
                    "node_id": element_in_list
                })

                temp_dict = dict()
                temp_dict[keywords[label]] = \
                    node["node_properties"][keywords[label]]
                temp_dict["node_type"] = label
                node_list.append(temp_dict)

            # if not present, append the data coming from the post to the list
            else:
                node_list.append({
                    keywords[label]: create_info[keywords[label]],
                    "node_type": label
                })

        # append new book data coming from the post
        temp_dict = dict()
        temp_dict["node_type"] = "Book"
        temp_dict["isbn"] = create_info["isbn"]
        temp_dict["comments"] = create_info["comments"]
        temp_dict["title"] = create_info["title"]
        temp_dict["pub_format"] = create_info["pub_format"]
        temp_dict["language"] = create_info["language"]
        temp_dict["date_published"] = datetime.strptime(
            create_info["date_published"], '%Y')
        temp_dict["cover"] = create_info["cover"]
        temp_dict["barcode"] = "%s001" % create_info["isbn"]
        node_list.append(temp_dict)

        # append library data coming from the post
        temp_dict = dict()
        temp_dict["node_type"] = "Library"
        temp_dict["name"] = create_info["library"]
        node_list.append(temp_dict)

        return Response({"resp": node_list}, status=status.HTTP_200_OK)

    def _retrieve_fuzzy_node_from_list(self, node_label, filter_keyword):
        '''_retrieve_fuzzy_node_from_list This method performs the fuzzy search of the node on its specific list.

        This private method performs the fuzzy search on the list of nodes related to the inspected node.
        If anything is found, it returns the data taken from the list instead the data provided.

        Args:
            node_label (string): label of the node.
            filter_keyword (string): attribute on which filter the node list.

        Returns:
            HTTPResponse: dictionary with the element to be considered and its status code.
        '''

        dao = ReadConstantsDao()
        node_keyword_dict = {
            "Author": dao.fetch_authors(),
            "Publisher": dao.fetch_publishers(),
            "Saga": dao.fetch_sagas(),
        }

        try:
            elements_list = node_keyword_dict[node_label]

        except KeyError:
            data = Response(
                {"error_msg": "Unable to find key %s. Please verify" %
                    (node_label)},
                status=status.HTTP_400_BAD_REQUEST
            )
            return data

        except Exception as e:
            data = Response(
                {"error_msg": "Unable to find list due to %s" % (e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            return data

        pattern_string = filter_keyword
        for element in elements_list:
            query_string = element
            r = regex.compile('(%s){e<=%s}' %
                              (pattern_string, MAX_FUZZY_DISTANCE))
            fuzzy_result = r.match(query_string)
            is_found = fuzzy_result is not None

            if is_found:
                data = Response(element, status=status.HTTP_200_OK)
                break
            else:
                data = Response("", status=status.HTTP_404_NOT_FOUND)

        return data

    def _merge_new_nodes(self, merge_data_list):
        '''_merge_new_nodes This method creates all the nodes on the data db (Neo4J).

        This private method creates the book node and merges all other nodes in order to avoid creating a duplicated.

        Args:
            merge_data_list (list): list of nodes to be created/merged on db.

        Returns:
            HTTPResponse: dictionary with the result of the operations.
            The body is under the key "msg" or "error_msg".
        '''

        try:
            author_dict = merge_data_list[0]
            author_dict.pop("node_type")
            publisher_dict = merge_data_list[1]
            publisher_dict.pop("node_type")
            saga_dict = merge_data_list[2]
            saga_dict.pop("node_type")
            book_dict = merge_data_list[3]
            book_dict.pop("node_type")
            library_dict = merge_data_list[4]
            library_dict.pop("node_type")

        except Exception as e:
            data = Response(
                {"error_msg": str(e),
                    "level": "Not all parameters where found"},
                status=status.HTTP_400_BAD_REQUEST
            )
            return data

        try:
            db.begin()
            # creating nodes (apart from library)
            book_node = Book.get_or_create(book_dict)[0]
            author_node = Author.get_or_create(author_dict)[0]
            publisher_node = Publisher.get_or_create(publisher_dict)[0]
            saga_node = Saga.get_or_create(saga_dict)[0]
            library_node = Library.nodes.get(**library_dict)

            # creating relationship
            book_node.belongs_to.connect(saga_node)
            publisher_node.published.connect(book_node)
            library_node.hosted.connect(book_node)
            author_node.wrote.connect(book_node)
            author_node.serialized.connect(saga_node)

            db.commit()
            data = Response(
                {"msg": f"all done"},
                status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            db.rollback()
            data = Response(
                {"error_msg": str(e),
                    "level": "new nodes creation"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return data
