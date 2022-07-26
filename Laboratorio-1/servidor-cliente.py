import socket as skt

def tablero(tableroGato): # Imprime el tablero
	print('. 0 | 1 | 2')
	print('0 ' + tableroGato[0][0] + ' | ' + tableroGato[0][1] + ' | ' + tableroGato[0][2])
	print('----+---+---')
	print('1 ' + tableroGato[1][0] + ' | ' + tableroGato[1][1] + ' | ' + tableroGato[1][2])
	print('----+---+---')
	print('2 ' + tableroGato[2][0] + ' | ' + tableroGato[2][1] + ' | ' + tableroGato[2][2])

def marcaTablero(tableroGato, jugada, jugador): #Marca el tablero, que corresponde a una matriz de 3x3. Se marca "o" para jugador y "x" para el Bot.
	pos = jugada.split(',') #Verificar por parte del intermedio si está ocupada la casilla
	if jugador == 1:
		tableroGato[int(pos[1])][int(pos[0])] = 'o' # Las posiciones están al revés para poder seguir la regla de (x,y).
	else:
		tableroGato[int(pos[1])][int(pos[0])] = 'x'

address = 'localhost'
serverPort = 8001
clientSocket = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
clientSocket.connect((address, serverPort))
print("Conexión establecida con servidor intermedio en el puerto:",serverPort)
response = None

bigFlag = True # Flag para terminar el programa

while bigFlag:
	print('-------- Bienvenido al Juego --------')
	print('- Seleccione una opcion')
	print('1-Jugar')
	print('2-Salir')
	toSend = input()
	clientSocket.send(toSend.encode())

	if toSend == "1": # Ingresa si el cliente pulsa "1-Jugar"
		response = clientSocket.recv(1024).decode() # Recibe la confirmación del servidor intermediario para comenzar
		
		if response == "OK":
			print('respuesta de disponibilidad: OK')
			print('--------Comienza el Juego--------')
			tableroGato = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
			tablero(tableroGato)
			while True:
				player = input("Ingrese su jugada (x,y): ")
				clientSocket.send(player.encode()) 
				print('==============================')
				bot = clientSocket.recv(1024).decode()
				print('bot:',bot)
				comando = bot.split(",")
				if  comando[2] == "nada": # El formato que envía el servidor intermediario es del tipo "x,y,comando", siendo comando
					marcaTablero(tableroGato, player, 1) 			# las opciones "jugador", "bot", "empate" o "nada", dependiendo
					marcaTablero(tableroGato, bot, 2)				# de qué pasa luego de la jugada realizada. Esto puede terminar
					tablero(tableroGato)							# inmediatamente el juego al encontrar el ganador o haber un empate
				else:
					tablero(tableroGato)
					break		
			tablero(tableroGato)
			if comando[2] == "jugador": # Opciones en caso de que comando 
				print("Ganas la partida")
				print("------------------------------------")
			elif comando[2] == "bot":
				print("El bot gana la partida")
				print("------------------------------------")
			elif comando[2] == "empate":
				print("¡Hay un empate!")
				print("------------------------------------")
		else: # Gato no disponible
			print('respuesta de disponibilidad: NO')
			print('cerrando...')
			bigFlag = False #Se termina la ejecución
	else:
		bigFlag = False #Se termina la ejecución

clientSocket.close()