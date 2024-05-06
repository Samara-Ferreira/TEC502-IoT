# importações necessárias
from time import sleep

# função do menu da aplicação
from clear import clear
from device import view_fridge_device, get_all_devices
from api import (turn_on_device, turn_off_device,
                 change_data_device, receive_data_device, add_item_device,
                 remove_item_device, view_items_device)

# variáveis globais
len_print1 = 50


# função do menu da geladeira
def menu_application(ip_api, port_api):
    option = "-1"
    while option != "0":
        sleep(2)
        clear()
        print("\n\t+" + "-" * len_print1 + "+")
        print("\t|" + " MENU DA APLICAÇÃO".center(len_print1) + "|")
        print("\t+" + "-" * len_print1 + "+")
        print("\t|" + " [1] Selecionar um dispositivo".ljust(len_print1) + "|")
        print("\t|" + " [0] Fechar a aplicação".ljust(len_print1) + "|")
        print("\t+" + "-" * len_print1 + "+")

        print("\n\tDigite o número da opção desejada: ")
        option = str(input("\t> "))

        # opção para selecionar um dispositivo
        if option == "1":
            return_devices = get_all_devices(ip_api, port_api, True)

            if return_devices is not None:
                dict_devices = eval(return_devices)

                print("\n\t>> Digite o IP do dispositivo para acessar o menu: ")
                device_id = str(input("\t> "))

                # verificar se o ID é válido
                while device_id not in dict_devices or device_id == "":
                    if device_id == "0":
                        break
                    get_all_devices(ip_api, port_api, True)
                    print("\n\tIP inválido! Digite novamente: ")
                    device_id = str(input("\t> "))

                if device_id == "0":
                    print("\n\t> Voltando ao menu da aplicação...")
                else:
                    print("\n\tDispositivo selecionado: GELADEIRA")
                    menu_fridge(device_id, ip_api, port_api, dict_devices)

        # opção para fechar a aplicação
        elif option == "0":
            print("\t>> Encerrando aplicação...")
            sleep(1)

        else:
            print("\t> Opção inválida! Tente novamente.\n")


# função do menu da geladeira
def menu_fridge(device_id, ip_api, port_api,  dict_devices):
    option = "-1"

    while option != "0" and dict_devices[device_id]["connection"] != "desconectada":
        sleep(2)
        clear()
        print("\t+" + "-" * len_print1 + "+")
        print("\t|" + " MENU DA GELADEIRA".center(len_print1) + "|")
        print("\t+" + "-" * len_print1 + "+")
        print("\t|" + " [1] Visualizar os dados da geladeira".ljust(len_print1) + "|")
        print("\t|" + " [2] Ligar a geladeira".ljust(len_print1) + "|")
        print("\t|" + " [3] Desligar a geladeira".ljust(len_print1) + "|")
        print("\t|" + " [4] Mudar a temperatura da geladeira".ljust(len_print1) + "|")
        print("\t|" + " [5] Retornar a temperatura da geladeira".ljust(len_print1) + "|")
        print("\t|" + " [6] Adicionar itens a geladeira".ljust(len_print1) + "|")
        print("\t|" + " [7] Remover itens da geladeira".ljust(len_print1) + "|")
        print("\t|" + " [8] Retornar a lista de itens da geladeira".ljust(len_print1) + "|")
        print("\t|" + " [0] Voltar para o menu da aplicação".ljust(len_print1) + "|")
        print("\t+" + "-" * len_print1 + "+")

        if dict_devices[device_id]["connection"] == "desconectada":
            print("\n\t> Dispositivo desconectado! Voltando ao menu da aplicação...")
            option = "0"
        else:
            print("\n\tDigite a opção desejada: ")
            option = str(input("\t> "))

            # como atualizar o dicionário aqui?
            dict_devices = eval(get_all_devices(ip_api, port_api, False))

            if dict_devices[device_id]["connection"] == "desconectada":
                print("\n\t> Dispositivo desconectado! Voltando ao menu da aplicação...")
                option = "0"
            else:
                # opção para visualizar os dados da geladeira
                if option == "1":
                    view_fridge_device(device_id, ip_api, port_api)

                # opção para ligar a geladeira
                elif option == "2":
                    confirm = turn_on_device(device_id, ip_api, port_api)
                    print(confirm)

                # opção para desligar a geladeira
                elif option == "3":
                    confirm = turn_off_device(device_id, ip_api, port_api)
                    print(confirm)

                # opção para mudar a temperatura da geladeira
                elif option == "4":
                    print("\tDigite a nova temperatura: ")
                    new_data = float(input("\t> "))
                    confirm = change_data_device(device_id, new_data, ip_api, port_api)
                    print(confirm)

                # opção para retornar a temperatura da geladeira
                elif option == "5":
                    confirm = receive_data_device(device_id, ip_api, port_api)
                    print(confirm)

                # opção para adicionar itens a geladeira
                elif option == "6":
                    print("\tDigite o item que deseja adicionar: ")
                    item = str(input("\t> ")).lower()
                    print("\tDigite a quantidade do item: ")
                    quantity = int(input("\t> "))

                    data = f"{item},{quantity}"
                    confirm = add_item_device(device_id, data, ip_api, port_api)
                    print(confirm)

                # opção para remover itens da geladeira
                elif option == "7":
                    print("\tDigite o item que deseja remover: ")
                    item = str(input("\t> ")).lower()
                    print("\tDigite a quantidade do item: ")
                    quantity = int(input("\t> "))

                    data = f"{item},{quantity}"
                    confirm = remove_item_device(device_id, data, ip_api, port_api)
                    print(confirm)

                # opção para visualizar os itens da geladeira
                elif option == "8":
                    confirm = view_items_device(device_id, ip_api, port_api)
                    print(confirm)

                # opção para voltar ao menu da aplicação
                elif option == "0":
                    print("\n\t> Voltando para o menu da aplicação...")

                else:
                    print("\n\tOpção inválida!Tente novamente.\n")
