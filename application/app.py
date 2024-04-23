"""" Módulo responsável por criar a aplicação que irá se comunicar com a API RESTful """

# importação de bibliotecas necessárias
import requests
import os

# variáveis globais
IP_API = "localhost"
PORT_API = 5000

dict_devices = {}


# menu da aplicação
def menu_application():
    os.system("cls")
    while True:
        get_devices()

        print("+" + "-" * 50 + "+")
        print("|" + " MENU DA APLICAÇÃO".center(50) + "|")
        print("+" + "-" * 50 + "+")
        print("|" + " [1] Selecionar um dispositivo".ljust(50) + "|")
        print("|" + " [0] Fechar a aplicação".ljust(50) + "|")
        print("|" + " [-1] Fechar o broker".ljust(50) + "|")
        print("+" + "-" * 50 + "+")

        print("\nDigite o número da opção desejada: ")
        option = str(input("> "))

        if option == "1":
            os.system("cls")
            print()
            get_devices()
            print("Digite o ID do dispositivo para acessar o menu: ")
            device_id = str(input("> "))

            while str(device_id) not in dict_devices:
                print("DICIONARIO ", dict_devices)
                os.system("cls")
                print()
                get_devices()
                print("ID inválido! Digite novamente: ")
                device_id = str(input("> "))

            if dict_devices[device_id]["category"] == "sensor":
                print("Dispositivo selecionado: SENSOR")
                menu_sensor(device_id)
            else:
                print("Dispositivo selecionado: GELADEIRA")
                menu_fridge(device_id)

        elif option == "0":
            print("Encerrando aplicação...")
            break

        elif option == "-1":
            close_api()
            break

        else:
            print("Opção inválida! Tente novamente.\n")

    close_api()


# menu do sensor
def menu_sensor(device_id):
    os.system("cls")
    while True:
        # mostrar dados do sensor no menu
        view_sensor_device(device_id)

        print("+" + "-" * 50 + "+")
        print("|" + " MENU DO SENSOR".center(50) + "|")
        print("+" + "-" * 50 + "+")
        print("|" + " [1] Ligar o sensor".ljust(50) + "|")
        print("|" + " [2] Desligar o sensor".ljust(50) + "|")
        # fica a pergunta... é possível mudar esse dado na aplicação?
        print("|" + " [3] Mudar o dado do sensor".ljust(50) + "|")
        print("|" + " [4] Retornar o dado do sensor".ljust(50) + "|")
        print("|" + " [5] Visualizar os dados do sensor".ljust(50) + "|")
        print("|" + " [0] Voltar para o menu da aplicação".ljust(50) + "|")
        print("+" + "-" * 50 + "+")

        print("\nDigite a opção desejada: ")
        option = str(input("> "))

        if option == "1":
            confirm = turn_on_device(device_id)
            print(confirm)
        elif option == "2":
            confirm = turn_off_device(device_id)
            print(confirm)
        elif option == "3":
            print("Digite o novo dado: ")
            new_data = float(input("> "))
            confirm = change_data_device(device_id, new_data)
            print(confirm)
        elif option == "4":
            confirm = receive_data_device(device_id)
            print(confirm)
        elif option == "5":
            data = view_data_device(device_id)
            print(data)
        elif option == "0":
            print("Voltando...")
            break
        else:
            print("\nERRO: opção inválida!\n")


# menu da geladeira
def menu_fridge(device_id):
    os.system("cls")
    while True:
        view_frigde_device(device_id)

        print("+" + "-" * 50 + "+")
        print("|" + " MENU DA GELADEIRA".center(50) + "|")
        print("+" + "-" * 50 + "+")
        print("|" + " [1] Ligar a geladeira".ljust(50) + "|")
        print("|" + " [2] Desligar a geladeira".ljust(50) + "|")
        print("|" + " [3] Mudar a temperatura da geladeira".ljust(50) + "|")
        print("|" + " [4] Retornar a temperatura da geladeira".ljust(50) + "|")
        print("|" + " [5] Visualizar os dados da geladeira".ljust(50) + "|")
        print("|" + " [6] Adicionar itens a geladeira".ljust(50) + "|")
        print("|" + " [7] Remover itens da geladeira".ljust(50) + "|")
        print("|" + " [8] Retornar a quantidade de itens da geladeira".ljust(50) + "|")
        print("|" + " [9] Retornar a lista de itens da geladeira".ljust(50) + "|")
        print("|" + " [0] Voltar para o menu da aplicação".ljust(50) + "|")
        print("+" + "-" * 50 + "+")

        print("\nDigite a opção desejada: ")
        option = str(input("> "))

        if option == "1":
            confirm = turn_on_device(device_id)
            print(confirm)

        elif option == "2":
            confirm = turn_off_device(device_id)
            print(confirm)

        elif option == "3":
            print("Digite a nova temperatura: ")
            new_data = float(input("> "))
            confirm = change_data_device(device_id, new_data)
            print(confirm)

        elif option == "4":
            confirm = receive_data_device(device_id)
            print(confirm)

        elif option == "5":
            data = view_data_device(device_id)
            print(data)

        elif option == "6":
            print("Digite o item que deseja adicionar: ")
            item = str(input("> ")).lower()
            print("Digite a quantidade do item: ")
            quantity = int(input("> "))
            data = [item, quantity]
            confirm = add_item_device(device_id, data)
            print(confirm)

        elif option == "7":
            print("Digite o item que deseja remover: ")
            item = str(input("> ")).lower()
            confirm = remove_item_device(device_id, item)
            print(confirm)

        elif option == "8":
            confirm = view_quantity_device(device_id)
            print(confirm)


# função para visualizar os dados do sensor
def view_sensor_device(device_id):
    data = eval(view_data_device(device_id))
    print("+" + "-" * 30 + "+")
    print("|" + " DADOS DO SENSOR".center(30) + "|")
    print("+" + "-" * 30 + "+")
    print("|" + f"ID: {device_id}".ljust(30) + "|")
    print("|" + f"Status: {data['status']}".ljust(30) + "|")
    print("|" + f"Temperatura: {data['data']}".ljust(30) + "|")
    print("+" + "-" * 30 + "+\n")


# função para visualizar os dados da geladeira
def view_frigde_device(device_id):
    data = eval(view_data_device(device_id))
    print("+" + "-" * 30 + "+")
    print("|" + " DADOS DA GELADEIRA".center(30) + "|")
    print("+" + "-" * 30 + "+")
    print("|" + f"ID: {device_id}".ljust(30) + "|")
    print("|" + f"Status: {data['status']}".ljust(30) + "|")
    print("|" + f"Temperatura: {data['data']}".ljust(30) + "|")
    print("|" + f"Itens: {data['items']}".ljust(30) + "|")
    print("+" + "-" * 30 + "+\n")


# função para obter os dispositivos conectados
def get_devices():
    global dict_devices
    url = f"http://{IP_API}:{PORT_API}/devices"
    response = requests.get(url)
    dict_devices = response.json()

    print("+" + "-" * 120 + "+")
    print("|" + " DISPOSITIVOS CONECTADOS".center(120) + "|")
    print("+" + "-" * 120 + "+")
    for key, value in dict_devices.items():
        print("|" + f"Dispositivo {key}: {value}".ljust(120) + "|")
    print("+" + "-" * 120 + "+")


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


# ------------------ funções específicas para a geladeira ------------------ #

# função para adicionar itens a geladeira
def add_item_device(device_id, data):
    url = f"http://{IP_API}:{PORT_API}/devices/{device_id}/add/{data[0]}/{data[1]}"
    response = requests.post(url)
    return response.json()


# função para remover itens da geladeira
def remove_item_device(device_id, item):
    url = f"http://{IP_API}:{PORT_API}/devices/{device_id}/remove/{item}"
    response = requests.post(url)
    return response.json()


# função para visualizar a quantidade de itens na geladeira
def view_quantity_device(device_id):
    url = f"http://{IP_API}:{PORT_API}/devices/{device_id}/view/quantity"
    response = requests.get(url)
    return response.json()


# função para visualizar os itens da geladeira
def view_items_device(device_id):
    url = f"http://{IP_API}:{PORT_API}/devices/{device_id}/view/items"
    response = requests.get(url)
    return response.json()


# função para fechar a aplicação
def close_api():
    url = f"http://{IP_API}:{PORT_API}/shutdown"
    response = requests.post(url)
    if response.status_code == 200:
        print("Broker encerrado com sucesso!")
    else:
        print("ERRO: não foi possível encerrar o Broker.")


if __name__ == "__main__":
    menu_application()
