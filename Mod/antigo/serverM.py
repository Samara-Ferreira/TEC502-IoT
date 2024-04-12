'''
DESCRIÇÃO 
- servidor que fará comunicação via TCP/UDP com os dispositivos, e comunicação via HTTP com a aplicação 
com a API RESTful para a aplicação
- o recebimento de informação do dispositivo será via sockets (UDP)
- o envio de comandos para o dispositivo será via sockets (TCP)
- a comunicação com a aplicação será via HTTP
- fazer o codigo com classe e objeto para o servidor 
'''

import socket

#HOST = "0.0.0.0"
HOST = "localhost"
TCP_PORT = 5000
UDP_PORT = 5005

# melhor um dicionário?
devicesConnected = []

def main():
    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    tcp_server.bind((HOST, TCP_PORT))
    tcp_server.listen(5)

    udp_server.bind((HOST, UDP_PORT))
    
    print("Servidor iniciado!\n")
    
    while True:
        device_socket, device_address = tcp_server.accept()
        devicesConnected.append({"ip": device_address[0]})
        print(f"Conexão estabelecida com {device_address}.\n")
        print(f"Dispositivos conectados: {devicesConnected}\n")

        # thread para enviar comando para o dispositivo
        device_thread = threading.Thread(target=handleDevice, args=(device_socket))
        device_thread.start()
        

def handleDevice(device_socket):
    while True:
        try:
            data = device_socket.recv(2048)
            if not data:
                print("Conexão encerrada.\n")
                devicesConnected.remove({"ip": device_socket.getpeername()[0]})
                break

            # broadcast? necessário mesmo?
            for device in devicesConnected:
                if device["ip"] != device_socket.getpeername()[0]:
                    device_socket.send(data)
                    print(f"Comando enviado para {device['ip']}.\n")
        except:
            print("Erro ao enviar comando.\n")
            devicesConnected.remove({"ip": device_socket.getpeername()[0]})


def receiveUDP(udp_server):
    try: 
        while True:
            data, address = udp_server.recvfrom(2048).decode("utf-8")
            print(f"Dados do dispositivo {address}: {data.decode('utf-8')}\n")
    except:
        print("Erro ao receber dados do dispositivo.\n")
    finally:
        udp_server.close()


if __name__ == "__main__":
    main()



# Código sem classe e objeto

# Lista de dispositivos conectados
devicesConnected = []
socketsList = []

HOST = "localhost"
PORT_TCP = 5000
PORT_UDP = 5000
udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # UDP
tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP


def main():
    # sockets para comunicação TCP e UDP
    try: 
        # conexão dos sockets à mesma PORT_TCPa
        tcp_server.bind((HOST, PORT_TCP))
        tcp_server.listen(5)    # máximo de 5 conexões
        udp_server.bind((HOST, PORT_UDP))   
        print("Servidor iniciado!\n")
    except:
        return print(f"Erro ao conectar ao servidor.\n")
        
    # threads para lidar com as conexões TCP e UDP 
    threading.Thread(target=deviceConnection, args=[tcp_server]).start()
    # criando uma thread para receber os dados do dispositivo via UDP
    #threading.Thread(target=udpDataDevice, args=[udp_server]).start()

def deviceConnection(tcp_server):
    while True:
        try:
            print("Aguardando conexões...\n")
            device, address = tcp_server.accept()  # aceitar conexão do dispositivo
            devicesConnected.append({"ip": address[0]})
            socketsList.append(device)
            print(f"Conexão estabelecida com {address}\n")
            print(f"Dispositivos conectados: {devicesConnected}\n")

        except:
            print(f"Erro ao aceitar conexão.\n")


def sendCommandDevice():
    socketsList[0].send("Iniciar".encode("utf-8"))
    print("Server: Comando enviado para o dispositivo.\n")
    data_device, address = udp_server.recvfrom(2048)
    return {"hgg":data_device.decode("utf-8")}

# faça para receber os dados do dispositivo via UDP
def udpDataDevice(udp_server):
    while True:
        try:
            data_device, address = udp_server.recvfrom(2048)  # receber dados do dispositivo
            print(f"Dados do dispositivo {address}: {data_device.decode('utf-8')}\n")
            return {"Dados": data_device.decode("utf-8")}
        except:
            print(f"Erro ao receber dados do dispositivo.\n")


# receber os comandos da aplicação via HTTP
def receiveDataApplication():
    pass

# enviar os dados dos dispositivos para a aplicação via HTTP
def sendDataApplication():
    pass


if __name__ == "__main__":
    main()
