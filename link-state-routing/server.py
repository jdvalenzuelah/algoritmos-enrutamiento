import eventlet
import socketio

server = socketio.Server()

app = socketio.WSGIApp(server)

nodes = {}

@server.event
def connect(sid, data):
    print(sid)

@server.event
def new_node(sid, data):
    global nodes
    nodes[data['id']] = sid

@server.event
def connect_to(sid, data):
    global nodes
    print(f'------- {nodes} --------')
    for id in nodes.keys():
        if id == data['to']:
            server.emit('new_graph_connection', data, room=nodes[id])

@server.event
def send_to(sid, data):
    global nodes
    for id in nodes.keys():
        if id == data['to']:
            server.emit(data['event'], data['data'], room=nodes[id])

if __name__ == "__main__":
    eventlet.wsgi.server(eventlet.listen(('', 500)), app)
