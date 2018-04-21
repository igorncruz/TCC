#importando a classe de Dados
import sys, http.client, time, datetime
from pathlib import Path
# Se o cliente for executado no windows, descomentar a linha abaixo
sys.path.insert(0, str(Path().resolve()))
# Se o cliente for executado no linux, descomentar a linha abaixo
# sys.path.insert(0, str(Path().resolve().parent.parent))

from data import Data
import util

class Client():
	_dados = Data()
	conn = ''
	startExperimentTS = ''

	def sendTestPackage(self):
		print("enviando pacote de testes")
		headers = {'Content-type': 'application/json'}
		
		packageContent = self._dados.getRandom()
		
		self.conn.request("POST", "/markdown", packageContent, headers)

		response = self.conn.getresponse()
		print(response.status, response.reason)

	def establishConnection(self, address='localhost', port=8080):
		print('Estabelecendo conexão com ' + address + '...')
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
		
		self.sendTestPackage()

		print("iniciando o experimento às {0}".format(util.getFormattedDatetimeWithMillisec()))

		if (reps <= 0):
			reps = self._dados.length

		for i in range(0, reps):
			print("iniciando repetição {} às {}".format(i+1, str(util.getFormattedDatetimeWithMillisec())))
			self.sendPackage()
			time.sleep(timePerRep)
	
	def sendPackage(self):
		print("Enviando pacote ...")
		#simulando o envio do pacote
		time.sleep(0.4)
		print("Pacote enviado.")

def main():
	client = Client()
	address = input('Digite o endereço do servidor: (ou deixe em branco caso seja "localhost")\n')
	if (address == ''):
		client.establishConnection(port=8080)
	else:
		client.establishConnection(address=address, port=8080)
	client.startExperiment(reps=10)


if __name__ == '__main__':
	main()

