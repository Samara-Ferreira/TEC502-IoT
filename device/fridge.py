""" Este arquivo é responsável por manter o estado e as operações da geladeira, fazendo as modificações dos dados e
recuperação deles, quando necessário """

# importações das bibliotecas necessárias
from time import sleep
import random

# dicionário que guarda os dados da geladeira
fridge = {
    "ip": 0,
    "ip_broker": 0,
    "id": 0,
    "temperature": 0.0,
    "category": "atuador",
    "items": {},
    "status": "desligada",
    "connection": "desconectada",
    "udp_thread": False,
    "random_thread": False,
}

length_print = 50


# ------------- funções SET do dispositivo ------------- #
# função para setar o ip da geladeira
def set_fridge_ip(ip):
    fridge["ip"] = ip


# função para setar o ip do broker da geladeira
def set_fridge_broker_ip(ip_broker):
    fridge["ip_broker"] = ip_broker


# função para setar o id da geladeira
def set_fridge_id(id):
    fridge["id"] = id


# função para setar o estado de conexão da geladeira
def set_fridge_connection_status(status):
    fridge["connection"] = status


# função para setar o status da thread udp
def set_udp_thread_status(status):
    fridge["udp_thread"] = status


# função para setar o status da thread de valores randomicos
def set_random_thread_status(status):
    fridge["random_thread"] = status


# ------------- funções GET do dispositivo ------------- #
# função para obter o status da conexão da geladeira
def get_fridge_connection_status():
    return fridge["connection"]


# função para obter o status da thread udp
def get_udp_thread_status():
    return fridge["udp_thread"]


# função para obter o status da geladeira
def get_fridge_status():
    return fridge["status"]


# função para obter os itens da geladeira
def get_fridge_items():
    return fridge["items"]


# função para obter o status da thread udp
def get_udp_thread_status():
    return fridge["udp_thread"]


# função para obter o status da thread de valores randomicos
def get_random_thread_status():
    return fridge["random_thread"]


# função para obter os dados da geladeira
def get_fridge_data():
    return fridge


# função para obter o status da geladeira
def get_fridge_status():
    return fridge["status"]


# função para obter o ip do servidor broker
def get_fridge_ip_broker():
    return fridge["ip_broker"]


# função para obter a temperatura da geladeira
def get_fridge_temperature():
    return fridge["temperature"]


# ------------- funções normais do dispositivo ------------- #

# função para gerar os valores randomicos
def random_temperature():
    # caso da geladeira esteja desligada
    if fridge["status"] == "desligada":
        return "\tErro: não é possível modificar a temperatura, pois a geladeira está desligada!\n"
    # caso a geladeira esteja ligada
    else:
        while fridge["status"] == "ligada" and fridge["random_thread"] is True:
            change_temperature(round(random.uniform(-18, 4), 2))
            sleep(2)


# função para ligar a geladeira
def turn_on_fridge():
    fridge["status"] = "ligada"


# função para desligar a geladeira
def turn_off_fridge():
    fridge["status"] = "desligada"
    fridge["temperature"] = 0.0
    fridge["items"] = {}
    fridge["random_thread"] = False
    fridge["udp_thread"] = False


# função para mudar a temperatura da geladeira
def change_temperature(new_temperature):
    fridge["temperature"] = new_temperature


# função para adicionar os itens na geladeira
def add_item(item, quantity):
    if item in fridge["items"]:
        fridge["items"][item] += quantity
        return "\tConfirmação: item encontrado e quantidade atualizada!\n"
    else:
        fridge["items"][item] = quantity
        return "\tConfirmação: item adicionado!\n"


def remove_item(item, quantity):
    if item not in fridge["items"]:
        return "\tErro: item não encontrado!\n"
    elif fridge["items"][item] < quantity:
        return "\tErro: quantidade insuficiente!\n"
    else:
        fridge["items"][item] -= quantity
        if fridge["items"][item] == 0:
            del fridge["items"][item]
        return "\tConfirmação: item removido!\n"


# função para visualizar os dados da geladeira
def view_data():
    print("\n\t+" + "-" * length_print + "+")
    print("\t| " + " DADOS DA GELADEIRA".center(length_print) + "|")
    print("\t+" + "-" * length_print + "+")
    print("\t| " + f"IP: {fridge['ip']}".ljust(length_print) + "|")
    print("\t| " + f"IP Broker: {fridge['ip_broker']}".ljust(length_print) + "|")
    print("\t| " + f"ID: {fridge['id']}".ljust(length_print) + "|")
    print("\t| " + f"Temperatura: {fridge['temperature']}ºC".ljust(length_print) + "|")
    print("\t| " + f"Status: {fridge['status']}".ljust(length_print) + "|")
    print("\t| " + f"Categoria: {fridge['category']}".ljust(length_print) + "|")
    print("\t| " + f"Conexão: {fridge['connection']}".ljust(length_print) + "|")
    print("\t| " + f"Itens: {fridge['items']}".ljust(length_print) + "|")
    print("\t+" + "-" * length_print + "+\n")
