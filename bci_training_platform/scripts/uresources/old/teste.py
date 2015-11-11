import numpy as np

def importa(nome_do_arquivo):
	return np.matrix([[float(x) for x in y] for y in [y.split('\t') \
		for y in open(nome_do_arquivo,'r').read().split('\r\n')[0:-1]]]).T

#a=importa("parameters.txt")




