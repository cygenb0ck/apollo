import datetime
import linecache
import sys

import pprint
pp = pprint.PrettyPrinter( indent=2, depth=6 )
dp = pp.pprint


def print_exception():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print("EXCEPTION IN ({0}, LINE {1} \"{2}\"): {3}".format(filename, lineno, line.strip(), exc_obj) )


def get_pretty_date( uts_str ):
    return datetime.datetime.fromtimestamp( int( uts_str ) ).strftime('%Y-%m-%d %H:%M:%S')


def get_date_key_from_uts( uts_time ):
    return datetime.datetime.fromtimestamp( int( uts_time ) ).strftime('%Y-%m-%d')


def get_full_trackname( track ):
    return track['artist']['#text'] + ' - ' + track['name']