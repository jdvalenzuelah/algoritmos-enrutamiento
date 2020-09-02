import socket
import json
import pickle
from dvr import *

routing = json.load(open('nodes.json'))
names = list(routing.keys())

nodes = dict()
available = names.copy()

'''
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 8080))

while True:
	data = s.recv(1024)
	message = ''
	try:
		message = data.decode('ascii').split('||')
'''

graph = DVR(routing, names[0])
print(graph)
