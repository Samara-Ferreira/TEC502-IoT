'''
DESCRIÇÃO 
- este código é um servidor que fará comunicações com dispositivos
- o envio de comandos para os dispositivos será via sockets (TCP)
- o recebimento de informações dos dispositivos para o servidor será via sockets (UDP)
- o servidor possui um IP e uma porta, sendo o IP = localhost e a porta = 5000
'''

import threading
import socket

# Lista de dispositivos conectados
devicesConnected = []

HOST = "localhost"
PORT = 5000

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # Vinculando os sockets à mesma porta
        server.bind((HOST, PORT))
        server.listen(5)
        udp_server.bind((HOST, PORT))
        print("Servidor iniciado!\n")
    except:
        print(f"Erro ao conectar ao servidor.\n")
        return  # Sair da função se não for possível conectar ao servidor

    # Iniciar threads para lidar com as conexões TCP e UDP
    threading.Thread(target=tcpConnections, args=[server]).start()
    threading.Thread(target=udpData, args=[udp_server]).start()

def tcpConnections(server):
    while True:
        try:
            print("Aguardando conexões TCP...\n")
            client, address = server.accept()  # Aceitar conexão do cliente
            devicesConnected.append(client)
            print(f"Conexão estabelecida com {address}\n")
            print(f"Dispositivos conectados: {devicesConnected}\n")

            # Iniciar uma nova thread para lidar com o cliente
            threading.Thread(target=tcpClient, args=[client]).start()

        except:
            print(f"Erro ao aceitar conexão.\n")

def tcpClient(client):
    while True:
        try:
            data_message = client.recv(2048).decode("utf-8")  # Receber dados do cliente

            print(f"Mensagem recebida via TCP de {client}: {data_message}\n")

            for client in devicesConnected:
                if client != client:
                    try:
                        client.send(data_message.encode("utf-8"))  # Enviar mensagem para o cliente
                    
                    except:
                        print(f"Erro ao enviar mensagem para o cliente.\n")
                        devicesConnected.remove(client)

            # Adicionar lógica para responder ao cliente, se necessário

        except:
            print(f"Erro ao receber mensagem do cliente.\n")
            client.close()
            devicesConnected.remove(client)
            break

def udpData(udp_server):
    while True:
        try:
            data, address = udp_server.recvfrom(2048)  # Receber dados via UDP
            print(f"Mensagem recebida de {address}: {data.decode('utf-8')}\n")
        except:
            print(f"Erro ao receber mensagem via UDP.\n")

main()
