# coding: utf-8

import json


class SerializeableBase(object):
    _id = 1

    def __init__(self):
        self.id = SerializeableBase._id
        SerializeableBase._id += 1

    def to_json(self):
        raise RuntimeError("Not implemented for class {n}!".format(n=self.__class__.__name__))


class Node(SerializeableBase):
    def __init__(self, name=None, json=None):
        """

        :param name:
        :type name: str
        """
        if name and json:
            raise RuntimeError("cannot construct from name and json")

        if name:
            super(Node, self).__init__()
            self.name = name
            self.edges = []

        elif json:
            self.id = json["id"]
            self.name = json["name"]
            self.edges = json["edges"]

        else:
            raise RuntimeError("cannot construct from nothing")

    @classmethod
    def from_name(cls, name):
        return Node(name=name)

    @classmethod
    def from_json(cls, json):
        return Node(json=json)

    def to_json(self):
        return {
            "id" : self.id,
            "name": self.name,
            "edges": self.edges
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
        # self.edges[node.id] = edge
        self.edges.append(edge.id)

    def is_equal(self, other):
        if self.name != other.name:
            return False

        if self.edges != other.edges:
            return False
        return True


class Edge(SerializeableBase):
    def __init__(self, nodes=None, json=None):
        """

        :param node_1:
        :type node_1: Node
        :param node_2:
        :type node_2: Node
        """
        if nodes and json:
            raise RuntimeError("cannot construct from nodes and json!")

        if nodes:
            node_1 = nodes[0]
            node_2 = nodes[1]
            super(Edge, self).__init__()

            # self.nodes = {node_1.name: node_1, node_2.name: node_2}
            self.nodes = (node_1.id, node_2.id)

            node_1.add_edge(self, node_2)
            node_2.add_edge(self, node_1)

            self.raw_edges = [] # type: list[tuple[int, int]]
            self.refined_value = None

        elif json:
            self.id = json["id"]
            self.nodes = tuple(json["nodes"])
            self.raw_edges = json["raw_edges"]

        else:
            raise RuntimeError("cannot construct from nothing")

    @classmethod
    def from_nodes(cls, node1, node2):
        return Edge(nodes=[node1, node2])

    @classmethod
    def from_json(cls, json):
        return Edge(json=json)

    def to_json(self):
        return {
            "id": self.id,
            "nodes" : self.nodes,
            "raw_edges" : [(r[0], r[1]) for r in self.raw_edges],
            "refined_value" : self.refined_value
        }

    # def __repr__(self):
    #     return "<E:{n} {id}>".format(n=self.na)

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
        self.nodes_by_name = {}
        self.nodes_by_id = {}
        self.edges_by_id = {}

    def get_node_by_name(self, name):
        if name not in self.nodes_by_name:
            n = Node(name)
            self.nodes_by_name[name] = n
            self.nodes_by_id[n.id] = n
        return self.nodes_by_name[name]

    def get_edge(self, node1, node2):
        ids = [node1.name, node2.name]
        ids.sort()
        id = "_###_".join(ids)
        if id not in self.edges_by_id:
            self.edges_by_id[id] = Edge.from_nodes(node1, node2)
        return self.edges_by_id[id]

    def save(self, mongo_db):
        col_nodes = mongo_db["nodes"]
        col_edges = mongo_db["edges"]

        for n in self.nodes_by_id.values():
            col_nodes.insert_one(GraphJsonEncoder().default(n))

        for e in self.edges_by_id.values():
            col_edges.insert_one(GraphJsonEncoder().default(e))

    def load(self, mongo_db):
        # build all edges
        for edge in mongo_db["edges"].find({}):
            e = Edge.from_json(edge)
            self.edges_by_id[e.id] = e

        # build nodes
        for node in mongo_db["nodes"].find({}):
            n = Node.from_json(node)
            self.nodes_by_id[n.id] = n
            self.nodes_by_name[n.name] = n

    def refine(self, refine_func):
        for e in self.edges_by_id.values():
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