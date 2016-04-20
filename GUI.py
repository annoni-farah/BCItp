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

    #funcao que carrea a fonte
    def fonts(self):
        self.fonte=pg.font.Font(self.pathtoresources +"ubuntu.bold.ttf", 20)
                                 
                    
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
        a=user_interface()
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