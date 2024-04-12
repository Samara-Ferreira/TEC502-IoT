import requests


# enviar comandos para o servidor serverM.py


# dados recebidos do servidor serverM.py
response = requests.get('http://localhost:5000/devices')
print(f"\nResposta do servidor: {response.text}\n")
print(f"\nStatus da resposta: {response.status_code}\n")
print(f"\nDispositivos: {response.json()}\n")
print(f"\nTipo da resposta: {type(response)}\n")
print(f"\nTipo de requisição: {type(response.json())}\n")

