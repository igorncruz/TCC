# -*- coding: utf-8 -*-
import sys, datetime, time, signal
from nyamuk import *
from pathlib2 import Path
sys.path.insert(0, str(Path().resolve()))
sys.path.insert(0, str(Path().resolve().parent))
from data2 import Data
import util

TAB_1 = '\t - '

# To start a mosquitto broker: sudo service mosquitto start
# To stop a mosquitto broker: sudo service mosquitto stop
# To see the status of mosquitto broker: sudo service mosquitto status
# To subscribe to a mosquitto broker in command line: mosquitto_sub -h localhost -t "tcc" -v
# To publish on a mosquitto broker in command line: mosquitto_pub -h localhost -t "tcc" -m "Hello MQTT"
# By default, the mosquitto broker is initialize on 1883 port


class MQTTClient():
    _dados = Data()
    client = Nyamuk("tcc_client")
    lostPkgs = []
    delayPkgs = []
    TIMEOUT = 10
    MAX_SEND_ATTEMPT_NUMBER = 3

    def timeout_handler(self, num, stack):
        print("\n!! Timeout nível de aplicação !!")
        raise Exception("timeout-aplicação")

    def connect(self, address):
        print 'Endereço do servidor: ' + address
        self.client.server = address
        self.client.connect(version=4)
        self.client.publish('tcc', 'testando!', qos=1)
        self.client.packet_write()

    def reconnect(self):
        self.client.disconnect()
        self.client.connect(version=4)

    def startExperiment(self, reps, fileName, timePerRep=1):
        print "\nIniciando o experimento às {0}".format(
            util.getFormattedDatetimeWithMillisec())

        if (reps <= 0):
            reps = self._dados.length()

        print "Quantidade de pacotes que serão enviados: {}".format(reps)
        duracao = timePerRep * reps
        print "Tempo estimado de duração do experimento: {} ({})\n".format(
            util.getFormattedDateTimeFromSeconds(duracao),
            str(datetime.timedelta(seconds=duracao)))

        for i in range(0, reps):
            print "iniciando repetição {} às {}".format(
                i + 1, str(util.getFormattedDatetimeWithMillisec()))
            self.sendPackage(i)
            time.sleep(timePerRep)
        self.generateDelayAndLostFiles(fileName)

        print "Número de repetições: " + str(reps)
        print "Nome do arquivo: " + fileName

    def sendPackage(self, index):
        print TAB_1 + "Obtendo os dados p/ envio ..."
        dados = self._dados.getByIndex(index)
        sentPkgCount = 0
        self.reconnect()
        while sentPkgCount < self.MAX_SEND_ATTEMPT_NUMBER:
            sentPkgTimestamp = time.time()
            signal.signal(signal.SIGALRM, self.timeout_handler)
            signal.alarm(self.TIMEOUT)
            try:
                #id = uuid.uuid4().time_mid
                id = "{}.{}".format(str(index + 1), str(sentPkgCount))
                sentPkgTimestamp = time.time()
                print TAB_1 + "Enviando pacote {} ...".format(id)

                self.client.publish('tcc', dados, qos=1)
                self.client.packet_write()
                # print TAB_1 + "Pacote id {} enviado: {}  {}".format(
                #     id, response.status, response.reason)
                responseTimestamp = time.time()
                # print str(response)
                self.delayPkgs.append((id, sentPkgTimestamp,
                                       responseTimestamp))
                sentPkgCount = self.MAX_SEND_ATTEMPT_NUMBER

            except Exception as e:
                self.lostPkgs.append(sentPkgTimestamp)
                print("!! Pacote dropado !! - Erro: {}!".format(str(e)))
                self.reconnect()
                sentPkgCount += 1
            finally:
                signal.alarm(0)

    def generateDelayAndLostFiles(self, fileName):
        if (len(self.delayPkgs) > 0):
            fileDelay = open(fileName + "-delay.txt", 'w')
            for i in self.delayPkgs:
                fileDelay.write("{},{},{}\n".format(i[0], i[1], i[2]))

        if len(self.lostPkgs) > 0:
            fileLost = open(fileName + "-perda.txt", 'w')
            for i in self.lostPkgs:
                fileLost.write("{}\n".format(i))


def main():
    client = MQTTClient()
    address = raw_input(
        'Digite o endereco do servidor: (ou deixe em branco caso seja "localhost")\n'
    )
    print "\nEstabelecendo conexão..."
    # TODO: Conectar e enviar dado de teste...
    if (len(address) <= 0):
        address = "localhost"
    client.connect(address)
    print "Conexão estabelecida!"

    fileName = raw_input(
        '\nDigite o nome do arquivo (sem a extensão) em que serão registrados a perda de pacotes e delay a nível de aplicação (ou deixe em branco para escolher o nome "teste")\n'
    )
    # if (len(fileName) <= 0):
    #     fileName = "teste"

    reps = input(
        '\nQual é a quantidade de pacotes que você deseja enviar: (deixe em branco para enviar a quantidade máxima possível )\n'
    )

    try:
        reps = int(reps)
    except ValueError:
        reps = -1

    # ToDo: Iniciar o experimento
    client.startExperiment(reps, fileName)


if __name__ == "__main__":
    main()
