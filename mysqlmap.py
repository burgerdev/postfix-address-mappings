# -*- coding: utf-8 -*-

import os
import ConfigParser
import atexit

# config is in ./mysql.ini

_this_dir = os.path.dirname(__file__)
_configfile = os.path.join(_this_dir, "mysql.ini")

_config = ConfigParser.ConfigParser()
_config.read(_configfile)
_sql = _config.get("mysql", "query")

import MySQLdb as mdb
import sys
import os
import socket


class _MyConnection(object):
    _conn = None

    @classmethod
    def get_connection(cls):
        if cls.conn is None:
            host = _config.get("mysql", "host")
            user = _config.get("mysql", "user")
            pw = _config.get("mysql", "password")
            db = _config.get("mysql", "database")
            conn = mdb.connect(host, user, pw, db)
            cls._conn = conn
            atexit.register(conn.close)
        return cls._conn


def mysql_map(addr):
    with _MyConnection.get_connection().cursor() as cur:
        cur.execute(_sql, addr)
        res = cur.fetchone()
        return res
