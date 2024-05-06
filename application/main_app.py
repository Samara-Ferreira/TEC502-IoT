# este módulo importará as funções dos módulos e executará a aplicação

from menu import menu_application

length_print = 50

if __name__ == "__main__":
    print("\n\t+" + "-" * length_print + "+")
    print("\t|" + " INICIANDO A APLICAÇÃO".center(length_print) + "|")
    print("\t+" + "-" * length_print + "+")

    print("\t>> Digite o IP do servidor: ")
    ip_api = str(input("\t> "))

    port_api = "5555"

    menu_application(ip_api, port_api)
