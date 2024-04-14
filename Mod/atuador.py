'''
DESCRIÇÃO 
- ligar a geladeira
- desligar a geladeira
- mudar temperatura atual 
- para ligar e desligar, vão receber o comando via tcp e enviar via tcp 
- os dados, vão ser enviados para o servidor via udp
'''

import threading
import socket
import time
import sys

HOST = "localhost"

TCP_PORT = 5001
UDP_PORT = 5002

tcp_frigde = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
udp_frigde = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

frigde = {"address": 0,
        "ip": 0,
        "id": "GEL01",
        "data": 0,
        "categoria": "atuador",
        "status": False}

def main():
    # conexão com o servidor
    try:
        tcp_frigde.connect((HOST, TCP_PORT))
        setAddress(tcp_frigde.getsockname()[1])
        print(f"Conexão com o servidor estabelecida com a geladeira!\n")
    except Exception as e:
        return print("Erro ao conectar a geladeira ao servidor: {e}\n")
    
    threading.Thread(target=receiveTCP, args=[]).start()
    threading.Thread(target=menuFrigde, args=[]).start()

def setAddress(address):
    frigde["address"] = address

def turnOnFrigde():
    frigde["status"] = True
    sendTCP("CONFIRMAÇÃO: GELADEIRA LIGADA\n")

def turnOffFrigde():
    frigde["status"] = False
    sendTCP("CONFIRMAÇÃO: GELADEIRA DESLIGADA\n")

def changeTemperature(temperature):
    if (frigde["status"] == False):
        print("A geladeira está desligada.\n")
    else:
        frigde["data"] = temperature
        viewData()
        sendTCP(f"CONFIRMAÇÃO: TEMPERATURA ALTERADA PARA {temperature}\n")

def viewData():
    print("\nDADOS DA GELADEIRA:\n")
    print(f"Endereço: {frigde['address']}")
    print(f"IP: {frigde['ip']}")
    print(f"ID: {frigde['id']}")
    print(f"Temperatura: {frigde['data']}")
    print(f"Categoria: {frigde['categoria']}")
    print(f"Status: {frigde['status']}")

# menu para a geladeira no terminal do dispositivo 
def menuFrigde():
    while True:
        print("\nMENU DA GELADEIRA\n")
        print("[1] Ligar geladeira\n")
        print("[2] Desligar geladeira\n")
        print("[3] Mudar temperatura\n")
        print("[4] Visualizar os dados\n")
        print("[5] Encerrar o programa\n")
        
        option = input("Digite a opção desejada [geladeira]: ")
        
        if (option == "1"):
            turnOnFrigde()
        elif (option == "2"):
            turnOffFrigde()
        elif (option == "3"):
            temp = input("Digite a nova temperatura: ")
            changeTemperature(temp)
        elif (option == "4"):
            viewData()
        elif (option == "5"):
            print("Encerrando o programa...\n")
            tcp_frigde.close()
            break
        else:
            print("Opção inválida.\n")

def receiveTCP():
    while True:
        try: 
            messageReceive = tcp_frigde.recv(2048).decode("utf-8")
            print(f"Dados recebidos do servidor [geladeira]: {messageReceive}\n")

            command, data = messageReceive.split(":")

            if (command == "1"):
                turnOnFrigde()
                sendTCP("CONFIRMAÇÃO: GELADEIRA LIGADA\n")
            elif (command == "2"):
                turnOffFrigde()
                sendTCP("CONFIRMAÇÃO: GELADEIRA DESLIGADA\n")
            elif (command == "3"):
                changeTemperature(data)
                threading.Thread(target=sendUDP, args=[data]).start()
            elif (command == "4"):
                viewData()
            elif (command == "5"):
                print("Encerrando o programa...\n")
                sendTCP("CONFIRMAÇÃO: PROGRAMA ENCERRADO\n")
                break
            else:
                print("Comando inválido.\n")

        except Exception as e:
            print(f"Erro ao receber dados do servidor [geladeira]: {e}\n")
            break

def sendTCP(message):
    try:
        tcp_frigde.send(message.encode("utf-8"))
    except Exception as e:
        print(f"Erro ao enviar comando para o servidor: {e}\n")

def sendUDP(message):
    while True:
        try:
            udp_frigde.sendto(message.encode("utf-8"), (HOST, UDP_PORT))
            time.sleep(5)
        except Exception as e:
            print(f"Erro ao enviar dados para o servidor [geladeira] via UDP: {e}\n")
            break

if __name__ == "__main__":
    main()


