import requests
import urllib.parse
import time
import json

import lastfmapikey

api_key    = lastfmapikey.lastfm[ "api_key" ]
base_url   = "http://ws.audioscrobbler.com/2.0/"

last_api_call       = None
last_api_call_count = 0


def _api_call_limiter():
    global last_api_call
    global last_api_call_count

    if last_api_call == None:
        last_api_call = time.time()
        last_api_call_count = 1
        return

    now = time.time()

    if now > last_api_call:
        last_api_call_count = 1
        last_api_call = now
        return
    else:
        last_api_call_count += 1
        if last_api_call_count >= 5:
            time.sleep(1)
            last_api_call_count = 1
            last_api_call = time.time()
            return
        else:
            return


def _api_call(method, format="json"):
    _api_call_limiter()
    url = base_url
    url += "?method=" + method
    url += "&api_key=" + api_key
    url += "&format=" + format

    # print ("calling: " + url)

    response = requests.get(url)
    # print( response.status_code )
    # print(type(response.status_code))
    json_data = json.loads(response.text)

    return json_data


def api_get_user_info( username ):
    # http://ws.audioscrobbler.com/2.0/?method=user.getinfo&user=rj&api_key=YOUR_API_KEY&format=json
    userinfo = _api_call("user.getinfo&user=" + username)
    return userinfo


def api_get_recent_tracks(username, chunk_size, page):
    # http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=rj&api_key=YOUR_API_KEY&format=json
    recent_tracks_chunk = _api_call("user.getrecenttracks&user={u}&limit={l}&page={p}"
                                    .format(u=username, l=chunk_size, p=page))
    return recent_tracks_chunk


def api_get_top_tags_by_mbid(mbid):
    top_tags = _api_call("track.gettoptags&mbid=" + mbid)
    return top_tags


def api_get_top_tags_by_trackname(artist, track):
    top_tags = _api_call("track.gettoptags&artist=" + urllib.quote_plus(artist) + "&track=" + urllib.quote_plus(track))
    return top_tags


def api_get_top_tags(track):
    top_tags = None

    top_tags = api_get_top_tags_by_trackname(track["artist"]["#text"], track["name"])
    # tags by mbid seems broken
    '''
    if len( track["mbid"] ) > 0 :
        top_tags = api_get_top_tags_by_mbid( track["mbid"] )shelve
    else:
        top_tags = api_get_top_tags_by_trackname( track["artist"]["#text"], track["name"] )
    #'''
    return top_tags


def api_get_top_tags_for_artist(track):
    # /2.0/?method=artist.gettoptags&artist=cher&api_key=YOUR_API_KEY&format=json
    top_tags = _api_call('artist.gettoptags&artist=' + urllib.parse.quote_plus(track["artist"]["#text"]))
    return top_tags
