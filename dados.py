import random
import sys


class Dados():
	"""docstring for Dados"""
	def __init__(self):
		super(Dados, self).__init__()
		print(sys.path)
		path = sys.path[0] + '/dados.txt'
		dataFile = open(path, 'r')
		self.dados = dataFile.readlines()

	def obterAleatorio(self):
		return self.dados[random.randint(0,len(self.dados))]

if __name__ == '__main__':
    d = Dados()
    print(d.obterAleatorio())
