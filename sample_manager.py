#!/usr/bin/env python
from threading import Thread
from scipy import signal as sig
import sys, os, rospy, rospkg
import numpy as np
import open_bci_v3 as bci

from data_processing import *

#define a classe manager
class SampleManager:
    def __init__(self):

        self.globalpath=os.path.abspath(os.path.dirname(__file__))
        
            # OpenBCI config
        port = '/dev/ttyUSB0' # port which opnbci is connected (linux). windows = COM1
        baud = 115200
        board = bci.OpenBCIBoard(port=port, baud=baud)
        
        sleep(1) # need to include this to wait for test config setup
        
        try:
            board.start_streaming(self.get_data) # start getting data from amplifier
		
        except:
            board.stop()
            board.disconnect()
            
            
    def GetData(sample):
        # int64[2] data
        data = sample.channel_data
        
        return data
        
        
    def StoreData():
        
        
    
        
    #callback para lidar com as amostras, também define as 3 tarefas
    def callback_manager_smp(self,msg):
    
        #primera tarefa
        if self.task==1 and self.status==1:
            self.count+=1
            #append um vetor de amostras no arquivo
            self.file0.write("".join([str(y)+'\t' for y in np.matrix(msg.data).T.A1])[0:-1]+'\n')       
            #ao atingir o número totas entra aqui
            if self.count == self.number_samples:
                self.status=0
                self.count=0
                self.file0.close()
                #chama a função que calcula o CSP e LDA
                self.calcparams()
                print("ok")
                
        #segunda tarefa     
        elif self.task==2 and self.status==1:
            self.count+=1
            #append um vetor de amostras no arquivo
            self.file1.write("".join([str(y)+'\t' for y in np.matrix(msg.data).T.A1])[0:-1]+'\n')   
            #self.buffer=np.hstack((self.buffer,np.matrix(msg.data).T))
            #self.buffer=np.delete(self.buffer,0,1)
            
            #entra aqui ao final de cada ensaio
            if self.count == self.number_samples:
                self.file1.close()
                self.status=0
                self.count=0
                #print("done")
                #print("self.number_samples")
                X=loadAsMatrix(self.globalpath+'/users/%s/test1.txt' %self.user)
                #print(X.T[0])
                #print(X.T[2249])
                
                #classifica o ensaio
                self.temp=np.matrix(sig.convolve(X,self.fir))
                self.temp=self.temp.T[250*int(self.feature_window_02)//1000:250*int(self.feature_window_12)//1000].T
                self.temp=cov_(self.temp)
                self.temp=self.W_csp*self.temp*self.W_csp.T
                self.temp=np.matrix((np.log10(np.diag(self.temp))).T)
                self.temp=self.temp*self.W_lda
                
                #envia a classificação para a interface gráfica
                if self.temp>self.L:
                    # self.pub.publish('RT0')
                    print 'RT0'
                elif self.temp<self.L:
                    # self.pub.publish('RT1')
                    print 'RT0'
                
                #limpa o arquivo das amostras
                self.file1=open(self.globalpath + "/users/%s/test1.txt" %self.user,'w')
                
                #envia mensagem para a interface gráfica sinalizando que pode começar outro ensaio
                # self.pub.publish('TT')
                print 'TT'
                #print(self.temp)
                
                
                
        #quarta tarefa      
        elif self.task==4 and self.status==1:
            self.count+=1
            #armazena o vetor de amostras no buffer
            self.buffer=np.hstack((self.buffer,np.matrix(msg.data).T))
            self.buffer=np.delete(self.buffer,0,1)
            
            #entra aqui quando o vetor estiver cheio
            if self.count == self.number_samples + int(self.win_displacement)*250//1000:
                self.status=0
                self.temp=self.buffer
                self.count=self.number_samples
                self.status=1       
                #classifica o buffer
                self.temp=np.matrix(sig.convolve(self.temp,self.fir))
                self.temp=self.temp.T[250*3:250*6].T
                self.temp=cov_(self.temp)
                self.temp=self.W_csp*self.temp*self.W_csp.T
                self.temp=np.matrix((np.log10(np.diag(self.temp))).T)
                self.temp=self.temp*self.W_lda          
                #envia a classificaçao para a interface gráfica
                if self.temp>self.L:
                    # self.pub.publish('TX+1')
                    print 'TX+1'
                elif self.temp<self.L:
                    print 'TX-1'
                    # self.pub.publish('TX-1')
                #print(self.temp)

            
    #funcao que carrega o arquivo de parametros 1       
    def load_parameters_1(self):
        try:
            file=open(self.globalpath + "/users/" + self.user + "/" + "parameters_1.txt",'r')
        except:
            file=open(self.globalpath + "/users/" + self.user + "/" + "parameters_1.txt",'w')
        file=open(self.globalpath + "/users/" + self.user + "/" + "parameters_1.txt",'r')   
        self.alert_time = file.readline()[0:-1]
        self.cue_time = file.readline()[0:-1]
        self.task_time = file.readline()[0:-1]
        self.pause_time = file.readline()[0:-1]
        self.classes=[int(x) for x in file.readline()[0:-1].split(" ")]
        self.number_trials=file.readline()[0:-1]
        self.feature_window_0=file.readline()[0:-1]
        self.feature_window_1=file.readline()[0:-1]
        file.close()

    #funcao que carrega o arquivo de parametros 2   
    def load_parameters_2(self):
        try:
            file=open(self.globalpath + "/users/" + self.user + "/" + "parameters_2.txt",'r')
        except:
            file=open(self.globalpath + "/users/" + self.user + "/" + "parameters_2.txt",'w')
        file=open(self.globalpath + "/users/" + self.user + "/" + "parameters_2.txt",'r')   
        self.alert_time2 = file.readline()[0:-1]
        self.cue_time2 = file.readline()[0:-1]
        self.task_time2 = file.readline()[0:-1]
        self.pause_time2 = file.readline()[0:-1]
        self.classes2=[int(x) for x in file.readline()[0:-1].split(" ")]
        self.number_trials2=file.readline()[0:-1]
        self.feature_window_02=file.readline()[0:-1]
        self.feature_window_12=file.readline()[0:-1]
        file.close()
        
    #funcao que carrega o arquivo de parametros 4
    def load_parameters_4(self):
        try:
            file=open(self.globalpath + "/users/" + self.user + "/" + "parameters_4.txt",'r')
        except:
            file=open(self.globalpath + "/users/" + self.user + "/" + "parameters_4.txt",'w')
            self.save_parameters_4()
        file=open(self.globalpath + "/users/" + self.user + "/" + "parameters_4.txt",'r')   
        self.win_size = file.readline()[0:-1]
        self.win_displacement = file.readline()[0:-1]
        file.close()
