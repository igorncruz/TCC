# TCC
Código do meu trabalho do TCC

## Sobre
O trabalho trata de uma análise e comparação estatística entre 7 protocolos de comunicação mais conhecidos e utilizados na camada de aplicação no que se refere a Internet das Coisas (Internet of Things ou IoT). O protocolos analisados foram
- HTTP
- CoAP
- MQTT
- DDS
- AMQP
- XMPP
- STOMP

## Como foi desenvolvido
Para cada protocolo analisado, foi criado um servidor e um cliente de aplicação.

Para fazer o experimento, foi utilizado o [netem](https://wiki.linuxfoundation.org/networking/netem) e [TBF](https://www.systutorials.com/docs/linux/man/8-tc-tbf/) para simular uma rede de baixa qualidade.

Os dados transmitidos entre o cliente e o servidor foram dados reais pego de um estação meteorológia real e salvo num arquivo txt no formato JSON. Esses dados contém informações como temperatura, umidade, velocidade do vento, etc. 
Este arquivo de dados pode ser encontrado no arquivo [dados](dados.txt) na raiz do diretório

## Estrutura do Trabalho
O trabalho foi estruturado da seguinte forma: Cada protocolo analisado tem a sua pasta com uma implementação do cliente e servidor de aplicação.

## O Experimento
A realização do experimento envolveu 4 etapas básicas:
1. Configuração do ambiente;
2. Implementação da comunicação entre clientes e servidores de aplicação para cada protocolo (utilizando API's);
3. Simulação de uma rede de baixa qualidade
   - Alta latência;
   - Alta taxa de perda de pacotes;
   - Baixa banda;
4. Captura dos pacotes enviados entre o cliente e o servidor de cada protocolo;


### Configurações do ambiente
Neste trabalho foi utilizado um notebook Thinkpad rodando Ubuntu 16.04, uma placa Raspberry Pi (RPi) modelo 3B rodando Raspbian veroa XXXXX, e um switch de 4 portas da Multilaser para conectar o notebook com a placa e 2 cabos ethernet comuns de 1,5m cada

### Implementação dos protocolos

#### STOMP
Para realizar a comunicação no protocolo STOMP foi utilizado o [RabbitMQ](https://tecadmin.net/install-rabbitmq-server-on-ubuntu/) como broker com o plugin do [STOMP](http://www.rabbitmq.com/stomp.html) e como cliente foi utilizado a biblioteca [stomp.py](https://github.com/jasonrbriggs/stomp.py)

Após a instalação do RabbitMQ pelo link acima, para iniciar/obter status/parar serviço são utilizados os comandos
```
$ sudo service rabbitmq-server start
$ sudo service rabbitmq-server status
$ sudo service rabbitmq-server stop
```

Após startar o serviço, acessar http://localhost:15672 com login: guest/guest

#### AMQP
Como o protocolo AMQP utiliza a arquitetura pub-sub, foi possível reutilizar o RabbitMQ como broker do mesmo modo que o STOMP. Naturalmente por serem protocolos diferentes, utilizam portas diferente e bibliotecas diferentes.

A biblioteca utilizada como cliente foi a [Pika](https://github.com/pika/pika) (um tutorial bem simples de ser entendido pode ser encontrando no próprio site do RabbitMQ [aqui](https://www.rabbitmq.com/tutorials/tutorial-one-python.html) )


### Simulando a rede
Para simular a rede de baixa qualidade foi utilizado [este script](network-emulation/tc-con) rodado direto no terminal da placa RPi.

Para rodar o script é necessário entrar na pasta onde ele se encontra (neste caso a 'network-emulation') e rodar os scripts abaixo. O script aceita os comandos `start`, `show`, `restart`, `stop` e `status`
```
$ sudo ./tc-con start
$ sudo ./tc-con show
$ sudo ./tc-con restart
$ sudo ./tc-con stop
$ sudo ./tc-con status
```

Para alterar os parâmetros utilizados no experimento, abrir o arquivo do script num editor de texto qualquer e alterar os valores de:
- `RATE` para Limite de banda
- `DELAY` para o atraso no envio dos pacotes
- `PACKET_LOSS` para Taxa de perda de pacotes

##### Checar a simulação da rede

Como o envio de pacotes durante o experimento consome muito pouca banda, foi necessário verificar que a simulação da rede estava de fato funcionando. Para isso foi utilizado o iperf. Foram executados os comandos abaixo antes e após o início da simulação da rede.

**Testar Conexão TCP**

*Máquina Servidor (notebook) *
```
$ iperf -s
```

*Máquina Cliente (Raspeberry Pi)*
```
$ iperf -c [IP_DA_MAQUINA_DESTINO]
```

**Testar Conexão UDP**

*Máquina Servidor (notebook) *
```
$ iperf -s -u
```

*Máquina Cliente (Raspeberry Pi)*
```
$ iperf -c [IP_DA_MAQUINA_DESTINO] -u -b 10M
```


obs: é necessário primeiro rodar o comando do Servidor para depois rodar o comando do Cliente


### Captura de pacotes
Para realizar a captura de pacotes entre o cliente e o servidor foi utilizado o TCPDump.

Para capturar e salvar os pacotes transmitidos via TCP ou UDP foi utilizado o código abaixo rodando direto no terminal

**TCP**
```
TEM QUE FAZER ISSO
```

**UDP**
```
TEM QUE FAZER ISSO
```
