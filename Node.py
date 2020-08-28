import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import socket
import logging
from threading import Thread, Lock
from threaded import threaded

from typing import Iterable

logging.basicConfig(level=logging.DEBUG)

ENCONDING = 'utf-8'

class Node:

    def __init__(self, port: int, id: str):
        host = socket.gethostname()
        self.server_info = (host, int(port))

        self.id = id

        self.nodes = {}
        self.nodes_mutex = Lock()

        self.socket = None

    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        self.close()

    @threaded
    def start(self):
        logging.debug(f'starting server on port {self.server_info}')
        self._set_up_socket()
        while True:
            logging.info('Listening for connections...')
            conn, addr = self.socket.accept()
            logging.info(f'Incomming connection from {addr}')
            req = conn.recv(1024)
            req = self.parse_request(req)
            logging.info(f"Incomming req {req}")
            self.determine_action(req, conn)
    
    def determine_action(self, req, conn):
        type = req[0]
        if type == '1':
            node_id = req[1]
            node_w = req[2]
            self.save_incoming_node(node_id, node_w, conn)
    
    def connect_to_node(self, id: str, node_w: int, ip: str, port: int):
        if id == self.id:
            return
        
        node = socket.socket()
        node.connect((ip, port))
        node.sendall(self.protocol_serialize(1, [id, str(node_w)]))
        self._save_node(id, node_w, node)
    
    def save_incoming_node(self, node_id, node_w, conn):
        logging.info(f"Saving new node {node_id}")
        self._save_node(id, node_w, conn)
    
    def _set_up_socket(self):
        self.socket = socket.socket()
        self.socket.bind( self.server_info )
        self.socket.listen()                     
    
    def parse_request(self, req: bytes) -> str:
        return req.decode(ENCONDING).split(',')

    def protocol_serialize(self, type: int, data: Iterable[str]):
        data = ','.join(data)
        return f'{type},{data}'.encode(ENCONDING)
    
    def _save_node(self, id, w, node):
        self.nodes_mutex.acquire()
        self.nodes[id] = (node, w)
        self.nodes_mutex.release()
    
    def send_message_f(self, dest_id: str, message: str):
        """
        flooding
        """
        pass

    def send_message_dvr(self, dest_id: str, message: str):
        """
        Distance vector routing
        """
        pass

    def send_message_lsr(self, dest_id: str, message: str):
        """
        Link state routing
        """
        pass

    def close(self):
        logging.debug('closing connection')
        self.socket.close()