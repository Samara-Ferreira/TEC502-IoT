'''
SOBRE A API
- API (Application Programming Interface) é um conjunto de regras e padrões que 
permite a comunicação entre aplicações
- Objetivo dessa API: permitir a troca de mensagens entre dispositivos e aplicações
- URL base: localhost
- Endpoints:
    - localhost/devices (GET)                | Obter todos os dispositivos
    - localhost/devices (POST)               | Criar dispositivo
    - localhost/devices/devicesId (GET)      | Encontrar um dispositivo para enviar mensagem
    - localhost/devices/devicesI (DELETE) | Excluir um dispositivo
- Recursos:
    - Dispositivos

SOBRE OS DISPOSITIVOS
- Cada dispositivo possui:
    - id
    - nome
    - status (ligado ou desligado)
- Operações:
    - ligar o dispositivo
    - desligar o dispositivo
    - enviar mensagem
- Exemplos de dispositivos:
    - lâmpada
    - sensor de temperatura
    - sensor de presença
    - câmera
    - alarme

EXEMPLO DE UM DISPOSITIVO   
- Sensor de temperatura
    - id: 1
    - nome: Sensor de temperatura
    - status: on
- Operações do dispositivo:
    - ligar o sensor
    - desligar o sensor
    - solicitar a temperatura
    - pausar?
'''


from flask import Flask, request, jsonify

# criação de uma aplicação Flask
app = Flask(__name__)

# armazenamento dos dispositivos
devices = [{
    "id": 1,
    "name": "Device 1",
    "status": "on"
}, {
    "id": 2,
    "name": "Device 2",
    "status": "off"
}]

# rota para obter todos os dispositivos
@app.route('/devices', methods=['GET'])
def getDevices():
    return jsonify(devices)

# rota para criar um dispositivo
@app.route('/devices', methods=['POST'])
def createDevice(): 
    new_device = request.get_json()
    # verifica se o dispositivo já existe
    for device in devices:
        if device.get('id') == new_device.get('id'):
            return jsonify({'error': 'Device already exists'})
    devices.append(new_device)
    return jsonify(devices)

# rota para encontrar um dispositivo
@app.route('/devices/<int:device_id>', methods=['GET'])
def getDevice(device_id):
    for device in devices:
        if device.get('id') == device_id:
            return jsonify(device)
    return jsonify({'error': 'Device not found'})

# rota para excluir um dispositivo
@app.route('/devices/<int:device_id>', methods=['DELETE'])
def deleteDevice(device_id):
    for device in devices:
        if device.get('id') == device_id:
            devices.remove(device)
            return jsonify({'message': 'Device deleted'})
    return jsonify({'error': 'Device not found'})



'''# rota para ligar um dispositivo
@app.route('/devices/<int:device_id>/on', methods=['POST'])
def turn_on_device(device_id):
    for device in devices:
        if device.get('id') == device_id:
            device['status'] = 'on'
            return jsonify(device)
    return jsonify({'error': 'Device not found'})

# rota para desligar um dispositivo
@app.route('/devices/<int:device_id>/off', methods=['POST'])
def turn_off_device(device_id):
    for device in devices:
        if device.get('id') == device_id:
            device['status'] = 'off'
            return jsonify(device)
    return jsonify({'error': 'Device not found'})

# rota para enviar mensagem para um dispositivo
@app.route('/devices/<int:device_id>/message', methods=['POST'])
def send_message(device_id):
    message = request.get_json()
    for device in devices:
        if device.get('id') == device_id:
            return jsonify({'message': message})
    return jsonify({'error': 'Device not found'})
'''


# execução da aplicação
app.run(port=5000, host='localhost',debug=True)
