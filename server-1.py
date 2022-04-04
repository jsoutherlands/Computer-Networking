def tablero(tableroGato): #metemos la lista
	print('. 0 | 1 | 2')
	print('0 ' + tableroGato[0][0] + ' | ' + tableroGato[0][1] + ' | ' + tableroGato[0][2])
	print('----+---+---')
	print('1 ' + tableroGato[1][0] + ' | ' + tableroGato[1][1] + ' | ' + tableroGato[1][2])
	print('----+---+---')
	print('2 ' + tableroGato[2][0] + ' | ' + tableroGato[2][1] + ' | ' + tableroGato[2][2])

def marcaTablero(tableroGato, jugada):
	pos = jugada.split(',') #Verificar por parte del intermedio si esta ocuapda la casilla
	
	tableroGato[int(pos[1])][int(pos[0])] = 'o'
	#tableroGato[] = 'o'

def juego(tableroGato):
	print('-------- Bienvenido al Juego --------')
	print('- Seleccione una opcion')
	print('1-Jugar')
	print('2-Salir')
	n = int(input())
	#Respuesta de disponibilidad ok 
	print('--------Comienza el Juego--------')
	tablero(tableroGato)
	print('ingrese su jugada (x,y):')
	jugada= str(input())
	marcaTablero(tableroGato, jugada)
	print('===================')
	

tableroGato = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
marcaTablero(tableroGato, '2,0')
tablero(tableroGato)