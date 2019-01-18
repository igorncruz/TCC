# -*- coding: utf-8 -*-

# To start a mosquitto broker: sudo service mosquitto start
# To stop a mosquitto broker: sudo service mosquitto stop
# To see the status of mosquitto broker: sudo service mosquitto status
# To subscribe to a mosquitto broker in command line: mosquitto_sub -h localhost -t "tcc" -v
# To publish on a mosquitto broker in command line: mosquitto_pub -h localhost -t "tcc" -m "Hello MQTT"
# By default, the mosquitto broker is initialize on 1883 port

import paho.mqtt.client as mqtt
import sys, time, datetime
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
    startExperimentTS = ''
    __path = "basic"

    def establishConnection(self, address='localhost', port=1883):
        dataTest = 'Hello World!'
        print('endereco: ' + address)
        print('porta: ' + str(port))
        print('dados: ' + dataTest)

        self.mqttc.connect(address, port)
        response = self.mqttc.publish('tcc', dataTest)
        print('enviado: '+ str(response.is_published()))


    def startExperiment(self, reps=-1, timePerRep=1):
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

    def sendPackage(self, index):
        print(TAB_1 + "Enviando pacote ...")
        response = self.mqttc.publish('tcc', self._dados.getByIndex(index))
        print(TAB_1 + 'enviado: ' + str(response.is_published()))
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

    reps = input(
        '\nDigite a quantidade de pacotes que você deseja enviar: (ou deixe em branco para enviar a quantidade máxima possível )\n'
    )
    try:
        reps = int(reps)
    except ValueError:
        reps = -1

    client.startExperiment(reps)


if __name__ == '__main__':
    main()