# coding: utf-8

import unittest

import graph

class Test001Graph(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_00100_node(self):
        node1 = graph.node("new rave")
        self.assertEqual(node1.name, "new rave")
        self.assertDictEqual(node1.edges, {})
        node2 = graph.node("old rave")

        edge1 = graph.edge(node1, node2)

        self.assertEqual(edge1.nodes, {"new rave": node1, "old rave": node2})
        self.assertDictEqual(node1.edges, {node2.name: edge1})

        a_raw_edge = ( (30,60) )
        edge1.add_raw_edge( a_raw_edge )

        self.assertEqual(edge1.raw_edges, [(30, 60)])

        another_raw_edge = ( (99,1) )
        edge1.add_raw_edge(another_raw_edge)
        self.assertEqual(edge1.raw_edges, [(30, 60), (99,1)])
