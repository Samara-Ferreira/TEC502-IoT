# arquivo responsável por iniciar o servidor e lidar com as conexões TCP e UDP

# importações
import socket
from threading import Thread

from server_connections import device_connection

# constantes
HOST = str(socket.gethostbyname(socket.gethostname()))
PORT_TCP = 5551
PORT_UDP = 5552

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def main():
    try:
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
