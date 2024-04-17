'''
DESCRIÇÃO
- aplicação fará conexão com a api, para enviar comandos aos dispositivos
- essa aplicação ficará rodando um menu, e o usuário poderá escolher qual dispositivo deseja ligar ou desligar
- a comunicação entre a aplicação e a api será via HTTP
- serão aceitas entradas e então enviadas requisições para a api 
'''

# importação de bibliotecas necessárias
import requests
import os

# variáveis globais
IP_API = "localhost"
PORT_API = 5000

dict_devices = {}


# menu da aplicação 
def menu():
    os.system('cls')
    while True:
        print("----MENU DA APLICAÇÃO----")
        print("[1] Ligar dispositivo")
        print("[2] Desligar dispositivo")
        print("[3] Mudar dados do dispositivo")
        print("[4] Solicitar um dado do dispositivo")
        print("[5] Visualizar os dados do dispositivo")
        print("[0] Sair")
        print("------------")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            device_id = input("Digite o ID do dispositivo que deseja ligar: ")
            ligarDispositivo(device_id)
        elif opcao == "2":
            device_id = input("Digite o ID do dispositivo que deseja desligar: ")
            desligarDispositivo(device_id)
        elif opcao == "3":
            device_id = input("Digite o ID do dispositivo que deseja mudar os dados: ")
            new_data = input("Digite o novo dado: ")
            mudarDadosDispositivo(device_id, new_data)
        elif opcao == "4":
            device_id = input("Digite o ID do dispositivo que deseja solicitar os dados: ")
            solicitarDadosDispositivo(device_id)
        elif opcao == "5":
            device_id = input("Digite o ID do dispositivo que deseja visualizar os dados: ")
            dados = visualizarDadosDispositivo(device_id)
            print("DADOS ", dados)
        elif opcao == "0":
            break
        else:
            print("Opção inválida!\n")

# função para obter os dispositivos conectados
def obterDispositivos():
    url = f"http://{IP_API}:{PORT_API}/devices"
    response = requests.get(url)
    print(response)
    return response.json()

# função para ligar um dispositivo 
def ligarDispositivo(device_id):
    url = f"http://{IP_API}:{PORT_API}/devices/{device_id}/ligar"
    response = requests.post(url)
    print(response)
    # por que não retorna nada? print(response.json())
    return response.json()

# função para desligar um dispositivo
def desligarDispositivo(device_id):
    url = f"http://{IP_API}:{PORT_API}/devices/{device_id}/desligar"
    response = requests.post(url)
    print(response)
    return response.json()

# função para mudar os dados de um dispositivo
def mudarDadosDispositivo(device_id, new_data):
    url = f"http://{IP_API}:{PORT_API}/devices/{device_id}/mudar/{new_data}"
    response = requests.post(url)
    print(response)
    return response.json()

# função para solicitar os dados de um dispositivo
def solicitarDadosDispositivo(device_id):
    url = f"http://{IP_API}:{PORT_API}/devices/{device_id}/pegar"
    response = requests.get(url)
    print(response)
    return response.json()

# função para visualizar os dados de um dispositivo
def visualizarDadosDispositivo(device_id):
    url = f"http://{IP_API}:{PORT_API}/devices/{device_id}/visualizar"
    response = requests.get(url)
    print(response)
    return response.json()



# função principal
menu()






