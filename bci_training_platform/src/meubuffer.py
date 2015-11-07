import numpy as np

class meubuffer:           #classe para criacao do buffer
    def __init__(self,tamanho_max): #inicializazao do buffer com seu tamanho maximo como argumento
        self.max = tamanho_max
        self.data = np.float64([])
    def append(self,x):    #adiciona array de elementos ao buffer, elemento unitario necessita de []
        self.data=np.hstack((self.data,x))
        if len(self.data) > self.max:
            self.data = np.delete(self.data,np.arange(0,len(x)))
    def get(self):         #retorna os elementos do buffer
        return self.data
    def len(self):
        return len(self.data)
