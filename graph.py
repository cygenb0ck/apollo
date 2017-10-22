# coding: utf-8

class node(object):
    def __init__(self, name):
        self.name = name
        self.edges = {}

    def add_edge(self, edge, node ):
        self.edges[node.name] = edge



class edge(object):
    def __init__(self, node_1, node_2):
        self.nodes = {node_1.name: node_1, node_2.name: node_2}
        node_1.add_edge(self, node_2)
        node_2.add_edge(self, node_1)
        self.raw_edges = []

    def add_raw_edge(self, raw_edge):
        self.raw_edges.append(raw_edge)

