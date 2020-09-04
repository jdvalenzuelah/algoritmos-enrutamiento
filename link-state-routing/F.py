from Node import Node
from Graph import Graph

import eventlet
import socketio
import sys
import uuid
import redis

class Network:

    def __init__(self):
        self.node = None
        self.nodes = {}
        self.graph = None
        self.paths = None
        self.id = None
        self.connections = []
    
    def __graph_update(self):
        self.graph = Graph.create_from_nodes([self.nodes[x] for x in self.nodes.keys()])
        self.__update_cons()
    
    def __update_cons(self):
        for conn in self.connections:
            self.graph.connect(self.nodes[conn['from']], self.nodes[conn['to']], int(conn['w']))

    def start(self, id):
        self.id = id
        self.node = Node(id)
        self.nodes[id] = self.node
        self.__graph_update()
    
    def add_new_node(self, node):
        self.nodes[node.data] = node
        self.__graph_update()
    
    def connect_to_node(self, f, t, w):
        self.connections.append({'from': f, 'to': t, 'w': w})
        self.__graph_update()
        self.paths = {}
        for (weight, node) in self.graph.dijkstra(self.node):
            to = node[-1].data
            jumps = []
            for n in node:
                if n.data != self.node.data:
                    jumps.append(n.data)
            self.paths[to] = {'jumps': jumps, 'w': weight}
    
    def get_n_ids(self):
        n = []
        for conn in self.connections:
            if conn['from'] == self.id and self.id != conn['to'] and conn['from'] != conn['to']:
                n.append(conn['to'])
        return n

socket = socketio.Client()
nw = Network()
r = redis.Redis(host='localhost', port=6379, db=0)

def send_new_node():
    global socket, nw
    socket.emit('new_node', {'id': nw.id, 'pid': str(uuid.uuid1())})

def connect_to_node(id, w):
    global socket, nw
    nw.add_new_node(Node(id))
    nw.connect_to_node(nw.id, id, w)
    socket.emit('connect_to', {'from': nw.id, 'to': id, 'w': w, 'pid': str(uuid.uuid1())})

def check_pid(id, uuid):
    global r
    cached = r.get(f'{id}:{uuid}')
    return cached == None

def cache_pid(id, uuid):
    global r
    r.set(f'{id}:{uuid}' , uuid)

@socket.on('new_graph_connection')
def on_new_connection(data):
    global socket, nw

    if not check_pid(nw.id, data['pid']):
        return
    else:
        cache_pid(nw.id, data['pid'])

    nw.add_new_node(Node(data['from']))
    nw.add_new_node(Node(data['to']))
    nw.connect_to_node(data['from'], data['to'], int(data['w']))
    nids = nw.get_n_ids()
    for n in nids:
        socket.emit('send_to', {'to': n, 'data': data, 'event': 'new_graph_connection'})

def send_message(to, message):
    global nw, socket
    paths = nw.paths[to]
    next = paths['jumps'][0]
    socket.emit('send_msg', {'from': nw.id, 'to': to, 'next': next, 'message': message})

@socket.on('msg')
def on_msg(data):
    global nw, socket
    if data['next'] == nw.id:
        print(f'You received a message: {data}')
    else:
        send_message(data['to'], data['message'])

if __name__ == "__main__":
    ip = "127.0.0.1"
    port = 500
    id = 'F'
    socket.connect(f'http://{ip}:{port}')
    nw.start(id)
    send_new_node()
    connect_to_node('D', 3)
    connect_to_node('B', 8)

    while True:
        to = input("Enviar mensaje a: ")
        message = input("Ingrese mensaje")
        send_message(to, message)