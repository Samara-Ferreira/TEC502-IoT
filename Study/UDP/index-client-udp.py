"""
CONEXÃO SOCKET
- funcionamento peer-to-peer: cliente e servidor
    - cliente: solicitação de conexão
    - servidor: aceitação de conexão
    - comunicação bidirecional entre cliente e servidor
- cliente: solicitação de conexão
- aplicação conectando com outra aplicação precisa de uma API
    - é o que chamamos de sockets de rede (API de comunicação)
- sockets de rede: permitem a comunicação entre aplicações
- camada de transporte: TCP (Transmission Control Protocol) e UDP (User Datagram Protocol)
- TCP: confiável, orientado à conexão, controle de fluxo, controle de congestionamento
- UDP: não confiável, sem controle de fluxo, sem controle de congestionamento
- sockets TCP: socket.SOCK_STREAM
- sockets UDP: socket.SOCK_DGRAM
- sockets: permitem a comunicação entre aplicações
    - quando usa sockets, não precisa se preocupar com essa camada de transporte
    - simplesmente importa um socket especifico para qual irá querer
"""

# IP do servidor: localhost
# Porta do servidor: 1200

# #from http.server import BaseHTTPRequestHandler, HTTPServer

import socket

# criação de um socket UDP
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# associação do servidor a porta 1200
server.bind(("localhost", 1200))

print("\nServidor iniciado!\n")

while True:
    # recebe a mensagem do cliente
    message, address = server.recvfrom(2048)    # recebe a mensagem do cliente e o endereço IP do cliente que enviou a mensagem 
    print(f"Mensagem recebida de {address}: {message.decode('utf-8')}")

    # envia a mensagem para o cliente
    server.sendto(message, address)
    print(f"Mensagem enviada para {address}: {message.decode('utf-8')}")     

