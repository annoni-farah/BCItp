# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 14:45:00 2016

@author: rafael
"""

#!/usr/bin/env python
import os, platform,sys, pygame as pg
from random import shuffle
from pygame.locals import *
from time import sleep

import GUI

reload(GUI)

#esses codigos permitem testar a interface gráfica no windows
#if platform.system()=='Linux':
#   import rospy
#   from std_msgs.msg import String
    
#define classe da interface gráfica 
class user_interface_control:
    def __init__(self):
        
        ui = GUI.user_interface()
        ui.up_menu_0()        
        
        #define o fps para o pygame
        self.fps=30
        self.clock=pg.time.Clock()
        #variavel pra armazenar o tempo
        self.playtime=0

        #define variáveis

        #variavel menu assume o valor do menu atual
        self.menu=0

        #variavel pra armazenar o usuário
        self.user=''

        #caminho global para esse arquivo
        globalpath = os.path.abspath(os.path.dirname(__file__))
        self.pathtousers = globalpath + '/data/users/'         

        #define variavel para a posiçao do fantasma(0,0 é o centro da dela)
        self.ghostpos_x=0
        self.ghostpos_y=0

        
        def change_menu(self, menu_idx):
            
            if menu_idx == 0:
                ui.up_menu_0()
            elif menu_idx == 1:
                ui.up_menu_1()
        
        
        def on_button(self):
            if ui.mouse_press():
                ui.locate_mouse_press()
                if ui.check_button_press(0,1):
                    ui.up_menu_1()
    

if __name__ == '__main__': # this code is only executed if this module is not imported
    
    cui = user_interface_control()
    
    while(1):
        if(cui.check_button()):
            cui.change_menu(1)
            
        sleep(1/60)
        