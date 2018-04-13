#importando a classe de Dados
import sys
from pathlib import Path
sys.path.insert(0, str(Path().resolve().parent.parent))
from dados import Dados
import http.client, urllib.parse

class Cliente():
	_dados = Dados()
	"""docstring for Cliente"""
	def enviarPacote(self):
		print("enviando pacote")
		params = urllib.parse.urlencode({'@number': 12524, '@type': 'issue', '@action': 'show'})
		headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
		conn.request("POST", "", params, headers)
		response = conn.getresponse()
		print(response.status, response.reason)

	def estabelecerConexao(self, address='localhost', port=8080):
		print('Estabelecendo conexão...')
		conn = http.client.HTTPConnection(address, port)
		conn.request("HEAD", "/")
		res = conn.getresponse()
		if res.status == 200:
			print('conexão estebelecida!')
		else:
			print('Erro estabelecendo conexão!')


cliente = Cliente()
cliente.estabelecerConexao(port=8080)
cliente.enviarPacote()