# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 14:45:00 2016

@author: rafael
"""

#!/usr/bin/env python
import os, platform, sys, pygame as pg
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
        self.pathtoresources = globalpath + '/data/resources/'
        self.pathtousers = globalpath + '/data/users/'         
            
        #define variavel para tamanho da janela, utilizada para resize da janela
        self.screen_w, self.screen_h=self.screen.get_size()
        #define variavel para armazenar posiçao do mouse
        self.mouse_x, self.mouse_y=0,0

        #define variavel para a posiçao do fantasma(0,0 é o centro da dela)
        self.ghostpos_x=0
        self.ghostpos_y=0

        #carrega as imagens dos botoes
        self.bottoms()
        #carrega a lista de usuarios
        self.files()
        #carrega a fonte a ser utilizada
        self.fonts()
        #define os parametros padrão para calibração, teste de classificaçao e treinamento do usuario
        self.values()

        #define cor do fundo da tela
        self.color=(33,155,74)

        #cria loop
        self.loop()

    #funcao que carrega as imagens
    def bottoms(self):
        

        self.login=pg.image.load(self.pathtoresources +"login.png")
        self.new=pg.image.load(self.pathtoresources +"new.png")
        self.type_your_user=pg.image.load(self.pathtoresources +"type_your_user.png")
        self.space_to_type=pg.image.load(self.pathtoresources +"space_to_type.png")
        self.back=pg.image.load(self.pathtoresources +"back.png")
        self.create=pg.image.load(self.pathtoresources +"create.png")
        self.enter=pg.image.load(self.pathtoresources +"enter.png")
        self.user_already_exists=pg.image.load(self.pathtoresources +"user_already_exists.png")
        self.user_does_not_exist=pg.image.load(self.pathtoresources +"user_does_not_exist.png")
        self.user_created=pg.image.load(self.pathtoresources +"user_created.png")
        self.calibration=pg.image.load(self.pathtoresources +"calibration.png")
        self.options=pg.image.load(self.pathtoresources +"options.png")
        self.test_1=pg.image.load(self.pathtoresources +"test_1.png")
        self.test_2=pg.image.load(self.pathtoresources +"test_2.png")
        self.test_game_1=pg.image.load(self.pathtoresources +"test_game_1.png")
        self.alert=pg.image.load(self.pathtoresources +"alert.png")
        self.cue=pg.image.load(self.pathtoresources +"cue.png")
        self.task=pg.image.load(self.pathtoresources +"task.png")
        self.pause=pg.image.load(self.pathtoresources +"pause.png")
        self.total=pg.image.load(self.pathtoresources +"total.png")
        self.bb2=pg.image.load(self.pathtoresources +"blank_box_2.png")
        self.right_hand=pg.image.load(self.pathtoresources +"right_hand.png")
        self.left_hand=pg.image.load(self.pathtoresources +"left_hand.png")
        self.feet=pg.image.load(self.pathtoresources +"feet.png")
        self.bb1=pg.image.load(self.pathtoresources +"blank_box.png")
        self.mb1=pg.image.load(self.pathtoresources +"marked_box.png")
        self.feature_window=pg.image.load(self.pathtoresources +"feature_window.png")
        self.trials_per_class=pg.image.load(self.pathtoresources +"trials_per_class.png")
        self.total_time_calibration=pg.image.load(self.pathtoresources +"total_time.png")
        self.start=pg.image.load(self.pathtoresources +"start.png")
        self.signs=pg.image.load(self.pathtoresources +"signs.png")
        self.beep = pg.mixer.Sound(self.pathtoresources +"beep.ogg")
        self.ghost0=pg.image.load(self.pathtoresources +"red_ghost.png")
        self.window_size=pg.image.load(self.pathtoresources +"window_size.png")         
        self.displacement=pg.image.load(self.pathtoresources +"displacement.png")   
        
    #funcao que carrega a lista de usuarios
    def files(self):
        self.users_list=self.pathtousers+"users_list.txt"

    #funcao que carrea a fonte
    def fonts(self):
        self.fonte=pg.font.Font(self.pathtoresources +"ubuntu.bold.ttf", 20)

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
            
    #login and create user screen    
    def menu_0(self):  
        self.screen.fill(self.color)
        self.screen.blit(self.login,(self.screen_w//2 - 55,self.screen_h//2 - 20 - 30))
        self.screen.blit(self.new,(self.screen_w//2 - 55,self.screen_h//2 - 20 + 30))
        if pg.mouse.get_pressed()==(1,0,0): #mouse pressed event bottom left
            print 'pressed'
            if -55<self.mouse_x<55:              #cursor                -55 < x_pos  < +55
                if -50<self.mouse_y<-10:         #cursor                -50 < y_pos  <  -10    
                    self.menu=2 
                elif 10<self.mouse_y<50:         #cursor                 10 < y_pos  < +50
                    self.menu=1
    
    #create user screen
    def menu_1(self):
        self.screen.fill(self.color)
        self.screen.blit(self.type_your_user,(self.screen_w//2 - 110,self.screen_h//2 - 20 - 30)) #size (220,40)  delay (-110 + 0, -20 -30)
        self.screen.blit(self.space_to_type,(self.screen_w//2 - 110,self.screen_h//2 - 20 + 30)) #size (220,40)  delay (-110 + 0, -20 +30)
        self.screen.blit(self.back,(self.screen_w//2-20-110-110,self.screen_h//2 - 20 + 30)) #size (110,40)  delay (-20 -110 - 110 + 0, -20 +30)
        self.screen.blit(self.create,(self.screen_w//2+20+110,self.screen_h//2 - 20 + 30)) #size (110,40)  delay (-20 -110 - 110 + 0, -20 +30)
        self.nickname=self.fonte.render(str(self.user), 1, (255,255,255))
        self.screen.blit(self.nickname,(self.screen_w//2 - self.nickname.get_width()//2,self.screen_h//2 - 20 +50 - self.nickname.get_height()//2))
        if pg.mouse.get_pressed()==(1,0,0) and self.mouse_flag==0: #mouse pressed event bottom left
            self.mouse_flag=1
            print(self.mouse_flag)
            if 10<self.mouse_y<50:              #cursor                -55 < x_pos  < +55
                if -240<self.mouse_x<-130:         #cursor                -50 < y_pos  <  -10    
                    self.menu=0
                    self.menu_flag=0
                    self.user=""
                elif 130<self.mouse_x<240:         #cursor                 10 < y_pos  < +50
                    self.users_file()
                    
        if pg.mouse.get_pressed()==(0,0,0):
            self.mouse_flag=0
        if self.menu_flag==1:
            self.screen.blit(self.user_already_exists,(self.screen_w//2 -120,self.screen_h//2 - 20 + 90)) #size (240,40)  delay (-120 + 0, -20 +90)
        elif self.menu_flag==2:
            self.screen.blit(self.user_created,(self.screen_w//2 -120,self.screen_h//2 - 20 + 90)) #size (240,40)  delay (-120 + 0, -20 +90)                        
                    
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
    
    # Login Screen
    def menu_2(self):
        self.screen.fill(self.color)
        self.screen.blit(self.type_your_user,(self.screen_w//2 - 110,self.screen_h//2 - 20 - 30)) #size (220,40)  delay (-110 + 0, -20 -30)
        self.screen.blit(self.space_to_type,(self.screen_w//2 - 110,self.screen_h//2 - 20 + 30)) #size (220,40)  delay (-110 + 0, -20 +30)
        self.screen.blit(self.back,(self.screen_w//2 -20 -110 - 110,self.screen_h//2 - 20 + 30)) #size (110,40)  delay (-20 - 110 - 110 + 0, -20 +30)           
        self.screen.blit(self.enter,(self.screen_w//2+20+110,self.screen_h//2 - 20 + 30)) #size (110,40)  delay (-20 -110 - 110 + 0, -20 +30)
        self.nickname=self.fonte.render(str(self.user), 1, (255,255,255))
        self.screen.blit(self.nickname,(self.screen_w//2 - self.nickname.get_width()//2,self.screen_h//2 - 20 +50 - self.nickname.get_height()//2))     
        if pg.mouse.get_pressed()==(1,0,0)  and self.mouse_flag==0: #mouse pressed event bottom left
            self.mouse_flag=1
            if 10<self.mouse_y<50:              #cursor                -55 < x_pos  < +55
                if -240<self.mouse_x<-130:         #cursor                -50 < y_pos  <  -10    
                    self.menu=0
                    self.menu_flag=0
                    self.user=""
                elif 130<self.mouse_x<240:         #cursor                 10 < y_pos  < +50
                    self.users_file()

        if pg.mouse.get_pressed()==(0,0,0):
            self.mouse_flag=0
        if self.menu_flag==1:
            self.screen.blit(self.user_does_not_exist,(self.screen_w//2 -120,self.screen_h//2 - 20 + 90)) #size (240,40)  delay (-120 + 0, -20 +90)

    # User screen (after logging in)
    def menu_3(self):
        self.screen.fill(self.color)
        self.screen.blit(self.calibration,(self.screen_w//2 -110,self.screen_h//2 - 20 - 90)) #size (220,40)  delay (- 110 + 0, -20 -90)
        self.screen.blit(self.options,(self.screen_w//2 +110 + 20,self.screen_h//2 - 20 - 90)) #size (110,40)  delay (110 + 20, -20 -90)
        
        self.screen.blit(self.test_1,(self.screen_w//2 -55,self.screen_h//2 - 20 - 30)) #size (110,40)  delay (-55 + 0, -20 -30)
        self.screen.blit(self.options,(self.screen_w//2 +110 + 20,self.screen_h//2 - 20 - 30)) #size (110,40)  delay (-55 + 0, -20 -30)
        
        #self.screen.blit(self.test_2,(self.screen_w//2 -55,self.screen_h//2 - 20 +30)) #size (110,40)  delay (-55 + 0, -20 +30)
        #self.screen.blit(self.options,(self.screen_w//2 +110 + 20,self.screen_h//2 - 20 +30)) #size (110,40)  delay (-55 + 0, -20 +30)

        self.screen.blit(self.test_game_1,(self.screen_w//2 -110,self.screen_h//2 - 20 +90)) #size (220,40)  delay (- 110 + 0, -20 +90)
        self.screen.blit(self.options,(self.screen_w//2 +110 + 20,self.screen_h//2 - 20 +90)) #size (110,40)  delay (-55 + 0, -20 +90)  
        
        self.screen.blit(self.back,(self.screen_w//2 -55,self.screen_h//2 - 20 + 150)) #size (110,40)  delay (-20 - 110 - 110 + 0, -20 +30)
        
        if pg.mouse.get_pressed()==(1,0,0)  and self.mouse_flag==0: #mouse pressed event bottom left
            self.mouse_flag=1
            if -110<self.mouse_y<-70:
                if -110<self.mouse_x<110:
                    self.menu=4
                elif 130<self.mouse_x<240:
                    self.menu=5
                    
            elif -50<self.mouse_y<-10:
                if -55<self.mouse_x<55:
                    self.menu=6
                elif 130<self.mouse_x<240:
                    self.menu=7
                
            elif 70<self.mouse_y<110:
                if -110<self.mouse_x<110:
                    self.menu=10
                elif 130<self.mouse_x<240:
                    self.menu=12

            elif 130<self.mouse_y<170:
                if -55<self.mouse_x<55:
                    self.menu=0
                    self.user=""
                    self.values()
                    
        if pg.mouse.get_pressed()==(0,0,0):
            self.mouse_flag=0

    # Calibration Screen
    def menu_4(self):
        self.screen.fill(self.color)
        self.screen.blit(self.start,(self.screen_w//2 - 110,self.screen_h//2 - 20 - 30)) #size (220,40)  delay (-110 + 0, -20 -30)
        self.screen.blit(self.back,(self.screen_w//2 -55,self.screen_h//2 - 20 + 150)) #size (110,40)  delay (-20 - 110 - 110 + 0, -20 +30)
        
        if pg.mouse.get_pressed()==(1,0,0)  and self.mouse_flag==0: #mouse pressed event bottom left
            self.mouse_flag=1
            #botao voltar
            if 130<self.mouse_y<170:              #cursor                -55 < x_pos  < +55
                if -55<self.mouse_x<55:         #cursor                -50 < y_pos  <  -10    
                    self.menu=3
            #botao start        
            elif -50<self.mouse_y<-10:
                if -110<self.mouse_x<110:         #cursor                -50 < y_pos  <  -10 
                    #gera lista de ensaios  
                    self.lista0=self.classes*int(self.number_trials)
                    shuffle(self.lista0) #embaralha lista
                    self.save_marcas() #salva as marcações
                    #envia mensagem para o manager indicando a calibraçao
#                   if platform.system()=='Linux':
#                       self.pub.publish('NC')
                    pg.mouse.set_visible(False)
                    self.screen.fill((127,127,127))
                    pg.display.update()
                    pg.time.wait(5000)
                    #envia mensagem para o manager indicando que pode comecar a tarefa de calibraçao
#                   if platform.system()=='Linux':
#                       self.pub.publish('XX')
                    #apresenta as imagens para todos os ensaios da lista
                    for element in self.lista0:
                        self.task_(element)
                    #if platform.system()=='Linux':
                    #   self.pub.publish('XY')
                    pg.mouse.set_visible(True)
                    self.menu=3
                    
        if pg.mouse.get_pressed()==(0,0,0):
            self.mouse_flag=0
            
    #funcao que salva as marcações para os ensaios da calibraçao        
    def save_marcas(self):
        self.file0 = open(self.pathtousers + "%s/marcas.txt" %self.user,'w')
        for index,element in enumerate(self.lista0):
            self.file0.write(str(index*(int(self.alert_time)+int(self.cue_time)+int(self.task_time)+int(self.pause_time))*250/1000)+"\t"+str(element)+"\n")
        self.file0.close()
        
    #funcao que para cada tipo de tarefa plota as imagens dos ensaios
    def task_(self,i):
        i+=1
        self.beep.play()
        self.screen.fill((127,127,127))
        self.screen.blit(self.signs,(self.screen_w//2 - 158, self.screen_h//2 - 148),Rect(0,0,316,296))
        pg.display.update()
        pg.time.wait(int(self.alert_time))
        self.screen.fill((127,127,127))
        pg.time.wait(100)
        self.screen.blit(self.signs,(self.screen_w//2 - 158, self.screen_h//2 - 148),Rect(i*316,0,316,296))
        pg.display.update()
        pg.time.wait(int(self.cue_time))
        self.screen.fill((127,127,127))
        pg.display.update()
        pg.time.wait(int(self.task_time))
        self.screen.blit(self.signs,(self.screen_w//2 - 158, self.screen_h//2 - 148),Rect(5*316,0,316,296))
        pg.display.update()
        pg.time.wait(int(self.pause_time))          
        
    # Calibration Menu 
    def menu_5(self):
        self.screen.fill(self.color)
        self.screen.blit(self.alert,(self.screen_w//2 -110*4,self.screen_h//2 - 20 - 150)) #size (220,40)  delay (- 110 + 0, -20 -90)
        self.screen.blit(self.cue,(self.screen_w//2 -110*4,self.screen_h//2 - 20 - 90)) #size (220,40)  delay (- 110 + 0, -20 -90)
        self.screen.blit(self.task,(self.screen_w//2 -110*4,self.screen_h//2 - 20 - 30)) #size (220,40)  delay (- 110 + 0, -20 -90)
        self.screen.blit(self.pause,(self.screen_w//2 -110*4,self.screen_h//2 - 20 + 30)) #size (220,40)  delay (- 110 + 0, -20 -90)
        self.screen.blit(self.total,(self.screen_w//2 -110*4,self.screen_h//2 - 20 + 90)) #size (220,40)  delay (- 110 + 0, -20 -90)
        self.screen.blit(self.back,(self.screen_w//2 -55,self.screen_h//2 - 20 + 150)) #size (110,40)  delay (-20 - 110 - 110 + 0, -20 +30)
        
        self.screen.blit(self.total_time_calibration,(self.screen_w//2 +110*2,self.screen_h//2 +140)) #size (110,40)  delay (-20 - 110 - 110 + 0, -20 +30)
        self.screen.blit(self.bb2,(self.screen_w//2 +110*2+55,self.screen_h//2 +140+40+10)) #size (220,40)  delay (- 110 + 0, -20 -90)
        
        self.total_time_calibration_=self.fonte.render(str((int(self.total_time)*int(self.number_trials)*len(self.classes)//6000)/10   )+" min", 1, (255,255,255))
        self.screen.blit(self.total_time_calibration_,(self.screen_w//2 - self.total_time_calibration_.get_width()//2+110*3,self.screen_h//2 +210 - self.total_time_calibration_.get_height()//2))
        
        self.screen.blit(self.bb2,(self.screen_w//2 -110*3+20,self.screen_h//2 - 20 - 150)) #size (220,40)  delay (- 110 + 0, -20 -90)
        self.screen.blit(self.bb2,(self.screen_w//2 -110*3+20,self.screen_h//2 - 20 - 90)) #size (220,40)  delay (- 110 + 0, -20 -90)
        self.screen.blit(self.bb2,(self.screen_w//2 -110*3+20,self.screen_h//2 - 20 - 30)) #size (220,40)  delay (- 110 + 0, -20 -90)
        self.screen.blit(self.bb2,(self.screen_w//2 -110*3+20,self.screen_h//2 - 20 + 30)) #size (220,40)  delay (- 110 + 0, -20 -90)
        self.screen.blit(self.bb2,(self.screen_w//2 -110*3+20,self.screen_h//2 - 20 + 90)) #size (220,40)  delay (- 110 + 0, -20 -90)
        
        self.alert_time_=self.fonte.render(str(self.alert_time)+" ms", 1, (255,255,255))
        self.cue_time_=self.fonte.render(str(self.cue_time)+" ms", 1, (255,255,255))
        self.task_time_=self.fonte.render(str(self.task_time)+" ms" ,1, (255,255,255))
        self.pause_time_=self.fonte.render(str(self.pause_time)+" ms", 1, (255,255,255))
        self.total_time_=self.fonte.render(str(self.total_time)+" ms", 1, (255,255,255))
        
        self.screen.blit(self.alert_time_,(self.screen_w//2 - self.alert_time_.get_width()//2-110*2+20-55,self.screen_h//2 -150 - self.alert_time_.get_height()//2))
        self.screen.blit(self.cue_time_,(self.screen_w//2 - self.cue_time_.get_width()//2-110*2+20-55,self.screen_h//2 -90 - self.cue_time_.get_height()//2))           
        self.screen.blit(self.task_time_,(self.screen_w//2 - self.task_time_.get_width()//2-110*2+20-55,self.screen_h//2 -30 - self.task_time_.get_height()//2))    
        self.screen.blit(self.pause_time_,(self.screen_w//2 - self.pause_time_.get_width()//2-110*2+20-55,self.screen_h//2 +30 - self.pause_time_.get_height()//2)) 
        self.screen.blit(self.total_time_,(self.screen_w//2 - self.total_time_.get_width()//2-110*2+20-55,self.screen_h//2 +90 - self.total_time_.get_height()//2)) 
        
        self.screen.blit(self.right_hand,(self.screen_w//2 -110,self.screen_h//2 - 20 - 150)) #size (220,40)  delay (- 110 + 0, -20 -90)
        self.screen.blit(self.left_hand,(self.screen_w//2 -110,self.screen_h//2 - 20 - 90)) #size (220,40)  delay (- 110 + 0, -20 -90)
        self.screen.blit(self.feet,(self.screen_w//2 -110,self.screen_h//2 - 20 - 30)) #size (220,40)  delay (- 110 + 0, -20 -90)
        
        self.screen.blit(self.feature_window,(self.screen_w//2 +110*2,self.screen_h//2 - 20 -150)) #size (220,40)  delay (- 110 + 0, -20 -90)
        
        self.screen.blit(self.bb2,(self.screen_w//2 +110*2-10,self.screen_h//2 - 20 -90)) #size (220,40)  delay (- 110 + 0, -20 -90)
        self.screen.blit(self.bb2,(self.screen_w//2 +110*3+10,self.screen_h//2 - 20 -90)) #size (220,40)  delay (- 110 + 0, -20 -90)
        
        self.feature_window_0_=self.fonte.render(str(self.feature_window_0)+" ms", 1, (255,255,255))
        self.feature_window_1_=self.fonte.render(str(self.feature_window_1)+" ms", 1, (255,255,255))
        
        self.screen.blit(self.feature_window_0_,(self.screen_w//2 - self.feature_window_0_.get_width()//2+110*2-10+55,self.screen_h//2 -90 - self.feature_window_0_.get_height()//2))
        self.screen.blit(self.feature_window_1_,(self.screen_w//2 - self.feature_window_1_.get_width()//2+110*3+10+55,self.screen_h//2 -90 - self.feature_window_1_.get_height()//2))   
        
        self.screen.blit(self.trials_per_class,(self.screen_w//2 +110*2,self.screen_h//2 - 20 +30)) #size (220,40)  delay (- 110 + 0, -20 -90)
        self.screen.blit(self.bb2,(self.screen_w//2 +110*2+55,self.screen_h//2 - 20 + 90)) #size (220,40)  delay (- 110 + 0, -20 -90)
        
        self.number_trials_=self.fonte.render(str(self.number_trials), 1, (255,255,255))
        self.screen.blit(self.number_trials_,(self.screen_w//2 - self.number_trials_.get_width()//2+110*3,self.screen_h//2 +90 - self.number_trials_.get_height()//2))
        
        if 0 in self.classes:
            self.screen.blit(self.mb1,(self.screen_w//2 +110+20,self.screen_h//2 - 20 - 150)) #size (220,40)  delay (- 110 + 0, -20 -90)
        else:
            self.screen.blit(self.bb1,(self.screen_w//2 +110+20,self.screen_h//2 - 20 - 150)) #size (220,40)  delay (- 110 + 0, -20 -90)
        if 1 in self.classes:
            self.screen.blit(self.mb1,(self.screen_w//2 +110+20,self.screen_h//2 - 20 - 90)) #size (220,40)  delay (- 110 + 0, -20 -90)
        else:
            self.screen.blit(self.bb1,(self.screen_w//2 +110+20,self.screen_h//2 - 20 - 90)) #size (220,40)  delay (- 110 + 0, -20 -90)
        if 2 in self.classes:
            self.screen.blit(self.mb1,(self.screen_w//2 +110+20,self.screen_h//2 - 20 - 30)) #size (220,40)  delay (- 110 + 0, -20 -90)
        else:
            self.screen.blit(self.bb1,(self.screen_w//2 +110+20,self.screen_h//2 - 20 - 30)) #size (220,40)  delay (- 110 + 0, -20 -90)
        
        if pg.mouse.get_pressed()==(1,0,0)  and self.mouse_flag==0: #mouse pressed event bottom left
            self.mouse_flag=1
            if -310<self.mouse_x<-200:
                if -170<self.mouse_y<-130:
                    self.menu_flag=1
                elif -110<self.mouse_y<-70:
                    self.menu_flag=2
                elif -50<self.mouse_y<-10:
                    self.menu_flag=3
                elif 10<self.mouse_y<50:
                    self.menu_flag=4
                else:
                    self.menu_flag=0
                    
            elif 130<self.mouse_x<170:
                if -170<self.mouse_y<-130:
                    if 0 in self.classes:
                        self.classes.remove(0)
                    else:
                        self.classes.insert(0,0)
                elif -110<self.mouse_y<-70:
                    if 1 in self.classes:
                        self.classes.remove(1)
                    else:
                        self.classes.insert(1,1)
                elif -50<self.mouse_y<-10:
                    if 2 in self.classes:
                        self.classes.remove(2)
                    else:
                        self.classes.insert(2,2)
            elif -110<self.mouse_y<-70:
                if 210<self.mouse_x<320:
                    self.menu_flag=5
                elif 340<self.mouse_x<450:
                    self.menu_flag=6
                else:
                    self.menu_flag=0
                
            elif 70<self.mouse_y<110:
                if 275<self.mouse_x<275+110:
                    self.menu_flag=7
                else:self.menu_flag=0
                    
            elif 130<self.mouse_y<170:
                if -55<self.mouse_x<55:
                    self.menu=3
                    self.save_parameters_1()
                    self.menu_flag=0
                    
        if pg.mouse.get_pressed()==(0,0,0):
            self.mouse_flag=0

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
    
    # Game test 1 - Only ghost wandering on black screen
    def menu_6(self):
        self.screen.fill(self.color)
        self.screen.blit(self.start,(self.screen_w//2 - 110,self.screen_h//2 - 20 - 30)) #size (220,40)  delay (-110 + 0, -20 -30)
        self.screen.blit(self.back,(self.screen_w//2 -55,self.screen_h//2 - 20 + 150)) #size (110,40)  delay (-20 - 110 - 110 + 0, -20 +30)
        
        if pg.mouse.get_pressed()==(1,0,0)  and self.mouse_flag==0: #mouse pressed event bottom left
            self.mouse_flag=1
            if 130<self.mouse_y<170:              #cursor                -55 < x_pos  < +55
                if -55<self.mouse_x<55:         #cursor                -50 < y_pos  <  -10    
                    self.menu=3
            elif -50<self.mouse_y<-10:
                if -110<self.mouse_x<110:         #cursor                -50 < y_pos  <  -10 
                    self.lista02=self.classes2*int(self.number_trials2)
                    shuffle(self.lista02)
                    self.save_marcas2()
#                   if platform.system()=='Linux':
#                       self.pub.publish('T1')
                    pg.mouse.set_visible(False)
                    self.screen.fill((127,127,127))
                    pg.display.update()
                    file=open(self.pathtousers + self.user + "/" + "results_t1.txt",'w')
                    tax_right=0
                    pg.time.wait(5000)
                    for element in self.lista02:
                        self.T1_flag=1
#                       if platform.system()=='Linux':
#                           self.pub.publish('XX')
                        self.task_2(element)
                        pg.time.wait(500)
                        while self.T1_flag:
                            pass
                        self.screen.fill((127,127,127))
                        pg.display.update()
                        if (self.RT==0   and element==0) or (self.RT==1 and element==1):
                            self.ans=self.fonte.render("Right", 1, (30,30,250))
                            tax_right+=1
                        elif (self.RT==0     and element==1) or (self.RT==1 and element==0):
                            self.ans=self.fonte.render("Wrong", 1, (250,30,30))
                        elif self.RT==-1:
                            self.ans=self.fonte.render("Failure", 1, (250,30,30))
                        self.screen.blit(self.ans,(self.screen_w//2 - self.ans.get_width()//2,self.screen_h//2 - self.ans.get_height()//2))
                        self.RT=-1
                        pg.display.update()
                        pg.time.wait(3000)
                    file.write(str(tax_right*100/len(self.lista02))+"\n")       
                    file.close()
                        
                        
                        
                    pg.mouse.set_visible(True)
                    self.menu=3
                    
        if pg.mouse.get_pressed()==(0,0,0):
            self.mouse_flag=0
        
    #funcao que para cada tipo de tarefa plota as imagens dos ensaios do teste  
    def task_2(self,i):
        i+=1
        self.beep.play()
        self.screen.fill((127,127,127))
        self.screen.blit(self.signs,(self.screen_w//2 - 158, self.screen_h//2 - 148),Rect(0,0,316,296))
        pg.display.update()
        pg.time.wait(int(self.alert_time2))
        self.screen.fill((127,127,127))
        pg.time.wait(100)
        self.screen.blit(self.signs,(self.screen_w//2 - 158, self.screen_h//2 - 148),Rect(i*316,0,316,296))
        pg.display.update()
        pg.time.wait(int(self.cue_time2))
        self.screen.fill((127,127,127))
        pg.display.update()
        pg.time.wait(int(self.task_time2))
        self.screen.blit(self.signs,(self.screen_w//2 - 158, self.screen_h//2 - 148),Rect(5*316,0,316,296))
        pg.display.update()
        pg.time.wait(int(self.pause_time2))
        
    # Classification Menu
    def menu_7(self):
        self.screen.fill(self.color)
        self.screen.blit(self.alert,(self.screen_w//2 -110*4,self.screen_h//2 - 20 - 150)) #size (220,40)  delay (- 110 + 0, -20 -90)
        self.screen.blit(self.cue,(self.screen_w//2 -110*4,self.screen_h//2 - 20 - 90)) #size (220,40)  delay (- 110 + 0, -20 -90)
        self.screen.blit(self.task,(self.screen_w//2 -110*4,self.screen_h//2 - 20 - 30)) #size (220,40)  delay (- 110 + 0, -20 -90)
        self.screen.blit(self.pause,(self.screen_w//2 -110*4,self.screen_h//2 - 20 + 30)) #size (220,40)  delay (- 110 + 0, -20 -90)
        self.screen.blit(self.total,(self.screen_w//2 -110*4,self.screen_h//2 - 20 + 90)) #size (220,40)  delay (- 110 + 0, -20 -90)
        self.screen.blit(self.back,(self.screen_w//2 -55,self.screen_h//2 - 20 + 150)) #size (110,40)  delay (-20 - 110 - 110 + 0, -20 +30)
        

        self.screen.blit(self.bb2,(self.screen_w//2 -110*3+20,self.screen_h//2 - 20 - 150)) #size (220,40)  delay (- 110 + 0, -20 -90)
        self.screen.blit(self.bb2,(self.screen_w//2 -110*3+20,self.screen_h//2 - 20 - 90)) #size (220,40)  delay (- 110 + 0, -20 -90)
        self.screen.blit(self.bb2,(self.screen_w//2 -110*3+20,self.screen_h//2 - 20 - 30)) #size (220,40)  delay (- 110 + 0, -20 -90)
        self.screen.blit(self.bb2,(self.screen_w//2 -110*3+20,self.screen_h//2 - 20 + 30)) #size (220,40)  delay (- 110 + 0, -20 -90)
        self.screen.blit(self.bb2,(self.screen_w//2 -110*3+20,self.screen_h//2 - 20 + 90)) #size (220,40)  delay (- 110 + 0, -20 -90)
        
        self.alert_time_2=self.fonte.render(str(self.alert_time2)+" ms", 1, (255,255,255))
        self.cue_time_2=self.fonte.render(str(self.cue_time2)+" ms", 1, (255,255,255))
        self.task_time_2=self.fonte.render(str(self.task_time2)+" ms" ,1, (255,255,255))
        self.pause_time_2=self.fonte.render(str(self.pause_time2)+" ms", 1, (255,255,255))
        self.total_time_2=self.fonte.render(str(self.total_time2)+" ms", 1, (255,255,255))
        
        self.screen.blit(self.alert_time_2,(self.screen_w//2 - self.alert_time_2.get_width()//2-110*2+20-55,self.screen_h//2 -150 - self.alert_time_2.get_height()//2))
        self.screen.blit(self.cue_time_2,(self.screen_w//2 - self.cue_time_2.get_width()//2-110*2+20-55,self.screen_h//2 -90 - self.cue_time_2.get_height()//2))            
        self.screen.blit(self.task_time_2,(self.screen_w//2 - self.task_time_2.get_width()//2-110*2+20-55,self.screen_h//2 -30 - self.task_time_2.get_height()//2)) 
        self.screen.blit(self.pause_time_2,(self.screen_w//2 - self.pause_time_2.get_width()//2-110*2+20-55,self.screen_h//2 +30 - self.pause_time_2.get_height()//2))  
        self.screen.blit(self.total_time_2,(self.screen_w//2 - self.total_time_2.get_width()//2-110*2+20-55,self.screen_h//2 +90 - self.total_time_2.get_height()//2))  
        
        self.screen.blit(self.right_hand,(self.screen_w//2 -110,self.screen_h//2 - 20 - 150)) #size (220,40)  delay (- 110 + 0, -20 -90)
        self.screen.blit(self.left_hand,(self.screen_w//2 -110,self.screen_h//2 - 20 - 90)) #size (220,40)  delay (- 110 + 0, -20 -90)
        self.screen.blit(self.feet,(self.screen_w//2 -110,self.screen_h//2 - 20 - 30)) #size (220,40)  delay (- 110 + 0, -20 -90)
        
        self.screen.blit(self.feature_window,(self.screen_w//2 +110*2,self.screen_h//2 - 20 -150)) #size (220,40)  delay (- 110 + 0, -20 -90)
        
        self.screen.blit(self.bb2,(self.screen_w//2 +110*2-10,self.screen_h//2 - 20 -90)) #size (220,40)  delay (- 110 + 0, -20 -90)
        self.screen.blit(self.bb2,(self.screen_w//2 +110*3+10,self.screen_h//2 - 20 -90)) #size (220,40)  delay (- 110 + 0, -20 -90)
        
        self.feature_window_0_2=self.fonte.render(str(self.feature_window_02)+" ms", 1, (255,255,255))
        self.feature_window_1_2=self.fonte.render(str(self.feature_window_12)+" ms", 1, (255,255,255))
        
        self.screen.blit(self.feature_window_0_2,(self.screen_w//2 - self.feature_window_0_2.get_width()//2+110*2-10+55,self.screen_h//2 -90 - self.feature_window_0_2.get_height()//2))
        self.screen.blit(self.feature_window_1_2,(self.screen_w//2 - self.feature_window_1_2.get_width()//2+110*3+10+55,self.screen_h//2 -90 - self.feature_window_1_2.get_height()//2))    
        
        self.screen.blit(self.trials_per_class,(self.screen_w//2 +110*2,self.screen_h//2 - 20 +30)) #size (220,40)  delay (- 110 + 0, -20 -90)
        self.screen.blit(self.bb2,(self.screen_w//2 +110*2+55,self.screen_h//2 - 20 + 90)) #size (220,40)  delay (- 110 + 0, -20 -90)
        
        self.number_trials_2=self.fonte.render(str(self.number_trials2), 1, (255,255,255))
        self.screen.blit(self.number_trials_2,(self.screen_w//2 - self.number_trials_2.get_width()//2+110*3,self.screen_h//2 +90 - self.number_trials_2.get_height()//2))
        
        if 0 in self.classes2:
            self.screen.blit(self.mb1,(self.screen_w//2 +110+20,self.screen_h//2 - 20 - 150)) #size (220,40)  delay (- 110 + 0, -20 -90)
        else:
            self.screen.blit(self.bb1,(self.screen_w//2 +110+20,self.screen_h//2 - 20 - 150)) #size (220,40)  delay (- 110 + 0, -20 -90)
        if 1 in self.classes2:
            self.screen.blit(self.mb1,(self.screen_w//2 +110+20,self.screen_h//2 - 20 - 90)) #size (220,40)  delay (- 110 + 0, -20 -90)
        else:
            self.screen.blit(self.bb1,(self.screen_w//2 +110+20,self.screen_h//2 - 20 - 90)) #size (220,40)  delay (- 110 + 0, -20 -90)
        if 2 in self.classes2:
            self.screen.blit(self.mb1,(self.screen_w//2 +110+20,self.screen_h//2 - 20 - 30)) #size (220,40)  delay (- 110 + 0, -20 -90)
        else:
            self.screen.blit(self.bb1,(self.screen_w//2 +110+20,self.screen_h//2 - 20 - 30)) #size (220,40)  delay (- 110 + 0, -20 -90)
        
        if pg.mouse.get_pressed()==(1,0,0)  and self.mouse_flag==0: #mouse pressed event bottom left
            self.mouse_flag=1
            if -310<self.mouse_x<-200:
                if -170<self.mouse_y<-130:
                    self.menu_flag=1
                elif -110<self.mouse_y<-70:
                    self.menu_flag=2
                elif -50<self.mouse_y<-10:
                    self.menu_flag=3
                elif 10<self.mouse_y<50:
                    self.menu_flag=4
                else:
                    self.menu_flag=0
                    
            elif 130<self.mouse_x<170:
                if -170<self.mouse_y<-130:
                    if 0 in self.classes2:
                        self.classes2.remove(0)
                    else:
                        self.classes2.insert(0,0)
                elif -110<self.mouse_y<-70:
                    if 1 in self.classes2:
                        self.classes2.remove(1)
                    else:
                        self.classes2.insert(1,1)
                elif -50<self.mouse_y<-10:
                    if 2 in self.classes2:
                        self.classes2.remove(2)
                    else:
                        self.classes2.insert(2,2)
            elif -110<self.mouse_y<-70:
                if 210<self.mouse_x<320:
                    self.menu_flag=5
                elif 340<self.mouse_x<450:
                    self.menu_flag=6
                else:
                    self.menu_flag=0
                
            elif 70<self.mouse_y<110:
                if 275<self.mouse_x<275+110:
                    self.menu_flag=7
                else:self.menu_flag=0
                    
            elif 130<self.mouse_y<170:
                if -55<self.mouse_x<55:
                    self.menu=3
                    self.save_parameters_2()
                    self.menu_flag=0
                    
        if pg.mouse.get_pressed()==(0,0,0):
            self.mouse_flag=0

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
            
    #menu do elemento gráfico (prepara e envia mensagem ao manager)
    def menu_10(self):
        self.screen.fill(self.color)
        self.screen.blit(self.start,(self.screen_w//2 - 110,self.screen_h//2 - 20 - 30)) #size (220,40)  delay (-110 + 0, -20 -30)
        self.screen.blit(self.back,(self.screen_w//2 -55,self.screen_h//2 - 20 + 150)) #size (110,40)  delay (-20 - 110 - 110 + 0, -20 +30)
        
        if pg.mouse.get_pressed()==(1,0,0)  and self.mouse_flag==0: #mouse pressed event bottom left
            self.mouse_flag=1
            if 130<self.mouse_y<170:              #cursor                -55 < x_pos  < +55
                if -55<self.mouse_x<55:         #cursor                -50 < y_pos  <  -10    
                    self.menu=3
            elif -50<self.mouse_y<-10:
                if -110<self.mouse_x<110: 
                    self.menu=11
#                   if platform.system()=='Linux':
#                       self.pub.publish('GA')
                    self.GA_flag=1
                    pg.time.wait(3000)
#                   if platform.system()=='Linux':
#                       self.pub.publish('XX')
                    pg.mouse.set_visible(False)
                        
        if pg.mouse.get_pressed()==(0,0,0):
            self.mouse_flag=0
                    
    #menu com o elemento gráfico
    def menu_11(self):
        self.screen.fill((11,12,12))
        self.screen.blit(self.ghost0,(self.screen_w//2-77//2+self.ghostpos_x*77,self.screen_h//2-77//2+self.ghostpos_y*77),Rect(0,0,77,77))
        
    # Training config screen
    def menu_12(self):
        self.screen.fill(self.color)
        self.screen.blit(self.back,(self.screen_w//2 -55,self.screen_h//2 - 20 + 150)) #size (110,40)  delay (-20 - 110 - 110 + 0, -20 +30)
        self.screen.blit(self.window_size,(self.screen_w//2 -110*4,self.screen_h//2 - 20 - 90)) #size (220,40)  delay (- 110 + 0, -20 -90)
        self.screen.blit(self.displacement,(self.screen_w//2 -110*4,self.screen_h//2 - 20 + 30)) #size (110,40)  delay (-20 - 110 - 110 + 0, -20 +30)
        
        self.screen.blit(self.bb2,(self.screen_w//2 -110*2+55,self.screen_h//2 - 20 - 90)) #size (220,40)  delay (- 110 + 0, -20 -90)
        self.screen.blit(self.bb2,(self.screen_w//2 -110*2+55,self.screen_h//2 - 20 + 30)) #size (220,40)  delay (- 110 + 0, -20 -90)
        
        self.win_size_=self.fonte.render(str(self.win_size)+" ms", 1, (255,255,255))
        self.win_displacement_=self.fonte.render(str(self.win_displacement)+" ms", 1, (255,255,255))
        
        self.screen.blit(self.win_size_,(self.screen_w//2 - self.win_size_.get_width()//2-110,self.screen_h//2 -90 - self.win_size_.get_height()//2))   
        self.screen.blit(self.win_displacement_,(self.screen_w//2 - self.win_displacement_.get_width()//2-110,self.screen_h//2 +30 - self.win_displacement_.get_height()//2))   
        
        
        if pg.mouse.get_pressed()==(1,0,0)  and self.mouse_flag==0: #mouse pressed event bottom left
            self.mouse_flag=1
            if 130<self.mouse_y<170:
                if -55<self.mouse_x<55:
                    self.menu=3
                    self.save_parameters_4()
                    self.menu_flag=0
                    
            elif -165<self.mouse_x<-55:
                if -110<self.mouse_y<-70:
                    self.menu_flag=1
                elif 10<self.mouse_y<50:
                    self.menu_flag=2
                    
                else:self.menu_flag=0
            else:self.menu_flag=0
                    
        if pg.mouse.get_pressed()==(0,0,0):
            self.mouse_flag=0
            
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
        

user_interface()