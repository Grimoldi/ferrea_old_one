from abc import ABCMeta
from neomodel import db


class NodeUtils:
    ''' This class handles the serialization of relationships.

    The class expose the public method serialize_relationships that is able
    to serialize the relationships from an ending node.
    '''
    __metaclass__ = ABCMeta

    def serialize_relationships(self, nodes):
        '''serialize_relationships This method serialize the relationship that insists on a node.

        This public method gets a list of nodes as a parameter, than for each node
        it gets all the relationship incoming on the node and return the type of the relationship.

        Args:
            nodes (list): list of nodes that need to get their relationships.

        Returns:
            list: list with node serialization and type of relationships insisting on the node.
        '''
        serialized_nodes = []
        for node in nodes:
            # serialize node
            serialized_node = node.serialize

            query = (
                "MATCH (start_node) "
                "WHERE id(start_node) IN [$self] "
                "MATCH (end_node) "
                "WHERE id(end_node) IN [$end_node] "
                "MATCH (start_node)-[rel]-(end_node)"
                "RETURN type(rel) as node_relationship"
            )
            params = {'end_node': node.id}

            results, colums = self.cypher(query, params)
            serialized_node['node_relationship'] = results[0][0]

            serialized_nodes.append(serialized_node)

        return serialized_nodes
