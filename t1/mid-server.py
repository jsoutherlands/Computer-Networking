import socket as skt


#Socket de comunicación con cachipun-server
serverUDPAddr = "localhost"
serverUDPPort = 50002
serverUDPSocket = skt.socket(skt.AF_INET, skt.SOCK_DGRAM)

print("Conexión establecida con cachipun server en el puerto:",serverUDPPort)
#Socket de comunicación con el cliente
serverTCPPort = 50001
serverTCPSocket = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
serverTCPSocket.bind(("",serverTCPPort))
serverTCPSocket.listen(1)

print("Servidor TCP escuchando en:",serverTCPPort)


print("")

clientTCPSocket, clientTCPAddr = serverTCPSocket.accept()

player = clientTCPSocket.recv(2048).decode() #Recibe si el jugador quiere jugar o cerrar el programa

print("Client:",player)

flag = True

while flag:
    serverUDPSocket.sendto(player.encode(), (serverUDPAddr,serverUDPPort)) #Envía el deseo de jugar del cliente a cachipun-server
    if player == "1":
        #recibe respuesta de cachipun server, si acepta envia un Ok y el puerto del juego, si no envia No y un 0
        gameStatus, addr = serverUDPSocket.recvfrom(2048) 
        gameStatus = gameStatus.decode().split(";")
        new_port = int(gameStatus[1])
        gameStatus = gameStatus[0]
        print(gameStatus)
        print(new_port)
        if gameStatus == "Ok": #Si cachipun server desea jugar
            clientTCPSocket.send(gameStatus.encode()) #Envia mensaje al cliente para que juegue
            player = None
            options = ["Piedra", "Papel", "Tijera"]
            playerPoints = 0
            botPoints = 0
            
            #cilco del juego que corre hasta que un jugador llega a los 3 puntos
            while playerPoints < 3 and botPoints < 3:
                player = int(clientTCPSocket.recv(2048).decode()) #Jugada del cliente

                #Envía mensaje a cachipun-server
                serverUDPSocket.sendto("A jugar".encode(), (serverUDPAddr,new_port))
                cpu, addr = serverUDPSocket.recvfrom(2048) #Recibe jugada de cachipun-server
                cpu = int(cpu.decode())

                print("-El bot jugó " + options[cpu-1])
#---------------------------------------------------------------------------------------HASTA ACA--------#
                #Condicional para ganar
                if (player == 1 and cpu == 3) or (player == 2 and cpu == 1) or (player == 3 and cpu == 2):
                    playerPoints += 1
                    msg = "-> El bot jugó " + options[cpu-1] + "\n-> Ganas la ronda!" + "\n-> Marcador: " + str(playerPoints) + " - " + str(botPoints)
                    clientTCPSocket.send(msg.encode())
                #Condicional para perder
                elif (cpu == 1 and player == 3) or (cpu == 2 and player == 1) or (cpu == 3 and player == 2):
                    botPoints +=1
                    msg = "-> El bot jugó " + options[cpu-1] + "\n-> Pierdes la ronda :c" + "\n-> Marcador: " + str(playerPoints) + " - " + str(botPoints)
                    clientTCPSocket.send(msg.encode())
                #Empate
                else:
                    msg = "-> El bot jugó " + options[cpu-1] + "\n-> Empate!" + "\n-> Marcador: " + str(playerPoints) + " - " + str(botPoints)
                    clientTCPSocket.send(msg.encode())
            #Condicionales para enviar el ganador al cliente
            if playerPoints == 3:
                clientTCPSocket.send("player".encode())
            elif botPoints == 3:
                clientTCPSocket.send("bot".encode())
            serverUDPSocket.sendto("STOP".encode(), (serverUDPAddr,new_port)) #Envía un stop a cachipun-server para detener el ciclo del juego
        else:
            clientTCPSocket.send(gameStatus.encode()) #Envia el No de server-cachipun
            print("No hay disponibilidad de juego, el servidor se cerrará")
            flag = False
    else:
        flag = False
        #Envía el 2 para cerrar el servidor cachipun-server
        serverUDPSocket.sendto(str(player).encode(), (serverUDPAddr,new_port))
        print("El servidor se cerrará")
    player = clientTCPSocket.recv(2048).decode()

clientTCPSocket.close() #Cierra el socket con el client server
