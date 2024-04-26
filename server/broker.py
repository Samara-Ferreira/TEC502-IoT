""" Módulo responsável por criar um servidor broker que recebe dados de dispositivos via TCP e UDP. """

# importação de bibliotecas necessárias
import threading
import socket
import time

# dicionário para guardar os sockets dos dispositivos
socketsDevice = {}

allDevices = {}

# variáveis globais
HOST = "localhost"
TCP_PORT = 5001
UDP_PORT = 5002

# sockets para comunicação com os dispositivos
tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # UDP


# função principal
def main():
    try:
        # conexão dos sockets à mesma porta
        tcp_server.bind((HOST, TCP_PORT))
        tcp_server.listen(5)    # máximo de 5 conexões

        udp_server.bind((HOST, UDP_PORT))
        print("CONFIRMAÇÃO: servidor iniciado!\n")

    except Exception as e:
        return print(f"ERRO: não foi possível iniciar o servidor: {e}\n")

    # threads para lidar com as conexões TCP e UDP
    threading.Thread(target=device_connection, args=[]).start()


# função para lidar com as conexões dos dispositivos
def device_connection():
    while True:
        try:
            print("Aguardando conexões...\n")
            device, address = tcp_server.accept()  # aceitar conexão do device
            print(f"CONFIRMAÇÃO: conexão estabelecida com {address}\n")

            # pegando o endereço do dispositivo e salvando no dicionário de sockets
            device_address = address[1]  # MUDAR PARA 0 PARA PEGAR O IP
            socketsDevice[str(device_address)] = device

            print(f"Dispositivos conectados: {socketsDevice}\n")

            # enviando o ip do dispositivo para o código do dispositivo
            message = f"{'-1'}:{str(device_address)}"
            device.send(message.encode("utf-8"))

            # criando uma thread para receber os dados do device via UDP
            threading.Thread(target=receive_data_udp, args=[]).start()
            # criando uma thread para receber os dados do device via TCP
            threading.Thread(target=receive_data_tcp, args=[device, device_address]).start()

        except Exception as e:
            print(f"ERRO: não foi possível conectar com o dispositivo: {e}\n")
            break


# função para receber os dados via UDP
def receive_data_udp():
    while True:
        data, address = udp_server.recvfrom(2048)
        print(f"CONFIRMAÇÃO: recebido {data.decode("utf-8")} de {address} via UDP.\n")


# função para receber os dados via TCP
def receive_data_tcp(device, device_address):
    while True:
        try:
            data = device.recv(2048)

            # caso seja para encerrar a conexão entre o dispositivo e o broker
            if data.decode('utf-8') == "CLOSE":
                del socketsDevice[str(device_address)]
                time.sleep(0.5)
                device.close()
                print(f"Conexão encerrada com o dispositivo {device_address}!\n")
                break

        except Exception as e:
            print(f"ERRO: não foi possível receber dados via TCP: {e}\n")
            break


# REVER ESSA PARTE
# função para pegar os dados dos dispositivos via TCP
def get_data_tcp():
    for device in socketsDevice:
        try:
            message = f"{'4'}:{0}"
            socketsDevice[device].send(message.encode("utf-8"))

            #response = receive_data_tcp(socketsDevice[device])
            #allDevices[device] = eval(response)

        except Exception as e:
            print(f"ERRO: não foi possível pegar os dados dos dispositivos: {e}\n")
    return #allDevices


# função para receber os comandos da API e enviar para os dispositivos
def receive_command_api(device_address, command, data):
    # para obter todos os dispositivos e salvar em um dicionário
    if device_address == "0":
        get_data_tcp()

    # para obter um dispositivo específico
    else:
        if device_address in socketsDevice:
            try:
                message = f"{command}:{data}"
                socketsDevice[device_address].send(message.encode("utf-8"))
                print(f"CONFIRMAÇÃO: comando enviado para o dispositivo: {message}\n")

                #response = receive_data_tcp(socketsDevice[device_address])
                #return response

            except Exception as e:
                print(f"ERRO: não foi possível enviar o comando para o dispositivo: {e}\n")


# função para encerrar o servidor
def close_broker():
    for device in socketsDevice.values():
        device.close()
    tcp_server.close()
    udp_server.close()

    print("Broker encerrado com sucesso!")


# chamando a função principal
if __name__ == "__main__":
    main()