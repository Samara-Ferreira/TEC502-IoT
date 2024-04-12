import threading    
import socket


clients = []    # Lista de clientes conectados

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind(("localhost", 5000))    # Associa o servidor a porta 5000
        server.listen(5)                    # Espera por no máximo 5 conexões
        print("\nServidor iniciado!\n")
    except:
        return print("\nNão foi possível iniciar o servidor!\nJá tem outro em execução\n")
    
    while True:
        print("Aguardando conexões...\n")
        client, address = server.accept()   # Aceita a conexão do cliente
        clients.append(client)              # Adiciona o cliente na lista de clientes
        print(f"Conexão estabelecida com {address}\n")
        print(f"Clientes conectados: {clients}\n")
        # Cria uma thread para tratar as mensagens do cliente
        thread = threading.Thread(target=messagesTreatment, args=[client])
        thread.start()                      # Inicia a thread



def messagesTreatment(client):
    while True:
        try:
            message = client.recv(2048).decode("utf-8")    # Recebe a mensagem do cliente
            print(message)
            broadcast(client, message)                      # Envia a mensagem para todos os clientes
        except:
            # Fecha a conexão quando ocorre um erro
            print("\nErro ao receber mensagem do cliente.\n")
            print("Pressione <Enter> para continuar...")
            client.close()
            deleteClient(client)
            break 

def broadcast(client, message):
    for client in clients:
        if client != client:
            try:
                client.send(message.encode("utf-8"))    # Envia a mensagem para o cliente
            except:
                # Quando um cliente foi desconectado
                print("\nErro ao enviar mensagem para o cliente!\n")
                deleteClient(client)

def deleteClient(client):
    clients.remove(client)


main()