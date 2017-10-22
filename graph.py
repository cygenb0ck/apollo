# coding: utf-8


class node(object):
    def __init__(self, name):
        """

        :param name:
        :type name: str
        """
        self.name = name
        self.edges = {}

    def add_edge(self, edge, node ):
        """
        adds an edge to the node.
        :param edge: the edge connecting this node to the passed in node
        :type edge: edge
        :param node: the node we want a connection to
        :type node: node
        :return:
        """
        self.edges[node.name] = edge


class edge(object):
    def __init__(self, node_1, node_2):
        """

        :param node_1:
        :type node_1: node
        :param node_2:
        :type node_2: node
        """
        self.nodes = {node_1.name: node_1, node_2.name: node_2}
        node_1.add_edge(self, node_2)
        node_2.add_edge(self, node_1)
        self.raw_edges = []

    def add_raw_edge(self, raw_edge):
        """
        adds a raw edge
        :param raw_edge:
        :type raw_edge: tuple(int, int)
        :return: None
        """
        self.raw_edges.append(raw_edge)

class node_factory(object):
    nodes = {}

    @classmethod
    def get_node(cls, name):
        if name not in cls.nodes:
            cls.nodes[name] = node(name)
        return cls.nodes[name]

class edge_factory(object):
    edges = {}

    @classmethod
    def get_edge(cls, node1, node2):
        ids = [node1.name, node2.name]
        ids.sort()
        id = "_".join(ids)
        if id not in cls.edges:
            cls.edges[id] = edge(node1, node2)
        return cls.edges[id]
