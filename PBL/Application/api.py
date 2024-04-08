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
'''

from flask import Flask, request, jsonify
import serverM

IP_SERVER = "localhost"
HOST = 5001

# criação de uma aplicação Flask
app = Flask(__name__)

# armazenamento dos dispositivos
'''Estrutura
- id (str): identificador do dispositivo
- IP (str): endereço IP do dispositivo -> valor é atualizado quando escolhe um dispositivo
- name (str): nome do dispositivo
- initialized (bool): indica se o dispositivo foi inicializado'''

devices = [{
    "id": "SET01",
    "IP": IP_SERVER,
    "name": "Sensor de temperatura",
    "initialized": True
}]

# rota para obter todos os dispositivos
@app.route("/devices", methods=["GET"])
def getDevices():
    return jsonify(serverM.devicesConnected)

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
    return jsonify(serverM.sendCommandDevice())

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
    return jsonify({"Erro": "dispositivo não encontrado.\n"})


serverM.main()

app.run(port=HOST)




'''

'''

