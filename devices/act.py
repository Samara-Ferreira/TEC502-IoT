""" Módulo que contem a classe principal """
import threading

# importação de bibliotecas necessárias
from devices.fridge import Fridge           # isso não funciona lá?
from devices.network import Network         # isso não funciona lá?

import random
import time


class Actuator:
    def __init__(self):
        self.fridge = Fridge()
        self.network = Network()
        self.length_print = 50
        self.length_print2 = 100

    # método para iniciar o programa
    def start(self):
        self.menu_fridge()

    def close(self):
        self.network.disconnect_device()
        self.network.udp_server.close()
        self.fridge.turn_off()
        print(">> Programa encerrado com sucesso!\n")
        time.sleep(1)

    # método para gerar valores randomicos para a temperatura
    def random_data(self):
        if not self.fridge.udp_thread:
            self.fridge.udp_thread = True
            threading.Thread(target=self.network.send_udp, args=[self.fridge.return_data()]).start()

        while self.fridge.random_thread and self.fridge.status:
            self.fridge.change_data(round(random.uniform(-18, 4), 2))
            time.sleep(5)

    def menu_fridge(self):
        while True:
            print(("+" + "-" * self.length_print + "+").center(self.length_print2))
            print(("|" + " MENU DA GELADEIRA".center(self.length_print) + "|").center(self.length_print2))
            print(("+" + "-" * self.length_print + "+").center(self.length_print2))
            print(("|" + " [1] Ligar a geladeira".ljust(self.length_print) + "|").center(self.length_print2))
            print(("|" + " [2] Desligar a geladeira".ljust(self.length_print) + "|").center(self.length_print2))
            print(("|" + " [3] Mudar a temperatura da geladeira".ljust(self.length_print) + "|").center(self.length_print2))
            print(("|" + " [4] Gerar valores randomicos para a temperatura".ljust(self.length_print) + "|").center(self.length_print2))
            print(("|" + " [5] Conectar ao broker".ljust(self.length_print) + "|").center(self.length_print2))
            print(("|" + " [6] Desconectar do broker".ljust(self.length_print) + "|").center(self.length_print2))
            print(("|" + " [7] Alterar nome do dispositivo".ljust(self.length_print) + "|").center(self.length_print2))
            print(("|" + " [0] Encerrar programa".ljust(self.length_print) + "|").center(self.length_print2))
            print(("+" + "-" * self.length_print + "+").center(self.length_print2))

            print("\nEscolha uma opção: ")
            option = str(input("> "))

            if option == "1":
                print(self.fridge.turn_on())

            elif option == "2":
                print(self.fridge.turn_off())

            elif option == "3":
                if not self.fridge.status:
                    print(">> A geladeira está desligada! Ligue a geladeira para mudar a temperatura.\n")
                else:
                    # verificação se o dado é um float, ficar pedindo até que seja um float
                    print("Digite a nova temperatura da geladeira: ")
                    new_data = float(input("> "))

                    while not isinstance(new_data, float):
                        print("Digite a nova temperatura da geladeira: ")
                        new_data = float(input("> "))

                    print(self.fridge.change_data(new_data))

                    # enviar os dados via UDP
                    if not self.fridge.udp_thread:
                        self.fridge.udp_thread = True
                        threading.Thread(target=self.network.send_udp, args=[self.fridge.return_data()]).start()

                    # verificar se a thread para gerar valores randomicos está ativa
                    if self.fridge.random_thread:
                        self.fridge.random_thread = False

            # opção para gerar valores randomicos para a temperatura
            elif option == "4":
                if not self.fridge.status:
                    print(">> A geladeira está desligada! Ligue a geladeira para gerar valores randomicos.\n")

                else:
                    if not self.fridge.random_thread:
                        self.fridge.random_thread = True
                        threading.Thread(target=self.random_data, args=[]).start()

            elif option == "5":
                self.network.connect_broker()

            elif option == "6":
                self.network.disconnect_device()
                self.fridge.turn_off()

            elif option == "7":
                print("Digite o novo nome do dispositivo: ")
                new_name = str(input("> "))
                self.fridge.set_id(new_name)

            elif option == "0":
                self.close()
                break

            else:
                print("Opção inválida! Tente novamente.\n")

    # método para processar os comandos recebidos via API
    def process_commands(self):
        while True:
            try:
                data = self.network.receive_tcp()

                if ":" in data:
                    command, data = data.split(":")

                    # opção para setar o ip da geladeira
                    if command == "-1":
                        self.fridge.set_ip(str(data))

                    # opção para visualizar os dados de um dispositivo
                    elif command == "1":
                        response = self.fridge.return_data()
                        self.network.send_tcp(response)

                    # opção para ligar um dispositivo
                    elif command == "2":
                        response = self.fridge.turn_on()
                        self.network.send_tcp(response)

                    # opção para desligar um dispositivo
                    elif command == "3":
                        response = self.fridge.turn_off()
                        self.network.send_tcp(response)

                    # opção para mudar os dados de um dispositivo
                    elif command == "4":
                        if not self.fridge.status:
                            response = ">> A geladeira está desligada! Ligue a geladeira para mudar a temperatura."
                            self.network.send_tcp(response)
                        else:
                            response = self.fridge.change_data(float(data))

                            if not self.fridge.udp_thread:
                                self.fridge.udp_thread = True
                                threading.Thread(target=self.network.send_udp, args=[self.fridge.return_data()]).start()

                            self.network.send_tcp(response)

                    # opção para retornar os dados de um dispositivo
                    elif command == "5":
                        if not self.fridge.udp_thread:
                            self.fridge.udp_thread = True
                            threading.Thread(target=self.network.send_udp, args=[self.fridge.return_data()]).start()

                        self.network.send_tcp(f"Temperatura atual: {self.fridge.get_data()}ºC")

                    # opção para adicionar itens na geladeira
                    elif command == "6":
                        item, quantity = data.split(",")
                        response = self.fridge.add_item(item, int(quantity))
                        self.network.send_tcp(response)

                    # opção para remover itens da geladeira
                    elif command == "7":
                        item, quantity = data.split(",")
                        response = self.fridge.remove_item(item, int(quantity))
                        self.network.send_tcp(response)

                    # opção para visualizar os itens da geladeira
                    elif command == "8":
                        response = self.fridge.items
                        self.network.send_tcp(str(response))

            except Exception as e:
                print(f"ERRO: não foi possível processar o comando: {e}\n")
                break


# instanciando a classe principal
actuator = Actuator()
actuator.start()
