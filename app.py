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
def menu_application():
    os.system('cls')
    while True:
        get_devices()

        print("----MENU DA APLICAÇÃO----")
        print("[1] Selecionar um dispositivo")
        print("[0] Fechar a aplicação")
        #print("[-1] Desligar o broker")

        option = str(input("Escolha uma opção: "))

        if option == "1":
            get_devices()
            device_id = str(input("Digite o ID do dispositivo que deseja selecionar: "))
            menu_device(device_id)
        elif option == "0":
            print("Encerrando aplicação...")
            break
        elif option == "-1":
            close_api()


# menu do dispositivo
def menu_device(device_id):
    os.system('cls')
    while True:
        get_devices()

        print("----MENU DO DISPOSITIVO----")
        print("[1] Ligar dispositivo")
        print("[2] Desligar dispositivo")
        print("[3] Mudar dado do dispositivo")
        print("[4] Solicitar um dado do dispositivo")
        print("[5] Visualizar os dados do dispositivo")
        print("[0] Voltar para o menu da aplicação")
        print("------------")
        option = str(input("Escolha uma opção: "))

        if option == "1":
            confirm = turn_on_device(device_id)
            print(confirm)
        elif option == "2":
            confirm = turn_off_device(device_id)
            print(confirm)
        elif option == "3":
            new_data = float(input("Digite o novo dado: "))
            confirm = change_data_device(device_id, new_data)
            print(confirm)
        elif option == "4":
            confirm = receive_data_device(device_id)
            print(confirm)
        elif option == "5":
            dados = view_data_device(device_id)
            print(dados)
        elif option == "0":
            print("Voltando...")
            break
        else:
            print("Opção inválida!\n")


# função para obter os dispositivos conectados
def get_devices():
    url = f"http://{IP_API}:{PORT_API}/devices"
    response = requests.get(url)
    dict_devices = response.json()
    print("DISPOSITIVOS CONECTADOS")
    for key, value in dict_devices.items():
        print(f"Dispositivo {key}: {value}")


# função para ligar um dispositivo
def turn_on_device(device_id):
    url = f"http://{IP_API}:{PORT_API}/devices/{device_id}/on"
    response = requests.post(url)
    return response.json()


# função para desligar um dispositivo
def turn_off_device(device_id):
    url = f"http://{IP_API}:{PORT_API}/devices/{device_id}/off"
    response = requests.post(url)
    return response.json()


# função para mudar os dados de um dispositivo
def change_data_device(device_id, new_data):
    url = f"http://{IP_API}:{PORT_API}/devices/{device_id}/change/{new_data}"
    response = requests.post(url)
    if response.content:
        return response.json()
    else:
        print(response)
        return None


# função para solicitar os dados de um dispositivo
def receive_data_device(device_id):
    url = f"http://{IP_API}:{PORT_API}/devices/{device_id}/return"
    response = requests.get(url)
    return response.json()


# função para visualizar os dados de um dispositivo
def view_data_device(device_id):
    url = f"http://{IP_API}:{PORT_API}/devices/{device_id}/view"
    response = requests.get(url)
    return response.json()


# função para fechar a aplicação
def close_api():
    url = f"http://{IP_API}:{PORT_API}/shutdown"
    response = requests.post(url)
    if response.status_code == 200:
        print("Broker encerrado com sucesso!")
    else:
        print("Erro ao encerrar o Broker.")


if __name__ == "__main__":
    menu_application()
