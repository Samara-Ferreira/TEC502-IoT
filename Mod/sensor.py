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

tcp_sensor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
udp_sensor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sensor = {"address": 0, 
        "ip": 0,
        "id": "SET01",
        "data": 0,
        "categoria": "sensor",
        "status": False}

def main():
    # conexão com o servidor
    try:
        tcp_sensor.connect((HOST, TCP_PORT))
        setAddress(tcp_sensor.getsockname()[1])
        print(f"Conexão com o servidor estabelecida com o sensor!\n")
    except Exception as e:
        return print(f"Erro ao conectar o sensor ao servidor: {e}\n")
    
    threading.Thread(target=receiveTCP, args=[]).start()
    threading.Thread(target=menuSensor, args=[]).start()

def setAddress(address):
    sensor["address"] = address

def turnOnSensor():
    sensor["status"] = True
    sendTCP("CONFIRMAÇÃO: SENSOR LIGADO\n")

def turnOffSensor():
    sensor["status"] = False
    sendTCP("CONFIRMAÇÃO: SENSOR DESLIGADO\n")

def changeTemperature(temperature):
    if (sensor["status"] == False):
        print("O sensor está desligado.\n")
    else:
        sensor["data"] = temperature
        visualizarDados()
        sendTCP(f"CONFIRMAÇÃO: TEMPERATURA ALTERADA PARA {temperature}\n")

def viewData():
    print("\nDADOS DO SENSOR:\n")
    print(f"Endereço: {sensor['address']}")
    print(f"IP: {sensor['ip']}")
    print(f"ID: {sensor['id']}")
    print(f"Temperatura: {sensor['data']}")
    print(f"Categoria: {sensor['categoria']}")
    print(f"Status: {sensor['status']}")
    print("\n")

def menuSensor():
    while True:
        print("\nMENU DO SENSOR\n")
        print("[1] Ligar o sensor\n")
        print("[2] Desligar o sensor\n")
        print("[3] Pedir a temperatura\n")
        print("[4] Visualizar os dados\n")
        print("[5] Encerrar o programa\n")

        # obtendo o comando por meio do terminal
        option = input("Digite a opção desejada [sensor]: ")

        if (option == "1"):
            turnOnSensor()
        elif (option == "2"):
            turnOffSensor()
        elif (option == "3"):
            temp = input("Digite a temperatura atual: ")
            changeTemperature(temp)
        elif (option == "4"):
            viewData()
        elif (option == "5"):
            print("Encerrando o programa...\n")
            tcp_sensor.close()
            break
        else:
            print("Opção inválida.\n")

def receiveTCP():
    while True:
        try:
            messageReceive = tcp_sensor.recv(2048).decode("utf-8")
            print(f"Dados recebidos do servidor [sensor]: {messageReceive}\n")

            command, data = messageReceive.split(":")

            

            if (command == "1"):
                turnOnSensor()
                sendTCP("CONFIRMAÇÃO: SENSOR LIGADO\n")
            elif (command == "2"):
                turnOffSensor()
                sendTCP("CONFIRMAÇÃO: SENSOR DESLIGADO\n")
            elif (command == "3"):
                changeTemperature(data)
                threading.Thread(target=sendUDP, args=[data]).start()
            elif (command == "4"):
                viewData()
            elif (command == "5"):
                print("Encerrando o programa.\n")
                sendTCP("CONFIRMAÇÃO: PROGRAMA ENCERRADO\n")
                break
            else:
                print("Comando inválido.\n")

        except Exception as e:
            print(f"Erro ao receber mensagem do servidor [sensor]: {e}\n")
            break

# enviar mensagem para o servidor via TCP
def sendTCP(message):
    try:
        tcp_sensor.send(message.encode("utf-8"))
    except Exception as e:
        print(f"Erro ao enviar mensagem para o servidor via TCP: {e}\n")

# enviar mensagem para o servidor via UDP
def sendUDP(message):
    while True:
        try: 
            # message = f"{sensor['id']}:{sensor['data']}"
            udp_sensor.sendto(message.encode("utf-8"), (HOST, UDP_PORT))
            time.sleep(5)  
        except Exception as e:
            print(f"Erro ao enviar mensagem para o servidor via UDP: {e}\n")  
            break


if __name__ == "__main__":
    main()