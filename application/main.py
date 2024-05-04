# este módulo importará as funções dos módulos e executará a aplicação

from menu import menu_application

if __name__ == "__main__":
    print("\n\t>> Iniciando aplicação...")
    '''print("\t>> Digite o IP do servidor: ")
    ip_api = str(input("\t> "))'''
    ip_api = "192.168.0.111"

    '''print("\t>> Digite a porta do servidor: ")
    port_api = str(input("\t> "))'''
    port_api = "5555"

    menu_application(ip_api, port_api)
