from stompest.config import StompConfig
from stompest.sync import Stomp

import sys, time, datetime
from pathlib import Path
# Se o cliente for executado no windows ou Visual Studio Code, descomentar a linha abaixo
sys.path.insert(0, str(Path().resolve()))
# Se o cliente for executado no linux, descomentar a linha abaixo
# sys.path.insert(0, str(Path().resolve().parent))
# print Path().resolve()
from data import Data
import util

TAB_1 = '\t - '


class Client():
    _dados = Data()
    startExperimentTS = ''
    client = ''
    queue = '/queue/tcc_stomp'


    def establishConnection(self, address='localhost', port=61613):
        dataTest = 'Hello World!'
        print('endereco: ' + address)
        print('porta: ' + str(port))
        print('dados: ' + dataTest)

        config = StompConfig('tcp://{}:{}'.format(address, port))
        self.client = Stomp(config)
        self.client.connect()
        self.client.send(self.queue, dataTest.encode())

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
        self.client.send(self.queue, self._dados.getByIndex(index).encode())


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

# CONFIG = StompConfig('tcp://localhost:61613')
# QUEUE = '/queue/test'

# if __name__ == '__main__':
#     client = Stomp(CONFIG)
#     client.connect()
#     client.send(QUEUE, 'Mozão é mô fofinha'.encode())
#     client.send(QUEUE, 'Linda, gostosa, cheirosa e cheia de charme'.encode())
#     client.disconnect()