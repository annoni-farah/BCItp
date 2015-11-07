#!/usr/bin/env python
from threading import Thread
from scipy import signal as sig
import sys, os, rospy, rospkg
import numpy as np
from std_msgs.msg import Float64MultiArray, Float64, MultiArrayDimension, String

rospack = rospkg.RosPack()
mypath=rospack.get_path('bci_training_platform') + '/scripts/'

DOING_NOTHING = 0
DOING_SAMPLES = 1
DOING_CALC = 2
JOB_STOP = -1
JOB_GOING = 0
JOB_END = 1
JOB_STATUS = -1
NUM_SECONDS = 1*4*8*250
storage_callback0=0

def importa(nome_do_arquivo):
	return np.matrix([[float(x) for x in y] for y in [y.split('\t') \
		for y in open(nome_do_arquivo,'r').read().split('\n')[0:-1]]]).T

def callback_manager_gui(data):
	global Y, file0, Y, file3, storage_callback0
	t=data.data
	print('ok')
	if storage_callback0==0:
		file0 = open(t,'w')
	elif storage_callback0==1:
		Y=importa(t)
	elif storage_callback0==2:
		file3 = open(t,'w')
		print(storage_callback0)
	storage_callback0+=1

def callback_manager_smp(msg_received):
	global X, NUM_SECONDS, JOB_STATUS
	if NUM_SECONDS > 0 and JOB_STATUS==JOB_GOING:
		X=np.hstack((X,np.matrix(msg_received.data).T))
		X=np.delete(X,0,1)
		NUM_SECONDS-=1
		if NUM_SECONDS == 0:
			JOB_STATUS = JOB_END

def get_samples(NUM_CHANNELS,NUM_SAMPLES):
	global X, JOB_STATUS
	X=np.matrix([[0]*NUM_CHANNELS]*NUM_SAMPLES).T
	JOB_STATUS=JOB_GOING
	while JOB_STATUS==JOB_GOING:
		pass
	JOB_STATUS=JOB_END

def save_to_txt():
	global X, NUM_SECONDS, file0
	for element in X.T:
		file0.write("".join([str(y)+'\t' for y in element.A1])[0:-1]+'\n')
	file0.close()
	NUM_SECONDS-=1

def cov_(X):
	cov = X*X.T
	return cov/cov.trace()

def calcparams():
	global file3, X, Y
	X=X[0:8]
	ind_T = np.argsort(Y[1].A1)
	Y[1] = Y[1].A1[ind_T]
	Y[0] = Y[0].A1[ind_T]
	fir=np.matrix(sig.firwin(21,[8,30],pass_zero=False,nyq=125.0))
	X_bp=np.matrix(sig.convolve(X,fir))
	X_T=[X_bp.T[y+3*250:y+6*250].T for y in Y.tolist()[0]]
	classe=[1,2,3,4]
	for classe1 in classe:
		for classe2 in classe:
			if classe2 > classe1:
					Xa = X_T[3*(classe1-1):3*classe1]          #array de matrizes de sinais da classe a
					Xb = X_T[3*(classe2-1):3*classe2]          #array de matrizes se sinais da classe b
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
					for element in W_:
						file3.write("".join([str(y)+'\t' for y in element.A1])+'\n')
					for element2 in W2:
						file3.write("".join([str(y)+'\t' for y in element2.A1]))
					file3.write("\t0\t0\n")
	file3.close()

def manager():
	global storage_callback0
	rospy.init_node('manager', anonymous=True)
	rospy.Subscriber('manager_gui', String, callback_manager_gui, queue_size=1000)
	rospy.Subscriber('manager_smp', Float64MultiArray, callback_manager_smp)
	while storage_callback0!=4:
		pass
	get_samples(8,NUM_SECONDS)
	save_to_txt()
	#calcparams()
	print("ok")



manager()
