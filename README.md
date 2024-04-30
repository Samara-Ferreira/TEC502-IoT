# PBL-Redes
Projeto de PBL da disciplina MI - Concorrência e Conectividade.

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


## O que deve ser feito e testado 

- [] testar todas as funções nos dispositivos 
- [] colocar os ip e as portas em um arquivo separado 

## Broker
- [] é possível fechar o broker com um comando da aplicação?
- [] lock nas threads de envio e recebimento de mensagens
- [] ta pegando uma lista suja? mostra dispositivos anteriores

## Geladeira
### menu da aplicação
- [x] ligar e desligar a geladeira
- [] retornar a temperatura atual
- [] retornar a lista de itens e suas quantidades
- [] adicionar alimentos e suas quantidades
- [] remover alimentos e suas quantidades
- [] alterar nome dispositivo

### menu do dispositivo
- [x] ligar e desligar a geladeira
- [x] alterar a temperatura pelo input
- [x] alterar a temperatura por valores randomicos
- [x] conectar ao broker
- [x] desconectar do broker
- [x] encerrar programa
- [x] alterar nome dispositivo
- [] quando eu peço a temperatura e só depois conecto ao broker, não vai

### erros
- [] quando encerro programa e a conexão com o broker está ativa