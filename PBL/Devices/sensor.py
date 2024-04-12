'''
DESCRIÇÃO 
- este código é um exemplo de um dispositivo sensor de temperatura
- o envio dos dados para o servidor será via sockets (UDP)
- o usuário informa o valor da temperatura atual, por meio de um input 
e manda para o servidor conectado via sockets (UDP)
- o dispositivo recebe mensagens do servidor via sockets (TCP) 
- o dispositivo ao ser acionado, pode ligar-se para a obtenção dos dados de temperatura 
(loop que o usuário informa o valor da temperatura atual, e manda para o servidor, 
podendo interromper esse processo)
- o menu será composto por:
    - iniciar obtenção de dados
    - parar obtenção de dados
'''

import threading
import socket


def main():
    udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        tcp_client.connect(("localhost", 5000))
    except:
        return print("\nErro ao conectar ao servidor.\n")
    
    username = input("Digite seu nome de usuário: ")
    print("Usuário conectado ao servidor.\n")

    receive_thread = threading.Thread(target=receiveMessage, args=[tcp_client])
    send_thread = threading.Thread(target=sendMessage, args=[udp_client, username])

    receive_thread.start()
    send_thread.start()

    receive_thread.join()
    send_thread.join()  

    udp_client.close()
    tcp_client.close()


def receiveMessage(tcp_client):
    while True:
        try:
            message = tcp_client.recv(2048).decode("utf-8")
            print(f"Mensagem recebida do servidor: {message}\n")
        except:
            break

def menu():
    # Menu para iniciar ou parar a obtenção de dados
    print("\nMenu")
    print("1. Iniciar obtenção de dados")
    print("2. Parar obtenção de dados")
    return int(input("Digite a opção desejada: "))

def sendMessage(udp_client, username):
    menu_option = 0

    while True:
        if (menu_option == 0):
            menu_option = menu()

        if (menu_option == 2):
            print("Parando obtenção de dados...\n")
            break

        message = input("Digite a temperatura atual: ")
        udp_client.sendto(f"<{username}> {message}\n".encode("utf-8"), ("localhost", 5000))
        
        menu_option = 0

main()



