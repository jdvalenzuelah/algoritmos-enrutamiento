from Node import Node

if __name__ == "__main__":
    with Node(3333, 'C') as node:
        node.connect_to_node('127.0.0.1', 3132, 'B', 5)
        node.start()