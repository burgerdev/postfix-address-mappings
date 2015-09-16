#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import sys
import os
import logging
import atexit
import re

from threading import Thread


from hashaddressmap import hash_address_map
from mysqlmap import mysql_map

logger = logging.getLogger("mappingserver")
logging.basicConfig(level=logging.INFO)


class Acceptor(Thread):
    daemon = True
    __re = re.compile("get (.*)\n")

    def run(self):
        assert hasattr(self, "connection")
        try:
            conn = self.connection
            req = conn.recv(4096)
            m = self.__re.match(req)
            if m is not None:
                addr = m.groups()[0]
                answer = self.__map(addr)
            else:
                answer = "400 malformed request"
            conn.sendall(answer)
        finally:
            logger.info("connection terminated")
            self.connection.close()

    def __map(self, s):
        for foo in self.maps:
            try:
                s = foo(s)
            except Exception as err:
                logger.warn("Lookup error: {}".format(str(err)))
                return "500 lookup error\n"
        return "200 {}\n".format(s)


def create_socket(port=30303):
    server_address = "localhost"
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    logger.info('starting up on {}:{}'.format(server_address, port))
    sock.bind((server_address, port))
    atexit.register(sock.close)
    return sock


def serve_forever(sock, maps):
    # Listen for incoming connections
    sock.listen(1)

    while True:
        # Wait for a connection
        connection, client_address = sock.accept()
        acc = Acceptor()
        acc.connection = connection
        acc.maps = maps
        logger.info("new connection from '{}', starting thread..."
                    "".format(client_address))
        acc.start()


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("port", help="port to use", type=int)

    args = parser.parse_args()

    maps = [hash_address_map, mysql_map]
    sock = create_socket(port=args.port)
    serve_forever(sock, maps)

