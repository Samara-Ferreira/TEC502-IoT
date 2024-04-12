import threading 
import socket

def main():
    # Connect to the server on local computer IPV4 e TCP
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server on local computer
    try:
        client.connect(("localhost", 5000))
    except:
        return print("\nErro ao conectar ao servidor.\n")
    
    # Envia o nome do usuário para o servidor
    username = input("Digite seu nome de usuário: ")
    print("\nUsuário conectado ao servidor.\n")

    # Cria uma thread para receber mensagens
    receive_thread = threading.Thread(target=receiveMessage, args=[client])

    # Cria uma thread para enviar mensagens
    send_thread = threading.Thread(target=sendMessage, args=[client, username])

    # Inicia a thread
    receive_thread.start()
    send_thread.start()



def receiveMessage(client):
    while True:
        try:
            # Recebe a mensagem do servidor
            message = client.recv(2048).decode("utf-8")
            print(message+"\n")
        except:
            # Fecha a conexão quando ocorre um erro
            print("\nErro ao receber mensagem do servidor.\n")
            print("Pressione <Enter> para continuar...")
            client.close()
            break

# Função para enviar mensagens
def sendMessage(client, username):
    while True:
        try:
            # Envia a mensagem para o servidor
            message = input("\n")
            client.send(f"<{username}> {message}".encode("utf-8"))
        except:
            # Fecha a conexão quando ocorre um erro
            return print("\nErro ao enviar mensagem para o servidor.\n")



main()