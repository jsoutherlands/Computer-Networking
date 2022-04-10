import socket as skt

def tablero(tableroGato): 
	print('. 0 | 1 | 2')
	print('0 ' + tableroGato[0][0] + ' | ' + tableroGato[0][1] + ' | ' + tableroGato[0][2])
	print('----+---+---')
	print('1 ' + tableroGato[1][0] + ' | ' + tableroGato[1][1] + ' | ' + tableroGato[1][2])
	print('----+---+---')
	print('2 ' + tableroGato[2][0] + ' | ' + tableroGato[2][1] + ' | ' + tableroGato[2][2])

def marcaTablero(tableroGato, jugada, jugador):
	pos = jugada.split(',') #Verificar por parte del intermedio si esta ocuapda la casilla
	if jugador == 1:
		tableroGato[int(pos[1])][int(pos[0])] = 'o'
	else:
		tableroGato[int(pos[1])][int(pos[0])] = 'x'

address = 'localhost'
serverPort = 8001
clientSocket = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
clientSocket.connect((address, serverPort))
print("Conexión establecida con servidor intermedio en el puerto:",serverPort)
response = None

bigFlag = True #flag para terminar el programa

while bigFlag:
	print('-------- Bienvenido al Juego --------')
	print('- Seleccione una opcion')
	print('1-Jugar')
	print('2-Salir')
	toSend = input()
	clientSocket.send(toSend.encode())

	if toSend == "1":
		response = clientSocket.recv(1024).decode()
		
		if response == "OK":
			print('respuesta de disponibilidad: OK')
			print('--------Comienza el Juego--------')
			tableroGato = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
			tablero(tableroGato)
			player = input("Ingrese su jugada (x,y): ")
			while True:
				print('==================')

				clientSocket.send(player.encode()) #Envía jugada al mid-server
				bot = clientSocket.recv(1024).decode()
				print('bot:',bot)
				if  bot != 'empate' and bot != 'jugador' and bot != 'bot':
					marcaTablero(tableroGato, player, 1)
					marcaTablero(tableroGato, bot, 2)
				else:
					print('entre al false')
					break

				#response = clientSocket.recv(1024).decode()
				#print(response)
				#Recibe el resultado de la jugada
				#Verifica si algún jugador gana
				tablero(tableroGato)
				player = input("Ingrese su jugada (x,y): ")
				
			#response = clientSocket.recv(1024).decode() #Recibe quien gana la partida
			if bot == "jugador":
				print("Ganas la partida")
				print("------------------------------------")
			elif bot == "bot":
				print("El bot gana la partida")
				print("------------------------------------")
			elif bot == "empate":
				print("¡Hay un empate!")
				print("------------------------------------")
		else: #cachipun-server no puede jugar
			print("No hay disponibilidad de juego")
			bigFlag = False #Se termina la ejecución
	else:
		bigFlag = False #Se termina la ejecución



clientSocket.close()