""" Módulo responsável por criar o dispositivo atuador que irá se comunicar com o servidor """

# importação de bibliotecas necessárias
import threading
import socket
import time
import os

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
tcp_frigde = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
udp_frigde = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# dicionário para armazenar os dados da geladeira
frigde = {"ip": 0,
          "id": "GEL01",
          "data": 0.0,
          "category": "atuador",
          "items": {},
          "status": False}


# função principal
def main():
    try:
        tcp_frigde.connect((HOST, TCP_PORT))
        threading.Thread(target=receive_tcp, args=[]).start()
        menu_frigde()
    except Exception as e:
        print(f"ERRO: não foi possível se conectar com o servidor: {e}\n")
        close_program()


# menu para a geladeira no terminal do dispositivo
def menu_frigde():
    while True:
        os.system("cls")

        print("+" + "-" * 50 + "+")
        print("|" + " MENU DA GELADEIRA".center(50) + "|")
        print("+" + "-" * 50 + "+")
        print("|" + " [1] Ligar a geladeira".ljust(50) + "|")
        print("|" + " [2] Desligar a geladeira".ljust(50) + "|")
        print("|" + " [3] Mudar a temperatura da geladeira".ljust(50) + "|")
        print("|" + " [4] Retornar a temperatura da geladeira".ljust(50) + "|")
        print("|" + " [5] Visualizar os dados da geladeira".ljust(50) + "|")
        print("|" + " [6] Adicionar itens a geladeira".ljust(50) + "|")
        print("|" + " [7] Remover itens da geladeira".ljust(50) + "|")
        print("|" + " [8] Retornar a quantidade de itens da geladeira".ljust(50) + "|")
        print("|" + " [9] Retornar a lista de itens da geladeira".ljust(50) + "|")
        print("|" + " [0] Encerrar programa".ljust(50) + "|")
        print("+" + "-" * 50 + "+")

        print("\nDigite a opção desejada: ")
        option = str(input("> "))

        if option == "1":
            turn_on_frigde()

        elif option == "2":
            turn_off_frigde()

        elif option == "3":
            if frigde["status"] is False:
                print("ERRO: não é possível modificar a temperatura, pois a geladeira está desligada!\n")
            else:
                print("Digite a nova temperatura ")
                data = float(input("> "))
                change_temperature(data)

        elif option == "4":
            print("|" + f"Temperatura atual: ", round(get_temperature(), 2), "\n")

        elif option == "5":
            view_data()

        elif option == "6":
            print("Digite o item que deseja adicionar: ")
            item = str(input("> ")).lower()
            print("Digite a quantidade do item: ")
            quantity = int(input("> "))
            add_item(item, quantity)

        elif option == "7":
            view_items()
            print("Digite o item que deseja remover: ")
            item = str(input("> ")).lower()
            print("Digite a quantidade do item: ")
            quantity = int(input("> "))

            if item in frigde["items"]:
                if frigde["items"][item] >= quantity:
                    remove_item(item, quantity)
                else:
                    print("Não há itens suficientes para serem removidos!\n")
            else:
                print("Item não encontrado!\n")

        elif option == "8":
            print(f"Quantidade de itens na geladeira: {get_quantity()}\n")

        elif option == "9":
            view_items()

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
    if frigde["status"] is False:
        print("A geladeira está desligada, não é possível mudar os dados!\n")
    else:
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
    print("|" + " DADOS DA GELADEIRA".center(30) + "|")
    print("+" + "-" * 30 + "+")
    print("|" + f"ID: {frigde['id']}".ljust(30) + "|")
    print("|" + f"Temperatura: {frigde['data']}".ljust(30) + "|")
    print("|" + f"Status: {frigde['status']}".ljust(30) + "|")
    print("|" + f"Endereço: {frigde['ip']}".ljust(30) + "|")
    print("|" + f"Categoria: {frigde['category']}".ljust(30) + "|")
    print("|" + f"Quantidade de itens: {get_quantity()}".ljust(30) + "|")
    print("+" + "-" * 30 + "+\n")


# função para visualizar os itens da geladeira
def view_items():
    print("\n+" + "-" * 30 + "+")
    print("|" + " ITENS NA GELADEIRA".center(30) + "|")
    print("+" + "-" * 30 + "+")
    for item, quantity in frigde["items"].items():
        print("|" + f"{item}: {quantity}".ljust(30) + "|")
    print("+" + "-" * 30 + "+\n")


# função para encerrar o programa
def close_program():
    send_tcp("CLOSE")
    print("Encerrando o programa...\n")
    tcp_frigde.close()
    udp_frigde.close()
    exit()


# função para enviar uma mensagem via TCP
def send_tcp(message):
    try:
        tcp_frigde.send(message.encode("utf-8"))
    except Exception as e:
        print(f"ERRO: não foi possível enviar a mensagem via TCP: {e}\n")


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
                break


# função para receber uma mensagem via TCP
def receive_tcp():
    while True:
        try:
            data = tcp_frigde.recv(2048).decode("utf-8")
            command, data = data.split(":")

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
                    threading.Thread(target=send_udp, args=[data]).start()
                    send_tcp("CONFIRMAÇÃO: TEMPERATURA ALTERADA\n")

            elif command == "4":
                send_tcp(f"CONFIRMAÇÃO: TEMPERATURA ATUAL: {get_temperature()}\n")

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

            else:
                print("Comando inválido.\n")

        except Exception as e:
            print(f"ERRO: não foi possível receber os dados via TCP: {e}\n")
            break


# chamando a função principal
main()
