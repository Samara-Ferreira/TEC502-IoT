# arquivo responsável por lidar com as conexões dos disposisitovs,
# incluindo a aceitação de novas conexões e o envio de mensagens para os dispositivos

from threading import Thread
from time import sleep

sockets_device = {}
data_devices = ["", ""]
all_devices = {}


def device_connection(tcp_socket, udp_socket):
    while True:
        try:
            print("\n\t>> Esperando por novas conexões...")
            connection, address = tcp_socket.accept()
            print("\n\t>> Conexão estabelecida com: ", address)

            # address[1] pega a porta, address[0] pega o IP
            device_ip = address[0]
            sockets_device[str(device_ip)] = connection

            print(f"\tNúmero de dispositivos conectados: {len(sockets_device)}\n")
            print("\tEndereços dos dispositivos conectados: ")
            for ip in sockets_device:
                print(f"\t- {ip}\n")

            # mensagem para o dispositivo de que a conexão foi estabelecida
            message = f"{-1}:{device_ip}"
            sockets_device[str(device_ip)].send(message.encode("utf-8"))

            # criação de uma thread para receber os dados do dispositivo via TCP
            thread_receive_data = Thread(target=receive_data_tcp, args=[connection, device_ip])
            thread_receive_data.start()

            # criação de uma thread para receber os dados do dispositivo via UDP
            thread_receive_data = Thread(target=receive_data_udp, args=[udp_socket])
            thread_receive_data.start()

        except ConnectionResetError as e:
            print("\n\t>> Erro ao aceitar conexão: ", e)
            print("\n\t>> Tentando aceitar novas conexões...\n")
            break
            # no original, ele dá um break aqui, mas acho que não faz sentido


def receive_data_tcp(connection, device_ip):
    while True:
        try:
            data = connection.recv(2048)
            if data:
                if data.decode("utf-8") == "exit":
                    del sockets_device[str(device_ip)]
                    sleep(1)

                    connection.close()
                    print("\n\t>> Conexão encerrada com: ", device_ip)
                    break

                else:
                    data_devices[0] = data.decode("utf-8")
                    print("\n\t| DADOS TCP | dado recebido de ", device_ip, ": ", data.decode("utf-8"))
                    sleep(1)

        except ConnectionResetError as e:
            print("\n\t>> Erro ao receber dados via TCP: ", e)
            print("\n\t>> Tentando receber novos dados...\n")
            break
            # no original, ele dá um break aqui, mas acho que não faz sentido


def receive_data_udp(udp_socket):
    while True:
        data, address = udp_socket.recvfrom(2048)
        print("\n\t| DADOS UDP | dado recebido de ", address, ": ", data.decode("utf-8"))
        data_devices[1] = data.decode("utf-8")


def receive_command_api(device_address, command, data):
    # para obter os dados de todos os dispositivos e salvar em um dicionário
    if command == "-3":
        if not sockets_device:
            return "None"
        else:
            for device in sockets_device:
                try:
                    message = f"{'1'}:{0}"
                    sockets_device[device].send(message.encode("utf-8"))

                    # como eu troco o time sleep por uma flag? -> colocar uma flag ao invés do tempo de espera (time.sleep)
                    # como faço essa flag?

                    sleep(1)

                    if data_devices:
                        response = data_devices[0]
                        all_devices[device] = eval(response)

                except ConnectionResetError:
                    print(f"\tErro: conexão encerrada pelo dispositivo {device}!\n")
            return str(all_devices)

    # para obter um dispositivo específico
    else:
        if str(device_address) in sockets_device:
            try:
                message = f"{command}:{data}"
                sockets_device[str(device_address)].send(message.encode("utf-8"))

                # ideia: colocar uma flag ao invés do tempo
                sleep(1)

                # verificar se tem oq ser enviado
                if data_devices:
                    response = data_devices[0]
                    return str(response)

            except ConnectionResetError:
                print(f"\tErro: conexão encerrada pelo dispositivo {device_address}!\n")
