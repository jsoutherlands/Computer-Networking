import socket as skt

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
while flag :
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
			opciones = ["0,0","0,1","0,2","1,0","1,1","1,2","2,0","2,1","2,2"]
			gana_bot = 0
			gana_jug = 0

			while gana_jug < 1 and gana_bot < 1:
				player = (playerSocket.recv(1024).decode()) #jugada jugador
				player = player.split(',')
				serverSocket.sendto("listos".encode(),address, np)
				bot, addr = serverSocket.recvfrom(1024)
				bot = bot.decode().split(',')









