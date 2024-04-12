'''
DESCRIÇÃO 
- este código é um exemplo de um dispositivo
- o dispositivo envia mensagens para o servidor via sockets (UDP)
- o dispositivo recebe mensagens do servidor via sockets (TCP) 
- fazer o codigo com classe e objeto para o dispositivo
'''

# importação de bibliotecas necessárias
import threading
import socket


# Classe para o dispositivo
class Device:
    # construtor da classe
    def __init__(self, host, port_tcp, port_udp):
        self.host = host
        self.port_tcp = port_tcp
        self.port_udp = port_udp
        self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
        self.udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # UDP

    # método para iniciar o dispositivo
    def main(self):
        try:
            self.tcp_client.connect((self.host, self.port_tcp))  # conectar ao servidor
        except:
            return print("\nErro ao conectar ao servidor.\n")
        
        '''username = input("Digite seu nome de usuário: ")
        print("Usuário conectado ao servidor.\n")'''

        receive_thread = threading.Thread(target=self.receiveMessage, args=[self.tcp_client, self.udp_client])
        receive_thread.start()

    # receber mensagem do servidor via TCP
    def receiveMessage(self, tcp_client, udp_client):
        while True:
            try:
                message = tcp_client.recv(2048).decode("utf-8")
                print(f"Device: Mensagem recebida do servidor {message}.\n")
                self.commandsMessage(udp_client, message)
            except:
                break

    # enviar mensagem para o servidor via UDP
    def sendMessage(self, udp_client, message):      
        udp_client.sendto(message.encode("utf-8"), (self.host, self.port_udp))

    # comandos recebidos do servidor
    def commandsMessage(self, udp_client, message):
        print("Comando de iniciar do dispositivo recebido com sucesso!\n")
        threading.Thread(target=self.sendMessage, args=[udp_client, message]).start()


# instanciando a classe Device
device = Device("localhost", 5000, 5000)


if __name__ == "__main__":
    device.main()







PORT_TCP = 5000
PORT_UDP = 5000

def main():
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        tcp_client.connect(("localhost", PORT_TCP))
    except:
        return print("\nErro ao conectar ao servidor.\n")
    
    username = input("Digite seu nome de usuário: ")
    print("Usuário conectado ao servidor.\n")

    receive_thread = threading.Thread(target=receiveMessage, args=[tcp_client, udp_client])
    

    receive_thread.start()
    #send_thread.start()

    receive_thread.join()
    #send_thread.join()  

    tcp_client.close()
    udp_client.close()


def receiveMessage(tcp_client, udp_client):
    while True:
        try:
            message = tcp_client.recv(2048).decode("utf-8")
            print(f"Device: Mensagem recebida do servidor {message}.\n")
            commandsMessage(udp_client, message)
        except:
            break

def sendMessage(udp_client, message):      
    #udp_client.sendto(f"<{username}> {message}\n".encode("utf-8"), ("localhost", PORT_TCP))
    udp_client.sendto(message.encode("utf-8"), ("localhost", PORT_UDP))


def commandsMessage(udp_client, message):
    # pensando na ideia de ter uma lista de comandos
    print("Device: Comando de iniciar do dispositivo recebido!\n")

    threading.Thread(target=sendMessage, args=[udp_client, message]).start()

    #sendMessage(udp_client, message)


if __name__ == "__main__":
    main()

