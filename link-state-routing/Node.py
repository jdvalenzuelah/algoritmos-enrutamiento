import socket
import logging
from threading import Thread, Lock
from threaded import threaded
import queue
import redis

logging.basicConfig(level=logging.DEBUG)

ENCONDING = 'utf-8'

"""
New node:
1,id,w,s
"""

r = redis.Redis(host='localhost', port=6379, db=0)

class Node:

    def __init__(self, port: int, id: str):
        host = socket.gethostname()
        self.server_info = (host, int(port))

        self.conn_queue = queue.Queue()
        self.queue_mutex = Lock()

        self.nodes = {}
        self.nodes_mutex = Lock()

        self.sequence = 0

        self.id = id

    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        self.close()

    def start(self):
        logging.debug(f'starting server on port {self.server_info}')
        self.set_up_socket()
        while True:
            logging.info('Listening for connections...')
            conn, addr = self.socket.accept()
            logging.info(f'Incomming connection from {addr}')
            self.push_new_connection(conn)
            logging.debug('Processing incoming request on new thread')
            self.handle_request()
    
    def set_up_socket(self):
        self.socket = socket.socket()
        self.socket.bind( self.server_info )
        self.socket.listen()                     
    
    def push_new_connection(self, conn):
        self.queue_mutex.acquire()
        self.conn_queue.put(conn)
        self.queue_mutex.release()
    
    def get_conn(self):
        self.queue_mutex.acquire()
        conn = self.conn_queue.get()
        self.queue_mutex.release()
        return conn
    
    def parse_request(self, req: bytes) -> str:
        req = req.decode(ENCONDING).strip()
        return req.split(',')
    
    def format_response(self, res: str) -> bytes:
        return res.encode(ENCONDING)

    @threaded
    def handle_request(self):
        conn = self.get_conn()
        req = conn.recv(1024)
        req = self.parse_request(req)

        logging.debug(f'Incomming request {req}')

        sequence = int(req[-1])
        if req[0] == '1':
            if self.validate_sequence(req[1], sequence):
                self._save_new_node(req[1], req[2], conn)
            else:
                logging.info(f'Invalid sequence {req}')

        """res = self.format_response('Hola mundo 2')
        conn.sendall(res)
        req = conn.recv(1024)
        req = self.parse_request(req)[0]
        logging.info(f'Accepted connection {conn}')
        res = self.format_response('Hola mundo')
        conn.sendall(res)
        self._listen_user(conn, '')"""
            
    def _save_new_node(self, id, weight, conn):
        logging.info(f'Saving new node {id}!')
        n2s = (id, weight, conn)
        self.nodes_mutex.acquire()
        self.nodes[id] = n2s
        self.nodes_mutex.release()
        logging.info('Node has been saved!')
    
    def _listen_user(self, conn, userid):
        while ( req := conn.recv(1024) ):
            logging.debug(f'Incomming request {req}')
            req = self.parse_request(req)
            for r in req:
                try:
                    self._process_all(r, conn, userid)
                except Exception as e:
                    logging.error(e)
    
    def connect_to_node(self, ip: str, port: int, id: str, weight: int):
        saved_node = self._get_node_by_id(id)
        if saved_node:
            if(weight != saved_node[1]):
                return

        sock = socket.socket()
        sock.connect((ip, port))
        req = f'1,{self.id},{weight},{self.get_sequence()}'
        logging.info(req)
        sock.sendall(req.encode(ENCONDING))

        self._save_new_node(id, weight, sock)
    
    def _get_node_by_id(self, id: str):
        self.nodes_mutex.acquire()
        node = self.nodes.get(id)
        self.nodes_mutex.release()
        return node

    def get_sequence(self) -> int:
        self.sequence += 1
        return self.sequence

    def _process_all(self, req, conn, userid):
        res = self.process_request(req, userid, conn)
        if res:
            res = self.format_response(res)
            conn.sendall(res)
    
    def process_request(self, req: str, conn):
        logging.info(f'req: {req}')
        
    def cache_sequence(self, id: str, seq: int):
        r.setex(id, 120, seq)
    
    def get_latest_sequence(self, id: str):
        seq = r.get(id)
        if seq:
            logging.info(f'Cached sequence for {id} -> {seq}')
            return int(seq.decode(ENCONDING))
    
    def validate_sequence(self, id: str, seq: int):
        current = self.get_latest_sequence(id)

        if current == None:
            logging.info(f'Sequence for {id} not found! caching new sequence {seq}')
            self.cache_sequence(id, seq)
            return True
        elif seq > current:
            logging.info(f'Sequence for {id} increase from {current} to {seq}')
            self.cache_sequence(id, seq)
            return True
        else:
            logging.error(f'Invalid sequence for {id}, current: {current} new: {seq}')
            return False
        


    def close(self):
        logging.debug('closing connection')
        self.socket.close()