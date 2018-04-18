#importando a classe de Dados
import sys
from pathlib import Path
# Se o cliente for executado no windows, descomentar a linha abaixo
sys.path.insert(0, str(Path().resolve()))
# Se o cliente for executado no linux, descomentar a linha abaixo
# sys.path.insert(0, str(Path().resolve().parent.parent))

from dados import Dados
import http.client, urllib.parse

class Cliente():
	_dados = Dados()
	conn = ''
	def enviarPacoteTeste(self):
		print("enviando pacote de testes")
		headers = {'Content-type': 'application/json'}
		
		# conteudoPacote = json.dumps(self._dados.obterAleatorio())
		conteudoPacote = self._dados.obterAleatorio()
		
		self.conn.request("POST", "/markdown", conteudoPacote, headers)

		response = self.conn.getresponse()
		print(response.status, response.reason)

	def estabelecerConexao(self, address='localhost', port=8080):
		print('Estabelecendo conexão com ' + address + '...')
		self.conn = http.client.HTTPConnection(address, port)
		self.conn.request("HEAD", "/")
		res = self.conn.getresponse()
		if res.status == 200:
			print('conexão estebelecida!')
		else:
			print('Erro estabelecendo conexão!')

def main():
	cliente = Cliente()
	address = input('Digite o endereço do servidor: (ou deixe em branco caso seja "localhost")\n')
	if (address == ''):
		print ("endereço vazio")
		cliente.estabelecerConexao(port=8080)
	else:
		print('o endereço digitado foi: '+ address)
		cliente.estabelecerConexao(address=address, port=8080)
	cliente.enviarPacoteTeste()
	input("Por quanto tempo você deseja enviar pacotes ?")

if __name__ == '__main__':
	main()

