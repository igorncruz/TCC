import random

class Dados():
	"""docstring for Dados"""
	def __init__(self):
		super(Dados, self).__init__()
		path = '/home/raphael/TCC/dados.txt'
		dataFile = open(path, 'r')
		self.dados = dataFile.readlines()

	def obterAleatorio(self):
		return self.dados[random.randint(0,len(self.dados))]
