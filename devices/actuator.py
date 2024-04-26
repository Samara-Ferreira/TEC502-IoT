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

socketList = ["", ""]

# dicionário para armazenar os dados da geladeira
fridge = {"ip": 0,
          "id": "GEL01",
          "data": 0.0,
          "category": "atuador",
          "items": {},
          "status": False,
          "connected": False,
          "udp_thread": False,
          "random_thread": False}


# função para se conectar ao broker
def connect_broker():
    # verificar se o dispositivo já está conectado
    if fridge["connected"]:
        print("ERRO: dispositivo já conectado ao broker!\n")
    # se não estiver conectado, tentar se conectar
    else:
        try:
            tcp_fridge = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            udp_fridge = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            tcp_fridge.connect((HOST, TCP_PORT))

            socketList[0] = tcp_fridge
            socketList[1] = udp_fridge

            threading.Thread(target=receive_tcp, args=[]).start()
            fridge["connected"] = True

            print("Dispositivo conectado ao broker!\n")

        except Exception as e:
            print(f"ERRO: não foi possível se conectar com o servidor: {e}\n")


# função para desconectar do broker
def disconnect_broker():
    # verificar se o dispositivo está desconectado
    if not fridge["connected"]:
        print("ERRO: dispositivo já desconectado do broker!\n")
    # se não estiver desconectado, tentar desconectar
    else:
        try:
            send_tcp("CLOSE")

            time.sleep(1)

            turn_off_fridge()
            fridge["connected"] = False
            socketList[0].close()

            print("Dispositivo desconectado do broker!\n")

        except Exception as e:
            print(f"ERRO: não foi possível desconectar do servidor: {e}\n")


# função para fechar o terminal do dispositivo
def close_program():
    if fridge["connected"]:
        disconnect_broker()

    socketList[1].close()
    print("Programa encerrado!\n")


# menu para a geladeira no terminal do dispositivo
def menu_fridge():
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
            print("ligando a geladeira...")
            turn_on_fridge()

        # opção para desligar a geladeira
        elif option == "2":
            turn_off_fridge()

        # opção para mudar a temperatura da geladeira
        elif option == "3":
            if fridge["status"] is False:
                print("ERRO: não é possível modificar a temperatura, pois a geladeira está desligada!\n")
            else:
                print("Digite a nova temperatura ")
                data = float(input("> "))
                change_temperature(data)

                if not fridge["udp_thread"]:
                    fridge["udp_thread"] = True
                    threading.Thread(target=send_udp, args=[]).start()

            # pausar a thread de valores randomicos se estiver ativa
            if fridge["random_thread"]:
                fridge["random_thread"] = False

        # opção para gerar valores randomicos para a temperatura (-18 a 4) de forma contínua
        elif option == "4":
            if fridge["status"] is False:
                print("ERRO: não é possível modificar a temperatura, pois a geladeira está desligada!\n")
            else:

                if not fridge["random_thread"]:
                    fridge["random_thread"] = True
                    threading.Thread(target=random_temperature, args=[]).start()

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
            fridge["id"] = str(input("> "))

        # opção para encerrar o programa
        elif option == "0":
            close_program()
            break

        else:
            print("ERRO: opção inválida!\n")


# função para gerar valores randomicos para a temperatura (-18 a 4) de forma contínua
def random_temperature():
    if fridge["status"] is False:
        print("ERRO: não é possível modificar a temperatura, pois a geladeira está desligada!\n")

    else:
        if not fridge["udp_thread"]:
            fridge["udp_thread"] = True
            threading.Thread(target=send_udp, args=[]).start()

        while fridge["status"] is True and fridge["random_thread"] is True:
            change_temperature(round(random.uniform(-18, 4), 2))
            time.sleep(5)


# função para setar o endereço da geladeira
def set_fridge_address(ip):
    fridge["ip"] = ip


# função para ligar a geladeira
def turn_on_fridge():
    fridge["status"] = True


# função para desligar a geladeira
def turn_off_fridge():
    fridge["status"] = False
    fridge["udp_thread"] = False
    fridge["random_thread"] = False


# função para retornar a temperatura atual
def get_temperature():
    return fridge["data"]


# função para retornar a quantidade de itens na geladeira
def get_quantity():
    return len(fridge["items"])


# função para mudar a temperatura da geladeira
def change_temperature(temperature):
    fridge["data"] = temperature


# função para adicionar itens a geladeira
def add_item(item, quantity):
    if item in fridge["items"]:
        fridge["items"][item] += quantity
    else:
        fridge["items"][item] = quantity


# função para remover itens da geladeira
def remove_item(item, quantity):
    if item not in fridge["items"]:
        return "ERRO: ITEM NÃO ENCONTRADO\n"
    # se a quantidade for maior que a quantidade de itens, remove o item
    elif fridge["items"][item] > quantity:
        fridge["items"][item] -= quantity
        return "CONFIRMAÇÃO: ITEM REMOVIDO\n"
    # se a quantidade for igual a quantidade de itens, remove o item
    elif fridge["items"][item] == quantity:
        del fridge["items"][item]
        return "CONFIRMAÇÃO: ITEM REMOVIDO\n"
    # se a quantidade for menor que a quantidade de itens, retorna erro
    else:
        return "ERRO: QUANTIDADE DE ITENS INSUFICIENTE\n"


# função para visualizar os dados da geladeira
def view_data():
    print("\n+" + "-" * 30 + "+")
    print("| " + " DADOS DA GELADEIRA".center(30) + "|")
    print("+" + "-" * 30 + "+")
    print("| " + f"IP: {fridge['ip']}".ljust(30) + "|")
    print("| " + f"ID: {fridge['id']}".ljust(30) + "|")
    print("| " + f"Temperatura: {fridge['data']}ºC".ljust(30) + "|")
    print("| " + f"Status: {fridge['status']}".ljust(30) + "|")
    print("| " + f"Endereço: {fridge['ip']}".ljust(30) + "|")
    print("| " + f"Categoria: {fridge['category']}".ljust(30) + "|")
    print("| " + f"Quantidade de itens: {get_quantity()}".ljust(30) + "|")
    print("| " + f"Conectado: {fridge['connected']}".ljust(30) + "|")
    print("| " + f"Thread UDP: {fridge['udp_thread']}".ljust(30) + "|")
    print("| " + f"Thread Random: {fridge['random_thread']}".ljust(30) + "|")
    print("+" + "-" * 30 + "+\n")


# função para visualizar os itens da geladeira
def view_items():
    print("\n+" + "-" * 30 + "+")
    print("|" + " ITENS NA GELADEIRA".center(30) + "|")
    print("+" + "-" * 30 + "+")
    for item, quantity in fridge["items"].items():
        print("|" + f"{item}: {quantity}".ljust(30) + "|")
    print("+" + "-" * 30 + "+\n")


# função para enviar uma mensagem via TCP
def send_tcp(message):
    try:
        socketList[0].send(message.encode("utf-8"))
    except Exception as e:
        print(f"ERRO: não foi possível enviar a mensagem via TCP: {e}\n")
        time.sleep(2)


def send_udp():
    while fridge["status"] is True and fridge["udp_thread"] is True:
        try:
            message = f"{fridge['data']} ºC"
            socketList[1].sendto(message.encode("utf-8"), (HOST, UDP_PORT))
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
                set_fridge_address(str(data))

            # opção para pegar os dados da geladeira
            if command == "1":
                send_tcp(str(fridge))

            # opção para ligar a geladeira
            elif command == "2":
                turn_on_fridge()
                send_tcp("CONFIRMAÇÃO: GELADEIRA LIGADA\n")

            # opção para desligar a geladeira
            elif command == "3":
                turn_off_fridge()
                send_tcp("CONFIRMAÇÃO: GELADEIRA DESLIGADA\n")

            # opção para mudar a temperatura da geladeira
            elif command == "4":
                if fridge["status"] is False:
                    send_tcp("A geladeira está desligada, não é possível mudar os dados!\n")
                else:
                    change_temperature(float(data))

                    if not fridge["udp_thread"]:
                        fridge["udp_thread"] = True
                        threading.Thread(target=send_udp, args=[]).start()

                    send_tcp("CONFIRMAÇÃO: TEMPERATURA ALTERADA\n")

            # opção para retornar a temperatura da geladeira
            elif command == "5":
                if not fridge["udp_thread"]:
                    fridge["udp_thread"] = True
                    threading.Thread(target=send_udp, args=[]).start()

                send_tcp(f"CONFIRMAÇÃO: TEMPERATURA ATUAL: {get_temperature()}\n")

            # opção para adicionar itens a geladeira
            elif command == "6":
                item = data.split(",")[0]
                quantity = int(data.split(",")[1])

                print("ITEM ", item, "QUANTIDADE ", quantity)
                add_item(item, quantity)
                send_tcp("CONFIRMAÇÃO: ITEM ADICIONADO\n")

            # opção para remover itens da geladeira
            elif command == "7":
                item = data.split(",")[0]
                quantity = int(data.split(",")[1])

                confirm = remove_item(item, quantity)
                send_tcp(confirm)

            # opção para visualizar a quantidade de itens na geladeira
            elif command == "8":
                send_tcp(f"QUANTIDADE DE ITENS NA GELADEIRA: {5()}\n")

            # opção para visualizar os itens da geladeira
            elif command == "9":
                send_tcp(f"ITENS NA GELADEIRA: {fridge['items']}\n")

        # REVER
        except Exception as e:
            if str(e) == "[WinError 10053] Uma conexão estabelecida foi anulada pelo software no computador host":
                break

            print(f"ERRO: não foi possível receber os dados via TCP: {e}\n")
            time.sleep(2)
            break


# chamando a função principal
menu_fridge()
