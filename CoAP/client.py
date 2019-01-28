#!/usr/bin/env python
# -*- coding: utf-8 -*-

#importando a classe de Dados
import sys, time, datetime
from pathlib2 import Path
# Se o cliente for executado no windows, descomentar a linha abaixo
# sys.path.insert(0, str(Path().resolve()))
# Se o cliente for executado no linux, descomentar a linha abaixo
print Path().resolve()
sys.path.insert(0, str(Path().resolve()))
sys.path.insert(0, str(Path().resolve().parent))
from data2 import Data
import util
from coapthon.client.helperclient import HelperClient

TAB_1 = '\t - '


class Client():
    _dados = Data()
    conn = ''
    startExperimentTS = ''
    __path = "basic"
    conn = ''
    lostPkgs = []
    delayPkgs = []

    def establishConnection(self, address='127.0.0.1', port=8080):
        print 'endereco: ' + address
        print 'porta: ' + str(port)
        print 'dados: ' + self._dados.getRandom()

        self.conn = HelperClient(server=(address, port))
        response = self.conn.post(self.__path, "testando conexão!")
        print 'resposta: ' + response.pretty_print()

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
        self.conn.stop()
        self.generateDelayAndLostFiles(fileName)

    def generateDelayAndLostFiles(self, fileName):
        if (len(self.delayPkgs) > 0):
            fileDelay = open(fileName + "-delay.txt", 'w')
            for i in self.delayPkgs:
                fileDelay.write("{},{}\n".format(repr(i[0]), repr(i[1])))

        if len(self.lostPkgs) > 0:
            fileLost = open(fileName + "-perda.txt", 'w')
            for i in self.lostPkgs:
                fileLost.write("{}\n".format(repr(i)))

    def sendPackage(self, index):
        print TAB_1 + "Enviando pacote ..."
        sentPkgTimestamp = time.time()
        try:
            response = self.conn.post(
                self.__path, self._dados.getByIndex(index), timeout=5)
            responseTimestamp = time.time()
            self.delayPkgs.append((sentPkgTimestamp, responseTimestamp))
            print TAB_1 + "Pacote enviado: " + str(response)
        except:
            self.lostPkgs.append(sentPkgTimestamp)
            print TAB_1 + "Pacote dropado."


def main():
    client = Client()
    address = raw_input(
        'Digite o endereco do servidor: (ou deixe em branco caso seja "localhost")\n'
    )
    if (address == ''):
        client.establishConnection(port=8080)
    else:
        client.establishConnection(address=address, port=8080)

    reps = raw_input(
        '\nDigite a quantidade de pacotes que você deseja enviar: (ou deixe em branco para enviar a quantidade máxima possível )\n'
    )

    fileName = raw_input(
        '\nDigite o nome do arquivo (sem a extensão) em que serão registrados a perda de pacotes e delay a nível de aplicação\n'
    )

    try:
        reps = int(reps)
    except ValueError:
        reps = -1

    client.startExperiment(reps, fileName)


if __name__ == '__main__':
    main()