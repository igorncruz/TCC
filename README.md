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
2. Simulação de uma rede de baixa qualidade
   - Alta latência;
   - Alta taxa de perda de pacotes;
   - Baixa banda;
3. Captura dos pacotes enviados entre o cliente e o servidor de cada protocolo;
4. Implementação da comunicação entre clientes e servidores de aplicação para cada protocolo (utilizando API's);


### 1. Configurações do ambiente
Neste trabalho foi utilizado um notebook Thinkpad rodando Ubuntu 16.04, uma placa Raspberry Pi (RPi) modelo 3B rodando Raspbian veroa XXXXX, e um switch de 4 portas da Multilaser para conectar o notebook com a placa e 2 cabos ethernet comuns de 1,5m cada

#### Configurando NTP
Para tentar eliminar ao máximo os fatores externos do experimento, antes de executá-lo foi necessário que os relógios tanto da rasp quanto do notebook estivessem sincronizados ao máximo. Para isso foi utilizado o ntp e ntpdate, instalado tanto na Rasp quanto no notebook via comando abaixo
```
$ sudo apt install ntp
$ sudo apt install ntpdate
```

Visando a melhor forma de realizar o experimento, resolveu-se utilizar o notebook como servidor ntp e a Rasp como client ntp para que a data/hora ficasse o mais sincronizado possível. Sendo assim, para configurar o notebook como servidor foi necessário executar [alguns passos](https://www.thegeekstuff.com/2014/06/linux-ntp-server-client/).

1. Editar o arquivo /etc/ntp.conf no Notebook
Foi incluida as seguintes linhas abaixo para que o notebook funcione como servidor ntp
```
restrict default kod nomodify notrap nopeer noquery #allows other clients to query your time server
restrict -6 default kod nomodify notrap nopeer noquery #The value -6 allows forces the DNS resolution to the IPV6 address resolution
#Add the local clock to the ntp.conf file so that if the 
#NTP server is disconnected from the internet, NTP server provides time from its local system clock.
server  127.127.1.0 # local clock 
fudge   127.127.1.0 stratum 10
#driftfile is used to log how far your clock is from what it should be
#and slowly ntp should lower this value as time progress.
driftfile /var/lib/ntp/ntp.drift 
logfile /var/log/ntp.log

```

2. Reiniciar o ntp no notebook
Após salvar o arquivo no passo anterior (precisa ter permissão de admin para salvar), foi reiniciado o serviço do ntp pelo terminal através do comando abaixo
```
$ sudo service ntp restart
```

Obs: Para saber se o serviço está rodando, executar o comando `$ sudo service ntp status`

3. Editar o /etc/ntp.conf na Rasp
Para que a Rasp consiga saber que o notebook agora é um servidor ntp, é necessário apenas incluir uma linha no ntp.conf da Rasp
```
server [IP_DO_NOTEBOOK] prefer
```
Nesse caso o IP_DO_NOTEBOOK era 10.42.0.1 na subrede entre ele e a Rasp, então o comando ficou `server 10.42.0.1 prefer`

4. Reiniciar o ntp na Rasp
Depois de salvar o arquivo no passo anterior, é necessário reiniciar o serviço do ntp pelo terminal 
```
$ sudo /etc/init.d/ntp start
```

Depois desses passos o servidor já está configurado. Pra testar a sincronização dos relógios pode-se alterar manualmente a data no notebook e em seguida rodar os seguintes comandos no terminal da Rasp

Realiza a busca de todos os servidores ntp disponíveis no arquivo de ntp.conf
```
$ ntpq -p
```
obs: deveria aparece na coluna *remote* o ip do notebook e na coluna *refid* o valor **LOCAL**. Caso não apareça ou apareça diferente, rodar o comando `sudo service ntp reload` e em seguida executar o passo 4 mencionando anteriormente.

Atualizar a data/hora da Rasp com a data/hora do notebook
```
$ sudo ntpdate -u [IP_DO_NOTEBOOK]
```
Nesse caso o IP_DO_NOTEBOOK era 10.42.0.1 na subrede entre ele e a Rasp, então o comando ficou `sudo ntpdate -u 10.42.0.1`

Para voltar a ajustar o horario do notebook com o horário da internet, executar no terminal do note o comando
```
$ sudo ntpdate -u b.st1.ntp.br
```


Durante a realização do experimento, o horário do notebook foi sincronizado com a internet e então foi executado o comando `$ sudo ntpdate -u [IP_DO_NOTEBOOK]` no terminal da Rasp até fosse obtido um offset abaixo de 0.00000...

### 2. Simulando a rede
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


### 3. Captura de pacotes
Para realizar a captura de pacotes tanto no cliente quanto no servidor foi utilizado o [TCPDump](http://www.ronnutter.com/raspberry-pi-intro-to-tcpdump/).

Para capturar e salvar os pacotes transmitidos via TCP ou UDP foi utilizado os comandos abaixo. Um tutorial sobre os comandos disponíveis para o TCPDump pode ser visto [aqui](https://www.tecmint.com/12-tcpdump-commands-a-network-sniffer-tool/) e [aqui](https://danielmiessler.com/study/tcpdump/)

Ao salvar o nome do arquivo foi utilizado a nomeclatura [NOME_DO_PROTOCOLO]\_factor_\[NIVEL_FATOR_UM]\_\[NIVEL_FATOR_DOIS]\_\[NIVEL_FATOR_TRES]\_\[server | client].pcap
Ex: http_factor_3_3_3_server.pcap

**TCP**
```
$ sudo tcpdump -w teste.pcap -i enp9s0 tcp and dst 10.42.0.1 and port 8080
```
**UDP**
```
TEM QUE FAZER ISSO
```

onde:
- `sudo tcpdump`: comando para iniciar o tcpdump;
- `-w teste.pcap`: gravar os pacotes capturados no arquivo com o nome "teste" e a extensão `.pcap`;
- `-i enp9s0`: escutar apenas os pacotes que passam pela interface "enp9s0". Para ver todas as interfaces disponíveis no dispositivo, rodar o comando ```$ sudo tcpdump -D```;
- `tcp` | `udp`: capturar apenas os pacotes cujo protocolo seja tcp ou udp;
- `dst 10.42.0.1`: capturar apenas os pacotes cujo destino seja o endereço de ip informado;
- `port`: capturar apenas os pacotes que passem pela porta informada;




### 4. Implementação dos protocolos

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


## Análise dos dados

### Análise dos pacotes

### Análise das repetições

Para realizar a análise das métricas obtidas na análise das repetições, foi utilizado a linguagem R e a ferramenta [R Stúdio](https://www.rstudio.com/) 

Para instalar o R foi necessário executar apenas os 2 comandos abaixo
```
$ sudo apt-get update
$ sudo apt-get install r-base
```

Já pra instalar o RStudio foi só baixar na parte de download pelo site no link acima o arquivo .deb

[AQUI](https://www.youtube.com/watch?v=AwMct_RzGGE) tem ótimas video aulas/tutoriais em PT-BR de como mexer com o RStudio, como importar dados CSV, gerar gráficos, realizar análises, entre outros.


