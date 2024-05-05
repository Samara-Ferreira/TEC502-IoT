# PBL-Redes
Projeto de PBL da disciplina MI - Concorrência e Conectividade.


# Tópicos de acordo com o barema

### Arquitetura da solução (componentes e mensagens)
- como a arquitetura foi desenvolvida
- quais os componentes e como eles se comunicam 
- qual a ordem das mensagens trocadas

#### Protocolo de comunicação entre dispositivo e Broker (camada de aplicação)
- que protocolos de comunicação foram desenvolvidos entre os disposisitivos e o Broker
- como é a "conversa" entre os disposisiitivos e o Broker

#### Protocolo de comunicação entre dispositivo e Broker (camada de transporte)
- que protocolos de comunicação foram utilizados entre os disposisitivos e o Broker
- tcp, udp?
- em quais situações e por que?

#### Interface da aplicação (REST)
- quais sao os verbos e rotas executados na camada de aplicação

#### Formatação, envio e tratamento de dados
- que tipo de formatação foi usada para transmitir os dados, permitindo que nós diferentes compreendam as mensagens trocadas

#### Tratamento de conexões simultâneas (threads)
- como threads foram usadas para tornar o sistema mais eficiente?
- há problemas de concorrência decorrente do uso de threads?
- se sim, como estas questões foram tratadas?

#### Gerenciamento do dispositivo
- é possível gerenciar o dispositivo (parar, alterar valores, etc)?
- isso pode ser feito remotamente?
- e via interface do próprio dispositivo?

#### Desempenho (uso de cache no Broker, filas, threads, etc.)
- o sistema utiliza algum mecanismo para melhorar o tempo de resposta para a aplicação?

#### Confiabilidade de solução (tratamento de conexões)
- tirando e recolocando o cabo de rede de algum dos nós, o sistema continua funcionando?
- TESTAR

#### Documentação do código 

#### Emprego do Docker


## Arquitetura da Solução

A arquitetura da solução foi desenvolvida de forma a permitir a comunicação entre 
dispositivos e o broker, de forma que os dispositivos possam enviar mensagens para o 
broker e o broker possa enviar mensagens para os dispositivos. A arquitetura foi 
desenvolvida em Python, versão 3.12, cuja a comunicação entre os dispositivos e o 
broker é feita através de sockets TCP/IP, e a comunicação entre a aplicação e o broker 
é feita através de requisições HTTP. 

### Componentes
Os principais componentes da arquitetura são:

- Dispositivo (geladeira): este componente tem várias funcionalidades, como enviar 
mensagens para o broker, receber mensagens do broker, e executar ações de acordo com 
as mensagens recebidas, como ligar e desligar a geladeira, alterar a temperatura, etc.

- Broker: este componente é responsável por receber mensagens dos dispositivos, armazenar as mensagens em uma fila
(tentativa de implementação), e enviar as mensagens para a aplicação. No momento, os dados são armazenados em uma 
lista de mensagens, e a aplicação acessa diretamente esta lista para obter as mensagens, sendo que a posição da mensagem
na lista é utilizada como identificador da mensagem, sendo a primeira mensagem enviada via TCP/IP e a segunda via UDP.

- Aplicação: este componente é responsável por enviar as mensagens ao broker, e exibir as mensagens recebidas do broker.
Ele faz isso através de requisições HTTP, utilizando o método POST para enviar mensagens ao broker, e o método GET para
obter as mensagens do broker.

- Threads: foram utilizadas threads para permitir que o broker possa atender a múltiplos dispositivos simultaneamente, 
fazendo com que várias operações ocorram de forma simultanea. Por exemplo, uma thread é usada para enviar dados via UDP,
e outra é usada para alterar a temperatura aleatoriamente.

As mensagens são trocadas entre o dispositivo e o broker usando um protocolo definido no código. As mensagens são strings que contêm um comando e possivelmente alguns dados, separados por dois pontos. Por exemplo, o comando "2" é usado para ligar a geladeira, e o comando "4" é seguido por um valor de temperatura para alterar a temperatura da geladeira.  A arquitetura também inclui tratamento de erros para lidar com várias exceções que podem ocorrer durante a comunicação de rede, como a conexão sendo encerrada inesperadamente.  Por fim, a arquitetura inclui funções para verificar a conexão com o broker e para monitorar essa conexão, desconectando-se e reconectando-se conforme necessário.

## Protocolo de comunicação entre dispositivo e Broker (camada de aplicação)

O protocolo de comunicação entre o dispositivo e o broker é baseado em mensagens, que são strings que contêm um 
comando e possivelmente alguns dados, separados por dois pontos. Por exemplo, o comando "2" é usado para 
ligar a geladeira, e o comando "4" é seguido por um valor de temperatura para alterar a temperatura da geladeira, 
quando recebidos pela aplicação. O broker espera receber mensagens nesse formato e responde com uma 
mensagem de confirmação ou erro, dependendo do comando recebido. O dispositivo envia mensagens para o broker 
usando um socket TCP/IP, e, quando a solicitação é a mudança de temperatura ou retorno dela, pela aplicação, o 
dispositivo envia mensagens de forma contínua para o broker usando um socket UDP. 

O protocolo de comunicação entre o dispositivo e o broker é implementado em Python, usando a biblioteca socket 
para criar e gerenciar as conexões de rede. O dispositivo e o broker usam a mesma porta para se comunicar, sendo 
a porta 5551 para a comunição TCP/IP, 5552 para comunicação UDP e a porta 5555 para a conexão com o broker. 

## Protocolo de comunicação entre dispositivo e Broker (camada de transporte)

O que seria a camada de transporte? essa camada é responsável por garantir a entrega dos dados entre o dispositivo 
e o broker.

O protocolo de comunicação entre o dispositivo e o broker é baseado em sockets TCP/IP e UDP. O dispositivo envia 
mensagens para o broker usando um socket TCP/IP, que é uma conexão orientada a conexão que garante a entrega dos
dados na ordem correta e sem perda de pacotes. O broker responde com uma mensagem de confirmação ou erro,
dependendo do comando recebido. O dispositivo envia mensagens para o broker usando um socket UDP, que é uma
conexão não orientada a conexão que não garante a entrega dos dados na ordem correta ou sem perda de pacotes.
O dispositivo envia mensagens de forma contínua para o broker usando um socket UDP, que é uma conexão não
orientada a conexão que não garante a entrega dos dados na ordem correta ou sem perda de pacotes.


## Interface da aplicação (REST)

A interface da aplicação é baseada em requisições HTTP, que são usadas para enviar mensagens ao broker e obter 
mensagens do broker. A aplicação envia mensagens para o broker usando o método POST, que é usado para enviar 
dados para o servidor, e o broker responde com uma mensagem de confirmação ou erro, dependendo do comando
recebido. A aplicação obtém mensagens do broker usando o método GET, que é usado para obter dados do servidor,
e o broker responde com as mensagens armazenadas em uma lista, que são exibidas na tela da aplicação.

os verbos e rotas executados na camada de aplicação são:
- GET /devices/<string:device_id>/view: esta rota é usada para visualizar os dados de um dispositivo específico.
O ID do dispositivo é passado como parâmetro na URL.
- POST /devices/<string:device_id>/on: esta rota é usada para ligar um dispositivo específico. O ID do dispositivo
é passado como parâmetro na URL.
- POST /devices/<string:device_id>/off: esta rota é usada para desligar um dispositivo específico. O ID do dispositivo
é passado como parâmetro na URL.
- POST /devices/<string:device_id>/change/<float:new_data>: Esta rota é usada para alterar os dados de um dispositivo 
específico. O ID do dispositivo e os novos dados são passados como parâmetros na URL. 
- GET /devices/<string:device_id>/return: Esta rota é usada para retornar os dados de um dispositivo específico. 
O ID do dispositivo é passado como parâmetro na URL.
- GET /devices: Esta rota é usada para obter todos os dispositivos conectados.
- POST /devices/<string:device_id>/add/<string:data>: Esta rota é usada para adicionar itens na geladeira. 
O ID do dispositivo e os dados do item são passados como parâmetros na URL.
- POST /devices/<string:device_id>/remove/<string:data>: Esta rota é usada para remover itens da geladeira. 
O ID do dispositivo e os dados do item são passados como parâmetros na URL.
- GET /devices/<string:device_id>/view/quantity: Esta rota é usada para visualizar a quantidade de itens na geladeira. 
O ID do dispositivo é passado como parâmetro na URL.
- GET /devices/<string:device_id>/view_items: Esta rota é usada para visualizar os itens da geladeira. O ID do 
dispositivo é passado como parâmetro na URL.

Cada rota é associada a uma função específica que é chamada quando a rota é acessada. As funções retornam uma 
resposta JSON, que é um formato de dados comum para APIs RESTful.

## Formatação, envio e tratamento de dados

As mensagens trocadas entre o dispositivo e o broker são strings que contêm um comando e possivelmente alguns dados,
separados por dois pontos. Por exemplo, o comando "2" é usado para ligar a geladeira, e o comando "4" é seguido por um
valor de temperatura para alterar a temperatura da geladeira. O broker espera receber mensagens nesse formato e responde
com uma mensagem de confirmação ou erro, dependendo do comando recebido. O dispositivo envia mensagens para o broker
usando um socket TCP/IP, e o broker responde com uma mensagem de confirmação ou erro, dependendo do comando recebido.

As mensagens trocadas entre a aplicação e o broker são strings que contêm um comando e possivelmente alguns dados,
separados por dois pontos. Por exemplo, o comando "2" é usado para ligar a geladeira, e o comando "4" é seguido por um
valor de temperatura para alterar a temperatura da geladeira. A aplicação envia mensagens para o broker usando o método
POST, que é usado para enviar dados para o servidor, e o broker responde com uma mensagem de confirmação ou erro,
dependendo do comando recebido. A aplicação obtém mensagens do broker usando o método GET, que é usado para obter
dados do servidor, e o broker responde com as mensagens armazenadas em uma lista, que são exibidas na tela da aplicação.

## Tratamento de conexões simultâneas (threads)

Threads foram usadas para tornar o sistema mais eficiente, permitindo que várias operações ocorram de forma simultânea.
Por exemplo, uma thread é usada para enviar dados via UDP, e outra é usada para alterar a temperatura aleatoriamente.
As threads são usadas para permitir que o broker possa atender a múltiplos dispositivos simultaneamente, fazendo com
que várias operações ocorram de forma simultânea. Por exemplo, uma thread é usada para enviar dados via UDP, e outra
é usada para alterar a temperatura aleatoriamente.

As threads são usadas para permitir que o broker possa atender a múltiplos dispositivos simultaneamente, fazendo com
que várias operações ocorram de forma simultânea. Por exemplo, uma thread é usada para enviar dados via UDP, e outra
é usada para alterar a temperatura aleatoriamente.


## Gerenciamento do dispositivo

É possível gerenciar o dispositivo (parar, alterar valores, etc) remotamente, através da aplicação. A aplicação envia
mensagens para o broker, que envia as mensagens para o dispositivo, que executa as ações de acordo com as mensagens
recebidas. Por exemplo, a aplicação pode enviar uma mensagem para ligar a geladeira, e o dispositivo liga a geladeira
de acordo com a mensagem recebida. O dispositivo também pode enviar mensagens para a aplicação, que exibe as mensagens
recebidas do dispositivo. Por exemplo, o dispositivo pode enviar uma mensagem para informar que a geladeira foi ligada,
e a aplicação exibe a mensagem recebida do dispositivo.

O dispositivo pode ser gerenciado remotamente, através da aplicação. A aplicação envia mensagens para o broker, que
envia as mensagens para o dispositivo, que executa as ações de acordo com as mensagens recebidas. Por exemplo, a
aplicação pode enviar uma mensagem para ligar a geladeira, e o dispositivo liga a geladeira de acordo com a mensagem
recebida. O dispositivo também pode enviar mensagens para a aplicação, que exibe as mensagens recebidas do dispositivo.
Por exemplo, o dispositivo pode enviar uma mensagem para informar que a geladeira foi ligada, e a aplicação exibe a
mensagem recebida do dispositivo.

## Desempenho (uso de cache no Broker, filas, threads, etc.)

O sistema utiliza threads para tornar o sistema mais eficiente, permitindo que várias operações ocorram de forma
simultânea. Por exemplo, uma thread é usada para enviar dados via UDP, e outra é usada para alterar a temperatura
aleatoriamente. As threads são usadas para permitir que o broker possa atender a múltiplos dispositivos simultaneamente,
fazendo com que várias operações ocorram de forma simultânea. Por exemplo, uma thread é usada para enviar dados via UDP,
e outra é usada para alterar a temperatura aleatoriamente.


## Confiabilidade de solução (tratamento de conexões)

O sistema é capaz de lidar com várias exceções que podem ocorrer durante a comunicação de rede, como a conexão sendo
encerrada inesperadamente. O sistema inclui tratamento de erros para lidar com várias exceções que podem ocorrer
durante a comunicação de rede, como a conexão sendo encerrada inesperadamente. O sistema inclui funções para verificar
a conexão com o broker e para monitorar essa conexão, desconectando-se e reconectando-se conforme necessário.


## Documentação do código


## Emprego do Docker

O Docker foi utilizado para facilitar a execução do projeto, permitindo que os componentes do projeto sejam executados
em containers separados. Isso torna mais fácil a execução do projeto em diferentes ambientes, sem a necessidade de
instalar dependências adicionais. O Docker foi utilizado para criar e executar os containers para o broker, o dispositivo
(geladeira) e a aplicação, em suas respectivas pastas. O Docker foi utilizado para criar e executar os containers para
o broker, o dispositivo (geladeira) e a aplicação, em suas respectivas pastas. O Docker foi utilizado para criar e
executar os containers para o broker, o dispositivo (geladeira) e a aplicação, em suas respectivas pastas.



## Execução do Projeto

### Github
- há duas formas de acessar o código fonte do projeto:
  - Atraves do gitclone: `git clone, caso você tenha o git instalado em sua máquina`
  - Através do download do arquivo zip: `download, caso você não tenha o git instalado em sua máquina`
  
Após acessar o código fonte, você deve acessar a pasta de cada um dos componentes do projeto, e executar cada um 
deles. Para executar o broker, você deve acessar a pasta broker, e executar o arquivo api_broker.py. Para executar o 
dispositivo (geladeira), você deve acessar a pasta device, e executar o arquivo menu_device.py. Para executar a 
aplicação, você deve acessar a pasta application, e executar o arquivo main.py. 

lembrando que para executar dessa forma, sem o Docker, é necessário ter o Python instalado em sua máquina, de 
preferência a versão 3.12. Além disso, serão necessárias as bibliotecas requests e o servidor Flask, que podem ser
instalados através do comando `pip install requests` e `pip install Flask` respectivamente, no terminal do seu
sistema operacional.

cada um dos componentes do projeto deve ser executado em um terminal separado, para que a comunicação entre eles 
possa ocorrer. 

### Docker
- Para executar o projeto utilizando o Docker, você deve acessar a pasta raiz do projeto, e executar o comando
`docker build -t nome_container .` no terminal do seu sistema operacional. Esse comando irá criar e executar os 
containers. Esse passo deve ser feito para cada um dos componentes do projeto, ou seja, para o broker, o dispositivo
(geladeira) e a aplicação, em suas respectivas pastas.
- 
- Após a execução do comando acima, você deve executar o comando `docker run -p 5555:5555 nome_container` para o 
broker
- 'docker run -p 5551:5551 -p 5552:5552 nome_container' para o dispositivo
- 'docker run -p 5555:5555 nome_container' para a aplicação


## Demonstração da Aplicação



- Clone o repositório do projeto: `git clone
- Acesse a pasta do projeto: `cd PBL-Redes`
- Execute o arquivo `main.py` para iniciar a aplicação: `python main.py`
- Acesse o endereç






## Sumário

- Introdução
  - Objetivo 
  - Requisitos
  - Tecnologias
- Desenvolvimento
  - Aplicação
  - API RESTful
  - Servidor broker
  - Dispositivos
  - Lógica de comunicação
  - Lógica de funcionamento
- Execução
  - Instalação
  - Demonstração da aplicação
- Resultados
- Conclusão
- Referências


