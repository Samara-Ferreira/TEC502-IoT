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
import requests # Importar a biblioteca requests para comunicação HTTP

# Lista de dispositivos conectados
devicesConnected = []

HOST = "localhost"
PORT = 5000

def main():
    # sockets para comunicação TCP e UDP
    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
    udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # UDP

    try: 
        # conexão dos sockets à mesma porta
        tcp_server.bind((HOST, PORT))
        tcp_server.listen(5)    # máximo de 5 conexões
        udp_server.bind((HOST, PORT))   
        print("Servidor iniciado!\n")
    except:
        return print(f"Erro ao conectar ao servidor.\n")
        
    # threads para lidar com as conexões TCP e UDP 
    threading.Thread(target=deviceConnection, args=[tcp_server]).start()
    # criando uma thread para receber os dados do dispositivo via UDP
    threading.Thread(target=udpDataDevice, args=[udp_server]).start()

def deviceConnection(tcp_server):
    while True:
        try:
            print("Aguardando conexões...\n")
            device, address = tcp_server.accept()  # aceitar conexão do dispositivo
            devicesConnected.append(device)
            print(f"Conexão estabelecida com {address}\n")
            print(f"Dispositivos conectados: {devicesConnected}\n")

        except:
            print(f"Erro ao aceitar conexão.\n")

# faça para receber os dados do dispositivo via UDP
def udpDataDevice(udp_server):
    while True:
        try:
            data_device, address = udp_server.recvfrom(2048)  # receber dados do dispositivo
            print(f"Dados do dispositivo {address}: {data_device.decode('utf-8')}\n")
        except:
            print(f"Erro ao receber dados do dispositivo.\n")


# receber os comandos da aplicação via HTTP
def receiveDataApplication():
    pass

# enviar os dados dos dispositivos para a aplicação via HTTP
def sendDataApplication():
    pass


main()
