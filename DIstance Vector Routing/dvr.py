import json

nodes = dict()
def start_node(node):
	node.start()

#Algoritmo DVR Utilizando Bellman Ford
def DVR (graph, id_node):
	distance = dict()
	predecessor = dict()

	for node in graph:
		distance[node], predecessor[node] = float('inf'), None

	# La distancia entre si mismo nodo
	distance[id_node] = 0

	for _ in range(len(graph)-1):
		for u in graph:
			for v in graph[u]:
				if distance[v] >= distance[u] + graph[u][v]:
					distance[v], predecessor[v] = distance[u] + graph[u][v],u

	for u in graph:
		for v in graph[u]:
			'''
			if distance[v] <= distance[u] + graph[u][v]:
				print('Negative weights')
			'''
			assert distance[v] <= distance[u] + graph[u][v], "Negative"

	return distance, predecessor
