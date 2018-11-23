# coding: utf-8

import itertools
import pymongo

import graph
import misc as M


mc = None
db = None

threshold_value = 50

def connect():
    global mc
    global db
    mc = pymongo.MongoClient()
    db = mc["lastfm"]


def build_graph():

    g = graph.Graph()

    tags_artists = db["top_tags_artists"]
    count = tags_artists.find({}).count()
    i = 1
    for tags in tags_artists.find({}):
        print("{i}/{c}".format(i=i, c=count))
        i += 1

        if len(tags["toptags"]["tag"]) < 2:
            continue


        for subset in itertools.combinations(tags["toptags"]["tag"], 2):
            name1 = subset[0]["name"]
            value1 = subset[0]["count"]
            name2 = subset[1]["name"]
            value2 = subset[1]["count"]

            if value1 < threshold_value or value2 < threshold_value:
                continue

            # TODO: optional first filter for low weights
            node1 = g.get_node_by_name(name1)
            node2 = g.get_node_by_name(name2)
            edge = g.get_edge(node1, node2)

            # after adding, we dont know which value of tuple belongs to which node
            edge.add_raw_edge((value1, value2))


    return g

def refine_graph(g):
    return g


if __name__ == "__main__":
    connect()
    g = build_graph()
    g.refine(graph.mul_arithmetic_mean)
    g.save()
