
from rest_framework import status
from rest_framework.response import Response

from neomodel import db

from ._modelentities import MODEL_ENTITIES
from backend.models import (
    Book,
)
from .readnodedao import ReadNodeDao


class CreateBookCopyDao():
    '''CreateBookCopyDao This class handles the creation of a book node on data db (Neo4J).

    The class expose the following methods:

    - create_copy: to create a new book of an already existing book.

    '''

    def __init__(self):
        '''__init__ Constructor

        Constructor of the class
        '''
        pass

    def create_copy(self, isbn, library):
        '''create_copy This method handles the request to add a new copy of an already existing book.

        This method takes the isbn, search the highest barcode for that isbn and increased it by 1.
        If the copy is the number #999, it returns a failure (barcode is isbn + number of copy, cap 999).

        Args:
            isbn (string): soft id of the book from which it can copy attributes and relationships.
            library (string): id of the library that will hosts the copy.

        Returns:
            HTTPResponse: dictionary with the result of the operations.
            The body is under the key "msg" or "error_msg".
        '''
        greatest_barcode = self._retrieve_highest_barcode(isbn=isbn)
        is_successful = greatest_barcode.status_code == 200
        if is_successful:
            nodes = self._retrieve_nodes_for_new_copy(
                greatest_barcode=greatest_barcode.data,
                isbn=isbn,
                library=library,
            )
            is_successful = nodes.status_code == 200
            if is_successful:
                return self._create_new_nodes_for_new_copy(*nodes.data)
            else:
                return Response(
                    {"error_msg": "error in retrieving barcode",
                        "error_msg": nodes.data},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(
                {"error_msg": "error in retrieving barcode",
                    "error_msg": greatest_barcode.data},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _retrieve_highest_barcode(self, isbn):
        '''_retrieve_highest_barcode This method retrieves the highest barcode in all the libraries for the new copy.

        This private method performs a query towards data db in order to find the greatest barcode for the isbn.
        The barcode has format <isbn><incremental>.
        This method can therefore find the greatest barcode related to a provided isbn.

        Args:
            isbn (string): soft id of the book

        Returns:
            HTTPResponse: dictionary with the highest barcode and its status code.
            The body is under the key "msg" or "error_msg".
        '''
        query = (
            "MATCH (b:Book) "
            'WHERE b.isbn = $isbn '
            "return b.barcode "
            "order by b.barcode desc"
        )
        params = {"isbn": str(isbn)}

        try:
            greatest_barcode = db.cypher_query(query, params=params)
            greatest_barcode = greatest_barcode[0][0][0]
            data = Response(greatest_barcode, status=status.HTTP_200_OK)

        except Exception as e:
            data = Response(
                {"error_msg": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return data

    def _retrieve_nodes_for_new_copy(self, isbn, greatest_barcode, library):
        '''_retrieve_nodes_for_new_copy This method retrieves a copy of the book to be used as model.

        This private method performs a query towards data db in order to find the an already listed book
        with the same isbn.
        It then return all the attribute of the node and the related nodes.
        It fullfill a list that is returned to the caller [Book, author, publisher, library, saga]

        Args:
            isbn (string): soft id of the book

        Returns:
            HTTPResponse: dictionary with a list of nodes and its status code.
            The body is under the key "msg" or "error_msg".
        '''
        # checking if maximum copy number has exceeded
        copy_number = int(greatest_barcode) % 1000
        is_copy_number_exceeded = copy_number == 999
        if is_copy_number_exceeded:
            data = Response(
                {"error_msg": "Exceeded maximum number of copy"},
                status=status.HTTP_501_NOT_IMPLEMENTED
            )
            return data

        # all fine, increment copy number
        new_copy_number = copy_number + 1
        new_barcode = "%s%s" % (isbn, str(new_copy_number).zfill(3))

        query = (
            "MATCH (b:Book)-[bel:BELONGS_TO]->(s:Saga) "
            "MATCH (p:Publisher)-[pub:PUBLISHED]->(b) "
            "MATCH (a:Author)-[wro:WROTE]->(b) "
            'WHERE b.barcode = $greatest_barcode '
            "RETURN b.barcode, bel, s.series, pub, p.publishing, wro, a.author"
        )
        params = {"greatest_barcode": greatest_barcode}

        try:
            return_list = list()
            nodes = db.cypher_query(query, params)
            nodes = nodes[0][0]
            book = nodes[0]
            belongs_to = nodes[1]
            saga = nodes[2]
            publisher = nodes[4]
            author = nodes[6]

            dao = ReadNodeDao()
            book_node = dao.filter_nodes(
                node_type=MODEL_ENTITIES['Book'],
                search_barcode=int(greatest_barcode)
            )[0]
            book_dict = book_node.serialize
            book_dict["node_properties"]["barcode"] = new_barcode
            book_dict["node_properties"]["date_published"] = datetime.strptime(
                book_dict["node_properties"]["date_published"], '%Y')
            return_list.append(book_dict)

            author_node = dao.filter_nodes(
                node_type=MODEL_ENTITIES['Author'],
                search_author=author
            )[0]
            return_list.append(author_node)

            publisher_node = dao.filter_nodes(
                node_type=MODEL_ENTITIES['Publisher'],
                search_publisher=publisher
            )[0]
            return_list.append(publisher_node)

            library_node = dao.filter_nodes(
                node_type=MODEL_ENTITIES['Library'],
                search_name=library
            )[0]
            return_list.append(library_node)

            saga_node = dao.filter_nodes(
                node_type=MODEL_ENTITIES['Saga'],
                search_series=saga
            )[0]
            return_list.append(saga_node)

            data = Response(return_list, status=status.HTTP_200_OK)

        except IndexError as e:
            data = Response(
                {"error_msg": str(e),
                 "level": "getter",
                 "current_list": "; ".join(elem for elem in return_list)},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            data = Response(
                {"error_msg": str(e),
                 "level": "getter"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        finally:
            return data

    def _create_new_nodes_for_new_copy(
        self,
        book_dict,
        author_node,
        publisher_node,
        library_node,
        saga_node
    ):
        '''_create_new_nodes_for_new_copy This method creates the new book node and link it with the related other nodes.

        This private method performs the creation of the new book node.
        It then links it with Author, Library, Saga... nodes as the carbon copy provided (actually the Library node is passed to the main method).
        Obviously, no User node is linked to this new node.

        Args:
            book_dict (dict): dictionary with book datas.
            author_node (dict): dictionary with author datas.
            publisher_node (dict): dictionary with publisher datas.
            library_node (dict): dictionary with library datas.
            saga_node (dict): dictionary with saga datas.

        Returns:
            HTTPResponse: dictionary with the result of the operations.
            The body is under the key "msg" or "error_msg".
        '''
        try:
            db.begin()
            new_copy = Book(**book_dict["node_properties"]).save()

            new_copy.belongs_to.connect(saga_node)
            publisher_node.published.connect(new_copy)
            library_node.hosted.connect(new_copy)
            author_node.wrote.connect(new_copy)
            db.commit()

        except Exception as e:
            db.rollback()
            data = Response(
                {"error_msg": str(e),
                    "level": "relationship creation"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            return data

        data = Response(
            {"msg": f"all done, new barcode {book_dict['node_properties']['barcode']}"},
            status=status.HTTP_200_OK)

        return data
