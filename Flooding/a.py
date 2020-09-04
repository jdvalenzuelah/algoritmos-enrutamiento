import socketio


sio = socketio.Client()

@sio.event
def connect():
    print('connection established')

@sio.event
def my_message(data):
    sio.emit('my_message', {
        "nodoFuente": nodo,
        'nodoDestino': nodoDestino,
        "saltos": saltos,
        "distancia": distancia,
        "nodosUsados":nodosUsados.append(nodo),
        "mensaje": mensaje
        })


@sio.event
def datos(data):
    print('nodoFuente ', data["nodoFuente"])
    print ("nodoDestino", data["nodoDestino"])
    print ("saltos", data["saltos"])
    print ("distancia", data["distancia"])
    print ("nodosUsados", data["nodosUsados"])
    print ("mensaje", data["mensaje"])


@sio.event
def sendinfo():
    sio.emit("infonodo",{
        "nombre": nodo
    })


@sio.event
def disconnect():
    print('disconnected from server')


sio.connect('http://localhost:5000')


#sio.wait()
if __name__ == "__main__":

    nodo = "a"
    sendinfo()
    
    nodoDestino = input ("Ingrese el Nodo de Destino\n")
    saltos=0
    distancia=0
    mensaje = input ("ingrese el mensaje\n")
    nodosUsados=[]
    
    my_message("funcion")

