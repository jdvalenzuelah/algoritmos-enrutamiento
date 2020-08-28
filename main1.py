from Node import Node

if __name__ == "__main__":
    with Node(9003, '1') as node:
        node.start()
        while True:
            pass