#importando a classe de Dados
import sys, http.client, time, datetime, uuid
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
lostPkgs = []
delayPkgs = []


def send(conn, index):
    print(TAB_1 + "Obtendo os dados p/ envio ...")
    dados = data.getByIndex(index)
    #sentPkg = False
    #while not sentPkg:
    sentPkgTimestamp = time.time()
        
    print(TAB_1 + "Enviando o pacote {} ...".format(index))
    try:
        id = uuid.uuid4().time_mid    
        headers = {
            'Content-type': 'application/json',
            'X-Timestamp': str(sentPkgTimestamp),
            'id': id,
        }
        sentPkgTimestamp = time.time()
        print(TAB_1 + "Enviando o pacote {} ...".format(id))
        conn.request("POST", "/markdown", dados, headers)
        print(TAB_1 + "Obtendo resposta do pacote {} ...".format(id))
        response = conn.getresponse()
        print(TAB_1 + "Pacote id {} enviado: {}  {}".format(
            index, response.status, response.reason))
        responseTimestamp = time.time()
        delayPkgs.append((id, sentPkgTimestamp, responseTimestamp))

        #sentPkg = True
    except Exception as e:
        print(TAB_1 + "Pacote id {} dropado".format(index))
        print(TAB_1 + "Exception: {}".format(e))
        lostPkgs.append(sentPkgTimestamp)
        


class Client():
    _dados = Data()
    conn = ''
    startExperimentTS = ''

    address = ""
    port = ""

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
        self.address = address
        self.port = port
        print('\nEstabelecendo conexão com ' + address + '...')
        self.conn = http.client.HTTPConnection(address, port)
        self.conn.request("HEAD", "/")
        res = self.conn.getresponse()
        if res.status == 200:
            print('conexão estebelecida!')

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

        # self.sendTestPackage()
        delayPkgs = []
        lostPkgs = []

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
        if (len(delayPkgs) > 0):
            fileDelay = open(fileName + "-delay.txt", 'w')
            for i in delayPkgs:
                fileDelay.write("{},{},{}\n".format(i[0], i[1], i[2]))

        if len(lostPkgs) > 0:
            fileLost = open(fileName + "-perda.txt", 'w')
            for i in lostPkgs:
                fileLost.write("{}\n".format(i))

    def sendPackage(self, index):
        t = threading.Thread(target=send, args=(self.conn, index))
        t.start()


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
