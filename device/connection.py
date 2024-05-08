# arquivo que vai lidar com as conexões TCP e UDP, incluindo
# o envio e recebimento de mensagens

""" Este arquivo é responsável por lidar com as comunicações do dispositivo, como a conexão com o Broker, envio
dos comandos via TCP/IP e recebimento das respostas via UDP, caso seja uma resposta com dados """

from threading import Thread
from fridge import *
import socket

HOST = "0"
TCP_PORT = 5571
UDP_PORT = 5572

sockets_list = ["", ""]


# função para fazer a conexão do Broker
def connect_broker():
    global HOST
    HOST = get_fridge_ip_broker()

    # caso a geladeira já esteja conectada ao Broker
    if get_fridge_connection_status() == "conectada":
        print("\tErro: conexão já estabelecida!\n")
    # caso a geladeira não esteja conectada ao Broker
    else:
        try:
            tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp_socket.settimeout(5)
            tcp_socket.connect((HOST, TCP_PORT))
            tcp_socket.settimeout(None)
            sockets_list[0] = tcp_socket

            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sockets_list[1] = udp_socket

            set_fridge_connection_status("conectada")

            # criação da Thread para receber os dados via TCP
            receive_data_tcp_thread = Thread(target=receive_data_tcp)
            receive_data_tcp_thread.start()

            print("\tConexão estabelecida com sucesso!\n")

        # possíveis erros que podem ocorrer
        except socket.timeout:
            print("\tErro: tempo de conexão encerrado!\n")
        except ConnectionRefusedError:
            print("\tErro: conexão recusada pelo servidor!\n")
        except socket.error:
            print("\tErro: conexão não estabelecida!\n")


# função para fazer a desconexão com o Broker
def disconnect_broker():
    # caso a geladeira já esteja desconectada
    if get_fridge_connection_status() == "desconectada":
        print("\tErro: conexão já encerrada!\n")
    # caso a geladeira não esteja conectada
    else:
        try:
            if sockets_list[0]:
                send_tcp("exit")
                sleep(1)

            turn_off_fridge()
            set_fridge_connection_status("desconectada")

            if sockets_list[0]:
                sockets_list[0].close()
                sockets_list[1].close()

            # parar o envio dos dados UDP
            set_udp_thread_status(False)

            print("\tConexão encerrada com sucesso!\n")

        # possíveis erros que podem acontecer
        except socket.error:
            print("\tErro: conexão não encerrada!\n")
        except AttributeError as e:
            print(f"\tErro: conexão não estabelecida!: {e}\n")
        except ConnectionResetError:
            print("\tErro: conexão encerrada pelo servidor!\n")


# função para fazer o envio dos dados via
def send_tcp(message):
    try:
        sockets_list[0].send(message.encode("utf-8"))

    except ConnectionResetError:
        print("\tErro: conexão encerrada pelo servidor!\n")
    except AttributeError:
        print("\tErro: conexão não estabelecida!\n")
    except socket.error:
        print("\tErro: conexão não estabelecida!\n")


def send_udp():
    while (get_fridge_connection_status() == "conectada") and (get_udp_thread_status() is True):
        try:
            message = f"{get_fridge_temperature()} ºC"
            sockets_list[1].sendto(message.encode("utf-8"), (HOST, UDP_PORT))
            sleep(5)

        except ConnectionResetError:
            print("\tErro: conexão encerrada pelo servidor!\n")
            break
        except AttributeError:
            print("\tErro: conexão não estabelecida!\n")
            break
        except socket.error:
            print("\tErro: conexão não estabelecida!\n")
            break


def receive_data_tcp():
    while get_fridge_connection_status() == "conectada":
        try:
            data = sockets_list[0].recv(2048)
            data = data.decode("utf-8")

            try:
                command, data = data.split(":")
                menu_receive_tcp(command, data)

            except ValueError:
                pass

        except socket.error:
            #print("\tErro socket: conexão encerrada de forma inesperada!\n")
            set_fridge_connection_status("desconectada")
            break
        except ConnectionResetError:
            print("\tErro: conexão encerrada pelo servidor!\n")
            break
        except AttributeError:
            break


def menu_receive_tcp(command, data):
    # comando para retornar o status de conexão
    if command == "-2":
        send_tcp(f"{get_fridge_connection_status()}")

    # comando para atualizar o IP do dispositivo
    elif command == "-1":
        set_fridge_ip(str(data))

    # comando pegar os dados do dispositivo
    elif command == "1":
        send_tcp(str(get_fridge_data()))

    # comando para ligar o dispositivo
    elif command == "2":
        turn_on_fridge()
        send_tcp("\tConfirmação: geladeira ligada!\n")

    # comando para desligar o dispositivo
    elif command == "3":
        turn_off_fridge()
        send_tcp("\tConfirmação: geladeira desligada!\n")

    # comando para mudar a temperatura
    elif command == "4":
        if get_fridge_status() == "desligada":
            send_tcp("\tErro: a geladeira está desligada, não é possível mudar os dados!\n")
        else:
            change_temperature(float(data))
            check_udp_thread()
            send_tcp("\tConfirmação: temperatura alterada!\n")

    # comando para retornar a temperatura
    elif command == "5":
        check_udp_thread()
        send_tcp(f"\tConfirmação: temperatura atual: {get_fridge_temperature()}ºC\n")

    # comando para adicionar um item
    elif command == "6":
        item = data.split(",")[0]
        quantity = int(data.split(",")[1])
        confirm = add_item(item, quantity)
        send_tcp(confirm)

    # comando para remover um item
    elif command == "7":
        item = data.split(",")[0]
        quantity = int(data.split(",")[1])
        confirm = remove_item(item, quantity)
        send_tcp(confirm)

    # comando para retornar os itens
    elif command == "8":
        message = f"\n\tITENS NA GELADEIRA: "
        items_dict = get_fridge_items()
        for item in items_dict:
            message += f"\n\t- {item}: {items_dict[item]} unidades"
        send_tcp(message)


def close_program():
    if get_fridge_connection_status() == "conectada":
        disconnect_broker()
    print("\tPrograma encerrado!\n")
    sleep(1)


def check_udp_thread():
    if not get_udp_thread_status():
        set_udp_thread_status(True)
        udp_thread = Thread(target=send_udp)
        udp_thread.start()


def check_random_thread(status):
    if status:
        if not get_random_thread_status():
            set_random_thread_status(True)
            random_thread = Thread(target=random_temperature)
            random_thread.start()
    else:
        set_random_thread_status(False)
