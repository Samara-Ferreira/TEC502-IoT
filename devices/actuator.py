""" Módulo responsável por criar o dispositivo atuador que irá se comunicar com o servidor """

# importação de bibliotecas necessárias
import threading
import socket
import random
import time

""" DISPOSITIVO: GELADEIRA """
""" Funcionalidades: 
    - ligar a geladeira
    - desligar a geladeira
    - mudar temperatura da geladeira
    - retornar temperatura da geladeira
    - visualizar os dados da geladeira
    - adicionar itens a geladeira e suas quantidades
    - remover itens da geladeira
    - retornar a quantidade de itens da geladeira
    - retornar a lista de itens da geladeira
    - encerrar programa """


# variáveis globais
HOST = "localhost"
TCP_PORT = 5001
UDP_PORT = 5002

# sockets para comunicação com o servidor
udp_frigde = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# lista de sockets para comunicação com o broker
socketList = []


# dicionário para armazenar os dados da geladeira
frigde = {"ip": 0,
          "id": "GEL01",
          "data": 0.0,
          "category": "atuador",
          "items": {},
          "status": False}


# função para se conectar ao broker
def connect_broker():
    try:
        tcp_frigde = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketList.append(tcp_frigde)

        tcp_frigde.connect((HOST, TCP_PORT))
        threading.Thread(target=receive_tcp, args=[]).start()
        print("Dispositivo conectado ao broker!\n")

    except Exception as e:
        print(f"ERRO: não foi possível se conectar com o servidor: {e}\n")
        close_program()


# função para desconectar do broker
def disconnect_broker():
    try:
        send_tcp("CLOSE")
        time.sleep(0.5)
        socketList[0].close()
        socketList.clear()
        print("Dispositivo desconectado do broker!\n")
    except Exception as e:
        print(f"ERRO: não foi possível desconectar do servidor: {e}\n")


# função para encerrar o programa
def close_program():
    try:
        if socketList:
            disconnect_broker()
        udp_frigde.close()
    except Exception as e:
        print(f"ERRO: não fo5i possível encerrar o programa: {e}\n")


# menu para a geladeira no terminal do dispositivo
def menu_frigde():
    while True:

        view_data()

        print("+" + "-" * 50 + "+")
        print("|" + " MENU DA GELADEIRA".center(50) + "|")
        print("+" + "-" * 50 + "+")
        print("|" + " [1] Ligar a geladeira".ljust(50) + "|")
        print("|" + " [2] Desligar a geladeira".ljust(50) + "|")
        print("|" + " [3] Mudar a temperatura da geladeira".ljust(50) + "|")
        print("|" + " [4] Gerar valores randomicos para a temperatura".ljust(50) + "|")
        print("|" + " [5] Conectar ao broker".ljust(50) + "|")
        print("|" + " [6] Desconectar do broker".ljust(50) + "|")
        print("|" + " [7] Alterar nome do dispositivo".ljust(50) + "|")
        print("|" + " [0] Encerrar programa".ljust(50) + "|")
        print("+" + "-" * 50 + "+")

        print("\nDigite a opção desejada: ")
        option = str(input("> "))

        # opção para ligar a geladeira
        if option == "1":
            turn_on_frigde()

        # opção para desligar a geladeira
        elif option == "2":
            turn_off_frigde()

        # opção para mudar a temperatura da geladeira
        elif option == "3":
            if frigde["status"] is False:
                print("ERRO: não é possível modificar a temperatura, pois a geladeira está desligada!\n")
            else:
                print("Digite a nova temperatura ")
                data = float(input("> "))
                change_temperature(data)

        # opção para gerar valores randomicos para a temperatura (-18 a 4)
        elif option == "4":
            change_temperature(round(random.uniform(-18, 4), 2))

        # opção para conectar ao broker
        elif option == "5":
            connect_broker()

        # opção para desconectar do broker
        elif option == "6":
            disconnect_broker()

        # opção para alterar o nome do dispositivo
        elif option == "7":
            # colocar aqui validações....
            print("Digite o novo nome do dispositivo: ")
            frigde["id"] = str(input("> "))

        # opção para encerrar o programa
        elif option == "0":
            close_program()
            break

        else:
            print("ERRO: opção inválida!\n")


# função para setar o endereço da geladeira
def set_frigde_address(ip):
    frigde["ip"] = ip


# função para ligar a geladeira
def turn_on_frigde():
    frigde["status"] = True


# função para desligar a geladeira
def turn_off_frigde():
    frigde["status"] = False


# função para retornar a temperatura atual
def get_temperature():
    return frigde["data"]


# função para retornar a quantidade de itens na geladeira
def get_quantity():
    return len(frigde["items"])


# função para mudar a temperatura da geladeira
def change_temperature(temperature):
    frigde["data"] = temperature


# função para adicionar itens a geladeira
def add_item(item, quantity):
    if item in frigde["items"]:
        frigde["items"][item] += quantity
    else:
        frigde["items"][item] = quantity


# função para remover itens da geladeira
def remove_item(item, quantity):
    # se a quantidade for maior que a quantidade de itens, remove o item
    if frigde["items"][item] > quantity:
        frigde["items"][item] -= quantity
    # se a quantidade for igual a quantidade de itens, remove o item
    elif frigde["items"][item] == quantity:
        del frigde["items"][item]


# função para visualizar os dados da geladeira
def view_data():
    print("\n+" + "-" * 30 + "+")
    print("| " + " DADOS DA GELADEIRA".center(30) + "|")
    print("+" + "-" * 30 + "+")
    print("| " + f"IP: {frigde['ip']}".ljust(30) + "|")
    print("| " + f"ID: {frigde['id']}".ljust(30) + "|")
    print("| " + f"Temperatura: {frigde['data']}ºC".ljust(30) + "|")
    print("| " + f"Status: {frigde['status']}".ljust(30) + "|")
    print("| " + f"Endereço: {frigde['ip']}".ljust(30) + "|")
    print("| " + f"Categoria: {frigde['category']}".ljust(30) + "|")
    print("| " + f"Quantidade de itens: {get_quantity()}".ljust(30) + "|")
    print("+" + "-" * 30 + "+\n")


# função para visualizar os itens da geladeira
def view_items():
    print("\n+" + "-" * 30 + "+")
    print("|" + " ITENS NA GELADEIRA".center(30) + "|")
    print("+" + "-" * 30 + "+")
    for item, quantity in frigde["items"].items():
        print("|" + f"{item}: {quantity}".ljust(30) + "|")
    print("+" + "-" * 30 + "+\n")


# função para enviar uma mensagem via TCP
def send_tcp(message):
    try:
        socketList[0].send(message.encode("utf-8"))
    except Exception as e:
        print(f"ERRO: não foi possível enviar a mensagem via TCP: {e}\n")
        time.sleep(2)


# função para enviar uma mensagem via UDP
def send_udp(message):
    while True:
        if frigde["status"] is False:
            break
        else:
            try:
                udp_frigde.sendto(message.encode("utf-8"), (HOST, UDP_PORT))
                time.sleep(5)
            except Exception as e:
                print(f"ERRO: não foi possível enviar a mensagem via UDP: {e}\n")
                time.sleep(2)
                break


# função para receber uma mensagem via TCP
def receive_tcp():
    while True:
        try:
            data = socketList[0].recv(2048).decode("utf-8")
            command, data = data.split(":")

            # opção para setar o endereço da geladeira
            if command == "-1":
                set_frigde_address(data)

            if command == "1":
                turn_on_frigde()
                send_tcp("CONFIRMAÇÃO: GELADEIRA LIGADA\n")

            elif command == "2":
                turn_off_frigde()
                send_tcp("CONFIRMAÇÃO: GELADEIRA DESLIGADA\n")

            elif command == "3":
                if frigde["status"] is False:
                    send_tcp("A geladeira está desligada, não é possível mudar os dados!\n")
                else:
                    change_temperature(float(data))
                    send_tcp("CONFIRMAÇÃO: TEMPERATURA ALTERADA\n")

            elif command == "4":
                threading.Thread(target=send_udp, args=[data]).start()
                #send_tcp(f"CONFIRMAÇÃO: TEMPERATURA ATUAL: {get_temperature()}\n")

            elif command == "5":
                send_tcp(str(frigde))

            elif command == "6":
                item = data.split(",")[0]
                quantity = int(data.split(",")[1])
                add_item(item, quantity)
                send_tcp("CONFIRMAÇÃO: ITEM ADICIONADO\n")

            elif command == "7":
                if data in frigde["items"]:
                    item, quantity = data.split(",")
                    quantity = int(quantity)

                    if frigde["items"][item] >= quantity:
                        remove_item(item, quantity)
                        send_tcp("CONFIRMAÇÃO: ITEM REMOVIDO\n")
                    else:
                        send_tcp("ERRO: QUANTIDADE DE ITENS INSUFICIENTE\n")

            elif command == "8":
                send_tcp(f"QUANTIDADE DE ITENS NA GELADEIRA: {get_quantity()}\n")

            elif command == "9":
                send_tcp(f"ITENS NA GELADEIRA: {frigde['items']}\n")

            elif command == "0":
                close_program()
                break

        except Exception as e:
            print(f"ERRO: não foi possível receber os dados via TCP: {e}\n")
            time.sleep(2)
            break


# chamando a função principal
menu_frigde()
