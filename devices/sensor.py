""" Módulo responsável por criar o dispositivo sensor que irá se comunicar com o servidor """

# importação de bibliotecas necessárias
import threading
import socket
import time
import os

""" DISPOSITIVO: SENSOR DE TEMPERATURA """
""" Funcionalidades: 
    - ligar o sensor
    - desligar o sensor
    - mudar a temperatura
    - retornar a temperatura
    - visualizar os dados do sensor
    - encerrar programa """

# variáveis globais
HOST = "localhost"
TCP_PORT = 5001
UDP_PORT = 5002

# sockets para comunicação com o servidor
tcp_sensor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
udp_sensor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# dicionário para armazenar os dados do sensor
sensor = {"ip": 0,
          "id": "SEN01",
          "data": 0.0,
          "category": "sensor",
          "status": False}


# função principal
def main():
    try:
        tcp_sensor.connect((HOST, TCP_PORT))
        threading.Thread(target=receive_tcp, args=[]).start()
        menu_sensor()
    except Exception as e:
        print(f"ERRO: não foi possível se conectar com o servidor: {e}\n")
        close_program()


# menu para o sensor no terminal do dispositivo
def menu_sensor():
    while True:
        os.system("cls")

        print("+" + "-" * 50 + "+")
        print("|" + " MENU DO SENSOR".center(50) + "|")
        print("+" + "-" * 50 + "+")
        print("|" + " [1] Ligar o sensor".ljust(50) + "|")
        print("|" + " [2] Desligar o sensor".ljust(50) + "|")
        print("|" + " [3] Mudar a temperatura do sensor".ljust(50) + "|")
        print("|" + " [4] Retornar a temperatura".ljust(50) + "|")
        print("|" + " [5] Visualizar os dados do sensor".ljust(50) + "|")
        print("|" + " [0] Encerrar programa".ljust(50) + "|")
        print("+" + "-" * 50 + "+")

        print("\nDigite a opção desejada: ")
        option = str(input("> "))

        if option == "1":
            turn_on_sensor()
        elif option == "2":
            turn_off_sensor()
        elif option == "3":
            if sensor["status"] is False:
                print("ERRO: não é possível modificar a temperatura, pois o sensor está desligado!\n")
            else:
                print("Digite a nova temperatura ")
                data = float(input("> "))
                change_data(data)
        elif option == "4":
            print("|" + f"Temperatura atual: ", round(get_data(), 2), "\n")
        elif option == "5":
            view_data()
        elif option == "0":
            close_program()
            break
        else:
            print("\tERRO: opção inválida!\n")


# função para setar o endereço do sensor
def set_sensor_address(ip):
    sensor["ip"] = ip


# função para ligar o sensor
def turn_on_sensor():
    sensor["status"] = True


# função para desligar o sensor
def turn_off_sensor():
    sensor["status"] = False


# função para retornar o dado do sensor
def get_data():
    return sensor["data"]


# função para mudar o dado do sensor
def change_data(data):
    sensor["data"] = data


# função para visualizar os dados do sensor
def view_data():
    print("\n+" + "-" * 30 + "+")
    print("|" + " DADOS DO SENSOR".center(30) + "|")
    print("+" + "-" * 30 + "+")
    print("|" + f"ID: {sensor['id']}".ljust(30) + "|")
    print("|" + f"Dado: {sensor['data']}".ljust(30) + "|")
    print("|" + f"Status: {sensor['status']}".ljust(30) + "|")
    print("|" + f"Endereço: {sensor['ip']}".ljust(30) + "|")
    print("|" + f"Categoria: {sensor['category']}".ljust(30) + "|")
    print("+" + "-" * 30 + "+\n")


# função para encerrar o programa
def close_program():
    send_tcp("CLOSE")
    print("Encerrando programa...\n")
    tcp_sensor.close()
    udp_sensor.close()
    exit()


# função para enviar uma mensagem via TCP
def send_tcp(message):
    try:
        tcp_sensor.send(message.encode("utf-8"))
    except Exception as e:
        print(f"ERRO: não foi possível enviar a mensagem via TCP: {e}\n")


# função para enviar uma mensagem via UDP
def send_udp(message):
    while True:
        if sensor["status"] is False:
            break
        else:
            try:
                udp_sensor.sendto(message.encode("utf-8"), (HOST, UDP_PORT))
                time.sleep(5)
            except Exception as e:
                print(f"ERRO: não foi possível enviar a mensagem via UDP: {e}\n")
                break


# função para receber os dados via TCP
def receive_tcp():
    while True:
        try:
            data = tcp_sensor.recv(2048).decode("utf-8")
            command, data = data.split(":")

            if command == "1":
                turn_on_sensor()
                send_tcp("CONFIRMAÇÃO: SENSOR LIGADO\n")
            elif command == "2":
                turn_off_sensor()
                send_tcp("CONFIRMAÇÃO: SENSOR DESLIGADO\n")
            elif command == "3":
                if sensor["status"] is False:
                    send_tcp("ERRO: SENSOR DESLIGADO\n")
                else:
                    change_data(float(data))
                    threading.Thread(target=send_udp, args=[data]).start()
                    send_tcp("CONFIRMAÇÃO: TEMPERATURA ALTERADA\n")
            elif command == "4":
                send_tcp(f"TEMPERATURA ATUAL: {get_data()}\n")
            elif command == "5":
                send_tcp(str(sensor))
            elif command == "0":
                send_tcp("CONFIRMAÇÃO: PROGRAMA ENCERRADO\n")
                close_program()
                break

        except Exception as e:
            print(f"ERRO: não foi possível receber os dados via TCP: {e}\n")
            break


# chamando a função principal
main()
