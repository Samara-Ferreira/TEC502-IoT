""" Módulo responsável por criar um servidor broker que recebe dados de dispositivos via TCP e UDP. """

# importação de bibliotecas necessárias
import threading
import socket
import time

# dicionário para guardar os sockets dos dispositivos
socketsDevice = {}

data_udp_devices = []

# lista para guardar os dados dos dispositivos: data_devices[0] = dados via TCP, data_devices[1] = dados via UDP
data_devices = ["", ""]

# dicionário para guardar os dados de todos os dispositivos
all_devices = {}

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
        # UMA ÚNICA CONEXÃO??
        tcp_server.listen(1)    # máximo de 5 conexões

        udp_server.bind((HOST, UDP_PORT))
        print("\n\t>> Servidor iniciado com sucesso!\n")

    # COLOCAR CADA UMA DAS EXCEÇÕES APÓS CRIAR AS CLASSES
    except Exception as e:
        # se a porta já estiver a ser usada, por exemplo (Address already in use) -> OSError
        # se o endereço for inválido (Invalid argument) -> OSError
        # outro: ConnectionRefusedError (se o servidor não estiver disponível) -> ConnectionRefusedError
        # outro: PermissionError (se o usuário não tiver permissão para acessar a porta) -> PermissionError
        # outro: TimeoutError (se o tempo de espera for excedido) -> TimeoutError
        # é bom colocar o tempo de espera para fazer uma conexão? -> sim, para não travar o programa
        # então implemente o tempo de espera e cada um desses erros possívels
        return print(f"ERRO: não foi possível iniciar o servidor: {e}\n")

    # threads para lidar com as conexões TCP e UDP
    threading.Thread(target=device_connection, args=[]).start()


# função para lidar com as conexões dos dispositivos
def device_connection():
    while True:
        try:
            print("\t>> Aguardando conexões...\n")
            device_socket, device_address = tcp_server.accept()  # aceitar conexão do device
            print(f"\tConexão estabelecida com o dispositivo: {device_address}\n")

            # pegando o endereço do dispositivo e salvando no dicionário de sockets
            # MUDAR PARA 0 PARA PEGAR O IP address[0]
            device_ip = device_address[1]
            socketsDevice[str(device_ip)] = device_socket

            print(f"\tNúmero de dispositivos conectados: {len(socketsDevice)}\n")
            print("\tEndereços dos dispositivos conectados: ")
            for ip in socketsDevice:
                print(f"\t- {ip}\n")

            message = f"{'-1'}:{device_ip}"
            socketsDevice[str(device_ip)].send(message.encode("utf-8"))

            # criando uma thread para receber os dados do device via UDP
            threading.Thread(target=receive_data_udp, args=[]).start()

            # criando uma thread para receber os dados do device via TCP
            threading.Thread(target=receive_data_tcp, args=[device_socket, device_address]).start()

        except Exception as e:
            print(f"ERRO: não foi possível conectar com o dispositivo: {e}\n")
            break


# função para receber os dados via UDP
def receive_data_udp():
    # colocar o tempo de espera aqui? -> sim, para não travar o programa
    while True:
        # verificar se o dispositivo está conectado com o broker através do socket
        # caso não está conectado
        data, address = udp_server.recvfrom(2048)
        print(f"DADOS UDP: dado recebido {data.decode('utf-8')} de {address} via UDP.")
        data_devices[1] = data.decode("utf-8")


# função para receber os dados via TCP e enviar para a aplicação
def receive_data_tcp(device_socket, device_address):
    while True:
        try:
            data = device_socket.recv(2048)

            # caso seja para encerrar a conexão entre o dispositivo e o broker
            if data.decode("utf-8") == "CLOSE":
                # TROCAR PRO IP
                del socketsDevice[str(device_address[1])]
                time.sleep(1)

                # fechando a conexão com o dispositivo
                device_socket.close()

                print(f"Conexão encerrada com o dispositivo {str(device_address)}!\n")
                break

            # colocando os dados recebidos via tcp na lista de dados
            if data:
                data_devices[0] = data.decode("utf-8")
                print("DADO TCP: dado recebido via TCP: ", data.decode('utf-8'))

        # EXCEPT PARA CADA UMA DAS EXCEÇÕES
        except Exception as e:
            print(f"ERRO: não foi possível receber dados via TCP: {e}\n")
            break


# função para receber os comandos da API e enviar para os dispositivos
def receive_command_api(device_address, command, data):
    # para obter os dados de todos os dispositivos e salvar em um dicionário
    if command == "-3":
        for device in socketsDevice:
            try:
                message = f"{'1'}:{0}"
                socketsDevice[device].send(message.encode("utf-8"))

                # como eu troco o time sleep por uma flag? -> colocar uma flag ao invés do tempo de espera (time.sleep)
                # como faço essa flag?

                time.sleep(1)

                if data_devices:
                    response = data_devices[0]
                    all_devices[device] = eval(response)

            except Exception as e:
                print(f"ERRO: não foi possível pegar os dados dos dispositivos: {e}\n")

        return str(all_devices)

    # para obter um dispositivo específico
    else:
        if str(device_address) in socketsDevice:
            try:
                message = f"{command}:{data}"
                socketsDevice[str(device_address)].send(message.encode("utf-8"))

                # ideia: colocar uma flag ao invés do tempo
                time.sleep(1)

                # verificar se tem oq ser enviado
                if data_devices:
                    response = data_devices[0]
                    return str(response)

            except Exception as e:
                print(f"ERRO: não foi possível enviar o comando para o dispositivo: {e}\n")


# chamando a função principal
if __name__ == "__main__":
    main()
