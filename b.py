import socket as skt

address = 'localhost'
 
 #go
serverPort = 5000
serverSocket = skt.socket(skt.AF_INET, skt.SOCK_DGRAM)

clientPort = 5001
clientSocket = skt.socket(skt.AF_INET, skt.SOCK_STREAM) #skt.AF_INET indica la direccion ipv4 y skt.SOCK_STREAM para el tipo de conexion tcp
clientSocket.bind(('', clientPort))
clientSocket.listen(1)

try:
	print('Esperando mensaje del cliente')
	playerSocket, playerAddr = clientSocket.accept()
	msg = playerSocket.recv(1024).decode()
	print('Mensaje del cliente', msg)
except:
	print("No hay conexión al a.py")
else:
	try:
		serverSocket.sendto(msg.encode(), (address, serverPort))
	except:
		print("Conexión fallida con el go")
	else:
		print("esperando mensaje del servidor")
		msg, addr = serverSocket.recvfrom(1024)

		print("mensaje del servidor", msg.decode())
		playerSocket.send(msg)