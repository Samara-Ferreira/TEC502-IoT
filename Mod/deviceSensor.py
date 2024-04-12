'''
DESCRIÇÃO 
- ligar 
- desligar 
- retornar velocidade 
- para ligar e desligar, vão receber o comando via tcp e enviar via tcp 
- os dados, vão ser enviados para o servidor via udp
'''

import threading
import socket
import time
import sys

HOST = "localhost"
TCP_PORT = 5001
UDP_PORT = 5002

tcp_device = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
udp_device = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def main():
    # conexão com o servidor
    try:
        tcp_device.connect((HOST, TCP_PORT))
        print("Dispositivo conectado ao servidor.\n")
    except:
        return print("Erro ao conectar ao servidor.\n")
    
    threading.Thread(target=receiveTCP, args=[]).start()
    
    option = "0"
    while (option != "4"):
        print("\nMENU:\n")
        print("[1] Ligar\n")
        print("[2] Desligar\n")
        print("[3] Retornar dados\n")
        print("[4] Sair\n")

        # obtendo o comando por meio do terminal
        option = input("Digite a opção desejada: ")

        if (option == "1"):
            ligarSensor()
        elif (option == "2"):
            desligarSensor()
        elif (option == "3"):
            temperatura = retornarDados()
            print(f"Temperatura atual: {temperatura}")
        elif (option == "4"):
            encerrarPrograma()
        else:
            print("Opção inválida.\n")

    #sairDevice(tcp_device, receive_thread)

def ligarSensor():
    sendTCP("VAI LIGAR")
    #sendTCP({"Status": True})
    # mudar status do sensor para ligado via tcp

def desligarSensor():
    sendTCP("VAI DESLIGAR")
    # mudar status do sensor para desligado via tcp

def retornarDados():
    print("Retornando dados do sensor.\n")
    temperatura = input("Digite a temperatura atual: ")
    return temperatura
    # retornar dados do sensor via udp

def receiveTCP():
    message = "0"
    while (message != "4"):
        try: 
            # recebendo o comando por meio da aplicação 
            message = tcp_device.recv(2048).decode("utf-8")
            print(f"Mensagem recebida do servidor {message}.\n")

            if (message == "1"):
                ligarSensor()
            elif (message == "2"):
                desligarSensor()
            elif (message == "3"):
                temperatura = retornarDados()
                send_thread = threading.Thread(target=sendUDP, args=[temperatura])
                send_thread.start()
            elif (message == "4"):
                print("desconectando...\n")
                break
            else:
                print("Comando inválido.\n")
        except:
            print("Erro ao receber mensagem do servidor.\n")


def sendTCP(message):
    try:
        tcp_device.send(message.encode("utf-8"))
        tcp_device.set
    except Exception as e:
        print(f"Erro ao enviar mensagem para o servidor via TCP: {e}\n")

def sendUDP(message):
    while True:
        try: 
            udp_device.sendto(message.encode("utf-8"), (HOST, UDP_PORT))
            time.sleep(5)  
        except Exception as e:
            print(f"Erro ao enviar mensagem para o servidor via UDP: {e}\n")  

def encerrarPrograma():
    print("Encerrando o programa.\n")
    #sys.exit()

"""def sairDevice(socket, thread):
    socket.close()
    thread.close()
    print("Dispositivo totalmente desconectado.\n")"""


if __name__ == "__main__":
    main()