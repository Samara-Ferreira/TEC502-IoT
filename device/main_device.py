# arquivo responsável por interagir com o usuário e chamar
# as funções apropriadas com base na entrada do usuário

# main_device.py
from fridge import *
from connection import connect_broker, disconnect_broker, close_program, check_random_thread
import socket
from clear import clear

HOST = "172.17.0.2"

lenght_print = 50


# menu para a geladeira no terminal do dispositivo
def menu_fridge():
    clear()
    global HOST

    print("\n\t+" + "-" * lenght_print + "+")
    print("\t|" + " Bem-vindo ao menu da geladeira! ".center(lenght_print) + "|")
    print("\t+" + "-" * lenght_print + "+\n")

    ip_device = str(socket.gethostbyname(socket.gethostname()))
    set_fridge_ip(ip_device)

    print("\t>> Digite o IP do broker: ")
    HOST = str(input("\t> "))

    # verificando se o IP é válido
    while HOST == "":
        print("\tERRO: o IP não pode ser vazio!\n")
        print("\t>> Digite o IP do broker: ")
        HOST = str(input("\t> "))

    '''print("\n\tDigite o ID do dispositivo: ")
    fridge_id = str(input("\t> ").upper())'''

    fridge_id = "gel01".upper()

    # verificando se tem 8 caracteres e não é vazio
    while fridge_id == "" or len(fridge_id) > 8:
        print("\tERRO: o ID deve ter no máximo 8 caracteres e não pode ser vazio!\n")
        fridge_id = str(input("\t> "))

    set_fridge_broker_ip(HOST)
    set_fridge_id(fridge_id)

    option = "-1"
    while option != "0":
        sleep(2)
        clear()

        print("\t+" + "-" * lenght_print + "+")
        print("\t|" + " MENU DA GELADEIRA".center(lenght_print) + "|")
        print("\t+" + "-" * lenght_print + "+")
        print("\t|" + " [1] Visualizar os dados da geladeira".ljust(lenght_print) + "|")
        print("\t|" + " [2] Ligar a geladeira".ljust(lenght_print) + "|")
        print("\t|" + " [3] Desligar a geladeira".ljust(lenght_print) + "|")
        print("\t|" + " [4] Mudar a temperatura da geladeira".ljust(lenght_print) + "|")
        print("\t|" + " [5] Gerar valores randomicos para a temperatura".ljust(lenght_print) + "|")
        print("\t|" + " [6] Conectar ao broker".ljust(lenght_print) + "|")
        print("\t|" + " [7] Desconectar do broker".ljust(lenght_print) + "|")
        print("\t|" + " [8] Alterar nome do dispositivo".ljust(lenght_print) + "|")
        print("\t|" + " [0] Encerrar programa".ljust(lenght_print) + "|")
        print("\t+" + "-" * lenght_print + "+")

        print("\n\t>> Digite a opção desejada: ")
        option = str(input("\t> "))

        # opção para visualizar os dados da geladeira
        if option == "1":
            view_data()

        # opção para ligar a geladeira
        elif option == "2":
            if (get_fridge_status()) == "ligada":
                print("\tErro: a geladeira já está ligada!\n")
            else:
                print("\tLigando a geladeira...\n")
                turn_on_fridge()

        # opção para desligar a geladeira
        elif option == "3":
            if get_fridge_status() == "desligada":
                print("\tErro: a geladeira já está desligada!\n")
            else:
                print("\tDesligando a geladeira...\n")
                turn_off_fridge()

        # opção para mudar a temperatura da geladeira
        elif option == "4":
            if get_fridge_status() == "desligada":
                print("\tErro: não é possível modificar a temperatura, pois a geladeira está desligada!\n")
            else:
                print("\tDigite o valor da nova temperatura: ")
                temperature = float(input("\t> "))
                change_temperature(temperature)
                check_random_thread(False)

        # opção para gerar valores randomicos para a temperatura
        elif option == "5":
            if get_fridge_status() == "desligada":
                print("\tErro: não é possível modificar a temperatura, pois a geladeira está desligada!\n")
            else:
                print("\tGerando valores randomicos para a temperatura...\n")
                check_random_thread(True)

        # opção para conectar ao broker
        elif option == "6":
            connect_broker()

        # opção para desconectar do broker
        elif option == "7":
            disconnect_broker()

        # opção para alterar o nome do dispositivo
        elif option == "8":
            print("\tDigite o novo ID do dispositivo: ")
            fridge_id = str(input("\t> "))

            # verificando se tem 8 caracteres e não é vazio
            while fridge["id"] == "" or len(fridge["id"]) > 8:
                print("\tERRO: o ID deve ter no máximo 5 caracteres e não pode ser vazio!\n")
                fridge_id = str(input("\t> "))
            set_fridge_id(fridge_id)

        # opção para encerrar o programa
        elif option == "0":
            close_program()

        else:
            print("\tErro: opção inválida! Tente novamente.\n")


# chamando a função principal
menu_fridge()
