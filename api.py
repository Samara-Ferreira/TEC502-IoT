# importação de bibliotecas necessárias
from flask import Flask, jsonify
import broker

HOST = "localhost"
PORT = 5000

# criação de uma aplicação Flask
app = Flask(__name__)

# rota para enviar o comando de ligar um dispositivo
@app.route("/devices/<string:device_id>/ligar", methods=["POST"])
def ligarDevice(device_id):
    return jsonify(broker.receive_command_api(device_id, "1", 0))

# rota para enviar o comando de desligar um dispositivo
@app.route("/devices/<string:device_id>/desligar", methods=["POST"])
def desligarDevice(device_id):
    return jsonify(broker.receive_command_api(device_id, "2", 0))

# rota para enviar o comando de mudar a temperatura de um dispositivo
@app.route("/devices/<string:device_id>/mudar/<float:new_data>", methods=["POST"])
def mudarTemperaturaDevice(device_id, new_data):
    #new_data = request.get_json().get("data")
    return jsonify(broker.receive_command_api(device_id, "3", new_data))

# rota para pegar o dado de um dispositivo específico
@app.route("/devices/<string:device_id>/pegar", methods=["GET"])
def pegarDadosDevice(device_id):
    return jsonify(broker.receive_command_api(device_id, "4", 0))

# rota para enviar o comando de visualizar os dados de um dispositivo específico
@app.route("/devices/<string:device_id>/visualizar", methods=["GET"])
def visualizarDadosDevice(device_id):
    return jsonify(broker.receive_command_api(device_id, "5", 0))

# rota para obter todos os dispositivos
@app.route("/devices", methods=["GET"])
def getDevices():
    return jsonify(broker.receive_command_api("0", "6", 0))


broker.main()

app.run(host=HOST, port=PORT)
