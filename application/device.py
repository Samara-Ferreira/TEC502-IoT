""" Este aquivo é responsável por conter as funções relacionadas ao dispositivo, como a visualização dos dados da
geladeira e a obtenção de todos os dispositivos conectados. """

# importação de bibliotecas
from time import sleep
from api import view_data_device, all_devices

# variáveis globais
len_print1 = 50


# função para visualizar os dados da geladeira
def view_fridge_device(device_id, ip_api, port_api):
    # obtendo os dados do dispositivo
    data = view_data_device(device_id, ip_api, port_api)
    # verificando se há dados
    if data:
        data = eval(view_data_device(device_id, ip_api, port_api))
        print("\t+-" + "-" * len_print1 + "-+")
        print("\t|" + " DADOS DA GELADEIRA".center(len_print1) + "|")
        print("\t+-" + "-" * len_print1 + "-+")
        print("\t|" + f"ID: {device_id}".ljust(len_print1) + "|")
        print("\t|" + f"Status: {data['status']}".ljust(len_print1) + "|")
        print("\t|" + f"Temperatura: {data['temperature']}".ljust(len_print1) + "|")
        print("\t|" + f"Itens: {data['items']}".ljust(len_print1) + "|")
        print("\t|" + f"Conexão: {data['connection']}".ljust(len_print1) + "|")
        print("\t+-" + "-" * len_print1 + "-+\n")
        sleep(2)
    # caso não haja dados
    else:
        print("\n\tNão tem dispositivo conectado!\n")


# função para obter todos os dispositivos conectados
def get_all_devices(ip_api, port_api):
    response = all_devices(ip_api, port_api)
    # verificando se há dispositivos conectados
    if response == "None":
        print("\n\t> Nenhum dispositivo conectado!\n")
        return None
    # caso haja dispositivos conectados
    else:
        return response
