# coding: utf-8

import math

import pymongo
import pprint
pp = pprint.PrettyPrinter( indent=2, depth=6 )
dp = pp.pprint

import lastfmapi as lapi
from misc import print_exception, get_pretty_date, get_full_trackname

chunk_size = 200
username = "cygenb0ck"


mc = None
db = None

def connect():
    global mc
    global db
    mc = pymongo.MongoClient("mongodb://localhost:27017")
    print(mc)
    db = mc["lastfm"]
    print(db)


def get_recent_tracks(userinfo):
    recent_tracks = db["recent-tracks"]

    request_count = int(math.ceil(float(userinfo["user"]["playcount"]) / chunk_size))
    # request_count = 5
    print("making " + str(request_count) + "calls ...")

    for i in range(request_count):
        recent_tracks_chunk = lapi.api_get_recent_tracks(username, chunk_size, i + 1)
        for track in recent_tracks_chunk["recenttracks"]["track"]:
            try:
                query = {
                    "date": track["date"]
                }
                count = recent_tracks.find(query).count()
                dp(count)
                if recent_tracks.find(query).count() > 0:
                    dp(get_pretty_date(track["date"]["uts"]) + " - " + get_full_trackname(track) + " already in db ...")
                    continue
                print('inserting ' + get_full_trackname(track) + ' ' + get_pretty_date(track['date']['uts']))

                rid = recent_tracks.insert_one(track).inserted_id
                count = recent_tracks.find(query).count()
                dp(count)

            except KeyError as e:
                print('handling KeyError: ', e)
                print_exception()
            except Exception as e:
                print("caught exception", e)
                print_exception()
            else:
                pass
            finally:
                pass
        print(str(i + 1) + "/" + str(request_count))

def query_db():
    recent_tracks = db["recent-tracks"]
    r = recent_tracks.find_one()
    dp(r)
    search = {
        "artist.#text": "A Flock of Seagulls"
    }
    # search = {
    #     "mbid": ""
    # }
    result = recent_tracks.find(search).sort( [ ("date.uts", 1) ] )
    for hit in result:
        dp(get_pretty_date(hit["date"]["uts"]) + " - " + get_full_trackname(hit))

def test():
    userinfo = lapi.api_get_user_info(username)
    pp.pprint(userinfo)
    get_recent_tracks(userinfo)


if __name__ == "__main__":
    connect()
    test()
    # query_db()


