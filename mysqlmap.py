# -*- coding: utf-8 -*-

import os
import ConfigParser
import atexit

# config is in ./mysql.ini

_this_dir = os.path.dirname(__file__)
_configfile = os.path.join(_this_dir, "mysql.ini")

_config = ConfigParser.RawConfigParser()
_config.read(_configfile)
_sql = _config.get("mysql", "query")

import MySQLdb as mdb
import os
import socket


class _MyConnection(object):
    _conn = None

    @classmethod
    def get_connection(cls):
        if cls._conn is None:
            host = _config.get("mysql", "host")
            user = _config.get("mysql", "user")
            pw = _config.get("mysql", "password")
            db = _config.get("mysql", "database")
            conn = mdb.connect(host, user, pw, db)
            cls._conn = conn
            atexit.register(conn.close)
        return cls._conn


class NotFoundError(Exception):
    pass

def mysql_map(addr):
    cur = _MyConnection.get_connection().cursor()
    cur.execute(_sql, {"address": addr})
    res = cur.fetchone()
    if res is None:
        raise NotFoundError("no matching entry")
    return res[0]


if __name__ == "__main__":
    import sys
    for s in sys.argv[1:]:
        print("=====")
        print(s)
        try:
            res = mysql_map(s)
        except NotFoundError as err:
            print(str(err))
        else:
            print(type(res))
            print(res)

