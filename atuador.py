# importação de bibliotecas necessárias
import threading
import socket
import time
import os

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
          "status": False}


# função principal
def main():
    try:
        tcp_frigde.connect((HOST, TCP_PORT))
        threading.Thread(target=receive_tcp, args=[]).start()
        menu_frigde()
    except Exception as e:
        print(f"Erro ao conectar com o servidor: {e}\n")
        close_program()


# menu para a geladeira no terminal do dispositivo
def menu_frigde():
    while True:
        os.system("cls")

        print("\n----MENU DA GELADEIRA----\n")
        print("[1] Ligar geladeira\n")
        print("[2] Desligar geladeira\n")
        print("[3] Mudar temperatura\n")
        print("[4] Retornar a temperatura\n")
        print("[5] Visualizar os dados da geladeira\n")
        print("[0] Encerrar programa\n")
        option = str(input("Digite a opção desejada: "))

        if option == "1":
            turn_on_frigde()
        elif option == "2":
            turn_off_frigde()
        elif option == "3":
            temperature = float(input("Digite a temperatura desejada: "))
            change_temperature(temperature)
        elif option == "4":
            print(f"Temperatura atual: ", round(get_temperature(), 2), "°C\n")
        elif option == "5":
            view_data()
        elif option == "0":
            close_program()
            break
        else:
            print("Opção inválida!\n")
            time.sleep(2)


# função para setar o endereço da geladeira
def set_ip(ip):
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


# função para mudar a temperatura da geladeira
def change_temperature(temperature):
    if frigde["status"] is False:
        print("A geladeira está desligada, não é possível mudar os dados!\n")
    else:
        frigde["data"] = temperature


# função para visualizar os dados da geladeira
def view_data():
    print("\n----DADOS DA GELADEIRA----\n")
    print(f"Endereço: {frigde['ip']}")
    print(f"ID: {frigde['id']}")
    print(f"Temperatura: {frigde['data']}°C")
    print(f"Categoria: {frigde['category']}")
    print(f"Status: {frigde['status']}")
    print("\n")


# função para encerrar o programa
def close_program():
    print("Encerrando o programa...\n")
    tcp_frigde.close()
    udp_frigde.close()
    exit()


# função para enviar uma mensagem via TCP
def send_tcp(message):
    try:
        tcp_frigde.send(message.encode("utf-8"))
    except Exception as e:
        print(f"Erro ao enviar mensagem via TCP: {e}\n")


# função para enviar uma mensagem via UDP
def send_udp(message):
    while True:
        try:
            udp_frigde.sendto(message.encode("utf-8"), (HOST, UDP_PORT))
            time.sleep(5)
        except Exception as e:
            print(f"Erro ao enviar mensagem via UDP: {e}\n")
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
            elif command == "0":
                send_tcp("CONFIRMAÇÃO: PROGRAMA ENCERRADO\n")
                close_program()
                break

            else:
                print("Comando inválido.\n")

        except Exception as e:
            print(f"Erro ao receber mensagem via TCP: {e}\n")
            break


# chamando a função principal
main()
