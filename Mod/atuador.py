'''
DESCRIÇÃO: Geladeira 
- Funcionalidades: ligar, desligar, mudar o valor atual da temperatura,
retornar a temperatura atual, visualizar os dados,
'''

# bibliotecas necessárias 
import threading
import socket
import time

# variáveis globais
HOST = "localhost"
TCP_PORT = 5001
UDP_PORT = 5002

threads = []

# sockets para comunicação com o servidor
tcp_frigde = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
udp_frigde = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# dicionário para armazenar os dados da geladeira
frigde = {"address": 0,
        "ip": 0,
        "id": "GEL01",
        "data": 0,
        "categoria": "atuador",
        "status": False}

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
        print("A geladeira está desligada, não é possível mudar os dados!\n")
    else:
        frigde["data"] = temperature
        sendTCP(f"CONFIRMAÇÃO: TEMPERATURA ALTERADA PARA {temperature}\n")

def getTemperature():
    return frigde["data"]

def viewData():
    print("\n----DADOS DA GELADEIRA----\n")
    print(f"Endereço: {frigde['address']}")
    print(f"IP: {frigde['ip']}")
    print(f"ID: {frigde['id']}")
    print(f"Temperatura: {frigde['data']}")
    print(f"Categoria: {frigde['categoria']}")
    print(f"Status: {frigde['status']}")
    print("\n")

# menu para a geladeira no terminal do dispositivo 
def menuFrigde():
    while True:
        print("\n--MENU DA GELADEIRA\n")
        print("[1] Ligar geladeira\n")
        print("[2] Desligar geladeira\n")
        print("[3] Mudar temperatura\n")
        print("[4] Retornar a temperatura\n")
        print("[5] Visualizar os dados\n")
        print("[6] Encerrar o programa\n")
        
        option = input("Digite a opção desejada: ")
        
        if (option == "1"):
            turnOnFrigde()
        elif (option == "2"):
            turnOffFrigde()
        elif (option == "3"):
            temp = input("Digite a nova temperatura: ")
            while (not(temp.isdigit)):
                print("Digite um valor numérico para a temperatura.\n")
                temp = input("Digite a nova temperatura: ")
            changeTemperature(temp)
        elif (option == "4"):
            print("Temperatura atual: {getTemperature()}\n")
        elif (option == "5"):
            viewData()
        elif (option == "6"):
            print("Encerrando o programa...\n")
            closeProgram()
            break
        else:
            print("Opção inválida.\n")

def receiveTCP():
    keep_alive = True
    while (keep_alive):
        try: 
            messageReceive = tcp_frigde.recv(2048).decode("utf-8")
            command, data = messageReceive.split(":")

            if (command == "1"):
                turnOnFrigde()
                sendTCP("CONFIRMAÇÃO: GELADEIRA LIGADA\n")
            elif (command == "2"):
                turnOffFrigde()
                sendTCP("CONFIRMAÇÃO: GELADEIRA DESLIGADA\n")
            elif (command == "3"):
                changeTemperature(data)
                send_thread = threading.Thread(target=sendUDP, args=[data]).start()
                threads.append(send_thread)
            elif (command == "4"):
                sendTCP(f"CONFIRMAÇÃO: TEMPERATURA ATUAL: {getTemperature()}\n")
            elif (command == "5"): 
                viewData()
            elif (command == "6"):
                print("Encerrando o programa...\n")
                sendTCP("CONFIRMAÇÃO: PROGRAMA ENCERRADO\n")
                keep_alive = False
                break
            else:
                print("Comando inválido.\n")

        except Exception as e:
            print(f"Erro ao receber dados do servidor via TCP: {e}\n")
            keep_alive = False

def sendTCP(message):
    try:
        tcp_frigde.send(message.encode("utf-8"))
    except Exception as e:
        print(f"Erro ao enviar comando para o servidor via TCP: {e}\n")

def sendUDP(message):
    while True:
        try:
            udp_frigde.sendto(message.encode("utf-8"), (HOST, UDP_PORT))
            time.sleep(5)
        except Exception as e:
            print(f"Erro ao enviar dados para o servidor via UDP: {e}\n")
            break

def closeProgram():
    for thread in threads:
        thread.join()

    tcp_frigde.close()
    udp_frigde.close()

# função principal

try:
    tcp_frigde.connect((HOST, TCP_PORT))
    setAddress(tcp_frigde.getsockname()[0]) # se quiser pegar o ip, seta com o getsockname()[0]
except Exception as e:
    print(f"Erro ao conectar a geladeira ao servidor: {e}\n")

# threads para receber os dados do servidor via TCP e para o menu da geladeira
receive_thread = threading.Thread(target=receiveTCP, args=[]).start()
menu_thread = threading.Thread(target=menuFrigde, args=[]).start()

threads.append(receive_thread)
threads.append(menu_thread)




