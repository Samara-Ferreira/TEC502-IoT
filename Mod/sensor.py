'''
DESCRIÇÃO 
- ligar 
- desligar 
- retornar velocidade 
- para ligar e desligar, vão receber o comando via tcp e enviar via tcp 
- os dados, vão ser enviados para o servidor via udp
'''

import threading
import socket
import time

HOST = "localhost"
TCP_PORT = 5001
UDP_PORT = 5002

tcp_device = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
udp_device = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

device = {"id": "SET01", 
        "data": 0,
        "categoria": "sensor",
        "status": False}

def main():
    # conexão com o servidor
    try:
        tcp_device.connect((HOST, TCP_PORT))
        print("Dispositivo conectado ao servidor.\n")
    except:
        return print("Erro ao conectar ao servidor.\n")
    
    threading.Thread(target=receiveTCP, args=[]).start()

    threading.Thread(target=menuDevice, args=[]).start()

def visualizarDados():
    print("\nDADOS DO DISPOSITIVO:\n")
    print(f"ID: {device['id']}")
    print(f"Temperatura: {device['data']}")
    print(f"Categoria: {device['categoria']}")
    print(f"Status: {device['status']}")
    print("\n")

def getId():
    return device["id"]

def ligarSensor():
    device["status"] = True
    sendTCP("CONFIRMAÇÃO: SENSOR LIGADO")

def desligarSensor():
    device["status"] = False
    sendTCP("CONFIRMAÇÃO: SENSOR DESLIGADO")

def mudarTemperatura(temperatura):
    if (device["status"] == False):
        print("O sensor está desligado.\n")
    else:
        device["data"] = temperatura
        visualizarDados()
        sendTCP(f"CONFIRMAÇÃO: TEMPERATURA ALTERADA PARA {temperatura}")

def menuDevice():
    while True:
        print("\nMENU:\n")
        print("[1] Ligar\n")
        print("[2] Desligar\n")
        print("[3] Retornar dados\n")
        print("[4] Visualizar os dados\n")
        print("[5] Encerrar o programa\n")

        # obtendo o comando por meio do terminal
        option = input("Digite a opção desejada: ")

        if (option == "1"):
            ligarSensor()
        elif (option == "2"):
            desligarSensor()
        elif (option == "3"):
            temperatura = input("Digite a temperatura atual: ")
            mudarTemperatura(temperatura)
        elif (option == "4"):
            visualizarDados()
        elif (option == "5"):
            print("Encerrando o programa.\n")
            break
        else:
            print("Opção inválida.\n")

def receiveTCP():
    while True:
        try:
            message = tcp_device.recv(2048).decode("utf-8")
            print(f"Mensagem recebida do servidor: {message}.\n")

            command, data = message.split(":")

            if (command == "1"):
                ligarSensor()
            elif (command == "2"):
                desligarSensor()
            elif (command == "3"):
                send_thread = threading.Thread(target=sendUDP, args=[data])
                send_thread.start()
                mudarTemperatura(data)
            elif (command == "4"):
                visualizarDados()
            elif (command == "5"):
                print("Encerrando o programa.\n")
                break
            else:
                print("Comando inválido.\n")

        except Exception as e:
            print(f"Erro ao receber mensagem do servidor: {e}\n")

def sendTCP(message):
    try:
        tcp_device.send(message.encode("utf-8"))
    except Exception as e:
        print(f"Erro ao enviar mensagem para o servidor via TCP: {e}\n")

def sendUDP(message):
    while True:
        try: 
            udp_device.sendto(message.encode("utf-8"), (HOST, UDP_PORT))
            time.sleep(5)  
        except Exception as e:
            print(f"Erro ao enviar mensagem para o servidor via UDP: {e}\n")  




if __name__ == "__main__":
    main()