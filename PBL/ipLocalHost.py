import socket

def main():
    try:
        # Obtém o endereço IP da máquina local
        host_address = socket.gethostbyname(socket.gethostname())
        print(f"Endereço IP {host_address}\n")
    except socket.error as e:
        print("Não foi possível obter o IP da máquina local.")
        print(e)

main()
