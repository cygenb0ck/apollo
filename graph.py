# coding: utf-8

import json


class SerializeableBase(object):
    __id = 1

    def __init__(self):
        self.id = SerializeableBase.__id
        SerializeableBase.__id += 1

    def to_json(self):
        raise RuntimeError("Not implemented for class {n}!".format(n=self.__class__.__name__))


class Node(SerializeableBase):
    def __init__(self, name):
        """

        :param name:
        :type name: str
        """
        super(Node, self).__init__()
        self.name = name
        self.edges = {}

    def to_json(self):
        return {
            "id" : self.id,
            "name": self.name,
            "edges" : [ e.id for e in self.edges.values() ]

        }

    def add_edge(self, edge, node ):
        """
        adds an edge to the node.
        :param edge: the edge connecting this node to the passed in node
        :type edge: Edge
        :param node: the node we want a connection to
        :type node: Node
        :return:
        """
        self.edges[node.name] = edge

    def is_equal(self, other):
        if self.name != other.name:
            return False

        print("self e", self.edges)
        print("other e", other.edges)

        if self.edges != other.edges:
            return False
        return True


class Edge(SerializeableBase):
    def __init__(self, node_1, node_2):
        """

        :param node_1:
        :type node_1: Node
        :param node_2:
        :type node_2: Node
        """
        super(Edge, self).__init__()

        self.nodes = {node_1.name: node_1, node_2.name: node_2}

        node_1.add_edge(self, node_2)
        node_2.add_edge(self, node_1)

        self.raw_edges = [] # type: list[tuple[int, int]]
        self.refined_value = None

    def to_json(self):
        return {
            "id": self.id,
            "nodes" : [n.id for n in self.nodes.values()],
            "raw_edges" : [(r[0], r[1]) for r in self.raw_edges],
            "refined_value" : self.refined_value
        }

    def add_raw_edge(self, raw_edge):
        """
        adds a raw edge
        :param raw_edge:
        :type raw_edge: tuple(int, int)
        :return: None
        """
        self.raw_edges.append(raw_edge)

    def refine(self, refine_func, min_len=None):
        if min_len and len(self.raw_edges < min_len):
            self.refined_value = -1

        self.refined_value = refine_func(self.raw_edges)


class Graph(object):
    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def get_node(self, name):
        if name not in self.nodes:
            self.nodes[name] = Node(name)
        return self.nodes[name]

    def node_from_mongo_json(self, mongo_json):
        # raise RuntimeError("implement me!")
        n = Node(mongo_json["name"])
        return n

    def get_edge(self, node1, node2):
        ids = [node1.name, node2.name]
        ids.sort()
        id = "_###_".join(ids)
        if id not in self.edges:
            self.edges[id] = Edge(node1, node2)
        return self.edges[id]

    def refine(self, refine_func):
        for e in self.edges.values():
            e.refine(refine_func)



class GraphJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (SerializeableBase)):
            return obj.to_json()
        return json.JSONEncoder.default(obj)


class RefineBase(object):
    def __init__(self, refine_function):
        self._func = refine_function

    def __call__(self, edge):
        self._func(edge)


class F_ar_mean_min():
    def __init__(self, min_len):
        self._min = min_len
    def __call__(self, raw_edges):
        pass


def mul_arithmetic_mean(raw_edges):
    return sum(x[0]*x[1] for x in raw_edges)/len(raw_edges)