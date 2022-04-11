import socket as skt

def verificar(tableroGato, contador_de_jugadas): # Verifica leyendo las casillas del tablero si es que existe algún ganador, o bien
	if contador_de_jugadas >= 5 :				 # un empate, contando la cantidad de jugadas realizadas.
		if tableroGato[0][0] == tableroGato[1][0] == tableroGato[2][0] != " ": # Fila vertical izquierda.
			if tableroGato[0][0] == "x":
				return 1
			else:
				return 2

		elif tableroGato[0][1] == tableroGato[1][1] == tableroGato[2][1] != " ": # Fila vertical central.
			if tableroGato[0][1] == "x":
				return 1
			else:
				return 2
			
		elif tableroGato[0][2] == tableroGato[1][2] == tableroGato[2][2] != " ": # Fila vertical derecha.
			if tableroGato[0][2] == "x":
				return 1
			else:
				return 2
			
		elif tableroGato[0][0] == tableroGato[0][1] == tableroGato[0][2] != " ": # Fila horizontal superior.
			if tableroGato[0][0] == "x":
				return 1
			else:
				return 2
			
		elif tableroGato[1][0] == tableroGato[1][1] == tableroGato[1][2] != " ": # Fila horizontal central.
			if tableroGato[1][0] == "x":
				return 1
			else:
				return 2
			
		elif tableroGato[2][0] == tableroGato[2][1] == tableroGato[2][2] != " ": # Fila horizontal inferior.
			if tableroGato[2][0] == "x":
				return 1
			else:
				return 2
			
		elif tableroGato[0][0] == tableroGato[1][1] == tableroGato[2][2] != " ": # Diagonal 1
			if tableroGato[0][0] == "x":
				return 1
			else:
				return 2
			
		elif tableroGato[2][0] == tableroGato[1][1] == tableroGato[0][2] != " ": # Diagonal 2
			if tableroGato[2][0] == "x":
				return 1
			else:
				return 2
	if contador_de_jugadas == 9: # Empate
		return 0

print("Bienvenid@ al servidor intermediario...")
#udp
address = 'localhost'
 
#go
serverPort = 8002
serverSocket = skt.socket(skt.AF_INET, skt.SOCK_DGRAM)
print("Conexión establecida con servidor gato en el puerto:",serverPort)

#tcp
clientPort = 8001
clientSocket = skt.socket(skt.AF_INET, skt.SOCK_STREAM) #skt.AF_INET indica la direccion ipv4 y skt.SOCK_STREAM para el tipo de conexion tcp
clientSocket.bind(('', clientPort))
clientSocket.listen(1)
print("Conexión establecida con servidor cliente en el puerto:",clientPort)

playerSocket, playerAddr = clientSocket.accept()
player = playerSocket.recv(1024).decode()

flag = True
while flag:
	serverSocket.sendto(player.encode(), (address,serverPort)) # Envía confirmación al servidor gato.
	if player == "1": # Si jugador quiere jugar envía 1.
		status,addr = serverSocket.recvfrom(1024) # Recibe status y el puerto nuevo de servidor gato.
		status = status.decode().split(";")
		np = int(status[1]) # Puerto aleatorio nuevo.
		status = status[0] # Estado del servidor gato.

		if status == "OK": 
			playerSocket.send(status.encode()) # Le envía el estado del servidor gato al servidor cliente.
			player = None
			tableroGato = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
			tab = ["0,0","0,1","0,2","1,0","1,1","1,2","2,0","2,1","2,2"] # Esta lista y la anterior se usan para traducir la jugada del bot y continuar con las jugadas.
			gana_bot = 0
			gana_jug = 0
			contador_de_jugadas = 0
			while gana_jug < 1 and gana_bot < 1: # Mientras no gane jugador o bot, se continúa jugando
				movi_player = (playerSocket.recv(1024).decode()) # Jugada del jugador
				print('El jugador juega: ', movi_player)
				movi_player = movi_player.split(',')
				tableroGato[int(movi_player[1])][int(movi_player[0])] = 'o' # Marca jugada del jugador
				contador_de_jugadas += 1
				# A continuación verificamos si con lo que jugó el jugador, existe victoria por su parte.
				# Se envía "0,0,estado", para que el servidor cliente solo tome en consideración el estado.
				# "0,0" es solamente para lograr el correcto funcionamiento del servidor cliente.
				if (verificar(tableroGato,contador_de_jugadas) == 1):
					playerSocket.send(("0,0,bot").encode())
					break
				elif (verificar(tableroGato,contador_de_jugadas)== 2):
					playerSocket.send(("0,0,jugador").encode())
					break
				elif (verificar(tableroGato, contador_de_jugadas) == 0):
					playerSocket.send(("0,0,empate").encode())
					break
				serverSocket.sendto("listos".encode(), (address, np)) # Avisa para que juegue el bot
				bot, addr = serverSocket.recvfrom(1024)
				bot = bot.decode()
				bot = tab[int(bot)]
				botcl = bot
				bot = bot.split(",")
				contador_de_jugadas += 1
				while (tableroGato[int(bot[1])][int(bot[0])] != " "): # Este while se usa en caso de que el bot elija una casilla ocupada.
					serverSocket.sendto("repita".encode(), (address, np)) # Avisa para que juegue el bot
					bot, addr = serverSocket.recvfrom(1024)
					bot = bot.decode()
					bot = tab[int(bot)]
					botcl = bot
					bot = bot.split(",")
					if contador_de_jugadas >= 9:
						break
				print('El bot juega: ', bot)
				tableroGato[int(bot[1])][int(bot[0])] = "x" # Marca la opcion seleccionada por el bot en el tablero
				# Verificamos nuevamente si existe un ganador.
				if (verificar(tableroGato,contador_de_jugadas) == 1):
					playerSocket.send((botcl+",bot").encode())
					break
				elif (verificar(tableroGato,contador_de_jugadas)== 2):
					playerSocket.send((botcl+",jugador").encode())
					break
				elif (verificar(tableroGato, contador_de_jugadas) == 0):
					playerSocket.send((botcl+",empate").encode())
					break
				else:
					playerSocket.send((botcl+",nada").encode())
			serverSocket.sendto("END".encode(), (address,np)) #avisamos que termina el juego al servidor gato
				
		else:
			playerSocket.send(status.encode()) # Envia el No de servidor gato.
			print("El servidor no se encuentra disponibles en estos momentos, intente mas tarde ")
			flag = False
	else:
		flag = False
		#Envía el 2 para cerrar el servidor gatito
		serverSocket.sendto(str(player).encode(), (address,np))
		print("El servidor se cerrará")
	player = playerSocket.recv(1024).decode()
playerSocket.close()
serverSocket.close()
				
# Casos en que gana: [0,0][1,0][2,0] | [0,1][1,1][2,1] | [0,2][1,2][2,2] 
# 					 [0,0][0,1][0,2] | [1,0][1,1][1,2] | [2,0][2,1][2,2] 
# 					 [0,0][1,1][2,2] | [2,0][1,1][0,2] 
# Total casos de victoria = 8
# Total casos de empate = 1