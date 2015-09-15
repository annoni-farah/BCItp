import numpy as np

class meubuffer:
	def __init__(self,tamanho_max):
		self.max = tamanho_max
		self.data = []
	def append(self,x):
		self.data=np.hstack((self.data,x))
		if len(self.data) > self.max:
			self.data = np.delete(self.data,np.arange(0,len(x)))
	def get(self):
		return self.data