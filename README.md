# Descrição do Projeto

# Arquitetura de Solução 

A arquitetura do projetpo foi desenvolvida no intuito de permitir a comunicação entre dispositivos, aplicação e um 
servidor broker. Dessa forma, é possível que a aplicação envie comandos para os dispositivos, que por sua vez, enviam
respostas para a aplicação, por meio de um intermediário, o servidor broker. A arquitetura do projeto é composta por
três módulos principais: 'application', 'device' e 'server'. Cada um desses módulos é responsável por uma parte da
comunicação. A seguir, são apresentadas as funcionalidades de cada um dos módulos.

### Módulo 'Application'

O módulo 'application' é responsável por enviar comandos para os dispositivos e receber as respostas dos dispositivos,
ou seja, tratam da lógica do cliente da aplicação. Para isso, a aplicação é composta por uma interface CLI 
(Command Line Interface) -- um tipo de interface de usuário que permite a interação com o sistema por meio de 
comandos de texto --, que permite ao usuário enviar comandos para os dispositivos. Há a interação com a API REST
para controlar os dispositivos.

A aplicação é composta pelos seguintes arquivos:
- `application/main_app.py`: este arquivo principal da aplicação. É o ponto de entrada da aplicação, fazendo a 
solicitação ao usuário do IP do servidor, e então chama a função menu_application(), no arquivo `menu.py`, que exibe
o menu de opções da aplicação;
- `application/menu.py`: este arquivo contém a lógica do menu da aplicação. Ele apresenta as opções de comandos que
podem ser enviados para os dispositivos, como visualizar os dispositivos conectados, ligar ou desligar um dispositivo,
entre outros;
- `application/device.py`: este arquivo contém as funções relacionadas ao dispositivo, como a função de visualizar os
dispositivos conectados e os dados de um dispositivo específico;
- `application/api.py`: este arquivo contém as funções que interagem com a API REST para o controle dos dispositivos.
Ele tem funções para obter todos os dispositivos conectados, ligar um dispositivo, desligar um dispositivo, entre 
outros; 

A aplicação é composta por um arquivo `main_app.py`, que é responsável por inicializar a aplicação e estabelecer a
comunicação com o servidor broker. Além disso, a aplicação é composta por um arquivo `menu.py`, que é responsável por
exibir o menu de opções da aplicação e permitir ao usuário enviar comandos para os dispositivos. Um outro arquivo
é o `device.py`, que é responsável por conter as funções relacionadas ao dispositivo, como a função de visualizar
os dispositivos conectados. Por fim, o arquivo `api.py` contem as funções relacionadas à comunicação com a API do
servidor broker (REST). 

### Módulo 'Device'

O módulo 'device' é responsável por lidar com as operações e funcionalidades do dispositivo. O dispositivo é capaz 
de receber comandos da aplicação, de forma remota, processá-los e enviar respostas para a aplicação, por meio do 
servidor broker. 

Além disso, o dispositivo possui sua própria interface CLI, que permite ao usuário enviar comandos para o 
dispositivo, fazer o processamento deles e retornar as respostas, sem a necessidade de passar pelo intermediário, o
servidor broker. 

O dispositivo é composto pelos seguintes arquivos:
- `connection.py`: este arquivo lida com as conexões TCP e UDP, que são utilizadas para a comunicação entre o
dispositivo e o servidor broker, incluindo o envio e o recebimento de mensagens;
- `device/fridge.py`: este arquivo mantém o estado e as operações do dispositivo (geladeira), como ligar, desligar,
adicionar itens, remover itens, entre outros;
- `device/main_device.py`: este arquivo principal do dispositivo. É o ponto de entrada do dispositivo, fazendo a
solicitação ao usuário do IP do servidor, e então chama a função menu_fridge(), que exibe o menu de opções do
dispositivo;


### Módulo 'Server'

O módulo 'server' é responsável por intermediar a comunicação entre a aplicação e os dispositivos. O servidor broker
é responsável por receber as mensagens da aplicação, encaminhá-las para os dispositivos, receber as respostas dos
dispositivos e encaminhá-las para a aplicação. Ele é responsável por receber a conexão dos dispositivos.

O servidor broker é composto pelos seguintes arquivos:
- `server/main_api.py`: este arquivo principal do servidor broker. Ele é responsável por criar a API REST que se 
comunica com o broker e com o usuário. Ele usa o FLask, um microframework web em Python, para criar as rotas que
podem ser acessadas para interagir com os dispositivos;
- `server/broker.py`: este arquivo lida com a criação do servidor broker, que é responsável por intermediar a 
comunicação entre a aplicação e os dispositivos;
- `server/broker_connections.py`: este arquivo lida com as conexões dos dispositivos, incluindo o envio e o recebimento
de mensagens, e a manutenção das conexões ativas;


# Protocolos de Comunicação 

## Camada de Aplicação 

## Camada de Transporte 

# Interface de Aplicação (REST)

A interface de aplicação do projeto foi desenvolvida utilizando o protocolo REST (Representational State Transfer),
que é um estilo de arquitetura de software que define um conjunto de restrições para a criação de serviços web. 

Essa aplicação é baseada em requisições HTTP, que são feitas a partir de um cliente (neste caso, a aplicação) para o 
servidor broker. As requisições do projeto são feitas a partir dos métodos HTTP, POST e GET, que são utilizados para
enviar e receber dados, respectivamente. 

A tabela a seguir apresenta as rotas da API REST do projeto, bem como os métodos HTTP utilizados e a descrição de cada
rota:

| Rota                           | Método HTTP | Descrição                                                   |
|--------------------------------|-------------|-------------------------------------------------------------|
| /devices                       | GET         | Retorna todos os dispositivos conectados ao servidor broker |
| /{device_id}/view              | GET         | Retorna os dados de um dispositivo específico               |
| /{device_id}/on                | POST        | Liga um dispositivo específico                              |
| /{device_id}/off               | POST        | Desliga um dispositivo específico                           |
| /{device_id}/change/{new_data} | POST        | Altera os dados de um dispositivo específico                |
| /{device_id}/return            | GET         | Recebe os dados de um dispositivo específico                |
| /{device_id}/add/{data}        | POST        | Adiciona itens a um dispositivo específico                  |
| /{device_id}/remove/{data}     | POST        | Remove itens de um dispositivo específico                   |
| /{device_id}/view_items        | GET         | Retorna os itens de um dispositivo específico               |

Cada função retorna um JSON com os dados solicitados. A seguir, são apresentados exemplos de requisições para cada 
uma das rotas da API REST do projeto apresentadas, usando o Insomnia:

![get_devices](images/get_devices.png)

...




# Transmissão dos Dados 

# Conexões Simultâneas 

# Dispositivo 

# Desempenho 

# Confiabilidade 

# Documentação do Código 

# Docker 

# Execução do Projeto

O projeto pode ser executado de duas formas: com o Docker ou sem o Docker. A execução com o Docker é mais simples, 
pois não é necessário instalar as dependências do projeto na máquina. Já a execução sem o Docker requer a instalação 
das dependências do projeto na máquina. Entretando, a execução com o Docker requer que o Docker esteja instalado na
máquina.

Para a execução do projeto, caso tenha o Git instalado em sua máquina, é necessário clonar o repositório através 
do link <link> e acessar os diretórios de cada um dos módulos do projeto. 

Caso não tenha o Git instalado em sua máquina, é possível baixar o projeto em formato zip através do link ```<link>```, e 
descompactar o arquivo baixado. Em seguida, acesse os diretórios de cada um dos módulos do projeto.

Para fins de organização, o projeto foi dividido em três módulos principais: 'application', 'device' e 'server'. Cada
um desses módulos foram explicaods em detalhes na seção 'Arquitetura de Solução'. 

A seguir, são apresentadas as instruções para a execução do projeto com e sem o Docker.

### Execução sem o Docker 

##### Pré-requisitos 

Para a execução do projeto sem o Docker, é necessário ter instalados na máquina as seguintes ferramentas:
- Python 3.8 ou superior;
- Pip, para instalação das dependências do projeto;
- Bibliotecas do Python, como a Flask e a requests, listadas no arquivo `requirements.txt` dos módulos 'application' 
e 'server';

##### Instalação das Dependências

Para instalar as dependências do projeto, acesse o diretório de cada um dos módulos do projeto e execute o seguinte
comando:

```pip install -r requirements.txt```

Ou pode instalar as dependências manualmente, através dos comandos:

```pip install Flask```

```pip install requests```

##### Execução dos Módulos

Para a execução dos módulos, é necessário navegar por cada um dos diretórios dos módulos e executar o arquivo
`main.py` de cada um deles, sendo:
- No módulo 'application', execute o comando `python main_app.py`;
- No módulo 'device', execute o comando `python main_device.py`;
- No módulo 'server', execute o comando `python main_api.py`.

Após a execução dos comandos, os módulos estarão em execução. Para a comunicação entre os módulos, é necessário que
o usuário atente-se ao pedido do ip do broker, que é solicitado ao inicializar a aplicação e ao conectar um dispositivo
ao servidor. Esse ip pode ser visualizado assim que o servidor é inicializado, como pode ser visualizado na imagem
a seguir e é necessário que o usuário insira esse ip manualmente na aplicaçção e no dispositivo, para que a 
comunicação entre eles seja estabelecida.

![init_broker](images/init_broker.png)

![init_device](images/init_device.png)

![init_app](images/init_app.png)


### Execução com o Docker

Para a execução do projeto com o Docker, é necessário que o Docker esteja instalado na máquina. Supondo que o Docker
esteja instalado, acesse o diretório de cada um dos módulos do projeto e execute o seguinte comando:

```docker build -t <nome_da_imagem> .```

Onde `<nome_da_imagem>` é o nome que será dado à imagem do módulo. Para os módulos 'application', 'device' e 'server',
tem-se os seguintes comandos:

```docker build -t application .```
    
```docker build -t device .```
    
```docker build -t server .```

Após a execução do comando, a imagem do módulo será criada. Em seguida, execute o seguinte comando para a execução
do container:

```docker run -p port:port -iti <nome_da_imagem>```

Onde `port` é a porta que será utilizada para a comunicação entre o container e a máquina host. Tendo isso em 
mente, a execução do container para o módulo 'application' é:

```docker run -p 5555:5555 -iti application```

Para o módulo 'device', é:

```docker run -p 5551:5551 -p 5552:5552/udp -iti device```

E para o módulo 'server', é:

```docker run -p 5555:5555 -p 5551:5551 -p 5552:5552/udp -iti server```

Após a execução dos comandos, os módulos estarão em execução. Para a comunicação entre os módulos, é necessário que
o usuário atente-se ao pedido do ip do broker, que é solicitado ao inicializar a aplicação e ao conectar um dispositivo
ao servidor. Esse ip pode ser visualizado assim que o servidor é inicializado, como pode ser visualizado na imagem 
acima, que apresenta a execução do servidor. É necessário que o usuário insira esse ip manualmente na aplicação e no
dispositivo, para que a comunicação entre eles seja estabelecida.

# Conclusão 

# Referências



