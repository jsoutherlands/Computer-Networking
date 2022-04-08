package main

import (
	"fmt"
	"math/rand"
	"net"
	"strconv"
)

func main() {

	PORT := ":8000" // revisar
	BUFFER := 1024
	s, err := net.ResolveUDPAddr("udp4", PORT)

	if err != nil {
		fmt.Println(err)
		return
	}
	connection, err := net.ListenUDP("udp4", s)
	if err != nil {
		fmt.Println(err)
		return
	}
	defer connection.Close()
	// Hasta aqui se enciende el servidor gato.
	buffer := make([]byte, BUFFER)

	for {
		n, addr, err := connection.ReadFromUDP(buffer) //Leyendo el mensaje del servidor intermedio
		if string(buffer[0:n]) == "1" {
			fmt.Println("El Jugador desea jugar")
			respond := rand.Intn(100)
			if respond > 4 {
				np := rand.Intn(57535) + 8000
				str_np := strconv.Itoa(np)

				message := []byte("OK;" + str_np)
				fmt.Printf("data: %s", message)

				_, err = connection.WriteToUDP(message, addr)
				if err != nil {
					fmt.Println(err)
					return
				}
				RANDOM_PORT := ":" + str_np
				BUFFER2 := 1024
				s2, err2 := net.ResolveUDPAddr("udp4", RANDOM_PORT) // inicia el socket UDP con el puerto generado
				if err2 != nil {
					fmt.Println(err2)
					return
				}
				connection2, err2 := net.ListenUDP("udp4", s2)
				buffer2 := make([]byte, BUFFER2)
				for {
					n2, addr2, err2 := connection2.ReadFromUDP(buffer2)
					if string(buffer2[0:n2]) == "END" {
						fmt.Println("Se cierra el servidor intermedio")
						break
					}
					fmt.Println("El jugador dice:" + string(buffer2[0:n2]))
					//IMPORTANTE CHEQUEAR COMO PASAR EL FORMATO DE (X,Y)
					//CHEQUEALOO
					jugada := strconv.Itoa(rand.Intn(4)) + strconv.Itoa(rand.Intn(4))
					mensaje2 := []byte(strconv.Itoa(jugada))
					fmt.Println("Servidor envía" + strconv.Itoa(jugada))
					_, err2 = connection2.WriteToUDP(mensaje2, addr2) // manda su jugada aleatoria al servidor intermediario
					if err2 != nil {
						fmt.Println(err2)
						break
					}
				}
				connection2.Close()
			} else {
				message := []byte("No;0")
				fmt.Println("El servidor gato no quiere jugar, miau miau")
				_, err = connection.WriteToUDP(message, addr) //Se el mensaje de no disponibilidad al servidor intermediario
				if err != nil {
					fmt.Println(err)
					return
				}
				fmt.Println("No se jugará")
				return
			}
		} else {
			// si no recibe el '1' correspondiente a la solicitud de jugar, significa que el jugador ha terminado la sesion.
			fmt.Println("El jugador cerró sesión")
			return
		}
	}
}
