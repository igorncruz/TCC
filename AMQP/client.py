#!/usr/bin/env python
import pika

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
    channel = ''
    queue = 'tcc_amqp'

    def establishConnection(self, address='localhost', port=5672):
        dataTest = 'Hello World!'
        print('endereco: ' + address)
        print('porta: ' + str(port))
        print('dados: ' + dataTest)

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=address))
        self.channel = connection.channel()
        self.channel.queue_declare(self.queue)
        response = self.channel.basic_publish(exchange='', routing_key=self.queue, body=dataTest)
        print(response)

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
        print('Fechando a conexão...')
        self.channel.connection.close()
        print('Finalizado!')

    def sendPackage(self, index):
        print(TAB_1 + "Enviando pacote ...")
        response = self.channel.basic_publish(
            exchange='',
            routing_key=self.queue,
            body=self._dados.getByIndex(index).encode())
        print(TAB_1 + 'enviado: ' + str(response))


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



# print(" [x] Sent 'Hello World!'")