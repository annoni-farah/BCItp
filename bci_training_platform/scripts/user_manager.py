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
		self.pub=rospy.Publisher('manager_gui', String, queue_size=100)
		self.NUM_CHANNELS=8
		self.sessions_cont=5
		self.sessions_duration=12
		self.NUM_classes=2
		self.NUM_SAMPLES=250*self.NUM_classes*self.sessions_duration*self.sessions_cont
		self.INTERVAL=125
		rospy.Subscriber('manager_smp', Float64MultiArray, self.callback_manager_smp)
		self.globalpath=os.path.abspath(os.path.dirname(__file__))
		self.buffer=np.matrix([[0]*self.NUM_CHANNELS]*self.NUM_SAMPLES).T
		self.status=0
		self.count=0
		self.task=0
		self.file3=[]
		self.user=""
		self.loop=1
		self.W_csp=[]
		self.W_lds=[]
		self.L=0
		while self.loop==1:
			pass


	def callback_manager_gui(self,msg):
		if msg.data[0:2]=="UN":
			self.user=msg.data[2:]
			print(msg.data[2:])
			try:	os.stat(self.globalpath + "/" + self.user)
			except:	os.mkdir(self.globalpath + "/" + self.user)
		elif msg.data[0:2]=="NC" and self.user!="":
			self.task=1
			self.file0=open(self.globalpath + "/%s/samples.txt" %self.user,'w')
			self.file3=open(self.globalpath + "/%s/parameters.txt" %self.user,'w')
			self.buffer=np.matrix([[0]*self.NUM_CHANNELS]*self.NUM_SAMPLES).T
			print(msg.data[2:])
		elif msg.data[0:2]=="XX" and self.user!="":
			self.status=1
		elif msg.data[0:2]=="XY" and self.user!="":
			self.status=0
		elif msg.data[0:2]=="CP":
			print("welldone")
			self.calcparams()
		elif msg.data[0:2]=="TR":
			print("/%s/parameters.txt" %self.user)
			self.file3=open(self.globalpath + "/%s/parameters.txt" %self.user,'r')
			self.buffer=np.matrix([[0]*self.NUM_CHANNELS]*self.INTERVAL).T
			self.loadparams()
			self.task=2
		elif msg.data[0:2]=="DY":
			self.loop=0


	def callback_manager_smp(self,msg):

		if self.task==1 and self.status==1:
			self.buffer=np.hstack((self.buffer,np.matrix(msg.data).T))
			self.buffer=np.delete(self.buffer,0,1)
			self.count+=1
			if self.count == self.NUM_SAMPLES:
				print('fim')
				self.status=0
				self.count=0
				self.file0=open(self.globalpath + "/%s/samples.txt" %self.user,'w')
				print('salving')
				for element in self.buffer.T:
					self.file0.write("".join([str(y)+'\t' for y in element.A1])[0:-1]+'\n')
				self.file0.close()
				print('saved')
				self.calcparams()

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
				self.temp=np.matrix((np.log10(np.diag(self.temp))).T)
				self.temp=self.temp*self.W_lda
				#print(1)
				if self.temp>self.L:
					self.pub.publish('TX+1')
				elif self.temp<self.L:
					self.pub.publish('TX-1')
				

	def loadparams(self):
		self.W_csp = (self.importa(self.globalpath + "/%s/parameters.txt" %self.user)).T
		self.W_lda = (self.W_csp[-1]).T[0:6]
		self.L=(self.W_csp[-1]).T[-1]
		self.W_csp = self.W_csp[0:-1]


	def importa(self,nome_do_arquivo):
		return np.matrix([[float(x) for x in y] for y in [y.split('\t') \
			for y in open(nome_do_arquivo,'r').read().split('\n')[0:-1]]]).T

	def calcparams(self):
		print('calc params')
		X=self.importa(self.globalpath+'/%s/samples.txt' %self.user)
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
						Xa = X_T[self.sessions_cont*(classe1-1):self.sessions_cont*classe1]          #array de matrizes de sinais da classe a
						Xb = X_T[self.sessions_cont*(classe2-1):self.sessions_cont*classe2]          #array de matrizes se sinais da classe b
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
						self.W_csp=W_n						
						Za = np.matrix((np.log10([np.diag(x) for x in [W_*X*W_.T for X in Ca_]])).T)
						Zb = np.matrix((np.log10([np.diag(x) for x in [W_*X*W_.T for X in Cb_]])).T)
						Ma, Mb = (sum(Za.T).T/len(Za.T)), (sum(Zb.T).T/len(Zb.T))
						Sa, Sb = (Za*Za.T - Ma*Ma.T), (Zb*Zb.T - Mb*Mb.T)
						W2 = (Sa + Sb).I * (Ma - Mb)
						self.W_lda=W2
						L = W2.T * (Ma + Mb) * 0.5
						self.L=L
				#		print("in")
						for element in W_:
							self.file3.write("".join([str(y)+'\t' for y in element.A1])[0:-1]+'\n')
						for element2 in W2:
							self.file3.write("".join([str(y)+'\t' for y in element2.A1]))
						self.file3.write("%s\t%s\n" %(L.A1[0],L.A1[0]))
		self.file3.close()
		print('did')

	




a=manager()

