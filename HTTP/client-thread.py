#importando a classe de Dados
import sys, http.client, time, datetime
from pathlib import Path
# Se o cliente for executado no windows ou Visual Code, descomentar a linha abaixo
# sys.path.insert(0, str(Path().resolve()))
# Se o cliente for executado no linux, descomentar a linha abaixo
sys.path.insert(0, str(Path().resolve().parent))
#importando o módulo de Thread
import threading

from data import Data
import util

TAB_1 = '\t - '

data = Data()
def send(conn, index):
    conn.request("POST", "/markdown", data.getByIndex(index))
    response = conn.getresponse()
    print(TAB_1 + "Pacote enviado: {}  {}".format(response.status, response.reason))

class Client():
    _dados = Data()
    conn = ''
    startExperimentTS = ''

    def sendTestPackage(self):
        print("\nenviando pacote de testes")
        # print("Timestamp:" + str(time.time()))
        headers = {
            'Content-type': 'application/json',
        }

        packageContent = self._dados.getRandom()

        self.conn.request("POST", "/markdown", packageContent, headers)

        response = self.conn.getresponse()
        print(response.status, response.reason)

    def establishConnection(self, address='localhost', port=8080):
        print('\nEstabelecendo conexão com ' + address + '...')
        self.conn = http.client.HTTPConnection(address, port)
        self.conn.request("HEAD", "/")
        res = self.conn.getresponse()
        if res.status == 200:
            print('conexão estebelecida!')

    #reps:

    #timePerRep:
    def startExperiment(self, reps = -1, timePerRep=1):
        """
		Inicia o Experimento
		>>Reps: quantidade de repetições que o experimento terá. 
				Cada repetição é igual a 1 pacote enviado.
				Caso seja <= 0 serão enviados todos os dados disponíveis
		>>timePerRep: 
				intervalo de tempo entre repetição, em segundos. 
				Padrão = 1seg
		"""

        # self.sendTestPackage()

        print("\nIniciando o experimento às {0}".format(util.getFormattedDatetimeWithMillisec()))

        if (reps <= 0):
            reps = self._dados.length()
        print("Quantidade de pacotes que serão enviados: {}".format(reps))
        duracao = timePerRep * reps
        print("Tempo estimado de duração do experimento: {} ({})\n".format(
            util.getFormattedDateTimeFromSeconds(duracao),
            str(datetime.timedelta(seconds=duracao))))

        for i in range(0, reps):
            print("iniciando repetição {} às {}".format(i+1, str(util.getFormattedDatetimeWithMillisec())))
            self.sendPackage(i)
            time.sleep(timePerRep)

    def sendPackage(self, index):
        print(TAB_1 + "Enviando pacote ...")
        # data = self._dados.getByIndex(index)

        t = threading.Thread(target=send, args=(self.conn, index))
        t.start()
        # self.conn.request("POST", "/markdown", data)
        # response = self.conn.getresponse()
        # print(TAB_1 + "Pacote enviado: {}  {}".format(response.status, response.reason))

def main():
    client = Client()
    address = input('Digite o endereço do servidor: (ou deixe em branco caso seja "localhost")\n')
    if (address == ''):
        client.establishConnection(port=8080)
    else:
        client.establishConnection(address=address, port=8080)

    reps = input('\nDigite a quantidade de pacotes que você deseja enviar: (ou deixe em branco para enviar a quantidade máxima possível )\n')

    try:
        reps = int(reps)
    except ValueError:
        reps = -1

    client.startExperiment(reps)


if __name__ == '__main__':
    main()
