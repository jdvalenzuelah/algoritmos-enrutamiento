import eventlet
import socketio

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})
datanodos = []
idnodos = []
destino = ""

@sio.event
def connect(sid, nodo):
    print('connect ', sid)

@sio.event
def my_message(sid,data):
    for i in range(len(datanodos)):
        if data["connect"]== datanodos[i]:
            destino = idnodos[i]
            sio.emit('datos', {
                "nodoFuente": data["nodoFuente"],
                'nodoDestino': data["nodoDestino"],
                "saltos": data["saltos"],
                "distancia": data["distancia"],
                "nodosUsados":data["nodosUsados"],
                "mensaje": data["mensaje"]
                },room=destino)

@sio.event
def infonodo(sid,data):
    print ("------------------------------")
    datanodos.append(data["nombre"])
    idnodos.append(sid)
    print(datanodos)
    print(idnodos)



@sio.event
def disconnect(sid):
    print('disconnect ', sid)


@sio.event
def data(sid, data):
    print ("data")


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)