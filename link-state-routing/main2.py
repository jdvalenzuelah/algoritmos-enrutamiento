from Node import Node

if __name__ == "__main__":
    with Node(3132, 'B') as node:
        node.connect_to_node('127.0.0.1', 3133, 'A', 10)
        node.start()