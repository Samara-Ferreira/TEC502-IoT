import socket

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    message = input("Digite a mensagem: ")
    client.sendto(message.encode("utf-8"), ("localhost", 1200))     # envia a mensagem para o servidor (endereço IP e porta do servidor)
    message, address = client.recvfrom(2048)    # recebe a mensagem do servidor e o endereço IP do servidor que enviou a mensagem
    print(f"Mensagem recebida de {address}: {message.decode('utf-8')}")