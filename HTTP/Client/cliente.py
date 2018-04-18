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
		print('Estabelecendo conexão...')
		self.conn = http.client.HTTPConnection(address, port)
		self.conn.request("HEAD", "/")
		res = self.conn.getresponse()
		if res.status == 200:
			print('conexão estebelecida!')
		else:
			print('Erro estabelecendo conexão!')


cliente = Cliente()
# cliente.estabelecerConexao(address='169.254.173.134', port=8080)
# cliente.enviarPacoteTeste()
