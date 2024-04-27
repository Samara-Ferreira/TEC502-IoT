""" Módulo com as funções específicas para a geladeira """

# código orientado a classe e objetos


# classe para a geladeira
class Fridge:
    # atributo para guardar os dados da geladeira
    def __init__(self, data=0.0, status=False, udp_thread=False, random_thread=False):
        self.ip = None
        self.id = None
        self.data = data
        self.status = status
        self.udp_thread = udp_thread
        self.random_thread = random_thread
        self.items = {}

    # método para setar o ip da geladeira
    def set_ip(self, ip):
        self.ip = ip

    # método para setar o id da geladeira
    def set_id(self, id):
        self.id = id

    # método para ligar a geladeira
    def turn_on(self):
        # verificar se a geladeira já está ligada
        if self.status:
            return ">> A geladeira já está ligada!\n"
        else:
            self.status = True
            return ">> Confirmação: geladeira ligada!\n"

    # método para desligar a geladeira
    def turn_off(self):
        # verificar se a geladeira já está desligada
        if not self.status:
            return ">> A geladeira já está desligada!\n"
        else:
            self.status = False
            self.udp_thread = False
            self.random_thread = False
            return ">> Confirmação: geladeira desligada!\n"

    # método para mudar a temperatura da geladeira
    def change_data(self, new_data):
        self.data = new_data
        return ">> Confirmação: temperatura da geladeira alterada!\n"

    # método para adicionar itens na geladeira
    def add_item(self, item, quantity):
        # verificar se o item já está na geladeira
        if item in self.items:
            self.items[item] += quantity
        else:
            self.items[item] = quantity
        return ">> Confirmação: item adicionado na geladeira!\n"

    # método para remover itens da geladeira
    def remove_item(self, item, quantity):
        # verificar se o item está na geladeira
        if item not in self.items:
            return ">> Erro: item não encontrado na geladeira!\n"
        # verificar se a quantidade do item é maior que a quantidade que deseja remover
        if self.items[item] >= quantity:
            self.items[item] -= quantity
        else:
            return ">> Erro: quantidade do item menor que a quantidade que deseja remover!\n"
        return ">> Confirmação: item removido da geladeira!\n"

    # método para retornar os dados da geladeira
    def return_data(self):
        return f"Temperatura: {self.data}ºC\nStatus: {'Ligada' if self.status else 'Desligada'}\n"

    # método para retornar a temperatura
    def get_data(self):
        return self.data

    # método para retornar os itens da geladeira
    def get_items(self):
        return self.items
