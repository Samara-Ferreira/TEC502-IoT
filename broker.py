'''
DESCRIÇÃO 
- servidor que fará comunicação via TCP/UDP com os dispositivos, e comunicação via HTTP com a aplicação 
com a API RESTful para a aplicação
- o recebimento de informação do dispositivo será via sockets (UDP)
- o envio de comandos para o dispositivo será via sockets (TCP)
- a comunicação com a aplicação será via HTTP
'''

import threading
import socket
import json

socketsDevice = {}

#devicesConnected = {}

HOST = "localhost"
TCP_PORT = 5001
UDP_PORT = 5002

tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # UDP

def main():
    try: 
        # conexão dos sockets à mesma porta
        # recebimento de uma tupla
        tcp_server.bind((HOST, TCP_PORT))
        tcp_server.listen(5)    # máximo de 5 conexões
        
        udp_server.bind((HOST, UDP_PORT))   
        print("Servidor iniciado!\n")

    except Exception as e:
        return print(f"Erro ao iniciar o servidor: {e}\n")
        
    # threads para lidar com as conexões TCP e UDP 
    threading.Thread(target=deviceConnection, args=[]).start()

def deviceConnection():
    while True:
        try:
            print("Aguardando conexões...\n")
            device, address = tcp_server.accept()  # aceitar conexão do device
            print(f"Conexão estabelecida com {address}\n")

            # pegando o endereço do dispositivo e salvando no dicionário de sockets (MUDAR PRA 0)
            device_address = address[1]            
            socketsDevice[str(device_address)] = device

            print(f"Dispositivos conectados: {socketsDevice}\n")

            # criando um dicionário para guardar os dados que estão sendo recebidos via UDP
            #devicesConnected[str(device_address)] = 0

            # criando uma thread para receber os dados do device via UDP
            threading.Thread(target=receiveDataUDP, args=[]).start()
            # criando uma thread para receber os dados do device via TCP
            threading.Thread(target=receiveDataTCP, args=[device]).start()

        except Exception as e:
            print(f"Erro ao conectar com o dispositivo: {e}\n")
            break

# função chamada na api para enviar comandos para o dispositivo via TCP
def sendCommandTCP(device_address, command, data):
    if device_address in socketsDevice:
        try: 
            message = f"{command}:{data}"
            socketsDevice[device_address].send(message.encode("utf-8"))
            print(f"Comando enviado para o dispositivo {message}\n")

            # recebendo a resposta do dispositivo
            response = receiveDataTCP(socketsDevice[device_address])
            return sendResponseHTTP(response)
        
        except Exception as e:
            print(f"Erro ao enviar comando para o dispositivo: {e}\n")

# função para enviar as respostas para a api via HTTP
def sendResponseHTTP(response):
    print("RESPOSTA ", response)
    return response

# faça para receber os dados do device via UDP
def receiveDataUDP():
    while True:
        try:
            data_device, address = udp_server.recvfrom(2048)  # receber dados do device
            print(f"Dados do dispositivo {address} via UDP: {data_device.decode('utf-8')}\n")
        except Exception as e:
            print(f"Erro ao receber dados do dispositivo via UDP: {e}")
            break

def receiveDataTCP(device):
    while True: 
        try: 
            data = device.recv(2048)  # receber dados do device
            print(f"Dados do dispositivo via TCP: {data.decode('utf-8')}\n")
            #dict_device = eval(data.decode('utf-8'))
            return data.decode('utf-8')
        
        except Exception as e:
            print(f"Erro ao receber dados do dispositivo via TCP: {e}")
            break

def closeProgram():
    tcp_server.close()
    udp_server.close()


if __name__ == "__main__":
    main()