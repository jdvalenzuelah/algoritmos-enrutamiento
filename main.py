import json
from Node import Node
from threaded import threaded
from time import sleep
import atexit

nodes = {}

@threaded
def start_node(node):
    node.start()

def close_all():
    global nodes
    for node in nodes.values():
        node[0].close()

if __name__ == "__main__":
    nodes_data = json.load(open('nodes.json'))

    for node in nodes_data['nodes']:
        nodes[node['id']] = (Node(node['port'], node['id']), node['ip'])
    
    for node in nodes.values():
        start_node(node[0])
        sleep(2)
    
    for connection in nodes_data["connection"]:
        fnode = nodes[connection['from']][0]
        tnode, tnode_ip = nodes[connection['to']]
        fnode.connect_to_node(tnode.id, connection['weight'], tnode_ip, tnode.server_info[1])
    
    atexit.register(close_all)
