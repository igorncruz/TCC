# -*- coding: utf-8 -*-

# To start a mosquitto broker: sudo service mosquitto start
# To stop a mosquitto broker: sudo service mosquitto stop
# To see the status of mosquitto broker: sudo service mosquitto status
# To subscribe to a mosquitto broker in command line: mosquitto_sub -h localhost -t "tcc" -v
# To publish on a mosquitto broker in command line: mosquitto_pub -h localhost -t "tcc" -m "Hello MQTT"
# By default, the mosquitto broker is initialize on 1883 port

import paho.mqtt.client as mqtt
import sys, time, datetime, signal
from pathlib import Path
# Se o cliente for executado no windows, descomentar a linha abaixo
# sys.path.insert(0, str(Path().resolve()))
# Se o cliente for executado no linux, descomentar a linha abaixo
# print Path().resolve()
sys.path.insert(0, str(Path().resolve()))
sys.path.insert(0, str(Path().resolve().parent))
from data2 import Data
import util

# mqttc = mqtt.Client('python_pub')
# mqttc.connect('localhost', 1883)
# mqttc.publish('tcc', 'Hello, World!')
# mqttc.loop(2) #timeout = 2s

TAB_1 = '\t - '


class Client():
    _dados = Data()
    mqttc = mqtt.Client('python_pub')
    lostPkgs = []
    delayPkgs = []
    address = ""
    port = ""
    TIMEOUT = 10
    MAX_SEND_ATTEMPT_NUMBER = 3

    def timeout_handler(self, num, stack):
        print("\n!! Timeout nível de aplicação !!")
        raise Exception("timeout-aplicação")

    def establishConnection(self, address='localhost', port=1883):
        self.address = address
        self.port = port
        print('\nEstabelecendo conexão com ' + address + '...')
        dataTest = 'Hello World!'
        self.mqttc.connect(address, port)
        response = self.mqttc.publish('tcc', dataTest)
        print('enviado: ' + str(response.is_published()))

    def startExperiment(self, reps=-1, fileName="teste", timePerRep=1):
        """
		Inicia o Experimento
		>>Reps: quantidade de repetições que o experimento terá. 
				Cada repetição é igual a 1 pacote enviado.
				Caso seja <= 0 serão enviados todos os dados disponíveis
		>>timePerRep: 
				intervalo de tempo entre repetição, em segundos. 
				Padrão = 1seg
		"""
        print("\nIniciando o experimento às {0}".format(
            util.getFormattedDatetimeWithMillisec()))

        if (reps <= 0):
            reps = self._dados.length()
        print("Quantidade de pacotes que serão enviados: {}".format(reps))
        duracao = timePerRep * reps
        print("Tempo estimado de duração do experimento: {} ({})\n".format(
            util.getFormattedDateTimeFromSeconds(duracao),
            str(datetime.timedelta(seconds=duracao))))

        for i in range(0, reps):
            print("iniciando repetição {} às {}".format(
                i + 1, str(util.getFormattedDatetimeWithMillisec())))
            self.sendPackage(i)
            time.sleep(timePerRep)
        self.generateDelayAndLostFiles(fileName)

    def generateDelayAndLostFiles(self, fileName):
        if (len(self.delayPkgs) > 0):
            fileDelay = open(fileName + "-delay.txt", 'w')
            for i in self.delayPkgs:
                fileDelay.write("{},{},{}\n".format(i[0], i[1], i[2]))

        if len(self.lostPkgs) > 0:
            fileLost = open(fileName + "-perda.txt", 'w')
            for i in self.lostPkgs:
                fileLost.write("{}\n".format(i))

    def sendPackage(self, index):
        print(TAB_1 + "Obtendo os dados p/ envio ...")
        dados = self._dados.getByIndex(index)
        sentPkgCount = 0
        while sentPkgCount < self.MAX_SEND_ATTEMPT_NUMBER:
            sentPkgTimestamp = time.time()
            signal.signal(signal.SIGALRM, self.timeout_handler)
            signal.alarm(self.TIMEOUT)
            try:
                id = "{}.{}".format(str(index + 1), str(sentPkgCount))
                print(TAB_1 + "Enviando pacote ...")
                response = self.mqttc.publish('tcc', dados, 2)
                response.wait_for_publish()
                print("{}Pacote id {} enviado: {}".format(
                    TAB_1, id, response.is_published()))
                responseTimestamp = time.time()
                self.delayPkgs.append((id, sentPkgTimestamp,
                                       responseTimestamp))
                sentPkgCount = self.MAX_SEND_ATTEMPT_NUMBER
            except Exception as ex:
                self.lostPkgs.append(sentPkgTimestamp)
                print("!! Pacote dropado !! - Erro: {}!".format(str(ex)))
                sentPkgCount += 1
            finally:
                signal.alarm(0)

        # while (not response.is_published()):
        #     print(TAB_1 + "enviando novamente...")
        #     self.mqttc.connect(address, port)
        #     response = self.mqttc.publish('tcc', self._dados.getByIndex(index))
        #     print(TAB_1 + 'enviado: ' + str(response.is_published()))
        # print TAB_1 + "Pacote enviado: {}  {}".format(response.status, response.reason))


def main():
    client = Client()
    address = input(
        'Digite o endereco do servidor: (ou deixe em branco caso seja "localhost")\n'
    )
    if (address == ''):
        client.establishConnection()
    else:
        client.establishConnection(address=address)
    fileName = input(
        '\nDigite o nome do arquivo (sem a extensão) em que serão registrados a perda de pacotes e delay a nível de aplicação\n'
    )
    reps = input(
        '\nDigite a quantidade de pacotes que você deseja enviar: (ou deixe em branco para enviar a quantidade máxima possível )\n'
    )
    try:
        reps = int(reps)
    except ValueError:
        reps = -1

    client.startExperiment(reps, fileName)


if __name__ == '__main__':
    main()