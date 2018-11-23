# coding: utf-8

import unittest

import json
import pymongo
import graph


class Test001Graph(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_00100_node(self):
        g = graph.Graph()
        node1 = g.get_node_by_name("new rave")
        self.assertIsInstance(node1._id, int)
        self.assertEqual(node1.name, "new rave")
        self.assertListEqual(node1.edges, [])

        node2 = g.get_node_by_name("old rave")
        self.assertNotEqual(node1.id, node2.id)

        edge1 = g.get_edge(node1, node2)
        self.assertNotEqual(node1.id, edge1.id)
        self.assertNotEqual(node2.id, edge1.id)

        # self.assertEqual(edge1.nodes, {"new rave": node1, "old rave": node2})
        self.assertEqual(edge1.nodes, (node1.id, node2.id))
        self.assertListEqual(node1.edges, [edge1.id])

        a_raw_edge = ( (30,60) )
        edge1.add_raw_edge( a_raw_edge )

        self.assertEqual(edge1.raw_edges, [(30, 60)])

        another_raw_edge = ( (99,1) )
        edge1.add_raw_edge(another_raw_edge)
        self.assertEqual(edge1.raw_edges, [(30, 60), (99,1)])

    def test_00200_providers(self):
        g = graph.Graph()
        node1 = g.get_node_by_name("new rave")
        node2 = g.get_node_by_name("new rave")
        self.assertIs(node1, node2)

        node3 = g.get_node_by_name("old rave")

        edge1 = g.get_edge(node1, node3)
        edge2 = g.get_edge(node1, node3)
        self.assertIs(edge1, edge2)


class Test002Jsonification(unittest.TestCase):
    def setUp(self):
        self.mc = pymongo.MongoClient()
        self.db = self.mc["graph_test"]
        self.collection_nodes = self.db["nodes"]
        self.collection_edges = self.db["edges"]

    def tearDown(self):
        self.mc.drop_database("graph_test")

    # @unittest.skip("xxxx {x}")
    def test_00300_json_encoder(self):
        g = graph.Graph()

        node1 = g.get_node_by_name("new rave")
        node2 = g.get_node_by_name("old rave")

        edge1 = g.get_edge(node1, node2)
        edge1.add_raw_edge((23,42))

        g.save(self.db)

        g.load(self.db)
        recreated_node = g.nodes_by_name["new rave"]
        self.assertTrue(node1.is_equal(recreated_node))

