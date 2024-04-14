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

# Lista de dispositivos conectados
devicesConnected = {}
socketsList = []

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
        tcp_server.listen(2)    # máximo de 5 conexões
        
        udp_server.bind((HOST, UDP_PORT))   
        print("Servidor iniciado!\n")
    except:
        return print(f"Erro ao conectar ao servidor.\n")
        
    # threads para lidar com as conexões TCP e UDP 
    threading.Thread(target=deviceConnection, args=[]).start()

def deviceConnection():
    while True:
        try:
            print("Aguardando conexões...\n")
            device, address = tcp_server.accept()  # aceitar conexão do device
            print(f"Conexão estabelecida com {address}\n")

            # nos PCs de lá, trocar para o 0
            device_address = address[1]            
            devicesConnected[device_address] = device
            print(f"Dispositivos conectados: {devicesConnected}\n")

            # criando uma thread para receber os dados do device via UDP
            threading.Thread(target=receiveDataUDP, args=[]).start()
            # criando uma thread para receber os dados do device via TCP
            threading.Thread(target=receiveDataTCP, args=[device]).start()

        except:
            print(f"Erro ao aceitar conexão.\n")
            break


def sendCommandTCP(device_address, command, data):
    device_address = int(device_address)
    if device_address in devicesConnected:
        try: 
            message = f"{command}:{data}"
            devicesConnected[device_address].send(message.encode("utf-8"))
            print(f"Comando enviado para o dispositivo {message}\n")
        except Exception as e:
            print(f"Erro ao enviar comando para o dispositivo: {e}\n")

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
        except Exception as e:
            print(f"Erro ao receber dados do dispositivo via TCP: {e}")
            break


if __name__ == "__main__":
    main()