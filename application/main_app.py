""" Este arquivo é o ponto de entrada da aplicação, no qual é importado as funções dos módulos e executado a
aplicação. """

# importações das funções dos módulos
from menu import menu_application
from clear import clear

length_print = 50

# execução da aplicação
if __name__ == "__main__":
    clear()

    print("\n\t+" + "-" * length_print + "+")
    print("\t|" + " INICIANDO A APLICAÇÃO".center(length_print) + "|")
    print("\t+" + "-" * length_print + "+")

    print("\t>> Digite o IP do servidor: ")
    ip_api = str(input("\t> ")).strip()

    port_api = 5575

    menu_application(ip_api, port_api)
