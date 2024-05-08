""" Módulo responsável por criar o servidor broker que irá se comunicar com os dispositivos """

# importações
import socket
from threading import Thread

from broker_connections import device_connection
from clear import clear

# constantes
HOST = str(socket.gethostbyname(socket.gethostname()))
PORT_TCP = 5571
PORT_UDP = 5572

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def main():
    try:
        clear()
        print("\tIP do servidor: ", HOST, "Porta TCP: ", PORT_TCP, "Porta UDP: ", PORT_UDP)

        tcp_socket.bind((HOST, PORT_TCP))
        tcp_socket.listen(1)

        udp_socket.bind((HOST, PORT_UDP))
        print("\n\t>> Servidor iniciado com sucesso!\n")

        thread_connection = Thread(target=device_connection, args=[tcp_socket, udp_socket])
        thread_connection.start()

    except socket.error as e:
        print("\n\t>> Erro ao iniciar o servidor: ", e)


if __name__ == "__main__":
    main()
