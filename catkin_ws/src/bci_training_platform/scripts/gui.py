#!/usr/bin/env python
import pygame, sys, os, random, rospy
from pygame.locals import *
from random import shuffle
from std_msgs.msg import String

def callback(data):
    global i, flag
    i = data.data
    flag=1

def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('canal5', String, callback)
    global i
    global flag,flag2
    while True:
        inicio()
        draw_inicio()
        main_menu()

def inicio():
    global screen,sound,beep,myFont,gray,black,blue,white,red,USER,FPS,nivel,score,cord,flag,flag2,i
    pygame.init()
    screen=pygame.display.set_mode((700,500),HWSURFACE|DOUBLEBUF|RESIZABLE)
    sound = pygame.mixer.Sound("resources/sounds/intro_sound2.ogg")
    beep = pygame.mixer.Sound("resources/sounds/beep.ogg")
    myFont = pygame.font.Font("resources/fonts/touch.ttf", 40)
    flag=0
    gray = (126,126,126)
    #gray = (54,220,220)
    black  = (0,0,0)
    blue = (0,0,255)
    white= (255, 255, 255)
    red = (255,0,0)
    USER=[]
    FPS = 15
    pygame.display.set_icon(pygame.image.load("resources/images/icon.jpg"))
    pygame.display.set_caption("Exodia Platform")
    global bg1,bg2,up,down,left,right,cruz,pause,menu,ghost,star
    bg1=pygame.image.load("resources/images/background/bg1.jpg")
    bg2=pygame.image.load("resources/images/background/bg2.jpg")
    up=pygame.image.load("resources/images/UP.jpg")
    down=pygame.image.load("resources/images/DOWN.jpg")
    left=pygame.image.load("resources/images/LEFT.jpg")
    right=pygame.image.load("resources/images/RIGHT.jpg")
    cruz=pygame.image.load("resources/images/CRUZ.jpg")
    pause=pygame.image.load("resources/images/clock.jpg")
    menu=pygame.image.load("resources/images/background/menu1.jpg")
    ghost=pygame.image.load("resources/images/ghostred.jpg")
    star=pygame.image.load("resources/images/star.jpg")
    screen.fill(gray)
    screen.blit(pygame.transform.smoothscale(bg1,(350,500)),(0,0))
    screen.blit(pygame.transform.smoothscale(bg2,(350,500)),(351,0))
    pygame.display.flip()
    global menu_list, FPSCLOCK
    menu_list = [["Start","Options","Exit"],["Existing User","New User","Back"],["Create User","Delete User","Back"]]
    FPSCLOCK = pygame.time.Clock()

def blit_T_S(arg0,arg1=False):
    if arg1==False: arg1=[0]*len(arg0)
    for i,x in enumerate(arg0):
        fig = pygame.transform.smoothscale(x[0],(x[1],x[2]))
        fig = pygame.transform.rotate(fig,arg1[i])
        A,B = fig.get_size()
        A_, B_ = (x[3]+x[1]//2) - A//2, (x[4]+x[2]//2) - B//2
        screen.blit(fig,(A_,B_))

def draw_(arg0,arg1,arg3=False,arg4=False,arg5=False,arg6=False,arg7=False):
    if arg3==False: arg3=w//9
    if arg5==False:
        screen.fill(gray)
        blit_T_S([[menu,w//5,h,w//2.5,0],[bg1,w//2,h,1-arg3,0],[bg2,w//2,h,w//2+(arg3-1),0]],arg4)
    else:
        screen.fill(arg5)
    if arg6!=False:
        temp=arg6
        if arg7==False:
            arg6=[0]*2*len(arg0)
        else:
            arg6=arg7
    else:
        arg6=[1]*2*len(arg0)
        temp=arg6

    for i,k in enumerate(arg0):
        k = myFont.render(k, 1, arg1[i])
        k_w,k_h = k.get_size()
        blit_T_S([[k,k_w*w//1366,k_h*h//706,((w/2)-(k_w*w//2736))*arg6[i*2]+temp[i*2],(h*(0.5*i+1)//3.92)*arg6[i*2+1]+temp[i*2+1]]])

def draw_inicio():
    global w,h,screen
    flag=0
    temp=1
    while True:
        for event in pygame.event.get(VIDEORESIZE or QUIT):
            if event.type==pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type==VIDEORESIZE:
                screen=pygame.display.set_mode(event.dict['size'],RESIZABLE)
                w,h=event.dict['size']
                if (event.dict['size']>(1000,600) and flag==0):
                    flag=1
                    sound.play();i=0
                    while i<w//9:
                        screen.fill(gray)
                        blit_T_S([[bg1,w//2,h,-i,0],[bg2,w//2,h,w//2+i,0]])
                        pygame.display.flip()
                        i+=10
                        pygame.time.wait(30)
                    draw_(menu_list[0],[white]*3)
                    pygame.display.flip()
                    return

def main_menu():
    global w,h,screen
    k=0
    while True:
        for i,event in enumerate(pygame.event.get()):
            if event.type==pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type==VIDEORESIZE:
                screen=pygame.display.set_mode(event.dict['size'],RESIZABLE)
                w,h=event.dict['size']
                draw_(menu_list[0],[white]*3)
            elif event.type==MOUSEBUTTONDOWN:
                a,b=event.dict['pos']
                temp = w/2.355<a<w/1.75
                if temp and h/1.91<b<h/1.604:      #botao exit
                    pygame.quit(); sys.exit()
                elif temp and h/2.61<b<h/2.076:     #botao options
                    pass
                elif temp and h/4.15<b<h/2.94:      #botao start
                    start_menu()
            elif event.type==MOUSEMOTION:
                a,b=event.dict['pos']
                temp = w/2.355<a<w/1.75
                if temp and h/1.91<b<h/1.604:      #botao exit
                    if k!=1: draw_(menu_list[0],[white,white,red]);k=1
                elif temp and h/2.61<b<h/2.076:     #botao options
                    if k!=2: draw_(menu_list[0],[white,red,white]);k=2
                elif temp and h/4.15<b<h/2.94:      #botao start
                    if k!=3: draw_(menu_list[0],[red,white,white]);k=3
                elif k!=4:
                    draw_(menu_list[0],[white]*3)
                    k=4
        pygame.display.flip();

def start_menu():
    global w,h,screen
    draw_(menu_list[1],[white]*3)
    k=0
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type==VIDEORESIZE:
                screen=pygame.display.set_mode(event.dict['size'],HWSURFACE|DOUBLEBUF|RESIZABLE)
                w,h=event.dict['size']
                draw_(menu_list[1],[white]*3)
            elif event.type==MOUSEBUTTONDOWN:
                a,b=event.dict['pos']
                temp = w/2.355<a<w/1.75
                if temp and h/1.91<b<h/1.604:      #botao back
                    draw_(menu_list[0],[white]*3)
                    return
                elif temp and h/2.61<b<h/2.076:     #botao newuser
                    newuser_menu()
                elif temp and h/4.15<b<h/2.94:      #botao existinguser
                    existinguser_menu()
                    pass
            elif event.type==MOUSEMOTION:
                a,b=event.dict['pos']
                temp = w/2.355<a<w/1.75
                if temp and h/1.91<b<h/1.604:      #botao exit
                    if k!=1: draw_(menu_list[1],[white,white,red]);k=1
                elif temp and h/2.61<b<h/2.076:     #botao options
                    if k!=2: draw_(menu_list[1],[white,red,white]);k=2
                elif temp and h/4.15<b<h/2.94:      #botao start
                    if k!=3: draw_(menu_list[1],[red,white,white]);k=3
                elif k!=4:
                        draw_(menu_list[1],[white]*3)
                        k=4
        pygame.display.flip();

def newuser_menu():
        global w,h,screen
        draw_(menu_list[2],[white]*3)
        while True:
            k=0
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit(); sys.exit()
                elif event.type==VIDEORESIZE:
                    screen=pygame.display.set_mode(event.dict['size'],HWSURFACE|DOUBLEBUF|RESIZABLE)
                    w,h=event.dict['size']
                    draw_(menu_list[2],[white]*3)
                elif event.type==MOUSEBUTTONDOWN:
                    a,b=event.dict['pos']
                    temp = w/2.355<a<w/1.75
                    if temp and h/1.91<b<h/1.604:      #botao back
                        draw_(menu_list[1],[white]*3)
                        return
                    elif temp and h/2.61<b<h/2.076:     #botao deleteuser
                        #menu_options()
                        pass
                    elif temp and h/4.15<b<h/2.94:      #botao createuser
                        createuser_menu()
                elif event.type==MOUSEMOTION:
                    a,b=event.dict['pos']
                    temp = w/2.355<a<w/1.75
                    if temp and h/1.91<b<h/1.604:      #botao exit
                        if k!=1: draw_(menu_list[2],[white,white,red]);k=1
                    elif temp and h/2.61<b<h/2.076:     #botao options
                        if k!=2: draw_(menu_list[2],[white,red,white]);k=2
                    elif temp and h/4.15<b<h/2.94:      #botao start
                        if k!=3: draw_(menu_list[2],[red,white,white]);k=3
                    elif k!=4:
                        draw_(menu_list[2],[white]*3);k=4
            pygame.display.flip()

def createuser_menu():
    global w,h,screen,char
    flag=0
    i=w//9 - 1
    while i<w*1.8//9:
        draw_([" "],[white],i)
        #blit_T_S([[bg1,w//2,h,-i,0],[bg2,w//2,h,w//2+i,0]])
        pygame.display.flip()
        i+=10
        pygame.time.wait(30)
    angle=0
    while angle<91:
        draw_([" "],[white],w*1.8//9 - 1,[angle,0,0])
        angle+=5
        pygame.display.flip()
        pygame.time.wait(5)
    draw_([" ","Type your nickname"],[white]*2,w*1.8//9 -1,(90,0,0))
    char=[]
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type==VIDEORESIZE:
                screen=pygame.display.set_mode(event.dict['size'],HWSURFACE|DOUBLEBUF|RESIZABLE)
                w,h=event.dict['size']
                draw_([" ","Type your nickname",],[white]*2,w*1.8//9 -1,(90,0,0))
            elif event.type==KEYDOWN:
                key=event.dict['key']
                if 64<key<91 or 96<key<123 or key==95 or 47<key<58:
                    char.append(chr(key))
                if key==K_BACKSPACE and len(char)>0:
                    del char[-1]
                draw_([" ","Type your nickname","".join(char)],[white]*3,w*1.8//9 -1,(90,0,0))
                if key==K_RETURN:
                    if len(char)==0:
                        draw_(menu_list[2],[white]*3)
                        return
                    try:
                        file=open("users/user_list.txt",'r')
                    except:
                        file=open("users/user_list.txt",'w')
                        file.close()
                        file=open("users/user_list.txt",'r')
                    temp=file.read().split('\n')
                    if "".join(char) in temp:
                        draw_([" ","Nickname already exist",],[white]*2,w*1.8//9 -1,(90,0,0))
                        char=[]
                        file.close
                        pygame.display.flip()
                        pygame.time.wait(1000)
                    else:
                        file=open("users/user_list.txt",'a')
                        file.write("".join(char)+"\n")
                        draw_([" ","Nickname created",],[white]*2,w*1.8//9 -1,(90,0,0))
                        pygame.display.flip()
                        file.close()
                        pygame.time.wait(1000)
                        draw_(menu_list[2],[white]*3)
                        return
                    draw_([" ","Type your nickname",],[white]*2,w*1.8//9 -1,(90,0,0))
                    pygame.display.flip()
            pygame.display.flip()

def deleteuser_menu():
    pass

def existinguser_menu():
    global w,h,screen,USER
    flag=0
    i=w//9 - 1
    while i<w*1.8//9:
        draw_([" "],[white],i)
        #blit_T_S([[bg1,w//2,h,-i,0],[bg2,w//2,h,w//2+i,0]])
        pygame.display.flip()
        i+=10
        pygame.time.wait(30)
    angle=0
    while angle<91:
        draw_([" "],[white],w*1.8//9 - 1,[angle,0,0])
        angle+=5
        pygame.display.flip()
        pygame.time.wait(5)
    draw_([" ","Type your nickname"],[white]*2,w*1.8//9 -1,(90,0,0))
    char=[]
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type==VIDEORESIZE:
                screen=pygame.display.set_mode(event.dict['size'],HWSURFACE|DOUBLEBUF|RESIZABLE)
                w,h=event.dict['size']
                draw_([" ","Type your nickname",],[white]*2,w*1.8//9 -1,(90,0,0))
            elif event.type==KEYDOWN:
                key=event.dict['key']
                if 64<key<91 or 96<key<123 or key==95 or 47<key<58:
                    char.append(chr(key))
                if key==K_BACKSPACE and len(char)>0:
                    del char[-1]
                draw_([" ","Type your nickname","".join(char)],[white]*3,w*1.8//9 -1,(90,0,0))
                if key==K_RETURN:
                    if len(char)==0:
                        draw_(menu_list[1],[white]*3)
                        return
                    try:
                        file=open("users/user_list.txt",'r')
                    except:
                        file=open("users/user_list.txt",'w')
                        file.close()
                        file=open("users/user_list.txt",'r')
                    temp=file.read().split('\n')
                    if "".join(char) in temp:
                        draw_([" ","Nickname found",],[white]*2,w*1.8//9 -1,(90,0,0))
                        file.close
                        pygame.display.flip()
                        pygame.time.wait(1000)
                        USER = "".join(char)
                        user_menu()
                    else:
                        draw_([" ","Nickname do not exist",],[white]*2,w*1.8//9 -1,(90,0,0))
                        char=[]
                        pygame.display.flip()
                        pygame.time.wait(1000)
                    draw_([" ","Type your nickname",],[white]*2,w*1.8//9 -1,(90,0,0))
                    pygame.display.flip()
            pygame.display.flip()

def user_menu():
    global w,h,screen,USER
    draw_([USER,"Calibration","Training","Back"],[blue]+[white]*3)
    k=0
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type==VIDEORESIZE:
                screen=pygame.display.set_mode(event.dict['size'],HWSURFACE|DOUBLEBUF|RESIZABLE)
                w,h=event.dict['size']
                draw_([USER,"Calibration","Training","Back"],[blue]+[white]*3)
            elif event.type==MOUSEBUTTONDOWN:
                a,b=event.dict['pos']
                temp = w/2.355<a<w/1.75
                if temp and h/1.5<b<h/1.3:      #botao back
                    USER=[]
                    return
                elif temp and h/2.61<b<h/2.076:     #botao training
                    calibration_menu()
                elif temp and h/1.91<b<h/1.604:      #botao calibration
                    training_menu()
            elif event.type==MOUSEMOTION:
                a,b=event.dict['pos']
                temp = w/2.355<a<w/1.75
                if temp and h/1.91<b<h/1.604:      #botao exit
                    if k!=1: draw_([USER,"Calibration","Training","Back"],[blue]+[white]+[red]+[white]);k=1
                elif temp and h/2.61<b<h/2.076:     #botao options
                    if k!=2: draw_([USER,"Calibration","Training","Back"],[blue]+[red]+[white]*2);k=2
                elif temp and h/1.5<b<h/1.3:      #botao start
                    if k!=3: draw_([USER,"Calibration","Training","Back"],[blue]+[white]*2+[red]);k=3
                elif k!=4:
                    draw_([USER,"Calibration","Training","Back"],[blue]+[white]*3);k=4
        pygame.display.flip()

def training_menu():
    global w,h,screen,USER
    draw_(["Start Training","Back"],[white]*2)
    k=0
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type==VIDEORESIZE:
                screen=pygame.display.set_mode(event.dict['size'],HWSURFACE|DOUBLEBUF|RESIZABLE)
                w,h=event.dict['size']
                draw_(["Start Training","Back"],[white]*2)
            elif event.type==MOUSEBUTTONDOWN:
                a,b=event.dict['pos']
                temp = w/2.355<a<w/1.75
                if temp and h/2.61<b<h/2.076:     #botao deleteuser
                    draw_([USER,"Calibration","Training","Back"],[blue]+[white]*3)
                    return
                elif temp and h/4.15<b<h/2.94:      #botao createuser
                    game_start()
            elif event.type==MOUSEMOTION:
                a,b=event.dict['pos']
                temp = w/2.355<a<w/1.75
                if temp and h/2.61<b<h/2.076:     #botao options
                    if k!=1: draw_(["Start Training","Back"],[white]+[red]);k=1
                elif temp and h/4.15<b<h/2.94:      #botao start
                    if k!=2: draw_(["Start Training","Back"],[red]+[white]);k=2
                elif k!=3:
                    draw_(["Start Training","Back"],[white]*2);k=3
        pygame.display.flip()

def game_start():
    global w,h,screen,USER,nivel,score,cord,flag,flag2,i
    nivel=0
    score=0
    temp=0
    i=0
    cord=[0,0]
    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                draw_(["Start Training","Back"],[white]*2)
                return
            #elif event.type==KEYDOWN:
            #    key=event.dict['key']
        #if flag==1 and flag2==1:
        #   flag2=0
        if i=='right':
            temp=1
        elif i=='left':
            temp=-1
        elif i=='up':
            temp=-2
        elif i=='down':
            temp=2
                #else: temp=0
        i=0
        game_fase(temp)
        temp=0
        pygame.display.flip()

def game_fase(arg0):
    global nivel,score,cord,screen,cordx,cordy
    temp1=0
    temp2=0
    score_by=1
    if nivel==0:
        if arg0==1:
            cord[0]-=arg0

        draw_(["Nivel %s" % nivel, "Score %s" % score],[white]*2,arg5=black,arg6=[0,0,0,w//30],arg7=[0,0,0,0])
        blit_T_S([[ghost,w//21,w//21,(w//2-w//42)-w*(cord[0])//21,(h//2-w//42)-w*cord[1]//21]])
        blit_T_S([[star,w//21,w//21,(w//2-w//42)-w*(-10)//21,(h//2-w//42)-w*(0)//21]])
        if cord==[-10,0]:
            score+=1
            cord=[0,0]
            if score==score_by:
                nivel+=1
    if nivel==1:
        if arg0==2:
            cord[1]-=(arg0/2)
        draw_(["Nivel %s" % nivel, "Score %s" % score],[white]*2,arg5=black,arg6=[0,0,0,w//30],arg7=[0,0,0,0])
        blit_T_S([[ghost,w//21,w//21,(w//2-w//42)-w*(cord[0])//21,(h//2-w//42)-w*(cord[1]+5)//21]])
        blit_T_S([[star,w//21,w//21,(w//2-w//42)-w*(0)//21,(h//2-w//42)-w*(-5)//21]])
        if cord==[0,-10]:
            score+=1
            cord=[0,0]
            if score==score_by*2:
                nivel+=1
    if nivel==2:
        if arg0==-1:
            cord[0]-=arg0
        draw_(["Nivel %s" % nivel, "Score %s" % score],[white]*2,arg5=black,arg6=[0,0,0,w//30],arg7=[0,0,0,0])
        blit_T_S([[ghost,w//21,w//21,(w//2-w//42)-w*(cord[0])//21,(h//2-w//42)-w*cord[1]//21]])
        blit_T_S([[star,w//21,w//21,(w//2-w//42)-w*(10)//21,(h//2-w//42)-w*(0)//21]])
        if cord==[10,0]:
            score+=1
            cord=[0,0]
            if score==score_by*3:
                nivel+=1
    if nivel==3:
        if arg0==-2:
            cord[1]-=(arg0/2)
        draw_(["Nivel %s" % nivel, "Score %s" % score],[white]*2,arg5=black,arg6=[0,0,0,w//30],arg7=[0,0,0,0])
        blit_T_S([[ghost,w//21,w//21,(w//2-w//42)-w*(cord[0])//21,(h//2-w//42)-w*(cord[1]-5)//21]])
        blit_T_S([[star,w//21,w//21,(w//2-w//42)-w*(0)//21,(h//2-w//42)-w*(5)//21]])
        if cord==[0,10]:
            score+=1
            cord=[random.randrange(-10,11),random.randrange(-5,6)]
            if score==score_by*4:
                nivel+=1
                cordx=random.randrange(-10,11)
                cordy=random.randrange(-5,6)
    if nivel==4:
        if (arg0==1 and cord[0]>-10) or (arg0==-1 and cord[0]<10):
            cord[0]-=arg0
        if (arg0==2 and cord[1]>-5) or (arg0==-2 and cord[1]<5):
            cord[1]-=(arg0/2)
        draw_(["Nivel %s" % nivel, "Score %s" % score],[white]*2,arg5=black,arg6=[0,0,0,w//30],arg7=[0,0,0,0])
        blit_T_S([[ghost,w//21,w//21,(w//2-w//42)-w*(cord[0])//21,(h//2-w//42)-w*cord[1]//21]])
        blit_T_S([[star,w//21,w//21,(w//2-w//42)-w*(cordx)//21,(h//2-w//42)-w*(cordy)//21]])
        if cord==[cordx,cordy]:
            score+=1
            cord=[random.randrange(-10,11),random.randrange(-5,6)]
            cordx=random.randrange(-10,11)
            cordy=random.randrange(-5,6)
    #if nivel==5:
        #if arg0==1 or arg0==-1:
            #cord[0]-=arg0
    #    if arg0==2 or arg0==-2:
    #        cord[1]-=(arg0/2)
    #    draw_(["Nivel %s" % nivel, "Score %s" % score],[white]*2,arg5=black,arg6=[0,0,0,w//30],arg7=[0,0,0,0])
    #    blit_T_S([[ghost,w//21,w//21,(w//2-w//42)-w*(cord[0])//21,(h//2-w//42)-w*cord[1]//21]])



def task_session(task_type):
    global w,h,screen
    screen.fill(black)
    pygame.display.flip()
    beep.play()
    blit_T_S([[cruz,w//5,w//5,w*2//5,(h*5-w)//10]])
    pygame.display.flip()
    pygame.time.wait(1500)
    screen.fill(black)
    pygame.display.flip()
    pygame.time.wait(200)
    blit_T_S([[task_type,w//5,w//5,w*2//5,(h*5-w)//10]])
    pygame.display.flip()
    pygame.time.wait(1300)
    screen.fill(black)
    pygame.display.flip()
    pygame.time.wait(3000)
    blit_T_S([[pause,w//5,w//5,w*2//5,(h*5-w)//10]])
    pygame.display.flip()
    pygame.time.wait(2000)
    screen.fill(black)
    pygame.display.flip()

def cali_instructions():
    global w,h,screen,USER
    draw_(["Hello!","These are the calibration session instructions",\
        "Press Left to back and Right to continue","ESC to return exit"],\
            [white]*4,arg5=black)
    temp2=0
    while True:
        for event in pygame.event.get(KEYDOWN):
            if event.type==KEYDOWN:
                key=event.dict['key']
                if key==K_ESCAPE:
                    return
                if key==K_RIGHT:
                    temp2+=1
                if key==K_LEFT:
                    temp2-=1
                if temp2==0:
                    draw_(["The calibration session is to generate data to calibrate","the characteristics extraction and classification algorithms",\
                        "each task will last for 8 seconds"],\
                            [white]*3,arg5=black,arg6=[0,0,0,0,0,0],arg7=[1,1,1,1,1,1])
                elif temp2==1:
                    draw_(["First: You will listen a BEEP","and a CROSS sign will appear for 1.5 seconds"],\
                        [white]*2,arg5=black,arg6=[0,-h/5,0,-h/5],arg7=[1,1,1,1])
                    pygame.display.flip()
                    pygame.time.wait(500)
                    beep.play()
                    blit_T_S([[cruz,w//5,w//5,w*2//5,(h*5-w)//10]])
                elif temp2==2:
                    draw_(["Second: When the CROSS sign disappear","a sign will appear to indicate the class of the task for 1.5 seconds"],\
                        [white]*2,arg5=black,arg6=[0,0,0,0],arg7=[1,1,1,1])
                elif temp2==3:
                    draw_(["UP arrow indicate the TONGUE"],\
                        [white],arg5=black,arg6=[0,-h//5],arg7=[1,1])
                    blit_T_S([[up,w//5,w//5,w*2//5,(h*5-w)//10]])
                elif temp2==4:
                    draw_(["DOWN arrow indicate the FEET"],\
                        [white],arg5=black,arg6=[0,-h//5],arg7=[1,1])
                    blit_T_S([[down,w//5,w//5,w*2//5,(h*5-w)//10]])
                elif temp2==5:
                    draw_(["RIGHT arrow indicate the RIGHT HAND"],\
                        [white],arg5=black,arg6=[0,-h//5],arg7=[1,1])
                    blit_T_S([[right,w//5,w//5,w*2//5,(h*5-w)//10]])
                elif temp2==6:
                    draw_(["LEFT arrow indicate the LEFT HAND"],\
                        [white],arg5=black,arg6=[0,-h//5],arg7=[1,1])
                    blit_T_S([[left,w//5,w//5,w*2//5,(h*5-w)//10]])
                elif temp2==7:
                    draw_(["When the task sign disapper you have to start the task","for 3 seconds"],\
                        [white]*2,arg5=black,arg6=[0,0,0,0],arg7=[1,1,1,1])
                elif temp2==8:
                    draw_(["After you will have a break of 2 seconds before the next task"],\
                        [white]*2,arg5=black,arg6=[0,-h//10],arg7=[1,1])
                    blit_T_S([[pause,w//5,w//5,w*2//5,(h*5-w)//10]])
                elif temp2==9:
                    draw_(["Let's take a RIGHT HAND example"],\
                        [white],arg5=black,arg6=[0,0],arg7=[1,1])
                elif temp2==10:
                    task_session(right)
                    pygame.event.clear()
                    draw_(["And a TONGUE example"],\
                        [white],arg5=black,arg6=[0,0],arg7=[1,1])
                elif temp2==11:
                    task_session(up)
                    pygame.event.clear()
                    draw_(["And a FEET example"],\
                        [white],arg5=black,arg6=[0,0],arg7=[1,1])
                elif temp2==12:
                    task_session(down)
                    pygame.event.clear()
                    draw_(["And a LEFT HAND example"],\
                        [white],arg5=black,arg6=[0,0],arg7=[1,1])
                elif temp2==13:
                    task_session(left)
                    pygame.event.clear()
                    draw_(["Now click in NEW and create a calibration"],\
                        [white],arg5=black,arg6=[0,0],arg7=[1,1])
                elif temp2==14:
                    return
        pygame.display.flip()
        FPSCLOCK.tick(FPS)


def calibration_menu():
    global w,h,screen,USER
    draw_(["Guide","New","Back"],[white]*3)
    while True:
        k=0
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type==VIDEORESIZE:
                screen=pygame.display.set_mode(event.dict['size'],HWSURFACE|DOUBLEBUF|RESIZABLE)
                w,h=event.dict['size']
                draw_(["Guide","New","Back"],[white]*3)
            elif event.type==MOUSEBUTTONDOWN:
                a,b=event.dict['pos']
                temp = w/2.355<a<w/1.75
                if temp and h/1.91<b<h/1.604:      #botao back
                    draw_([USER,"Calibration","Training","Back"],[blue]+[white]*3)
                    return
                elif temp and h/2.61<b<h/2.076:      #botao new calibration
                    screen=pygame.display.set_mode((0,0),HWSURFACE|DOUBLEBUF|FULLSCREEN)
                    pygame.mouse.set_visible(False)
                    new_calibration()
                    pygame.mouse.set_visible(True)
                    screen=pygame.display.set_mode((0,0),HWSURFACE|DOUBLEBUF|RESIZABLE)
                    draw_(["Guide","New","Back"],[white]*3)
                    pygame.display.flip()
                    #SDL_Maximize()
                elif temp and h/4.15<b<h/2.94:     #botao calibration guide
                    screen=pygame.display.set_mode((0,0),HWSURFACE|DOUBLEBUF|FULLSCREEN)
                    pygame.mouse.set_visible(False)
                    cali_instructions()
                    pygame.mouse.set_visible(True)
                    screen=pygame.display.set_mode((0,0),HWSURFACE|DOUBLEBUF|RESIZABLE)
                    draw_(["Guide","New","Back"],[white]*3)
                    pygame.display.flip()
                    #SDL_Maximize()
            elif event.type==MOUSEMOTION:
                a,b=event.dict['pos']
                temp = w/2.355<a<w/1.75
                if temp and h/1.91<b<h/1.604:      #botao exit
                    if k!=1: draw_(["Guide","New","Back"],[white,white,red]);k=1
                elif temp and h/2.61<b<h/2.076:     #botao options
                    if k!=2: draw_(["Guide","New","Back"],[white,red,white]);k=2
                elif temp and h/4.15<b<h/2.94:      #botao start
                    if k!=3: draw_(["Guide","New","Back"],[red,white,white]);k=3
                elif k!=4:
                    draw_(["Guide","New","Back"],[white]*3);k=4
        pygame.display.flip()

def new_calibration():
    global w,h,screen,USER
    N=70
    lista=[up,right,left,down]*N
    time=len(lista)*10
    time=time//60
    shuffle(lista)
    try:
        os.makedirs("users/"+USER)
    except:
        if not os.path.isdir("users/"+USER):
            raise
    i=0
    while True:
        try:
            file = open("users/"+USER+"/calibration%s.txt" % i, 'r')
        except:
            break
        i=i+1
    file = open("users/"+USER+"/calibration%s.txt" % i, 'w')
    i=0
    while True:
        for event in pygame.event.get():
            if event.type==KEYDOWN:
                key=event.dict['key']
                if key==K_ESCAPE:
                    return
                elif key==K_RETURN:
                    i=1
        if i==1: break
        draw_(["Duration: %s minutes" % time,"Press any key to start"],[white]*2,arg5=black)
        pygame.display.flip()
    for element in lista:
        task_session(element)
        for event in pygame.event.get(KEYDOWN):
                key=event.dict['key']
                if key==K_ESCAPE:
                    return

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
