# coding: utf-8

import itertools
import pymongo

import graph
import misc as M


mc = None
db = None


def connect():
    global mc
    global db
    mc = pymongo.MongoClient()
    db = mc["lastfm"]


def build_graph():
    tags_artists = db["top_tags_artists"]
    count = tags_artists.find({}).count()
    i = 1
    for tags in tags_artists.find({}):
        print("{i}/{c}".format(i=i, c=count))
        i += 1

        if tags["toptags"]["tag"] == []:
            continue

        for subset in itertools.combinations(tags["toptags"]["tag"], 2):
            name1 = subset[0]["name"]
            value1 = subset[0]["count"]
            name2 = subset[1]["name"]
            value2 = subset[1]["count"]

            # TODO: optional first filter for low weights
            node1 = graph.node_factory.get_node(name1)
            node2 = graph.node_factory.get_node(name2)

            edge = graph.edge_factory.get_edge(node1, node2)
            edge.add_raw_edge((value1, value2))


if __name__ == "__main__":
    connect()
    build_graph()
