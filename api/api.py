""" Módulo responsável por criar a API RESTful que irá se comunicar com o broker e com o usuário """

# importação de bibliotecas necessárias
from flask import Flask, jsonify
import server.broker as broker

HOST = "localhost"
PORT = 5000

# criação de uma aplicação Flask
app = Flask(__name__)


# rota para enviar o comando de ligar um dispositivo
@app.route("/devices/<string:device_id>/on", methods=["POST"])
def turn_on(device_id):
    return jsonify(broker.receive_command_api(device_id, "1", 0))


# rota para enviar o comando de desligar um dispositivo
@app.route("/devices/<string:device_id>/off", methods=["POST"])
def turn_off(device_id):
    return jsonify(broker.receive_command_api(device_id, "2", 0))


# rota para enviar o comando de mudar a temperatura de um dispositivo
@app.route("/devices/<string:device_id>/change/<float:new_data>", methods=["POST"])
def change_data(device_id, new_data):
    return jsonify(broker.receive_command_api(device_id, "3", new_data))


# rota para pegar o dado de um dispositivo específico
@app.route("/devices/<string:device_id>/return", methods=["GET"])
def return_data(device_id):
    return jsonify(broker.receive_command_api(device_id, "4", 0))


# rota para enviar o comando de visualizar os dados de um dispositivo específico
@app.route("/devices/<string:device_id>/view", methods=["GET"])
def view_device(device_id):
    return jsonify(broker.receive_command_api(device_id, "5", 0))


# rota para obter todos os dispositivos
@app.route("/devices", methods=["GET"])
def get_devices():
    return jsonify(broker.receive_command_api("0", "0", 0))


# ------------------ rotas específicas para a geladeira ------------------ #

# rota para adicionar itens na geladeira
@app.route("/devices/<string:device_id>/add/<string:item>/<int:quantity>", methods=["POST"])
def add_item(device_id, item, quantity):
    return jsonify(broker.receive_command_api(device_id, "6", [item, quantity]))


# rota para remover itens da geladeira
@app.route("/devices/<string:device_id>/remove/<string:item>", methods=["POST"])
def remove_item(device_id, item):
    return jsonify(broker.receive_command_api(device_id, "7", item))


# rota para visualizar a quantidade de itens na geladeira
@app.route("/devices/<string:device_id>/view/quantity", methods=["GET"])
def view_quantity(device_id):
    return jsonify(broker.receive_command_api(device_id, "8", 0))


# rota para visualizar os itens da geladeira
@app.route("/devices/<string:device_id>/view/items", methods=["GET"])
def view_items(device_id):
    return jsonify(broker.receive_command_api(device_id, "9", 0))


# rota para encerramento da api
@app.route("/shutdown", methods=["POST"])
def shutdown():
    broker.close_broker()
    return "Servidor desligando..."


broker.main()

app.run(host=HOST, port=PORT)
