#importando a classe de Dados
import sys, http.client, time, datetime, uuid, signal
from pathlib import Path
# Se o cliente for executado no windows ou Visual Code, descomentar a linha abaixo
# sys.path.insert(0, str(Path().resolve()))
# Se o cliente for executado no linux, descomentar a linha abaixo
sys.path.insert(0, str(Path().resolve().parent))

from data import Data
import util

TAB_1 = '\t - '

class Client():
    _dados = Data()
    conn = ''
    startExperimentTS = ''
    lostPkgs = []
    delayPkgs = []
    address = ""
    port = ""
    TIMEOUT = 10
    MAX_SEND_ATTEMPT_NUMBER = 3

    def timeout_handler(self, num, stack):
        print("\n!! Timeout nível de aplicação !!")
        raise Exception("timeout-aplicação")

    def establishConnection(self, address='localhost', port=8080):
        self.address = address
        self.port = port
        print('\nEstabelecendo conexão com ' + address + '...')
        self.conn = http.client.HTTPConnection(self.address,
            self.port)
        self.conn.request("HEAD", "/")
        res = self.conn.getresponse()
        if res.status == 200:
            print('conexão estebelecida!')

    def reestablishConnection(self):
        try:
            print("Reestabelecendo conexão")
            self.conn.close()
            self.conn = http.client.HTTPConnection(self.address, self.port)
            self.conn.connect()
        except Exception as ex:
            print(ex)
            self.reestablishConnection()

    #reps:

    #timePerRep:
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
        self.reestablishConnection()
        while sentPkgCount < self.MAX_SEND_ATTEMPT_NUMBER:
            sentPkgTimestamp = time.time()
            signal.signal(signal.SIGALRM, self.timeout_handler)
            signal.alarm(self.TIMEOUT)
            try:
                #id = uuid.uuid4().time_mid
                id = "{}.{}".format(str(index + 1), str(sentPkgCount))
                headers = {
                    'Content-type': 'application/json',
                    'X-Timestamp': str(sentPkgTimestamp),
                    'id': id,
                }
                sentPkgTimestamp = time.time()
                print(TAB_1 + "Enviando pacote...")
                self.conn.request("POST", "/markdown", dados, headers)
                print(TAB_1 + "Obtendo resposta...")
                response = self.conn.getresponse()
                print(TAB_1 + "Pacote id {} enviado: {}  {}".format(
                    id, response.status, response.reason))
                responseTimestamp = time.time()
                self.delayPkgs.append((id, sentPkgTimestamp,
                                       responseTimestamp))
                sentPkgCount = self.MAX_SEND_ATTEMPT_NUMBER

            except Exception as e:
                self.lostPkgs.append(sentPkgTimestamp)
                print("!! Pacote dropado !! - Erro: {}!".format(str(e)))
                self.reestablishConnection()
                sentPkgCount += 1
            finally:
                signal.alarm(0)


def main():
    client = Client()
    address = input(
        'Digite o endereço do servidor: (ou deixe em branco caso seja "localhost")\n'
    )
    if (address == ''):
        client.establishConnection(port=8080)
    else:
        client.establishConnection(address=address, port=8080)

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
