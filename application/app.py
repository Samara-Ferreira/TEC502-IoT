# importação de bibliotecas necessárias
import requests

"""" Módulo responsável por criar a aplicação que irá se comunicar com a API RESTful """
""" a opção de visualizar os dados está com o comando -2 """

# variáveis globais
IP_API = "0.0.0.0"
PORT_API = 5555

# variáveis globais para os prints
len_print1 = 50
len_print2 = 100

dict_devices = {}


# menu da aplicação
def menu_application():
    while True:
        print("+" + "-" * len_print1 + "+")
        print("|" + " MENU DA APLICAÇÃO".center(len_print1) + "|")
        print("+" + "-" * len_print1 + "+")
        print("|" + " [1] Selecionar um dispositivo".ljust(len_print1) + "|")
        print("|" + " [0] Fechar a aplicação".ljust(len_print1) + "|")
        print("+" + "-" * len_print1 + "+")

        print("\nDigite o número da opção desejada: ")
        option = str(input("> "))

        # opção para selecionar um dispositivo
        if option == "1":
            # selecionando um dispositivo para acessar o menu
            get_all_devices()

            print("Digite o ID do dispositivo para acessar o menu: ")
            device_id = str(input("> "))

            # verificar se o ID é válido
            while device_id not in dict_devices:
                if device_id == "0":
                    break

                get_all_devices()
                print("ID inválido! Digite novamente: ")
                device_id = str(input("> "))

            # verificar se o dispositivo é um sensor
            if dict_devices[device_id]["category"] == "sensor":
                print("Dispositivo selecionado: SENSOR")
                menu_sensor(device_id)

            # verificar se o dispositivo é uma geladeira
            else:
                print("Dispositivo selecionado: GELADEIRA")
                menu_fridge(device_id)

        # opção para fechar a aplicação
        elif option == "0":
            print("Encerrando aplicação...")
            # limpar dicionário
            dict_devices.clear()
            break

        # opção inválida
        else:
            print("Opção inválida! Tente novamente.\n")


# menu do sensor
def menu_sensor(device_id):
    while True:
        # mostrar dados do sensor no menu
        view_sensor_device(device_id)

        print("+" + "-" * len_print1 + "+")
        print("|" + " MENU DO SENSOR".center(len_print1) + "|")
        print("+" + "-" * len_print1 + "+")
        print("|" + " [1] Ligar o sensor".ljust(len_print1) + "|")
        print("|" + " [2] Desligar o sensor".ljust(len_print1) + "|")
        print("|" + " [3] Retornar o dado do sensor".ljust(len_print1) + "|")
        print("|" + " [0] Voltar para o menu da aplicação".ljust(len_print1) + "|")
        print("+" + "-" * len_print1 + "+")

        print("\nDigite a opção desejada: ")
        option = str(input("> "))

        # opção para ligar o sensor
        if option == "1":
            confirm = turn_on_device(device_id)
            print(confirm)

        # opção para desligar o sensor
        elif option == "2":
            confirm = turn_off_device(device_id)
            print(confirm)

        # opção para retornar o dado do sensor
        elif option == "3":
            confirm = receive_data_device(device_id)
            print(confirm)

        # opção para voltar ao menu da aplicação
        elif option == "0":
            print("Voltando...")
            break

        else:
            print("\nOpção inválida! Tente novamente.\n")


# menu da geladeira
def menu_fridge(device_id):
    while True:

        print("+" + "-" * len_print1 + "+")
        print("|" + " MENU DA GELADEIRA".center(len_print1) + "|")
        print("+" + "-" * len_print1 + "+")
        print("|" + " [1] Visualizar os dados da geladeira".ljust(len_print1) + "|")
        print("|" + " [2] Ligar a geladeira".ljust(len_print1) + "|")
        print("|" + " [3] Desligar a geladeira".ljust(len_print1) + "|")
        print("|" + " [4] Mudar a temperatura da geladeira".ljust(len_print1) + "|")
        print("|" + " [5] Retornar a temperatura da geladeira".ljust(len_print1) + "|")
        print("|" + " [6] Adicionar itens a geladeira".ljust(len_print1) + "|")
        print("|" + " [7] Remover itens da geladeira".ljust(len_print1) + "|")
        print("|" + " [8] Retornar a quantidade de itens da geladeira".ljust(len_print1) + "|")
        print("|" + " [9] Retornar a lista de itens da geladeira".ljust(len_print1) + "|")
        print("|" + " [0] Voltar para o menu da aplicação".ljust(len_print1) + "|")
        print("+" + "-" * len_print1 + "+")

        print("\nDigite a opção desejada: ")
        option = str(input("> "))

        # opção para visualizar os dados da geladeira
        if option == "1":
            view_fridge_device(device_id)

        # opção para ligar a geladeira
        elif option == "2":
            confirm = turn_on_device(device_id)
            print(confirm)

        # opção para desligar a geladeira
        elif option == "3":
            confirm = turn_off_device(device_id)
            print(confirm)

        # opção para mudar a temperatura da geladeira
        elif option == "4":
            print("Digite a nova temperatura: ")
            new_data = float(input("> "))

            confirm = change_data_device(device_id, new_data)
            print(confirm)

        # opção para retornar a temperatura da geladeira
        elif option == "5":
            confirm = receive_data_device(device_id)
            print(confirm)

        # opção para adicionar itens a geladeira
        elif option == "6":
            print("Digite o item que deseja adicionar: ")
            item = str(input("> ")).lower()

            print("Digite a quantidade do item: ")
            quantity = int(input("> "))
            data = f"{item},{quantity}"

            confirm = add_item_device(device_id, data)
            print(confirm)

        # opção para remover itens da geladeira
        elif option == "7":
            print("Digite o item que deseja remover: ")
            item = str(input("> ")).lower()

            print("Digite a quantidade do item: ")
            quantity = int(input("> "))
            data = f"{item},{quantity}"

            confirm = remove_item_device(device_id, data)
            print(confirm)

        # opção para visualizar a quantidade de itens na geladeira
        elif option == "8":
            confirm = view_quantity_device(device_id)
            print(confirm)

        # opção para visualizar os itens da geladeira
        elif option == "9":
            confirm = view_items_device(device_id)
            print(confirm)

        # opção para voltar ao menu da aplicação
        elif option == "0":
            print("Voltando...")
            break

        else:
            print("\nOpção inválida!\n")


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
def view_fridge_device(device_id):
    data = eval(view_data_device(device_id))

    print("+-" + "-" * len_print1 + "-+")
    print("|" + " DADOS DA GELADEIRA".center(len_print1) + "|")
    print("+-" + "-" * len_print1 + "-+")
    print("|" + f"ID: {device_id}".ljust(len_print1) + "|")
    print("|" + f"Status: {data['status']}".ljust(len_print1) + "|")
    print("|" + f"Temperatura: {data['data']}".ljust(len_print1) + "|")
    print("|" + f"Itens: {data['items']}".ljust(len_print1) + "|")
    print("|" + f"Conexão: {data['connected']}".ljust(len_print1) + "|")
    print("+-" + "-" * len_print1 + "-+\n")


# função para visualizar os dados de um dispositivo (1)
def view_data_device(device_id):
    url = f"http://{IP_API}:{PORT_API}/devices/{device_id}/view"
    response = requests.get(url)
    return response.json()


# função para ligar um dispositivo (2)
def turn_on_device(device_id):
    url = f"http://{IP_API}:{PORT_API}/devices/{device_id}/on"
    response = requests.post(url)
    return response.json()


# função para desligar um dispositivo (3)
def turn_off_device(device_id):
    url = f"http://{IP_API}:{PORT_API}/devices/{device_id}/off"
    response = requests.post(url)
    return response.json()


# função para mudar os dados de um dispositivo (4)
def change_data_device(device_id, new_data):
    url = f"http://{IP_API}:{PORT_API}/devices/{device_id}/change/{new_data}"
    response = requests.post(url)
    return response.json()


# função para solicitar o dado de um dispositivo (5)
def receive_data_device(device_id):
    url = f"http://{IP_API}:{PORT_API}/devices/{device_id}/return"
    response = requests.get(url)
    return response.json()


# função para obter todos os dispositivos (-3)
def get_all_devices():
    global dict_devices

    url = f"http://{IP_API}:{PORT_API}/devices"
    response = requests.get(url)
    dict_devices = eval(response.json())

    # verificar se tem itens no dicionário
    if not dict_devices:
        print("Nenhum dispositivo conectado.")
    else:
        for key, value in dict_devices.items():
            print(f"Dispositivo {key}: {value['category']}")
        print("+" + "-" * len_print1 + "+")


# ------------------ funções específicas para a geladeira ------------------ #

# função para adicionar itens a geladeira (6)
def add_item_device(device_id, data):
    url = f"http://{IP_API}:{PORT_API}/devices/{device_id}/add/{data}"
    response = requests.post(url)
    return response.json()


# função para remover itens da geladeira (7)
def remove_item_device(device_id, data):
    url = f"http://{IP_API}:{PORT_API}/devices/{device_id}/remove/{data}"
    response = requests.post(url)
    return response.json()


# função para visualizar a quantidade de itens na geladeira (8)
def view_quantity_device(device_id):
    url = f"http://{IP_API}:{PORT_API}/devices/{device_id}/view/quantity"
    response = requests.get(url)
    return response.json()


# função para visualizar os itens da geladeira (9)
def view_items_device(device_id):
    url = f"http://{IP_API}:{PORT_API}/devices/{device_id}/view/items"
    response = requests.get(url)
    return response.json()


if __name__ == "__main__":
    menu_application()
