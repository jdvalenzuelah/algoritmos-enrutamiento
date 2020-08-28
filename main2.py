from Node import Node

if __name__ == "__main__":
    with Node(9004, '1') as node:
        node.start()
        node.connect_to_node('2', 3, '127.0.0.1', 9003)
        while True:
            pass