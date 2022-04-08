import socket as skt

#Conexión con el socket 50001 del mid-server
serverAddr = "localhost"
serverPort = 50001
clientSocket = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
clientSocket.connect((serverAddr, serverPort))

print("Conexión establecida con mid server en el puerto:",serverPort)

response = None
options = ["Piedra", "Papel", "Tijera"]
bigFlag = True #flag para terminar el programa

print("------------------------------------")
print("Su cachipun piola")
print("------------------------------------")

while bigFlag:
    print("-Ingrese 1 para jugar")
    print("-Ingrese 2 para salir")
    print("------------------------------------")
    player = input("Ingrese opción: ")

    clientSocket.send(player.encode()) #Se envía un 1 para jugar o un 2 para apagar los servers

    if player == "1":
        #Se recibe respuesta del mid-server correspondiente al deseo de jugar de cachipun-server
        response = clientSocket.recv(2048).decode()

        if response == "Ok": #Cachipun-server desea jugar
            flag = True #flag para el ciclo del juego
            while flag:
                print("Ingrese 1 para Piedra")
                print("Ingrese 2 para Papel")
                print("Ingrese 3 para Tijera")
                print("------------------------------------")
                player = input("Ingrese jugada: ")
                clientSocket.send(player.encode()) #Envía jugada al mid-server
                response = clientSocket.recv(2048).decode() #Recibe el resultado de la jugada
                #Verifica si en el marcador algún jugador llega a los 3 puntos
                if "3" in response:
                    flag = False
                print("-> Jugaste " + options[int(player) - 1])
                print(response)
                print("------------------------------------")
            response = clientSocket.recv(2048).decode() #Recibe quien gana la partida
            if response == "player":
                print("Ganas la partida")
                print("------------------------------------")
            else:
                print("El bot gana la partida")
                print("------------------------------------")
        else: #cachipun-server no puede jugar
            print("No hay disponibilidad de juego")
            bigFlag = False #Se termina la ejecución
    else:
        bigFlag = False #Se termina la ejecución

clientSocket.close() #cierre de la conexión con el socket del mid-server