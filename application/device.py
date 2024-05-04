from time import sleep
from api import view_data_device, all_devices

# variáveis globais
len_print1 = 50


# função para visualizar os dados da geladeira
def view_fridge_device(device_id, ip_api, port_api):
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


def get_all_devices(ip_api, port_api):
    response = all_devices(ip_api, port_api)
    if response == "None":
        print("\n\t> Nenhum dispositivo conectado!\n")
        return None
    else:
        dict_devices = eval(response)
        print("\n\t+-" + "-" * len_print1 + "-+")
        print("\t|" + " DISPOSITIVOS CONECTADOS".center(len_print1) + "|")
        for device in dict_devices:
            print("\t+-" + "-" * len_print1 + "-+")
            print(f"\t|ID: {device}".ljust(len_print1) + "|")
            print(f"\t|Categoria: {dict_devices[device]['category']}".ljust(len_print1) + "|")
            print(f"\t|Conexão: {dict_devices[device]['connection']}".ljust(len_print1) + "|")
        return response
