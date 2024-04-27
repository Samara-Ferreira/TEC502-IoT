""" Módulo com as funções de conexão e comunicação """

# importação de bibliotecas necessáriasimport threading
import time
import socket
import threading
from devices.fridge import Fridge


# classes e métodos para a conexão e comunicação
class Network:
    # atributo para guardar os sockets dos dispositivos
    def __init__(self, host="localhost", tcp_port=5001, udp_port=5002):
        self.tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = host
        self.tcp_port = tcp_port
        self.udp_port = udp_port
        self.connected = False
        self.fridge = Fridge()

    # método para conectar o dispositivo ao servidor broker
    def connect_broker(self):
        if self.connected:
            print(">> Dispositivo já está conectado ao servidor broker!\n")
        else:
            try:
                self.tcp_server.connect((self.host, self.tcp_port))
                threading.Thread(target=self.receive_tcp, args=[]).start()
                self.connected = True
                print(">> Conexão com o servidor broker estabelecida com sucesso!\n")
            except Exception as e:
                return print(f"ERRO: não foi possível conectar com o servidor broker: {e}\n")

    # método para desconectar o dispositivo do servidor broker
    def disconnect_device(self):
        if not self.connected:
            print(">> Dispositivo não está conectado ao servidor broker!\n")
        else:
            try:
                self.send_tcp("CLOSE")
                time.sleep(0.5)             # FLAG
                self.tcp_server.close()
                self.connected = False
                print(">> Desconexão do servidor broker realizada com sucesso!\n")
            except Exception as e:
                print(f"ERRO: não foi possível desconectar do servidor broker: {e}\n")

    # método para enviar dados para o servidor broker via TCP
    def send_tcp(self, message):
        if self.connected:
            try:
                self.tcp_server.send(message.encode("utf-8"))
            except Exception as e:
                return print(f"ERRO: não foi possível enviar dados via TCP: {e}\n")
        else:
            print(">> Dispositivo não está conectado ao servidor broker!\n")

    # método para enviar os dados para o servidor broker via UDP
    def send_udp(self, data):
        while self.fridge.status and self.connected:
            try:
                message = f"{data} ºC"
                self.udp_server.sendto(message.encode("utf-8"), (self.host, self.udp_port))
                time.sleep(5)           # FLAG
            except Exception as e:
                print(f"ERRO: não foi possível enviar dados via UDP: {e}\n")
                break

    # método para receber os dados via TCP
    def receive_tcp(self):
        while self.connected:
            try:
                data = self.tcp_server.recv(2048)
                return data.decode("utf-8")
            except Exception as e:
                if str(e) == "[WinError 10054] Foi forçado o cancelamento de uma conexão existente pelo host remoto":
                    print(">> Conexão encerrada pelo servidor broker!\n")
                    self.connected = False
                    break
                print(f"ERRO: não foi possível receber dados via TCP: {e}\n")
                break
