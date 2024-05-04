# arquivo responsável por manter o estado e as operações da geladeira

import random

from time import sleep

# estado da geladeira: adiciono umidade??
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
    "random_thread": False
}

length_print = 50


def set_fridge_ip(ip):
    fridge["ip"] = ip


def set_fridge_broker_ip(ip_broker):
    fridge["ip_broker"] = ip_broker


def set_fridge_id(id):
    fridge["id"] = id


def set_fridge_connection_status(status):
    fridge["connection"] = status


def set_udp_thread_status(status):
    fridge["udp_thread"] = status


def set_random_thread_status(status):
    fridge["random_thread"] = status


def get_fridge_connection_status():
    return fridge["connection"]


def get_udp_thread_status():
    return fridge["udp_thread"]


def get_fridge_status():
    return fridge["status"]


def get_fridge_items():
    return fridge["items"]


def get_udp_thread_status():
    return fridge["udp_thread"]


def get_random_thread_status():
    return fridge["random_thread"]

# --------- funções get para quando for solicitada pela aplicação --------- #


def get_fridge_data():
    return fridge


def get_fridge_status():
    return fridge["status"]


def get_fridge_ip_broker():
    return fridge["ip_broker"]


def get_fridge_temperature():
    return fridge["temperature"]


# ---------  ---------   ---------   ---------#

def random_temperature():
    if fridge["status"] == "desligada":
        return "\tErro: não é possível modificar a temperatura, pois a geladeira está desligada!\n"
    else:
        while fridge["status"] == "ligada" and fridge["random_thread"] is True:
            change_temperature(round(random.uniform(-18, 4), 2))
            sleep(3)


def turn_on_fridge():
    fridge["status"] = "ligada"


def turn_off_fridge():
    fridge["status"] = "desligada"
    fridge["temperature"] = 0.0
    fridge["items"] = {}
    fridge["random_thread"] = False
    fridge["udp_thread"] = False


def get_temperature():
    return fridge["temperature"]


def change_temperature(new_temperature):
    fridge["temperature"] = new_temperature


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
