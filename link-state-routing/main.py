from Node import Node
from Graph import Graph

if __name__ == "__main__":
    a = Node('A')
    b = Node('B')
    c = Node('C')
    d = Node('D')
    e = Node('E')
    f = Node('F')
    g = Node('G')
    h = Node('H')
    i = Node('I')

    graph = Graph.create_from_nodes([a, b, c, d, e, f, g, h, i])

    graph.connect(a, b, 7)
    graph.connect(a, i, 1)
    graph.connect(a, c, 7)
    graph.connect(b, f, 2)
    graph.connect(i, d, 6)
    graph.connect(c, d, 5)
    graph.connect(f, d, 1)
    graph.connect(f, h, 4)
    graph.connect(f, g, 2)
    graph.connect(d, e, 1)
    graph.connect(e, g, 4)

    print([(weight, [n.data for n in node]) for (weight, node) in graph.dijkstra(a, b)])