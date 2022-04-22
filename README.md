# Projeto da disciplina de Infraestrutura de Comunicação 2021.2

## Como rodar
### Entrega 1: Implementação de Socket com esquema cliente-servidor
#### Rodando o servidor
1. Abra o terminal na pasta `delivery-1` do projeto (onde está o server.py)
2. Insira o comando `python3 server.py`

#### Rodando o cliente
1. Abra outro terminal na pasta `delivery-1` do projeto (onde está o client.py)
2. Insira o comando `python3 client.py`
3. Insira algum texto e pressiona enter para que seja enviado ao servidor

***

### Entrega 2: Implementação de confiabilidade sobre o UDP utilizando RDT 3.0
#### Rodando o interceptor
> Permite a demonstração do protocolo RDT, já que faz com que 20% dos pacotes sejam perdidos e outros 20% dos pacotes sejam corrompidos (mudando um bite da mensagem)
1. Abra um terminal na pasta `delivery-2` do projeto (onde está o interceptor.py)
2. Insira o comando `python3 interceptor.py`

#### Rodando o receiver
1. Abra o terminal (se o interceptor tiver sido executado, será necessário abrir outro terminal) na pasta `delivery-2` do projeto (onde está o receiver.py)
2. Insira o comando `python3 receiver.py`

#### Rodando o sender
1. Abra outro terminal na pasta `delivery-2` do projeto (onde está o sender.py)
2. Insira o comando `python3 sender.py`

***

## Grupo
- Eduardo Almeida de Queiroz (eaq)
- Beatriz Feitoza Souza	(bfs4)
- Eduardo Almeida de Queiroz	(eaq)
- Gabriela Maria Melo de Souza	(gmms)
- Marcos Antonio Vital de Lima	(mavl)
- Victor Emanuel Pessoa da Silva	(veps)
