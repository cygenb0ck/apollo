# coding: utf-8
import pprint
pp = pprint.PrettyPrinter( indent=2, depth=6 )
dp = pp.pprint


import pymongo

import lastfmapi as lapi

import misc

mc = None
db = None

def connect():
    global mc
    global db
    mc = pymongo.MongoClient()
    db = mc["lastfm"]


def get_top_tags_for_tracks():
    recent_tracks = db["recent-tracks"]
    tags_artists = db["top_tags_artists"]
    tracks = recent_tracks.find()
    count = tracks.count()
    i = 1
    for track in tracks:
        print("{i}/{c}".format(i=i, c=count))
        i += 1
        query = {
            "toptags.@attr.artist": track["artist"]["#text"]
        }
        if tags_artists.find(query).count() > 0:
            print("s")
            continue
        tags = lapi.api_get_top_tags_for_artist(track)
        tags_artists.insert_one(tags)


if __name__ == "__main__":
    connect()
    get_top_tags_for_tracks()
