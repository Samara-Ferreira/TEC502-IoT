# módulo conterá todas as funções relacionadas à API


# importações
import requests


# esse arquivo contem todas as funções relacionadas ao dispositivo
# função get_all_devices
def all_devices(ip_api, port_api):
    response = requests.get(f"http://{ip_api}:{port_api}/devices")
    return response.json()


# função para visualizar os dados da geladeira
def view_data_device(device_id, ip_api, port_api):
    response = requests.get(f"http://{ip_api}:{port_api}/devices/{device_id}/view")
    return response.json()


# função para ligar a geladeira
def turn_on_device(device_id, ip_api, port_api):
    response = requests.post(f"http://{ip_api}:{port_api}/devices/{device_id}/on")
    return response.json()


# função para desligar a geladeira
def turn_off_device(device_id, ip_api, port_api):
    response = requests.post(f"http://{ip_api}:{port_api}/devices/{device_id}/off")
    return response.json()


# função para mudar os dados da geladeira
def change_data_device(device_id, new_data, ip_api, port_api):
    response = requests.post(f"http://{ip_api}:{port_api}/devices/{device_id}/change/{new_data}")
    return response.json()


# função para retornar os dados da geladeira
def receive_data_device(device_id, ip_api, port_api):
    response = requests.get(f"http://{ip_api}:{port_api}/devices/{device_id}/return")
    return response.json()


# função para adicionar itens na geladeira
def add_item_device(device_id, data, ip_api, port_api):
    response = requests.post(f"http://{ip_api}:{port_api}/devices/{device_id}/add/{data}")
    return response.json()


# função para remover itens da geladeira
def remove_item_device(device_id, data, ip_api, port_api):
    response = requests.post(f"http://{ip_api}:{port_api}/devices/{device_id}/remove/{data}")
    return response.json()


# função para visualizar os itens da geladeira
def view_items_device(device_id, ip_api, port_api):
    response = requests.get(f"http://{ip_api}:{port_api}/devices/{device_id}/view_items")
    return response.json()
