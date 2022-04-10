import socket as skt

from sqlalchemy import table


def verificar(tableroGato, contador_de_jugadas):
	if contador_de_jugadas >= 5 :
		if tableroGato[0][0] == tableroGato[1][0] == tableroGato[2][0] != " ": #fila vertical izquierda
			if tableroGato[0][0] == "x":
				return 1
				
			else:
				return 2
			#break
		elif tableroGato[0][1] == tableroGato[1][1] == tableroGato[2][1] != " ":
			if tableroGato[0][1] == "x":
				return 1
			else:
				return 2
			#break
		elif tableroGato[0][2] == tableroGato[1][2] == tableroGato[2][2] != " ":
			if tableroGato[0][2] == "x":
				return 1
			else:
				return 2
			#break
		elif tableroGato[0][0] == tableroGato[0][1] == tableroGato[0][2] != " ":
			if tableroGato[0][0] == "x":
				return 1
			else:
				return 2
			#break
		elif tableroGato[1][0] == tableroGato[1][1] == tableroGato[1][2] != " ":
			if tableroGato[1][0] == "x":
				return 1
			else:
				return 2
			#break
		elif tableroGato[2][0] == tableroGato[2][1] == tableroGato[2][2] != " ":
			if tableroGato[2][0] == "x":
				return 1
			else:
				return 2
			#break
		elif tableroGato[0][0] == tableroGato[1][1] == tableroGato[2][2] != " ":
			if tableroGato[0][0] == "x":
				return 1
			else:
				return 2
			#break
		elif tableroGato[2][0] == tableroGato[1][1] == tableroGato[0][2] != " ":
			if tableroGato[2][0] == "x":
				return 1
			else:
				return 2
			#break
	if contador_de_jugadas == 9:#empate
		return 0


#udp
address = 'localhost'
 
#go
serverPort = 8002
serverSocket = skt.socket(skt.AF_INET, skt.SOCK_DGRAM)

#tcp
clientPort = 8001
clientSocket = skt.socket(skt.AF_INET, skt.SOCK_STREAM) #skt.AF_INET indica la direccion ipv4 y skt.SOCK_STREAM para el tipo de conexion tcp
clientSocket.bind(('', clientPort))
clientSocket.listen(1)

playerSocket, playerAddr = clientSocket.accept()
player = playerSocket.recv(1024).decode()

flag = True
while flag:
	serverSocket.sendto(player.encode(), (address,serverPort))
	if player == "1":
		status,addr = serverSocket.recvfrom(1024)
		status = status.decode().split(";")
		np = int(status[1])
		status = status[0]

		if status == "OK" : 
			playerSocket.send(status.encode())
			player = None
			tableroGato = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
			tab = ["0,0","0,1","0,2","1,0","1,1","1,2","2,0","2,1","2,2"]
			gana_bot = 0
			gana_jug = 0
			contador_de_jugadas = 0
			while gana_jug < 1 and gana_bot < 1:
				print('TABLERO DESPUES DE QUE MARCARON LOS 2 ',tableroGato)
				movi_player = (playerSocket.recv(1024).decode()) #jugada jugador
				movi_player = movi_player.split(',')
				tableroGato[int(movi_player[1])][int(movi_player[0])] = 'o' #marca
				contador_de_jugadas += 1
				print('MARCO O', tableroGato)
				'''if (verificar(tableroGato,contador_de_jugadas) == 1):
					gana_bot +=1
					break
				elif (verificar(tableroGato,contador_de_jugadas)== 2):
					gana_jug +=1
					break
				elif (verificar(tableroGato, contador_de_jugadas) == 0):
					break'''
				serverSocket.sendto("listos".encode(), (address, np)) #avisar para que juegue el bot
				bot, addr = serverSocket.recvfrom(1024)
				
				bot = bot.decode()
				bot = tab[int(bot)]
				print('BOT', bot)
				botcl = bot
				
				bot = bot.split(",")
				contador_de_jugadas += 1
				while (tableroGato[int(bot[1])][int(bot[0])] != " "): #puede fallat dont forget
					serverSocket.sendto("listos".encode(), (address, np)) #avisar para que juegue el bot
					bot, addr = serverSocket.recvfrom(1024)
					bot = bot.decode()
					bot = tab[int(bot)]
					botcl = bot
					bot = bot.split(",")
					if contador_de_jugadas >= 9:
						break
				print('BOOOOOOOOT',bot)
				#playerSocket.send(botcl.encode()) ##VER COMO LO RECIBE EL CLIENTE
				tableroGato[int(bot[1])][int(bot[0])] = "x"
				print('MARCO X',tableroGato)
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
				print(tableroGato)
				#aca viene la decision 
				print('contador de jugadas : ', contador_de_jugadas)
			serverSocket.sendto("END".encode(), (address,np)) #avisamos que termina el juego al servidor gato
			#if gana_jug == 1:
			#	playerSocket.send("jugador".encode())
			#elif gana_bot == 1:
			#	playerSocket.send("bot".encode())
			#else:
			#	playerSocket.send("empate".encode())
			
		else:
			playerSocket.send(status.encode()) #Envia el No de server-cachipun
			print("El servidor no se encuentra disponibles en estos momentos, intente mas tarde ")
			flag = False
	else:
		flag = False
		#Envía el 2 para cerrar el servidor cachipun-server
		serverSocket.sendto(str(player).encode(), (address,np))
		print("El servidor se cerrará")
	player = playerSocket.recv(1024).decode()
playerSocket.close() 
				
# Casos en que gana: [0,0][1,0][2,0] CHECK | [0,1][1,1][2,1] CHECK| [0,2][1,2][2,2] CHECK
# 					 [0,0][0,1][0,2] CHECK| [1,0][1,1][1,2]CHECK | [2,0][2,1][2,2] CHECK
# 					 [0,0][1,1][2,2] CHECK | [2,0][1,1][0,2] CHECK
# Total casos de victoria = 8
# Total casos de empate = 1