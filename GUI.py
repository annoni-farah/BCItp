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
        self.screen = pg.display.set_mode((900,500),HWSURFACE|DOUBLEBUF|RESIZABLE)#|pg.FULLSCREEN)

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
        globalpath = '/home/rafaelmd/codes/repo/bci_training_platform'
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
        self.load_images()
        #carrega a fonte a ser utilizada
        self.load_fonts()
        
        #loads the predefined config values
        self.load_values()
        #define cor do fundo da tela
        self.color=(33,155,74)

    #funcao que carrega as imagens
    def load_images(self):
        
        self.small_box=pg.image.load(self.pathtoresources +"blank_box_small.png")
        self.medium_box=pg.image.load(self.pathtoresources +"blank_box_medium.png")
        self.large_box=pg.image.load(self.pathtoresources +"blank_box_large.png")
        self.ghost=pg.image.load(self.pathtoresources +"ghost.png")
        
        # Signs:
        self.sign_start=pg.image.load(self.pathtoresources +"sign_start.png")
        self.sign_right=pg.image.load(self.pathtoresources +"sign_right.png")
        self.sign_left=pg.image.load(self.pathtoresources +"sign_left.png")
        self.sign_clock=pg.image.load(self.pathtoresources +"sign_clock.png")
        
    #funcao que carrea a fonte
    def load_fonts(self):
        self.font=pg.font.Font(self.pathtoresources +"ubuntu.bold.ttf", 20)

    #define parametros padrão 
    def load_values(self):
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

        #tamanho da janela em ms
        self.win_size="3000"
        #deslocamento em ms
        self.win_displacement="500"
                    
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
    def up_menu_0(self):  
        self.screen.fill(self.color) # set backgroung color
        
        self.add_button_text('medium', -55, -50, 'Login')
        self.add_button_text('medium', -55, 10, 'New')
        
        pg.display.update() 
        
#        if pg.mouse.get_pressed()==(1,0,0): #mouse pressed event bottom left
#            if -55<self.mouse_x<55:              #cursor                -55 < x_pos  < +55
#                if -50<self.mouse_y<-10:         #cursor                -50 < y_pos  <  -10    
#                    self.menu=2 
#                elif 10<self.mouse_y<50:         #cursor                 10 < y_pos  < +50
#                    self.menu=1
        

    #create user screen

    def up_menu_1(self):
        self.screen.fill(self.color)
        
        self.add_button_text('medium', -55, 130, 'Back')
        self.add_button_text('medium', 130, 10, 'Create')
        self.add_button_text('large', -110, -50, 'Type your user')
        self.add_button_text('large', -110, 10, '')
    
        pg.display.update()
#        if pg.mouse.get_pressed()==(1,0,0) and self.mouse_flag==0: #mouse pressed event bottom left
#            self.mouse_flag=1
#            print(self.mouse_flag)
#            if 10<self.mouse_y<50:              #cursor                -55 < x_pos  < +55
#                if -240<self.mouse_x<-130:         #cursor                -50 < y_pos  <  -10    
#                    self.menu=0
#                    self.menu_flag=0
#                    self.user=""
#                elif 130<self.mouse_x<240:         #cursor                 10 < y_pos  < +50
#                    self.users_file()
#                    
#        if pg.mouse.get_pressed()==(0,0,0):
#            self.mouse_flag=0
#        if self.menu_flag==1:
#            self.screen.blit(self.user_already_exists,(self.screen_w//2 -120,self.screen_h//2 - 20 + 90)) #size (240,40)  delay (-120 + 0, -20 +90)
#        elif self.menu_flag==2:
#            self.screen.blit(self.user_created,(self.screen_w//2 -120,self.screen_h//2 - 20 + 90)) #size (240,40)  delay (-120 + 0, -20 +90)                        
#            
    # Login Screen
    def up_menu_2(self):
        self.screen.fill(self.color)
    
        self.add_button_text('medium', -55, 130, 'Back')
        self.add_button_text('large', -110, -50, 'Type your user')
        self.add_button_text('large', -110, 10, '')
        self.add_button_text('medium', 130, 10, 'Enter')
        
        pg.display.update()
#        if pg.mouse.get_pressed()==(1,0,0)  and self.mouse_flag==0: #mouse pressed event bottom left
#            self.mouse_flag=1
#            if 10<self.mouse_y<50:              #cursor                -55 < x_pos  < +55
#                if -240<self.mouse_x<-130:         #cursor                -50 < y_pos  <  -10    
#                    self.menu=0
#                    self.menu_flag=0
#                    self.user=""
#                elif 130<self.mouse_x<240:         #cursor                 10 < y_pos  < +50
#                    self.users_file()
#
#        if pg.mouse.get_pressed()==(0,0,0):
#            self.mouse_flag=0
#        if self.menu_flag==1:
#            self.screen.blit(self.user_does_not_exist,(self.screen_w//2 -120,self.screen_h//2 - 20 + 90)) #size (240,40)  delay (-120 + 0, -20 +90)

    # User screen (after logging in)
    def up_menu_3(self):
        self.screen.fill(self.color)

        self.add_button_text('large', -110, -110, 'Calibration')
        self.add_button_text('medium', 130, -110, 'Options')
        self.add_button_text('large', -110, -50, 'Test')
        self.add_button_text('medium', 130, -50, 'Options')
        self.add_button_text('medium', -55, 130, 'Back')
    
        pg.display.update()
#        if pg.mouse.get_pressed()==(1,0,0)  and self.mouse_flag==0: #mouse pressed event bottom left
#            self.mouse_flag=1
#            if -110<self.mouse_y<-70:
#                if -110<self.mouse_x<110:
#                    self.menu=4
#                elif 130<self.mouse_x<240:
#                    self.menu=5
#                    
#            elif -50<self.mouse_y<-10:
#                if -55<self.mouse_x<55:
#                    self.menu=6
#                elif 130<self.mouse_x<240:
#                    self.menu=7
#                
#            elif 70<self.mouse_y<110:
#                if -110<self.mouse_x<110:
#                    self.menu=10
#                elif 130<self.mouse_x<240:
#                    self.menu=12
#
#            elif 130<self.mouse_y<170:
#                if -55<self.mouse_x<55:
#                    self.menu=0
#                    self.user=""
#                    self.values()
#                    
#        if pg.mouse.get_pressed()==(0,0,0):
#            self.mouse_flag=0

    # Calibration Screen
    def up_menu_4(self):
        self.screen.fill(self.color)
        
        self.add_button_text('medium', -55, -50, 'Start')
        self.add_button_text('medium', -55, 130, 'Back')
        
        pg.display.update()
#        self.add_element(self.start, -110, -50)
#        self.add_element(self.back, -55, 130)        
        
#        if pg.mouse.get_pressed()==(1,0,0)  and self.mouse_flag==0: #mouse pressed event bottom left
#            self.mouse_flag=1
#            #botao voltar
#            if 130<self.mouse_y<170:              #cursor                -55 < x_pos  < +55
#                if -55<self.mouse_x<55:         #cursor                -50 < y_pos  <  -10    
#                    self.menu=3
#            #botao start        
#            elif -50<self.mouse_y<-10:
#                if -110<self.mouse_x<110:         #cursor                -50 < y_pos  <  -10 
#                    #gera lista de ensaios  
#                    self.lista0=self.classes*int(self.number_trials)
#                    shuffle(self.lista0) #embaralha lista
#                    self.save_marcas() #salva as marcações
#                    #envia mensagem para o manager indicando a calibraçao
##                   if platform.system()=='Linux':
##                       self.pub.publish('NC')
#                    pg.mouse.set_visible(False)
#                    self.screen.fill((127,127,127))
#                    pg.display.update()
#                    pg.time.wait(5000)
#                    #envia mensagem para o manager indicando que pode comecar a tarefa de calibraçao
##                   if platform.system()=='Linux':
##                       self.pub.publish('XX')
#                    #apresenta as imagens para todos os ensaios da lista
#                    for element in self.lista0:
#                        self.task_(element)
#                    #if platform.system()=='Linux':
#                    #   self.pub.publish('XY')
#                    pg.mouse.set_visible(True)
#                    self.menu=3
#                    
#        if pg.mouse.get_pressed()==(0,0,0):
#            self.mouse_flag=0
        
    # Calibration Menu 
    def up_menu_5(self):
        
        self.screen.fill(self.color)

        self.add_button_text('medium', -110*4, -170, 'Alert')
        self.add_button_text('medium', -110*4, -110, 'Cue')
        self.add_button_text('medium', -110*4, -50, 'Task')
        self.add_button_text('medium', -110*4, 10, 'Pause')
        self.add_button_text('medium', -110*4, 70, 'Total')
        self.add_button_text('medium', -55, 130, 'Back')
        self.add_button_text('medium', -55, 70, 'Save')
        
        
#        default = str((int(self.total_time)*int(self.number_trials)*len(self.classes)//6000)/10)
#        unity = " min"
#        self.total_time_calibration_ = self.fill_element(default, unity)
#        self.add_element(self.total_time_calibration_, 110*3, 210)
        
        self.add_button_text('medium', -110*3+20, -170, '')
        self.add_button_text('medium', -110*3+20, -110, '')
        self.add_button_text('medium', -110*3+20, -50, '')
        self.add_button_text('medium', -110*3+20, 10, '')
        self.add_button_text('medium', -110*3+20, 70, '')
#        
#        self.alert_time_=self.font.render(str(self.alert_time)+" ms", 1, (255,255,255))
#        self.cue_time_=self.font.render(str(self.cue_time)+" ms", 1, (255,255,255))
#        self.task_time_=self.font.render(str(self.task_time)+" ms" ,1, (255,255,255))
#        self.pause_time_=self.font.render(str(self.pause_time)+" ms", 1, (255,255,255))
#        self.total_time_=self.font.render(str(self.total_time)+" ms", 1, (255,255,255))
        self.add_button_text('medium', -110*3+20, -170, '')
        self.add_button_text('medium', -110*3+20, -110, '')
        self.add_button_text('medium', -110*3+20, -50, '')
        self.add_button_text('medium', -110*3+20, 10, '')
        self.add_button_text('medium', -110*3+20, 70, '')
      
        self.add_button_text('medium', -110, -170, 'Right Hand')
        self.add_button_text('medium', -110, -110, 'Left Hand')
        self.add_button_text('medium', -110, -50, 'Feet')
        
        self.add_button_text('medium', 20, -170, '')
        self.add_button_text('medium', 20, -110, '')
        self.add_button_text('medium', 20, -50, '')
        
        self.add_button_text('large', 100*2, -170, 'Epoch')
        self.add_button_text('medium', 100*2, -110, '')
        self.add_button_text('medium', 100*3 + 20, -110, '')
        
        self.add_button_text('large', 100*2, 10, 'Trials per Class')
        self.add_button_text('medium', 100*2+55, 70, '')
        
        self.add_button_text('large', 100*2, 130, 'Total Time')
        self.add_button_text('medium', 100*2+55, 190, '')
        
        pg.display.update()
#        self.number_trials_=self.font.render(str(self.number_trials), 1, (255,255,255))
#        self.add_element(self.number_trials_, 110*2+55, 70)
       
#        if 0 in self.classes:
#            self.screen.blit(self.mb1,(self.screen_w//2 +110+20,self.screen_h//2 - 20 - 150)) #size (220,40)  delay (- 110 + 0, -20 -90)
#        else:
#            self.screen.blit(self.bb1,(self.screen_w//2 +110+20,self.screen_h//2 - 20 - 150)) #size (220,40)  delay (- 110 + 0, -20 -90)
#        if 1 in self.classes:
#            self.screen.blit(self.mb1,(self.screen_w//2 +110+20,self.screen_h//2 - 20 - 90)) #size (220,40)  delay (- 110 + 0, -20 -90)
#        else:
#            self.screen.blit(self.bb1,(self.screen_w//2 +110+20,self.screen_h//2 - 20 - 90)) #size (220,40)  delay (- 110 + 0, -20 -90)
#        if 2 in self.classes:
#            self.screen.blit(self.mb1,(self.screen_w//2 +110+20,self.screen_h//2 - 20 - 30)) #size (220,40)  delay (- 110 + 0, -20 -90)
#        else:
#            self.screen.blit(self.bb1,(self.screen_w//2 +110+20,self.screen_h//2 - 20 - 30)) #size (220,40)  delay (- 110 + 0, -20 -90)
#        
#        if pg.mouse.get_pressed()==(1,0,0)  and self.mouse_flag==0: #mouse pressed event bottom left
#            self.mouse_flag=1
#            if -310<self.mouse_x<-200:
#                if -170<self.mouse_y<-130:
#                    self.menu_flag=1
#                elif -110<self.mouse_y<-70:
#                    self.menu_flag=2
#                elif -50<self.mouse_y<-10:
#                    self.menu_flag=3
#                elif 10<self.mouse_y<50:
#                    self.menu_flag=4
#                else:
#                    self.menu_flag=0
#                    
#            elif 130<self.mouse_x<170:
#                if -170<self.mouse_y<-130:
#                    if 0 in self.classes:
#                        self.classes.remove(0)
#                    else:
#                        self.classes.insert(0,0)
#                elif -110<self.mouse_y<-70:
#                    if 1 in self.classes:
#                        self.classes.remove(1)
#                    else:
#                        self.classes.insert(1,1)
#                elif -50<self.mouse_y<-10:
#                    if 2 in self.classes:
#                        self.classes.remove(2)
#                    else:
#                        self.classes.insert(2,2)
#            elif -110<self.mouse_y<-70:
#                if 210<self.mouse_x<320:
#                    self.menu_flag=5
#                elif 340<self.mouse_x<450:
#                    self.menu_flag=6
#                else:
#                    self.menu_flag=0
#                
#            elif 70<self.mouse_y<110:
#                if 275<self.mouse_x<275+110:
#                    self.menu_flag=7
#                else:self.menu_flag=0
#                    
#            elif 130<self.mouse_y<170:
#                if -55<self.mouse_x<55:
#                    self.menu=3
#                    self.save_parameters_1()
#                    self.menu_flag=0
#                    
#        if pg.mouse.get_pressed()==(0,0,0):
#            self.mouse_flag=0
    
    
    #funcao que para cada tipo de tarefa plota as imagens dos ensaios do teste  
    def task(self, epoch_class):

        self.screen.fill((127,127,127))
        
        self.add_element(self.sign_start, -158, -148)
        pg.display.update()
        
        pg.time.wait(int(self.alert_time))
        
        self.screen.fill((127,127,127))
        
        pg.time.wait(100)
        
        if epoch_class == 0:
            self.add_element(self.sign_right, -158, -148)
            
        elif epoch_class == 1:    
            self.add_element(self.sign_left, -158, -148)

    
        pg.display.update()
        pg.time.wait(int(self.cue_time))
        
        self.screen.fill((127,127,127))
        
        pg.display.update()
        pg.time.wait(int(self.task_time))
        
        self.add_element(self.sign_clock, -158, -148)
        pg.display.update()
        
        pg.time.wait(int(self.pause_time))
        
                    
    #menu com o elemento gráfico
    def up_menu_6(self):
        self.screen.fill((11,12,12))
        
        self.add_element(self.ghost, 0, 0)
        
        pg.display.update()

    def add_element(self, element, posX, posY):
        
        self.screen.blit(element,(self.screen_w//2 + posX,self.screen_h//2 + posY))
        
        
    def add_button_text(self, size, posX, posY, text):
        if size == 'small':        
            box = self.small_box
        elif size == 'medium':        
            box = self.medium_box
        elif size == 'large':        
            box = self.large_box
            
        a = self.screen.blit(box,(self.screen_w//2 + posX,self.screen_h//2 + posY))
        t = self.font.render(text, 1, (255,255,255))
        self.screen.blit(t,(a.centerx - t.get_rect().centerx, a.centery - t.get_rect().centery))
        
            
if __name__ == '__main__': # this code is only executed if this module is not imported

    ui = user_interface()
    
    ui.up_menu_5()
    pg.display.update()