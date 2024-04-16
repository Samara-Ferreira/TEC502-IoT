'''
DESCRIÇÃO: Sensor de velocidade 
- Funcionalidades do sensor: ligar, desligar, mudar o valor da velocidade, retornar o valor da velocidade
'''


# bibliotecas necessárias 
import threading
import socket
import time
import os

# variáveis globais 
HOST = "localhost"
TCP_PORT = 5001
UDP_PORT = 5002

threads = []

# sockets para comunicação com o servidor 
tcp_sensor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
udp_sensor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# dicionário para armazenar os dados do sensor
sensor = {"ip": 0,
        "id": "SENV01",
        "data": 0,
        "category": "sensor",
        "status": False}

# função para setar o endereço do sensor
def setIP(ip):
    sensor["ip"] = ip

# função para ligar o sensor
def turnOnSensor():
    sensor["status"] = True

# função para desligar o sensor
def turnOffSensor():
    sensor["status"] = False

# função para retornar a velocidade atual
def getVelocity():
    return sensor["data"]

def getDic():
    return sensor

# função para visualizar os dados do sensor
def viewData():
    print("\n----DADOS DO SENSOR DE VELOCIDADE----\n")
    print(f"Endereço: {sensor['address']}")
    print(f"IP: {sensor['ip']}")
    print(f"ID: {sensor['id']}")
    print(f"Velocidade: {sensor['data']}")
    print(f"Categoria: {sensor['category']}")
    print(f"Status: {sensor['status']}")
    print("\n")

# menu do sensor
def menuSensor():
    os.system("cls")
    # simulação do 'do while'
    while True:
        print("\n--MENU DO SENSOR DE VELOCIDADE--\n")
        print("[1] Ligar o sensor\n")
        print("[2] Desligar o sensor\n")
        print("[3] Mudar velocidade\n")
        print("[4] Retornar velocidade\n")
        print("[5] Visualizar os dados\n")
        print("[6] Encerrar o programa\n")

        # obtendo o comando por meio do terminal
        option = input("Digite a opção desejada: ")

        if (option == "1"):
            turnOnSensor()
    
        elif (option == "2"):
            turnOffSensor()
        elif (option == "3"):
            velocity = input("Digite o valor da velocidade: ")
            while (not(velocity.isdigit())):
                print("Digite um valor inteiro para a velocidade.\n")
                velocity = input("Digite o valor da velocidade: ")

            # verificação se o sensor está ligado ou desligado
            if (sensor["status"] == False):
                print("O sensor está desligado, não é possível mudar os dados!\n")
            else:
                sensor["data"] = velocity

        elif (option == "4"):
            print(f"Velocidade atual: {getVelocity()}\n")
        elif (option == "5"):
            viewData()
        # condição para sair do laço 
        elif (option == "6"):
            print("Encerrando o programa...\n")
            closeProgram()
            break
        else:
            print("Opção inválida.\n")

# receber mensagem do servidor via TCP
def receiveTCP():
    keep_alive = True

    while (keep_alive):
        try: 
            messageReceive = tcp_sensor.recv(2048).decode("utf-8")
            command, data = messageReceive.split(":")

            if (command == "0"):
                sendTCP(str(sensor))

            elif (command == "1"):
                turnOnSensor()
                sendTCP("CONFIRMAÇÃO: SENSOR LIGADO\n")
            elif (command == "2"):
                turnOffSensor()
                sendTCP("CONFIRMAÇÃO: SENSOR DESLIGADO\n")
            elif (command == "3"):
                if (sensor["status"] == False):
                    # mudar para código de erro, quando for solicitado pelo servidor
                    sendTCP("O sensor está desligado, não é possível mudar os dados!\n")
                else:
                    sensor["data"] = data
                    sendTCP(f"CONFIRMAÇÃO: VELOCIDADE ALTERADA PARA {data}\n")
                    send_thread = threading.Thread(target=sendUDP, args=[data])
                    threads.append(send_thread)
                    send_thread.start()
                    
            elif (command == "4"):
                sendTCP(f"VELOCIDADE ATUAL: {getVelocity()}\n")
            elif (command == "5"):
                viewData()
            elif (command == "6"):
                print("Encerrando o programa...\n")
                sendTCP("CONFIRMAÇÃO: PROGRAMA ENCERRADO\n")
                closeProgram()
                keep_alive = False
            else:
                print("Comando inválido.\n")

        except Exception as e:
            print(f"Erro ao receber mensagem do servidor via TCP: {e}\n")
            keep_alive = False

# enviar mensagem para o servidor via TCP
def sendTCP(message):
    try:
        tcp_sensor.send(message.encode("utf-8"))
    except Exception as e:
        print(f"Erro ao enviar mensagem para o servidor via TCP: {e}\n")

# enviar mensagem para o servidor via UDP
def sendUDP(message):
    keep_alive = True

    while (keep_alive):
        try:
            udp_sensor.sendto(message.encode("utf-8"), (HOST, UDP_PORT))
            time.sleep(5)
        except Exception as e:
            print(f"Erro ao enviar mensagem para o servidor via UDP: {e}\n")
            keep_alive = False
    
def closeProgram():
    '''for i in range(len(threads)):
        try:
            threads[i].join()
        except Exception as e:
            print(f"Erro ao encerrar a thread: {e}\n")

    #threads.pop(0)
    print("\nthreads: ")
    print(threads)'''


    # fechando a conexão
    tcp_sensor.close()
    udp_sensor.close()


# função principal

# conexão com o servidor
try:
    tcp_sensor.connect((HOST, TCP_PORT))
    setIP(tcp_sensor.getsockname()[0])
except Exception as e:
    print(f"Erro ao conectar o sensor ao servidor: {e}\n")

# threads para receber os dados via TCP e para o menu do sensor
receive_thread = threading.Thread(target=receiveTCP, args=[])
threads.append(receive_thread)
receive_thread.start()
menu_thread = threading.Thread(target=menuSensor, args=[])
threads.append(menu_thread)
menu_thread.start()



