'''
DESCRIÇÃO 
- a aplicação fará conexão com o servidor, para enviar comandos aos dispositivos
- a aplicação os dados dos dispositivos 
- a comunicação entre a aplicação e o servidor será via HTTP
- categoria dos dispositivos:
    - sensor de temperatura (ST1)
    - sensor de umidade (SU1)
    - sensor de presença (SP1)
    - lâmpada   (L1)
    - câmera    (C1)
    - alarme    (A1)
- fazer o codigo com classe e objeto para a aplicação
'''

# importação de bibliotecas necessárias
from flask import Flask, request, jsonify
import broker

IP_SERVER = "localhost"
PORT = 5000

# criação de uma aplicação Flask
app = Flask(__name__)

# armazenamento dos dispositivos
'''Estrutura
- id (str): identificador do dispositivo
- IP (str): endereço IP do dispositivo -> valor é atualizado quando escolhe um dispositivo
- name (str): nome do dispositivo
- initialized (bool): indica se o dispositivo foi inicializado'''

"""CERTO 
devices = [{
    "id": "SET01",
    "ip": IP_SERVER,
    "tipo de dispositivo": "Sensor de temperatura",
    "status": True
}]"""

'''# provisorio...
devicesDict = {, 

                "IP2": {"id": "GEL01",
                        "number": 0,
                        "data": 0,
                        "categoria": "atuador",
                        "status": False}} '''

ipDevices = []

#------------------------------------------------

# rota para enviar o comando de ligar um dispositivo
@app.route("/devices/<string:device_id>/ligar", methods=["POST"])
def ligarDevice(device_id):
    return jsonify(broker.sendCommandTCP(device_id, "1", 0))

# rota para enviar o comando de desligar um dispositivo
@app.route("/devices/<string:device_id>/desligar", methods=["POST"])
def desligarDevice(device_id):
    return jsonify(broker.sendCommandTCP(device_id, "2", 0))

# rota para enviar o comando de mudar a temperatura de um dispositivo
@app.route("/devices/<string:device_id>/mudar/<int:new_data>", methods=["POST"])
def mudarTemperaturaDevice(device_id, new_data):
    #new_data = request.get_json().get("data")
    return jsonify(broker.sendCommandTCP(device_id, "3", new_data))

# rota para enviar o comando de visualizar os dados de um dispositivo
@app.route("/devices/<string:device_id>/visualizarDados", methods=["GET"])
def visualizarDadosDevice(device_id):
    return jsonify(broker.sendCommandTCP(device_id, "4", 0))


#------------------------------------------------

'''# rota para obter todos os dispositivos
@app.route("/devices", methods=["GET"])
def getDevices():
    #return jsonify(broker.devicesConnected)
    return jsonify(broker.sendCommandTCP())

# rota para criar um dispositivo
@app.route("/devices", methods=["POST"])
def createDevice(): 
    new_device = request.get_json()

    # verifica se o dispositivo já existe
    for device in devices:
        if device.get("id") == new_device.get("id"):
            return jsonify({"Erro": "dispositivo já existe.\n"})
        
    devices.append(new_device)
    return jsonify(devices)

# rota para encontrar um dispositivo
@app.route("/devices/<string:device_id>", methods=["GET"])
def getDevice(device_id):
    """for device in devices:
        if device.get("id") == device_id:
            return jsonify(device)"""
    return jsonify(broker.sendCommandDevice())

# rota para atualizar o IP do dispositivo
@app.route("/devices/<string:device_id>", methods=["PUT"])
def updateDeviceIP(server_id):
    new_ip = request.get_json().get("IP") # tem q vir do servidor
    for device in devices:
        if device.get("id") == server_id:
            device["IP"] = new_ip
            return jsonify(device)
    return jsonify({"Erro": "dispositivo não encontrado.\n"})

# rota para excluir um dispositivo
@app.route("/devices/<string:device_id>", methods=["DELETE"])
def deleteDevice(device_id):
    for device in devices:
        if device.get("id") == device_id:
            devices.remove(device)
            return jsonify({"Mensagem: dispositivo deletado.\n"})
    return jsonify({"Erro": "dispositivo não encontrado.\n"})'''


broker.main()

app.run(port=PORT)

