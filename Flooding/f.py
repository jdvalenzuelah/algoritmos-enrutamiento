import socketio


sio = socketio.Client()

@sio.event
def connect():
    print('connection established')

@sio.event
def my_message(data):
    for i in range(len(connect)):
        sio.emit('my_message', {
            "connect": connect[i],
            "nodoFuente": nodo,
            'nodoDestino': nodoDestino,
            "saltos": saltos+1,
            "distancia": distancia,
            "nodosUsados":nodosUsados,
            "mensaje": mensaje
            })
    menu()

    
    
@sio.event
def datos(data):
    
    nodosUsados=data["nodosUsados"]
    nodosUsados.append(nodo)


    #print (nodosUsados)
    if (data["nodoDestino"] == nodo):
        print("------------------info----------------")
        print('nodoFuente ', data["nodoFuente"])
        print ("nodoDestino", data["nodoDestino"])
        print ("saltos", data["saltos"])
        print ("nodosUsados", data["nodosUsados"])
        print("----------------mensaje---------------")
        print ("mensaje", data["mensaje"])
        print("--------------------------------------")
    
    menu()
    

    if (data["nodoDestino"] != nodo and hopCount >= data["saltos"]+1):
        for i in range(len(connect)):
            sio.emit('my_message', {
                "connect": connect[i],
                "nodoFuente": data["nodoFuente"],
                'nodoDestino': data["nodoDestino"],
                "saltos": data["saltos"]+1,
                "distancia": data["distancia"],
                "nodosUsados": data["nodosUsados"],
                "mensaje": data["mensaje"]
                })
        menu()


@sio.event
def sendinfo():
    sio.emit("infonodo",{
        "nombre": nodo
    })


@sio.event
def disconnect():
    print('disconnected from server')


sio.connect('http://localhost:5000')


def menu():
    global nodoDestino
    global saltos
    global distancia
    global mensaje
    global nodosUsados

    nodoDestino = input ("Ingrese el Nodo de Destino\n")
    saltos=0
    distancia=0

    mensaje = input ("ingrese el mensaje\n")
    nodosUsados=[nodo]
    my_message("funcion")



#sio.wait()
if __name__ == "__main__":

    nodo = "f"
    connect = ["b","h","g","d"]
    distanciaNodos= [2,4,3,3]

    hopCount=9
    sendinfo()
    
    menu()




