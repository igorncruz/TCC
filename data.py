import random
import sys


class Data():
	"""docstring for Dados"""
	def __init__(self):
		super(Data, self).__init__()
		path = sys.path[0] + '/dados.txt'
		dataFile = open(path, 'r')
		self.data = dataFile.readlines()

	def getRandom(self):
		return self.data[random.randint(0,len(self.data))]
	def length(self):
		return len(self.data)

def main():
    d = Data()
    print(d.getRandom())
    print(d.length())

if __name__ == '__main__':
	main()
