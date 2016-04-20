# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 14:45:00 2016

@author: rafael
"""

#!/usr/bin/env python
import os, platform,sys, pygame as pg
from random import shuffle
from pygame.locals import *

#esses codigos permitem testar a interface gráfica no windows
#if platform.system()=='Linux':
#   import rospy
#   from std_msgs.msg import String
    
#define classe da interface gráfica 
class user_interface:
    def __init__(self):
        #inicia o pygame
        pg.init()
        self.screen= pg.display.set_mode((900,500),HWSURFACE|DOUBLEBUF|RESIZABLE)#|pg.FULLSCREEN)

        #cria o node do ros o subscriber e o publisher
        #       if platform.system()=='Linux':
        #           rospy.init_node('listener', anonymous=True)
        #           rospy.Subscriber('manager_gui', String, self.callback)
        #           self.pub=rospy.Publisher('manager_gui', String, queue_size=100)

        #define o fps para o pygame
        self.fps=30
        self.clock=pg.time.Clock()
        #variavel pra armazenar o tempo
        self.playtime=0

        #define variáveis

        #variavel menu assume o valor do menu atual
        self.menu=0

        #flags utilizadas no código
        self.menu_flag=0
        self.mouse_flag=0
        self.T1_flag=0
        self.RT=0
        self.GA_flag=0
        self.retur=0

        #variavel pra armazenar o usuário
        self.user=''

        #caminho global para esse arquivo
        globalpath = os.path.abspath(os.path.dirname(__file__))
        self.pathtousers = globalpath + '/data/users/'         

        #define variavel para a posiçao do fantasma(0,0 é o centro da dela)
        self.ghostpos_x=0
        self.ghostpos_y=0

        #define cor do fundo da tela
        self.color=(33,155,74)

        #cria loop
        self.loop()
        
    #funcao que carrega a lista de usuarios
    def files(self):
        self.users_list=self.pathtousers+"users_list.txt"

    #define parametros padrão 
    def values(self):
        #tempo em ms das imagens na calibraçao
        self.alert_time="2000"
        self.cue_time="2000"
        self.task_time="3000"
        self.pause_time="2000"
        self.total_time=str(int(self.alert_time)+int(self.cue_time)+int(self.task_time)+int(self.pause_time))
        #classes mao direita e esquerda
        self.classes=[0,1]
        #janela de amostras da tarefa em ms começo e ms fim
        self.feature_window_0="3000"
        self.feature_window_1="6000"
        #número de testes por classe
        self.number_trials="20"

        #tempo em ms das imagens do teste de calibração
        self.alert_time2="2000"
        self.cue_time2="2000"
        self.task_time2="3000"
        self.pause_time2="2000"
        self.total_time2=str(int(self.alert_time)+int(self.cue_time)+int(self.task_time)+int(self.pause_time))
        #classes (mao direita e esquerda)
        self.classes2=[0,1]
        #janela de tempo a ser utilizada na classificaçao ms começo ms fim
        self.feature_window_02="3000"
        self.feature_window_12="6000"
        #número de ensaios por classe
        self.number_trials2="20"

        #tamanho da janela em ms
        self.win_size="3000"
        #deslocamento em ms
        self.win_displacement="500"
                        
    #define loop
    def loop(self): #main loop
        while True:
            #lida com as teclas apertadas, com o tamanho da janela modificada e com os valores escritos
            self.handler()
            #lida com o plote dos elementos gráficos de cada menu
            self.draw()
            #lida com o fps
            self.d=self.clock.tick(self.fps)
            #armazena o tempo
            self.playtime += self.d / 1000.0
            
    def handler(self):
        for event in pg.event.get():
                        
            # checks if the event triggered is a Quit. If so, closes the GUI and
            # sends a cmd to ROS indicating the GUI was closed
            if event.type==QUIT:
            #envia comando para fechar o manager caso feche a interface grafica
            #               if platform.system()=='Linux':
            #                   self.pub.publish("DY")
                pg.quit()
                sys.exit()
            # Deals with GUI resizing. If remove, GUI has a static shape   
            elif event.type==VIDEORESIZE:
                self.screen= pg.display.set_mode(event.size,HWSURFACE|DOUBLEBUF|RESIZABLE)
                self.screen_w, self.screen_h=self.screen.get_size()

            #lida com as teclas para os menus   
            elif event.type==KEYDOWN:
                #teclas, menu de criar usuario e logar
                if self.menu==1 or self.menu==2:
                    if len(self.user)<21:
                        if 64<event.key<91 or 96<event.key<123 or event.key==95 or 47<event.key<58:
                            self.user=self.user+chr(event.key)
                    if event.key==K_BACKSPACE and len(self.user)>0:
                        self.user=self.user[0:-1]
                    if event.key==K_RETURN:
                        self.retur=1
                #teclas, menu parametros da calibraçao
                elif self.menu==5:
                    if 47<event.key<58:
                        if self.menu_flag==1:
                            self.alert_time=str(int(self.alert_time+chr(event.key)))
                        elif self.menu_flag==2:
                            self.cue_time=str(int(self.cue_time+chr(event.key)))
                        elif self.menu_flag==3:
                            self.task_time=str(int(self.task_time+chr(event.key)))
                        elif self.menu_flag==4:
                            self.pause_time=str(int(self.pause_time+chr(event.key)))
                        elif self.menu_flag==5:
                            self.feature_window_0=str(int(self.feature_window_0+chr(event.key)))
                        elif self.menu_flag==6:
                            self.feature_window_1=str(int(self.feature_window_1+chr(event.key)))
                        elif self.menu_flag==7:
                            self.number_trials=str(int(self.number_trials+chr(event.key)))
                    if event.key==K_BACKSPACE:
                        if len(self.alert_time)>0 and self.menu_flag==1:
                            self.alert_time=self.alert_time[0:-1]
                            if len(self.alert_time)==0:
                                self.alert_time="0"
                        elif len(self.cue_time)>0 and self.menu_flag==2:
                            self.cue_time=self.cue_time[0:-1]
                            if len(self.cue_time)==0:
                                self.cue_time="0"
                        elif len(self.task_time)>0 and self.menu_flag==3:
                            self.task_time=self.task_time[0:-1]
                            if len(self.task_time)==0:
                                self.task_time="0"
                        elif len(self.pause_time)>0 and self.menu_flag==4:
                            self.pause_time=self.pause_time[0:-1]
                            if len(self.pause_time)==0:
                                self.pause_time="0"
                        elif len(self.feature_window_0)>0 and self.menu_flag==5:
                            self.feature_window_0=self.feature_window_0[0:-1]
                            if len(self.feature_window_0)==0:
                                self.feature_window_0="0"
                        elif len(self.feature_window_1)>0 and self.menu_flag==6:
                            self.feature_window_1=self.feature_window_1[0:-1]
                            if len(self.feature_window_1)==0:
                                self.feature_window_1="0"
                        elif len(self.number_trials)>0 and self.menu_flag==7:
                            self.number_trials=self.number_trials[0:-1]
                            if len(self.number_trials)==0:
                                self.number_trials="0"
                    self.total_time=str(int(self.alert_time)+int(self.cue_time)+int(self.task_time)+int(self.pause_time))
                #teclas, menu parametros do teste
                elif self.menu==7:
                    if 47<event.key<58:
                        if self.menu_flag==1:
                            self.alert_time2=str(int(self.alert_time2+chr(event.key)))
                            
                        elif self.menu_flag==2:
                            self.cue_time2=str(int(self.cue_time2+chr(event.key)))
                            
                        elif self.menu_flag==3:
                            self.task_time2=str(int(self.task_time2+chr(event.key)))
                            
                        elif self.menu_flag==4:
                            self.pause_time2=str(int(self.pause_time2+chr(event.key)))
                            
                        elif self.menu_flag==5:
                            self.feature_window_02=str(int(self.feature_window_02+chr(event.key)))
                            
                        elif self.menu_flag==6:
                            self.feature_window_12=str(int(self.feature_window_12+chr(event.key)))
                            
                        elif self.menu_flag==7:
                            self.number_trials2=str(int(self.number_trials2+chr(event.key)))
                            
                    if event.key==K_BACKSPACE:
                        if len(self.alert_time2)>0 and self.menu_flag==1:
                            self.alert_time2=self.alert_time2[0:-1]
                            if len(self.alert_time2)==0:
                                self.alert_time2="0"
                                
                        elif len(self.cue_time2)>0 and self.menu_flag==2:
                            self.cue_time2=self.cue_time2[0:-1]
                            if len(self.cue_time2)==0:
                                self.cue_time2="0"
                                
                        elif len(self.task_time2)>0 and self.menu_flag==3:
                            self.task_time2=self.task_time2[0:-1]
                            if len(self.task_time2)==0:
                                self.task_time2="0"
                                
                        elif len(self.pause_time2)>0 and self.menu_flag==4:
                            self.pause_time2=self.pause_time2[0:-1]
                            if len(self.pause_time2)==0:
                                self.pause_time2="0"
                                
                        elif len(self.feature_window_02)>0 and self.menu_flag==5:
                            self.feature_window_02=self.feature_window_02[0:-1]
                            if len(self.feature_window_02)==0:
                                self.feature_window_02="0"
                                
                        elif len(self.feature_window_12)>0 and self.menu_flag==6:
                            self.feature_window_12=self.feature_window_12[0:-1]
                            if len(self.feature_window_12)==0:
                                self.feature_window_12="0"
                                
                        elif len(self.number_trials2)>0 and self.menu_flag==7:
                            self.number_trials2=self.number_trials2[0:-1]
                            if len(self.number_trials2)==0:
                                self.number_trials2="0"
                                
                    self.total_time2=str(int(self.alert_time2)+int(self.cue_time2)+int(self.task_time2)+int(self.pause_time2))
                #teclas mover o fantasma
                elif self.menu==11:
                    if event.key==K_RETURN:
                        self.menu=10
                        pg.mouse.set_visible(True)
                        self.ghostpos_x=0
                        self.ghostpos_y=0
#                       if platform.system()=='Linux':
#                           self.pub.publish('XY')
                        
                    elif event.key==K_RIGHT and self.ghostpos_x<5:
                        self.ghostpos_x+=1
                        
                    elif event.key==K_LEFT and self.ghostpos_x>-5:
                        self.ghostpos_x-=1
                        
                    elif event.key==K_DOWN and self.ghostpos_y<5:
                        self.ghostpos_y+=1
                        
                    elif event.key==K_UP and self.ghostpos_y>-5:
                        self.ghostpos_y-=1
                #teclas, menu parametros do treinamento
                elif self.menu==12:
                    if 47<event.key<58:
                        if self.menu_flag==1:
                            self.win_size=str(int(self.win_size+chr(event.key)))
                            
                        elif self.menu_flag==2:
                            self.win_displacement=str(int(self.win_displacement+chr(event.key)))

                    if event.key==K_BACKSPACE:
                        if len(self.win_size)>0 and self.menu_flag==1:
                            self.win_size=self.win_size[0:-1]
                            if len(self.win_size)==0:
                                self.win_size="0"
                                
                        elif len(self.win_displacement)>0 and self.menu_flag==2:
                            self.win_displacement=self.win_displacement[0:-1]
                            if len(self.win_displacement)==0:
                                self.win_displacement="0"                           
                    
    def draw(self):
        #atualiza posição do mouse utilizadas para os cliques
        self.mouse_x, self.mouse_y=pg.mouse.get_pos()
        self.mouse_x = self.mouse_x - self.screen_w//2
        self.mouse_y = self.mouse_y - self.screen_h//2
        #seleciona o menu atual para ser plotado
        if self.menu==0:      #login and create user
            self.menu_0()
        elif self.menu==1:   #create user
            self.menu_1()
        elif self.menu==2:   #login user
            self.menu_2()
        elif self.menu==3:
            self.menu_3()
            print 3
        elif self.menu==4:
            self.menu_4()
            print 4
        elif self.menu==5:
            self.menu_5()
        elif self.menu==6:
            self.menu_6()
        elif self.menu==7:
            self.menu_7()
        elif self.menu==10:
            self.menu_10()
        elif self.menu==11:
            self.menu_11()
        elif self.menu==12:
            self.menu_12()
        #print(self.menu)
        pg.display.update()  #pygame update display

    # Creates a new user             
    def users_file(self):
        temp=0
        try:
            # Tries to write the user info to folder Users
            file=open(self.users_list,'r')
        except:
            # If not possible, creates the folder
            os.mkdir(pathtousers)
            file=open(self.users_list,'w')
            file=open(self.users_list,'r')
        for line in file.readlines():
            if line == (str(self.user)+'\n'):
                if self.menu==1:
                    self.menu_flag=1
                    self.user=""
                elif self.menu==2:
                    self.menu=3
                    self.load_parameters_1()
                    self.load_parameters_2()
                    self.load_parameters_4()
                    self.menu_flag=0
#                   if platform.system()=='Linux':
#                       self.pub.publish('US' +self.user)
                break
                
        else:
            if self.menu==1:
                file=open(self.users_list,'a')
                file.write(str(self.user)+'\n')
                os.mkdir(self.pathtousers + self.user)
                self.menu_flag=2
            if self.menu==2:
                self.menu_flag=1
                
        file.close()
 
    #funcao que salva as marcações para os ensaios da calibraçao        
    def save_marcas(self):
        self.file0 = open(self.pathtousers + "%s/marcas.txt" %self.user,'w')
        for index,element in enumerate(self.lista0):
            self.file0.write(str(index*(int(self.alert_time)+int(self.cue_time)+int(self.task_time)+int(self.pause_time))*250/1000)+"\t"+str(element)+"\n")
        self.file0.close()
    
    #funcaçao que salva os parametros da calibraçao(tempo das imagens, janela a ser utilizada, numero de ensaios por classe, classes)
    def save_parameters_1(self):
        file=open(self.pathtousers + self.user + "/" + "parameters_1.txt",'w')
        file.write(self.alert_time + '\n')
        file.write(self.cue_time + '\n')
        file.write(self.task_time + '\n')
        file.write(self.pause_time + '\n')
        file.write(" ".join([str(x) for x in self.classes])+"\n")
        file.write(self.number_trials+"\n")
        file.write(self.feature_window_0+"\n")
        file.write(self.feature_window_1+"\n")      
        file.close()
    
    #funcao que carrega os parametros da calibraçao
    def load_parameters_1(self):
        try:
            file=open(self.pathtousers + self.user + "/" + "parameters_1.txt",'r')
        except:
            file=open(self.pathtousers + self.user + "/" + "parameters_1.txt",'w')
            self.save_parameters_1()
        file=open(self.pathtousers + self.user + "/" + "parameters_1.txt",'r')   
        self.alert_time = file.readline()[0:-1]
        self.cue_time = file.readline()[0:-1]
        self.task_time = file.readline()[0:-1]
        self.pause_time = file.readline()[0:-1]
        self.classes=[int(x) for x in file.readline()[0:-1].split(" ")]
        self.number_trials=file.readline()[0:-1]
        self.feature_window_0=file.readline()[0:-1]
        self.feature_window_1=file.readline()[0:-1]
        file.close()

    #funcao que salva os parametros do teste
    def save_parameters_2(self):
        file=open(self.pathtousers + self.user + "/" + "parameters_2.txt",'w')
        file.write(self.alert_time2 + '\n')
        file.write(self.cue_time2 + '\n')
        file.write(self.task_time2 + '\n')
        file.write(self.pause_time2 + '\n')
        file.write(" ".join([str(x) for x in self.classes2])+"\n")
        file.write(self.number_trials2+"\n")
        file.write(self.feature_window_02+"\n")
        file.write(self.feature_window_12+"\n")     
        file.close()

    #funcao que carrega os parametros do teste
    def load_parameters_2(self):
        try:
            file=open(self.pathtousers + self.user + "/" + "parameters_2.txt",'r')
        except:
            file=open(self.pathtousers + self.user + "/" + "parameters_2.txt",'w')
            self.save_parameters_2()
        file=open(self.pathtousers + self.user + "/" + "parameters_2.txt",'r')   
        self.alert_time2 = file.readline()[0:-1]
        self.cue_time2 = file.readline()[0:-1]
        self.task_time2 = file.readline()[0:-1]
        self.pause_time2 = file.readline()[0:-1]
        self.classes2=[int(x) for x in file.readline()[0:-1].split(" ")]
        self.number_trials2=file.readline()[0:-1]
        self.feature_window_02=file.readline()[0:-1]
        self.feature_window_12=file.readline()[0:-1]
        file.close()
            
    #funcao que salva os parametros do treinamento
    def save_parameters_4(self):
        file=open(self.pathtousers + self.user + "/" + "parameters_4.txt",'w')
        file.write(self.win_size + '\n')
        file.write(self.win_displacement + '\n')
        file.close()
        
    #funcao que carrega os parametros do treinamento
    def load_parameters_4(self):
        try:
            file=open(self.pathtousers + self.user + "/" + "parameters_4.txt",'r')
        except:
            file=open(self.pathtousers + self.user + "/" + "parameters_4.txt",'w')
            self.save_parameters_4()
        file=open(self.pathtousers + self.user + "/" + "parameters_4.txt",'r')   
        self.win_size = file.readline()[0:-1]
        self.win_displacement = file.readline()[0:-1]
        file.close()
        
    #funco que processa as mensagem enviadas pelo node manager para mover o elementro gráfico ou qual foi a classificaçao do teste 1
    def callback(self,msg):
        if msg.data[0:4]=="TY-1" and self.ghostpos_y>-5:
            self.ghostpos_y-=1
        elif msg.data[0:4]=="TY+1" and self.ghostpos_y<5:
            self.ghostpos_y+=1
        elif msg.data[0:4]=="TX-1" and self.ghostpos_x>-5:
            self.ghostpos_x-=1
        elif msg.data[0:4]=="TX+1" and self.ghostpos_x<5:
            self.ghostpos_x+=1
        elif msg.data[0:2]=="RT":
            self.RT=int(msg.data[2])
        elif msg.data[0:2]=="TT":
            self.T1_flag=0