'''
DESCRIÇÃO 
- este código é um exemplo de um dispositivo
- o dispositivo envia mensagens para o servidor via sockets (UDP)
- o dispositivo recebe mensagens do servidor via sockets (TCP) 
'''
import threading
import socket

def main():
    udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        tcp_client.connect(("localhost", 5000))
    except:
        return print("\nErro ao conectar ao servidor.\n")
    
    username = input("Digite seu nome de usuário: ")
    print("Usuário conectado ao servidor.\n")

    receive_thread = threading.Thread(target=receiveMessage, args=[tcp_client])
    send_thread = threading.Thread(target=sendMessage, args=[udp_client, username])

    receive_thread.start()
    send_thread.start()

    receive_thread.join()
    send_thread.join()  

    udp_client.close()
    tcp_client.close()

def receiveMessage(tcp_client):
    while True:
        try:
            message = tcp_client.recv(2048).decode("utf-8")
            print(f"Mensagem recebida do servidor: {message}\n")
        except:
            break

def sendMessage(udp_client, username):
    while True:
        message = input("Digite a mensagem: ")
        #udp_client.sendto(message.encode("utf-8"), ("localhost", 5000))
        udp_client.sendto(f"<{username}> {message}\n".encode("utf-8"), ("localhost", 5000))

main()

