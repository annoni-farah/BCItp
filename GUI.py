# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 14:45:00 2016

@author: rafael
"""

#!/usr/bin/env python
import os, platform,sys, pygame as pg
from random import shuffle

from time import sleep
import numpy as np

#esses codigos permitem testar a interface gráfica no windows
#if platform.system()=='Linux':
#   import rospy
#   from std_msgs.msg import String
    
#define classe da interface gráfica 
class user_interface:
    def __init__(self):
        #inicia o pygame
        pg.init()
        self.screen = pg.display.set_mode((1000,600))#|pg.FULLSCREEN)

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
        self.load_images()
        
        self.generate_slots()
        #carrega a fonte a ser utilizada
        self.load_fonts()
        
        #loads the predefined config values
        self.load_values()
        #define cor do fundo da tela
        self.color=(0,0,0)

    #funcao que carrega as imagens
    def load_images(self):
        
        self.small_box=pg.image.load(self.pathtoresources +"blank_box_small.png")
        self.medium_box=pg.image.load(self.pathtoresources +"blank_box_medium.png")
        self.large_box=pg.image.load(self.pathtoresources +"blank_box_large_3.png")
        self.large_box_2=pg.image.load(self.pathtoresources +"blank_box_large_2.png")
        self.ghost=pg.image.load(self.pathtoresources +"ghost.png")
        
        # Signs:
        self.sign_start=pg.image.load(self.pathtoresources +"sign_start.png")
        self.sign_right=pg.image.load(self.pathtoresources +"sign_right.png")
        self.sign_left=pg.image.load(self.pathtoresources +"sign_left.png")
        self.sign_clock=pg.image.load(self.pathtoresources +"sign_clock.png")
        
    #funcao que carrea a fonte
    def load_fonts(self):
        self.font=pg.font.Font(self.pathtoresources + "ubuntu.bold.ttf", 20)

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

        pg.display.update()  #pygame update display
            
    #login and create user screen    
    def up_menu_0(self):  
        self.screen.fill(self.color) # set backgroung color
        
        self.add_button_text(7, 'Login')
        self.add_button_text(17, 'New')
        
        pg.display.update() 

    #create user screen
    def up_menu_1(self):
        self.screen.fill(self.color)
        
        self.add_button_text(22, 'Back')
        self.add_button_text(17, 'Create')
        self.add_button_text(2, 'Type your User')
        self.add_button_text(12, '')
    
        pg.display.update()
        
    # Login Screen
    def up_menu_2(self):
        self.screen.fill(self.color)
        
        
        self.add_button_text(22, 'Back')
        self.add_button_text(2, 'Type your user')
        self.add_button_text(12, '')
        self.add_button_text(17, 'Enter')
        
        pg.display.update()
        
    # User screen (after logging in)
    def up_menu_3(self):
        self.screen.fill(self.color)

        self.add_button_text(1, 'Calibration')
        self.add_button_text(3, 'Options')
        self.add_button_text(11, 'Test')
        self.add_button_text(13, 'Options')
        self.add_button_text(22, 'Back')
    
        pg.display.update()

    # Calibration Screen
    def up_menu_4(self):
        self.screen.fill(self.color)
        
        self.add_button_text(12, 'Start')
        self.add_button_text(22, 'Back')
        
        pg.display.update()   
        
    # Calibration Menu 
    def up_menu_5(self):
        
        self.screen.fill(self.color)

        self.add_button_text(0, 'Alert')
        self.add_button_text(5, 'Cue')
        self.add_button_text(10, 'Task')
        self.add_button_text(15, 'Pause')
        self.add_button_text(20, 'Total')
        self.add_button_text(24, 'Back')
        self.add_button_text(23, 'Save')
        
        self.add_button_text(1, '', 0)
        self.add_button_text(6, '', 0)
        self.add_button_text(11, '', 0)
        self.add_button_text(16, '', 0)
        self.add_button_text(21, '', 0)
 
        self.add_button_text(3, 'Epoch')
        self.add_button_text(8, '', 0)
        self.add_button_text(9, '', 0)
        
        self.add_button_text(13, 'Trials per Class')
        self.add_button_text(14, '', 0)
        
        self.add_button_text(18, 'Total Time')
        self.add_button_text(19, '', 0)
        
        pg.display.update()

    
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
    
    def generate_slots(self):
                
        box = self.large_box
        
        slots_X = [100, 300, 500, 700, 900]
        slots_X[:] = [x - box.get_width()/2 for x in slots_X]
        
        slots_Y = [60, 180, 300, 420, 540]
        slots_Y[:] = [x - box.get_height()/2 for x in slots_Y]
        
        print slots_X
        print slots_Y
                     
        s = np.array([slots_X[0], slots_Y[0]])

        for j in xrange(5):
            for i in xrange(5):
                s = np.vstack((s, [slots_X[i], slots_Y[j]]))
        
        self.slots = np.delete(s, 0, 0) 
                       
        s_max = np.copy(self.slots)

        s_max[:,0] = np.add(s_max[:,0], box.get_width())
        s_max[:,1] = np.add(s_max[:,1], box.get_height())
        
        self.slots_max = s_max
                    
        
    def add_button_text(self, slot_number, text, size_flag = 1):
        
        if size_flag:
            box = self.large_box_2
        else:
            box = self.large_box
            
            
        posX, posY  = self.slots[slot_number]    
        
        a = self.screen.blit(box,(posX, posY))
        t = self.font.render(text, 1, (255,255,255))
        self.screen.blit(t,(a.centerx - t.get_rect().centerx, a.centery - t.get_rect().centery))
    
    def mouse_press(self):
        return (pg.mouse.get_pressed() == (1,0,0))      
        
    def locate_mouse_press(self):
        self.mouse_x, self.mouse_y = pg.mouse.get_pos()

    def map_mouse_press(self):               
        rx = self.mouse_x > self.slots[:,0]
        ry = self.mouse_y > self.slots[:,1]
        
        rxm = self.mouse_x < self.slots_max[:,0]
        rym = self.mouse_y < self.slots_max[:,1]
        
        t1 = rx & ry
        t2 = rxm & rym
        
        t = t1 & t2
    
        slot_number = 100       
        
        if 1 in t: 
            slot_number = np.nonzero(t)[0][0]
            
        return slot_number
        
    def event_handler(self):
        for event in pg.event.get():
                        
            # checks if the event triggered is a Quit. If so, closes the GUI
            if event.type==pg.QUIT:
            #envia comando para fechar o manager caso feche a interface grafica
                self.close()    
                
            # Deals with GUI resizing. If remove, GUI has a static shape   
            elif event.type==pg.VIDEORESIZE:
                self.screen= pg.display.set_mode(event.size,HWSURFACE|DOUBLEBUF|RESIZABLE)
                self.screen_w, self.screen_h=self.screen.get_size()
    
        
    def close(self):
        pg.quit()
        sys.exit()
            
if __name__ == '__main__': # this code is only executed if this module is not imported

    ui = user_interface()
    
    ui.generate_slots()  
    
    ui.up_menu_5()
    
    p = 1000
#    ui.close()
    while(1):
        ui.event_handler()
        
        if(ui.mouse_press()):
            ui.locate_mouse_press()
            p = ui.map_mouse_press()
         
        if p == 22:
            ui.up_menu_0()
            
            
        ui.draw()
    