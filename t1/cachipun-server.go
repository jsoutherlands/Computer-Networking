package main

import (
	"fmt"
	"math/rand"
	"net"
	"strconv"
)

// función que printea el inicio del juego
func mensaje_bienvenida() {
	fmt.Println("[*] Bienvenidos al servidor 'LA SUBE' el mejor servidor de cachipun de Gratisjuegos.org")
}


func main() {
	go mensaje_bienvenida() 
	PUERTO := ":50002" 
	BUFFER := 2048
	s, err := net.ResolveUDPAddr("udp4", PUERTO) // Inicio  del socket UDP al cual se le consultará disponibilidad
	if err != nil { // Error en caso de que el puerto esté ocupado
		fmt.Println(err)
		return
	}

	fmt.Println("[*] El servicio para pedir partidas se ejecutara en el puerto localhost"+ PUERTO)

	connection, err := net.ListenUDP("udp4", s) 
	defer connection.Close()
	buffer := make([]byte, BUFFER)
	for {
		n, addr, err := connection.ReadFromUDP(buffer) // se lee el mensaje del servidor intermediario
		fmt.Println("# El cliente envio ->", string(buffer[0:n]))
		if string(buffer[0:n]) == "1" { // recibe 1 si el jugador desea jugar
			respond := rand.Intn(100) // genera el 90% de chance de disponibilidad
			if respond > 9 { 
				new_port := rand.Intn(15500) + 50003 // si está disponible genera un nuevo puerto aleatorio
				str_new_port := strconv.Itoa(new_port)
	
				message := []byte("Ok;" + str_new_port)
				fmt.Printf("data: %s\n", string(message))
				//Le envía al servidor intermediario que está listo para jugar y el puerto UDP donde se podrá comunicar
				_, err = connection.WriteToUDP(message, addr) 
				if err != nil {
					fmt.Println(err)
					return
				}
				PUERTO2 := ":" + str_new_port
				BUFFER2 := 2048
				s2, err2 := net.ResolveUDPAddr("udp4", PUERTO2) // inicia el socket UDP con el puerto generado
				if err2 != nil {
					fmt.Println(err2)
					return
				}
				connection2, err2 := net.ListenUDP("udp4", s2)
				fmt.Println("[*] Se iniciara el ejecutor de partidas en el puerto"+ PUERTO2)
				buffer2 := make([]byte, BUFFER2)
				for {
					n2, addr2, err2 := connection2.ReadFromUDP(buffer2) // recibe el mensaje del servidor intermediario
					if string(buffer2[0:n2]) == "STOP" { // si recibe STOP se termina un juego, y se cierra el socket aleatorio
						fmt.Println("[*] Cerrando el ejecutor de partidas")
						break
					}				
					fmt.Println("# El cliente envio ->"+ string(buffer2[0:n2]))
					move := rand.Intn(3) + 1 // genera una jugada aleatoria
					mensaje2 := []byte(strconv.Itoa(move))
					fmt.Println("#Enviaremos->"+ strconv.Itoa(move)) 
					_, err2 = connection2.WriteToUDP(mensaje2, addr2) // manda su jugada aleatoria al servidor intermediario 
					if err2 != nil {
						fmt.Println(err2)
						break;
					}
				}
				connection2.Close() // cierra el juego cuando el juego se acaba
	
			} else {
				//En caso de que no esté disponible
				message := []byte("No;0")
				fmt.Printf("data: %s\n", string(message))
				_, err = connection.WriteToUDP(message, addr) //Envía el mensaje de no disponibilidad al servidor intermediario
				if err != nil {
					fmt.Println(err)
					return
				}
				fmt.Println("[*] No hay disponibilidad de juego")
				return
			}
		}else {
			// si no recibe el '1' correspondiente a la solicitud de jugar, significa que el jugador ha terminado la sesion.
			fmt.Println("[*] El jugador ha cerrado al sesión")
			return
		}
	}

}
