import socket as skt

address = 'localhost'
serverPort = 5001
clientSocket = skt.socket(skt.AF_INET, skt.SOCK_STREAM)

try:
	clientSocket.connect((address, serverPort))
except:
	print("Conexión fallida")
else:
	toSend = input('Pulse enter para solicitar partida: ')
	clientSocket.send(toSend.encode())
	response = clientSocket.recv(1024).decode()
	print("respuesta del servidor", response)
finally:
	clientSocket.close()