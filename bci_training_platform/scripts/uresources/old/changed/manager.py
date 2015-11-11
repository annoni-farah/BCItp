#!/usr/bin/env python
from threading import Thread
from scipy import signal as sig
import sys, os, rospy, rospkg
import numpy as np
from std_msgs.msg import Float64MultiArray, Float64, MultiArrayDimension, String

def cov_(X):
	cov = X*X.T
	return cov/cov.trace()

class manager:
	def __init__(self):
		rospy.init_node('manager', anonymous=True)
		rospy.Subscriber('manager_gui', String, self.callback_manager_gui, queue_size=10)
		self.NUM_CHANNELS=8
		self.NUM_SAMPLES=250*4*12*1
		self.INTERVAL=125
		rospy.Subscriber('manager_smp', Float64MultiArray, self.callback_manager_smp)
		self.globalpath=os.path.abspath(os.path.dirname(__file__))
		self.buffer=np.matrix([[0]*self.NUM_CHANNELS]*self.NUM_SAMPLES).T
		self.status=0
		self.count=0
		self.task=0
		self.file3=[]open(self.globalpath + "/parameters.txt",'w')
		self.user=""
		self.loop=1
		self.W_csp=[]
		self.W_lds=[]
		while self.loop==1:
			pass


	def callback_manager_gui(self,msg):
		if msg.data[0:2]=="UN":
			self.user=msg.data[2:]
			self.file0=open(self.globalpath + "/samples.txt",'w')
			print(msg.data[2:])
		elif msg.data[0:2]=="NC":
			self.task=1
			self.file3=open(self.globalpath + "/parameters.txt",'w')
			self.buffer=np.matrix([[0]*self.NUM_CHANNELS]*self.NUM_SAMPLES).T
			print(msg.data[2:])
		elif msg.data[0:2]=="XX":
			self.status=1
		elif msg.data[0:2]=="CP":
			print("welldone")
			self.calcparams()
		elif msg.data[0:2]=="TR"
			self.file3=open(self.globalpath + "/parameters.txt",'r')
			self.buffer=np.matrix([[0]*self.NUM_CHANNELS]*self.INTERVAL).T
			self.loadparams()
			self.task=2


	def callback_manager_smp(self,msg):
		if self.task==1 and self.status==1:
			self.buffer=np.hstack((self.buffer,np.matrix(msg.data).T))
			self.buffer=np.delete(self.buffer,0,1)
			self.count+=1
			if self.count == self.NUM_SAMPLES:
				print('fim')
				self.status=0
				self.count=0
				self.file0=open(self.globalpath + "/samples.txt",'w')
				for element in self.buffer.T:
					self.file0.write("".join([str(y)+'\t' for y in element.A1])[0:-1]+'\n')
				self.file0.close()
				print('saved')
				#self.calcparams()
		elif self.task==2 and self.status==1:
			self.buffer=np.hstack((self.buffer,np.matrix(msg.data).T))
			self.buffer=np.delete(self.buffer,0,1)
			self.count+=1
			if self.count == 250:
				self.status=0
				self.count=0
				self.temp=self.buffer
				self.status=1
				self.temp=cov_(self.temp)
				self.temp=self.W_csp*self.temp*self.W_csp.T
				self.temp=np.matrix((np.log10(np.diag(sel.temp))).T)
				self.temp=self.W_lda.T*self.temp
				
			
	def loadparams():
		self.W_csp = self.importa(self.file3)
		self.W_lda = [-1]
		self.W_csp = self.W_csp[0:6]
		
	def importa(self,nome_do_arquivo):
		return np.matrix([[float(x) for x in y] for y in [y.split('\t') \
			for y in open(nome_do_arquivo,'r').read().split('\r\n')[0:-1]]]).T

	def calcparams(self):
		print('tentando')
		X=self.importa(self.globalpath+'/samples.txt')
		X=X[0:8]
		print(X.shape)
		Y=self.importa(self.globalpath+'/marcas.txt')
		ind_T = np.argsort(Y[1].A1)
		Y[1] = Y[1].A1[ind_T]
		Y[0] = Y[0].A1[ind_T]
		fir=np.matrix(sig.firwin(21,[8,30],pass_zero=False,nyq=125.0))
		X_bp=np.matrix(sig.convolve(X,fir))
		X_T=[X_bp.T[y+3*250:y+6*250].T for y in Y.tolist()[0]]
		classe=[1,2]
		for classe1 in classe:
			for classe2 in classe:
				if classe2 > classe1:
						Xa = X_T[72*(classe1-1):72*classe1]          #array de matrizes de sinais da classe a
						Xb = X_T[72*(classe2-1):72*classe2]          #array de matrizes se sinais da classe b
						Ca_ = [cov_(X) for X in Xa]                  #array de matrizes de covariancia da classe a
						Cb_ = [cov_(X) for X in Xb]
						Ca = sum(Ca_)/len(Ca_)
						Cb = sum(Cb_)/len(Cb_)
						C = Ca + Cb
						U,V = np.linalg.eigh(C)
						V = V[:,np.argsort(U)]
						U = np.matrix(np.diag(U[np.argsort(U)]))
						Q = np.sqrt(U.I)*V.T
						U2,V2 = np.linalg.eigh(Q*Ca*Q.T)
						V2 = V2[:,np.argsort(U2)]
						W = V2.T*Q
						W_n = 3
						W_ = W[np.arange(W_n).tolist() + \
								sorted((-1-np.arange(W_n)).tolist())]    #separa os 3 primeiros e os tres ultimos filtros espaciais
						Za = np.matrix((np.log10([np.diag(x) for x in [W_*X*W_.T for X in Ca_]])).T)
						Zb = np.matrix((np.log10([np.diag(x) for x in [W_*X*W_.T for X in Cb_]])).T)
						Ma, Mb = (sum(Za.T).T/len(Za.T)), (sum(Zb.T).T/len(Zb.T))
						Sa, Sb = (Za*Za.T - Ma*Ma.T), (Zb*Zb.T - Mb*Mb.T)
						W2 = (Sa + Sb).I * (Ma - Mb)
						L = W2.T * (Ma + Mb) * 0.5
						print("in")
						for element in W_:
							self.file3.write("".join([str(y)+'\t' for y in element.A1])+"\r")
						for element2 in W2:
							self.file3.write("".join([str(y)+'\t' for y in element2.A1])+str(L)+"\t"+str(L)+"\r\n")
		self.file3.close()

	




a=manager()

