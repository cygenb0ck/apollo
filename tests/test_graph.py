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
        node1 = g.get_node("new rave")
        self.assertIsInstance(node1._id, int)
        self.assertEqual(node1.name, "new rave")
        self.assertDictEqual(node1.edges, {})
        node2 = g.get_node("old rave")

        self.assertNotEqual(node1.id, node2.id)

        edge1 = g.get_edge(node1, node2)
        self.assertNotEqual(node1.id, edge1.id)
        self.assertNotEqual(node2.id, edge1.id)
        self.assertEqual(edge1.nodes, {"new rave": node1, "old rave": node2})
        self.assertDictEqual(node1.edges, {node2.name: edge1})

        a_raw_edge = ( (30,60) )
        edge1.add_raw_edge( a_raw_edge )

        self.assertEqual(edge1.raw_edges, [(30, 60)])

        another_raw_edge = ( (99,1) )
        edge1.add_raw_edge(another_raw_edge)
        self.assertEqual(edge1.raw_edges, [(30, 60), (99,1)])

    def test_00200_providers(self):
        g = graph.Graph()
        node1 = g.get_node("new rave")
        node2 = g.get_node("new rave")
        self.assertIs(node1, node2)

        node3 = g.get_node("old rave")

        edge1 = g.get_edge(node1, node3)
        edge2 = g.get_edge(node1, node3)
        self.assertIs(edge1, edge2)


class Test002Jsonification(unittest.TestCase):
    def setUp(self):
        self.mc = pymongo.MongoClient()
        self.db = self.mc["graph_test"]
        self.collection = self.db["c"]

    def tearDown(self):
        self.mc.drop_database("graph_test")

    def test_00300_json_encoder(self):
        g = graph.Graph()
        node1 = g.get_node("new rave")
        node2 = g.get_node("old rave")

        edge1 = g.get_edge(node1, node2)

        print(graph.GraphJsonEncoder().default(node1))
        print(graph.GraphJsonEncoder().default(node2))
        print(graph.GraphJsonEncoder().default(edge1))
        self.collection.insert_one(graph.GraphJsonEncoder().default(node1))
        json_from_db = self.collection.find_one({"name": "new rave"})
        print(json_from_db)
        print(json_from_db["name"])
        recreated_node = g.node_from_mongo_json(json_from_db)
        self.assertTrue(node1 == recreated_node)

