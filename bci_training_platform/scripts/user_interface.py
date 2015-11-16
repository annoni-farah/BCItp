#!/usr/bin/env python
import os, platform,sys, pygame as pg
from random import shuffle
from pygame.locals import *



if platform.system()=='Linux':
	import rospy
	from std_msgs.msg import String



class user_interface:
	def __init__(self):
		pg.init()
		if platform.system()=='Linux':
			rospy.init_node('listener', anonymous=True)
			rospy.Subscriber('manager_gui', String, self.callback)
			self.pub=rospy.Publisher('manager_gui', String, queue_size=100)
		self.screen= pg.display.set_mode((900,500),HWSURFACE|DOUBLEBUF|RESIZABLE)#|pg.FULLSCREEN)
		self.screen_w, self.screen_h=self.screen.get_size()
		self.mouse_x, self.mouse_y=0,0
		self.globalpath=os.path.abspath(os.path.dirname(__file__))
		self.back=pg.transform.smoothscale(pg.image.load(self.globalpath+"/resources/back.jpg"),(self.screen_w,self.screen_h))
		self.menu=0
		self.fps=20
		self.fonte=pg.font.Font(self.globalpath+"/resources/ubuntu.bold.ttf", 33)
		self.user=""
		self.beep = pg.mixer.Sound(self.globalpath+"/resources/beep.ogg")
		self.users_list=self.globalpath+"/users/users_list.txt"
		self.click_flag=(0,0,0)
		self.menu_pos=[[0+self.screen_w//6 - 218//2,self.screen_w//3 +self.screen_w//6 - 218//2]]
		self.menu0=pg.image.load(self.globalpath+"/resources/menu0.png")
		self.signs=pg.image.load(self.globalpath+"/resources/signs.png")
		self.sessions_cont=5
		self.lista0=[3,4]*self.sessions_cont    #task list
		shuffle(self.lista0)
		self.ghost0=pg.image.load(self.globalpath+"/resources/red_ghost.png")
		self.star=pg.transform.smoothscale(pg.image.load(self.globalpath+"/resources/star.jpg"),(77,77))
		self.enter=0
		self.clock=pg.time.Clock()
		self.playtime=0.0
		self.ghostpos_y=0
		self.ghostpos_x=0
		self.starpos_y=0
		self.starpos_x=0
		self.alert_time="1500"
		self.cue_time="1500"
		self.task_time="3000"
		self.break_time="3000"
		self.classes=[1,2,3]
		self.trials="80"
		self.score_time="30"
		self.time_toscore=0
		self.score_fase="10"
		self.menu7=0
		self.menu8=0
		self.menu6=0
		self.fase=0
		self.score=0
		self.nivel=0
		self.loop()

	def save(self):
		self.file0 = open(self.globalpath + "/users/%s/marcas.txt" %self.user,'w')
		for index,element in enumerate(self.lista0):
			self.file0.write(str(index*12*250)+"\t"+str(element)+"\n")
		self.file0.close()

	def loop(self): #main loop
		while True:
			self.handler()
			self.draw()
			self.d=self.clock.tick(self.fps)
			self.playtime += self.d / 1000.0

	def handler(self): #handler of events
		for event in pg.event.get():
			if event.type==QUIT:
				if platform.system()=='Linux':
					self.pub.publish("DY")
				pg.quit(); sys.exit()
			elif event.type==VIDEORESIZE:
				self.screen= pg.display.set_mode(event.size,HWSURFACE|DOUBLEBUF|RESIZABLE)
				self.screen_w, self.screen_h=self.screen.get_size()
				self.back=pg.transform.smoothscale(pg.image.load(self.globalpath+"/resources/back.jpg"),(self.screen_w,self.screen_h))
			elif event.type==KEYDOWN:
				if event.key==K_ESCAPE:
					if self.menu!=6:
						pg.quit();sys.exit()
					else:
						self.menu=3
						self.file.close()
						if platform.system()=='Linux':
							self.pub.publish('XY')
						self.menu6=0
						self.nivel=0
						
				if self.menu==1 or self.menu==2:
					if len(self.user)<21:
						if 64<event.key<91 or 96<event.key<123 or event.key==95 or 47<event.key<58:
							self.user=self.user+chr(event.key)
					if event.key==K_BACKSPACE and len(self.user)>0:
						self.user=self.user[0:-1]
					if event.key==K_RETURN:
						self.enter=1
				if self.menu==6:
					self.screen.fill((0,0,0))
					if event.key==K_UP and self.ghostpos_y>-4:
						self.ghostpos_y-=1
					elif event.key==K_DOWN and self.ghostpos_y<4:
						self.ghostpos_y+=1
					elif event.key==K_LEFT and self.ghostpos_x>-4:
						self.ghostpos_x-=1
					elif event.key==K_RIGHT and self.ghostpos_x<4:
						self.ghostpos_x+=1
					pg.event.clear()
				if self.menu==7:
					if event.key==K_RETURN:
						self.menu7=0
					elif event.key==K_TAB and self.menu7<5:
						self.menu7+=1						
					if self.menu7==1:
						if event.key==K_DELETE:
							self.alert_time=""
						if len(self.alert_time)<5:
							if 47<event.key<58:
								self.alert_time=self.alert_time+chr(event.key)
						if event.key==K_BACKSPACE and len(self.alert_time)>0:
							self.alert_time=self.alert_time[0:-1]
					elif self.menu7==2:
						if event.key==K_DELETE:
							self.cue_time=""
						if len(self.cue_time)<5:
							if 47<event.key<58:
								self.cue_time=self.cue_time+chr(event.key)
						if event.key==K_BACKSPACE and len(self.cue_time)>0:
							self.cue_time=self.cue_time[0:-1]
					elif self.menu7==3:
						if event.key==K_DELETE:
							self.task_time=""
						if len(self.task_time)<5:
							if 47<event.key<58:
								self.task_time=self.task_time+chr(event.key)
						if event.key==K_BACKSPACE and len(self.task_time)>0:
							self.task_time=self.task_time[0:-1]
					elif self.menu7==4:
						if event.key==K_DELETE:
							self.break_time=""
						if len(self.break_time)<5:
							if 47<event.key<58:
								self.break_time=self.break_time+chr(event.key)
						if event.key==K_BACKSPACE and len(self.break_time)>0:
							self.break_time=self.break_time[0:-1]
					elif self.menu7==5:
						if event.key==K_DELETE:
							self.trials=""
						if len(self.trials)<3:
							if 47<event.key<58:
								self.trials=self.trials+chr(event.key)
						if event.key==K_BACKSPACE and len(self.trials)>0:
							self.trials=self.trials[0:-1]
				if self.menu==8:
					if event.key==K_RETURN:
						self.menu8=0
					elif event.key==K_TAB and self.menu8<5:
						self.menu8+=1						
					if self.menu8==1:
						if event.key==K_DELETE:
							self.score_time=""
						if len(self.score_time)<5:
							if 47<event.key<58:
								self.score_time=self.score_time+chr(event.key)
						if event.key==K_BACKSPACE and len(self.score_time)>0:
							self.score_time=self.score_time[0:-1]
					elif self.menu8==2:
						if event.key==K_DELETE:
							self.score_fase=""
						if len(self.score_fase)<5:
							if 47<event.key<58:
								self.score_fase=self.score_fase+chr(event.key)
						if event.key==K_BACKSPACE and len(self.score_fase)>0:
							self.score_fase=self.score_fase[0:-1]
					
	def draw(self): #select menu and draw
		self.screen.blit(self.back,(0,0))
		self.mouse_x, self.mouse_y=pg.mouse.get_pos()
		if self.menu==0:
			self.menu_0()
		elif self.menu==1:
			self.menu_1()
		elif self.menu==2:
			self.menu_1()
		elif self.menu==3:
			self.menu_3()
		elif self.menu==4:
			self.menu_4()
		elif self.menu==5:
			self.menu_5()
		elif self.menu==6:
			self.menu_6()
		elif self.menu==7:
			self.menu_7()
		elif self.menu==8:
			self.menu_8()
		pg.display.update()

	def menu_0(self): #first menu [login, new user, exit]
		if self.screen_h//2 - 90<self.mouse_y<self.screen_h//2 + 90:
			for i in range(3):
				if i*self.screen_w//3+self.screen_w//6-109<self.mouse_x<i*self.screen_w//3+self.screen_w//6+109:
					self.screen.blit(self.menu0,(i*self.screen_w//3+self.screen_w//6-109,self.screen_h//2-90),Rect(218,180*i,218,180))
					if pg.mouse.get_pressed()==(1,0,0) and self.click_flag == (0,0,0):
						if i==0:    self.menu=1
						if i==1:    self.menu=2
						if i==2:    
							if platform.system()=='Linux':
								self.pub.publish("DY")
							pg.quit();sys.exit()
						self.click_flag=(1,0,0)
					elif pg.mouse.get_pressed()==(0,0,0):
						self.click_flag=(0,0,0)
				else:
					self.screen.blit(self.menu0,(i*self.screen_w//3+self.screen_w//6-109,self.screen_h//2-90),Rect(0,180*i,218,180))
		else:
			for i in range(3):
				self.screen.blit(self.menu0,(i*self.screen_w//3+self.screen_w//6-109,self.screen_h//2-90),Rect(0,180*i,218,180))

	def menu_1(self):  #login menu [insert user]
		self.screen.blit(self.menu0,(self.screen_w//2-218,self.screen_h//2 - 180),Rect(0,540,436,90))
		self.screen.blit(self.menu0,(self.screen_w//2-218,self.screen_h//2 - 45),Rect(0,630,436,90))
		self.nickname=self.fonte.render(str(self.user), 1, (255,255,255))
		self.screen.blit(self.nickname,(self.screen_w//2 - self.nickname.get_width()//2,self.screen_h//2 - 22))

		if self.screen_h//2 - 45 < self.mouse_y < self.screen_h//2 +45 or self.enter==1:
			if self.screen_w//2-218 - 121 < self.mouse_x< self.screen_w//2-218 - 12:
				self.screen.blit(self.menu0,(self.screen_w//2-218-121,self.screen_h//2 - 45),Rect(327,720,109,90))
				if pg.mouse.get_pressed()==(1,0,0) and self.click_flag == (0,0,0):
					self.menu=0
					self.user=""
					self.click_flag=(1,0,0)
				elif pg.mouse.get_pressed()==(0,0,0):
					self.click_flag=(0,0,0)
			else:
				self.screen.blit(self.menu0,(self.screen_w//2-218-121,self.screen_h//2 - 45),Rect(218,720,109,90))
			if self.screen_w//2+218 + 12 < self.mouse_x< self.screen_w//2+218 + 121 or self.enter==1:
				self.screen.blit(self.menu0,(self.screen_w//2+218+12,self.screen_h//2 - 45),Rect(109,720,109,90))
				if (pg.mouse.get_pressed()==(1,0,0) or self.enter==1) and self.click_flag == (0,0,0):
					if self.menu==1:
						try:
							file=open(self.users_list,'r')
						except:
							file=open(self.users_list,'w')
							file=open(self.users_list,'r')

						for line in file.readlines():
							if line == (str(self.user)+'\n'):
								self.menu=3																
								self.load_options()
								if platform.system()=='Linux':
									self.pub.publish("UN"+str(self.user))
									self.pub.publish("TM"+str((int(self.alert_time)+int(self.cue_time)+int(self.task_time)+int(self.break_time))*(int(self.trials)*len(self.classes))))
									self.pub.publish("TI"+self.trials)
									self.pub.publish("CL"+" ".join([str(x) for x in self.classes]))
								break
						else:
							self.user="USER DONT EXIST"						
					elif self.menu==2:
						try:
							file=open(self.users_list,'r')
						except:
							file=open(self.users_list,'w')
							file=open(self.users_list,'r')

						for line in file.readlines():
							if line == (str(self.user)+'\n'):
								self.user="USER ALREADY EXIST"
								break						
						else:
							file=open(self.users_list,'a')
							file.write(str(self.user)+'\n')
							os.mkdir(self.globalpath + "/users/" + self.user)
							self.save_options()
							self.user="CREATED"
						file.close()
					self.click_flag=(1,0,0)
					self.enter=0
				elif pg.mouse.get_pressed()==(0,0,0):
					self.click_flag=(0,0,0)
			else:
				self.screen.blit(self.menu0,(self.screen_w//2+218+12,self.screen_h//2 - 45),Rect(0,720,109,90))
		else:
			self.screen.blit(self.menu0,(self.screen_w//2-218-121,self.screen_h//2 - 45),Rect(218,720,109,90))
			self.screen.blit(self.menu0,(self.screen_w//2+218+12,self.screen_h//2 - 45),Rect(0,720,109,90))

	def menu_3(self):  #user menu [new calibration, guide, training, options,back]
		if self.screen_h//2-200<self.mouse_y<self.screen_h//2-110:  #new calibration
			if self.screen_w//2-218<self.mouse_x<self.screen_w//2+218:
				self.screen.blit(self.menu0,(self.screen_w//2-218,self.screen_h//2-200),Rect(0,900,436,90))
				if pg.mouse.get_pressed()==(1,0,0) and self.click_flag == (0,0,0):
					self.menu=5
					self.lista0=self.classes*int(self.trials)
					self.save()
					if platform.system()=='Linux':
						self.pub.publish("NC")
					self.click_flag=(1,0,0)
				elif pg.mouse.get_pressed()==(0,0,0):
					self.click_flag=(0,0,0)
			else:
				self.screen.blit(self.menu0,(self.screen_w//2-218,self.screen_h//2-200),Rect(0,810,436,90))
			if self.screen_w//2-318-20<self.mouse_x<self.screen_w//2-209-20: #calibration guide
				self.screen.blit(self.menu0,(self.screen_w//2-318-20,self.screen_h//2-200),Rect(109,990,109,90))
				if pg.mouse.get_pressed()==(1,0,0) and self.click_flag == (0,0,0):
					self.menu=4
					self.click_flag=(1,0,0)
				elif pg.mouse.get_pressed()==(0,0,0):
					self.click_flag=(0,0,0)
			else:
				self.screen.blit(self.menu0,(self.screen_w//2-318-20,self.screen_h//2-200),Rect(0,990,109,90))
			if self.screen_w//2+229<self.mouse_x<self.screen_w//2+229+150: #calibration options
				self.screen.blit(self.menu0,(self.screen_w//2+229,self.screen_h//2-200),Rect(150,1620,150,90))
				if pg.mouse.get_pressed()==(1,0,0) and self.click_flag == (0,0,0):
					self.menu=7
					self.click_flag=(1,0,0)
				elif pg.mouse.get_pressed()==(0,0,0):
					self.click_flag=(0,0,0)
			else:
				self.screen.blit(self.menu0,(self.screen_w//2+229,self.screen_h//2-200),Rect(0,1620,150,90))
		else:
			self.screen.blit(self.menu0,(self.screen_w//2-218,self.screen_h//2-200),Rect(0,810,436,90))
			self.screen.blit(self.menu0,(self.screen_w//2+229,self.screen_h//2-200),Rect(0,1620,150,90))
			self.screen.blit(self.menu0,(self.screen_w//2-318-20,self.screen_h//2-200),Rect(0,990,109,90))
		if self.screen_h//2-70<self.mouse_y<self.screen_h//2+20: #training
			if self.screen_w//2-218<self.mouse_x<self.screen_w//2+218:
				self.screen.blit(self.menu0,(self.screen_w//2-218,self.screen_h//2-70),Rect(0,1170,436,90))
				if pg.mouse.get_pressed()==(1,0,0) and self.click_flag == (0,0,0):
					self.menu=6
					self.file=open(self.globalpath+"/users/%s/scores.txt" %self.user,'w')
					if platform.system()=='Linux':
						self.pub.publish('TR')
					pg.time.wait(200)
					if platform.system()=='Linux':
						self.pub.publish('XX')
					self.click_flag=(1,0,0)
				elif pg.mouse.get_pressed()==(0,0,0):
					self.click_flag=(0,0,0)
			else:
				self.screen.blit(self.menu0,(self.screen_w//2-218,self.screen_h//2-70),Rect(0,1080,436,90))
			if self.screen_w//2+229<self.mouse_x<self.screen_w//2+229+150: #training options
				self.screen.blit(self.menu0,(self.screen_w//2+229,self.screen_h//2-70),Rect(150,1620,150,90))
				if pg.mouse.get_pressed()==(1,0,0) and self.click_flag == (0,0,0):
					self.menu=8
					self.click_flag=(1,0,0)
				elif pg.mouse.get_pressed()==(0,0,0):
					self.click_flag=(0,0,0)
			else:
				self.screen.blit(self.menu0,(self.screen_w//2+229,self.screen_h//2-70),Rect(0,1620,150,90))
		else:
			self.screen.blit(self.menu0,(self.screen_w//2-218,self.screen_h//2-70),Rect(0,1080,436,90))
			self.screen.blit(self.menu0,(self.screen_w//2+229,self.screen_h//2-70),Rect(0,1620,150,90))
		if self.screen_h//2+150 <self.mouse_y<self.screen_h//2+240: #back
			if self.screen_w//2-54<self.mouse_x<self.screen_w//2+54:
				self.screen.blit(self.menu0,(self.screen_w//2-54,self.screen_h//2+150),Rect(327,720,109,90))
				if pg.mouse.get_pressed()==(1,0,0) and self.click_flag == (0,0,0):
					self.menu=0
					self.user=""
					self.click_flag=(1,0,0)
				elif pg.mouse.get_pressed()==(0,0,0):
					self.click_flag=(0,0,0)
			else:
				self.screen.blit(self.menu0,(self.screen_w//2-54,self.screen_h//2+150),Rect(218,720,109,90))
		else:
			self.screen.blit(self.menu0,(self.screen_w//2-54,self.screen_h//2+150),Rect(218,720,109,90))

	def menu_7(self):  #options calibration
		self.screen.blit(self.menu0,(self.screen_w//2-400,self.screen_h//2-240),Rect(0,1710,300,45))
		self.screen.blit(self.menu0,(self.screen_w//2-80,self.screen_h//2-240),Rect(0,1845,300,45))
		self.screen.blit(self.menu0,(self.screen_w//2+240,self.screen_h//2-240),Rect(0,2070,180,45))
		for x in [1,2,3,4]:
			self.screen.blit(self.menu0,(self.screen_w//2-400+31,self.screen_h//2-240+57*x),Rect(109*(x-1),1755,109,45))
			if self.menu7==x:
				self.screen.blit(self.menu0,(self.screen_w//2-271+31,self.screen_h//2-240+57*x),Rect(109,1800,109,45))
			else:
				self.screen.blit(self.menu0,(self.screen_w//2-271+31,self.screen_h//2-240+57*x),Rect(0,1800,109,45))
			if self.screen_h//2-183+57*(x-1)<self.mouse_y<self.screen_h//2-183+45+57*(x-1):
				if self.screen_w//2-271+31<self.mouse_x<self.screen_w//2-271+31+109:
					if pg.mouse.get_pressed()==(1,0,0) and self.click_flag == (0,0,0):
						self.click_flag=(1,0,0)
						self.menu7=x
					elif pg.mouse.get_pressed()==(0,0,0):
						self.click_flag=(0,0,0)
			
			if x in self.classes:#seleciona quais classes
				self.screen.blit(self.menu0,(self.screen_w//2-80+42,self.screen_h//2-240+57*x),Rect(216,1845+45*x,216,45))
			else:
				self.screen.blit(self.menu0,(self.screen_w//2-80+42,self.screen_h//2-240+57*x),Rect(0,1845+45*x,216,45))
			if self.screen_w//2-80+42<self.mouse_x<self.screen_w//2-80+42+216:#seleciona qual menu
				if self.screen_h//2-240+57*x<self.mouse_y<self.screen_h//2-195+57*x:
					if pg.mouse.get_pressed()==(1,0,0) and self.click_flag == (0,0,0):
						if x in self.classes:
							self.classes.remove(x)
						else:
							self.classes.insert(x-1,x)
						self.click_flag=(1,0,0)
					elif pg.mouse.get_pressed()==(0,0,0):
						self.click_flag=(0,0,0)

		for i,x in enumerate([self.alert_time,self.cue_time,self.task_time,self.break_time]):
			self.screen.blit(self.fonte.render(str(x), 1, (255,255,255)),(self.screen_w//2-186-self.fonte.render(str(x), 1, (255,255,255)).get_width()//2,self.screen_h//2-179+57*i))
						
		if self.menu7==5:
			self.screen.blit(self.menu0,(self.screen_w//2+240+35,self.screen_h//2-240+57),Rect(109,1800,109,45))
		else:
			self.screen.blit(self.menu0,(self.screen_w//2+240+35,self.screen_h//2-240+57),Rect(0,1800,109,45))
		if self.screen_h//2-240+57<self.mouse_y<self.screen_h//2-240+57+45:
			if self.screen_w//2+240+35<self.mouse_x<self.screen_w//2+240+109:
				if pg.mouse.get_pressed()==(1,0,0) and self.click_flag == (0,0,0):
					self.click_flag=(1,0,0)
					self.menu7=5
				elif pg.mouse.get_pressed()==(0,0,0):
					self.click_flag=(0,0,0)
		self.screen.blit(self.fonte.render(str(self.trials), 1, (255,255,255)),(self.screen_w//2+295+35-self.fonte.render(str(self.trials), 1, (255,255,255)).get_width()//2,self.screen_h//2-179))
		if self.screen_h//2+150 <self.mouse_y<self.screen_h//2+240: #back
			if self.screen_w//2-54<self.mouse_x<self.screen_w//2+54:
				self.screen.blit(self.menu0,(self.screen_w//2-54,self.screen_h//2+150),Rect(327,720,109,90))
				if pg.mouse.get_pressed()==(1,0,0) and self.click_flag == (0,0,0):
					self.classes.sort()
					self.save_options()
					self.menu=3
					if platform.system()=='Linux':
						self.pub.publish("TM"+str((int(self.alert_time)+int(self.cue_time)+int(self.task_time)+int(self.break_time))*(int(self.trials)*len(self.classes))))
						self.pub.publish("TI"+self.trials)
						self.pub.publish("CL"+" ".join([str(x) for x in self.classes]))
					self.click_flag=(1,0,0)
				elif pg.mouse.get_pressed()==(0,0,0):
					self.click_flag=(0,0,0)
			else:
				self.screen.blit(self.menu0,(self.screen_w//2-54,self.screen_h//2+150),Rect(218,720,109,90))
		else:
			self.screen.blit(self.menu0,(self.screen_w//2-54,self.screen_h//2+150),Rect(218,720,109,90))

	def menu_8(self):  #training options
		self.screen.blit(self.menu0,(self.screen_w//2-400,self.screen_h//2-240),Rect(0,2115,300,45))
		self.screen.blit(self.menu0,(self.screen_w//2-80,self.screen_h//2-240),Rect(0,1845,300,45))
		#self.screen.blit(self.menu0,(self.screen_w//2+240,self.screen_h//2-240),Rect(0,2070,180,45))
		for x in [1,2]:
			self.screen.blit(self.menu0,(self.screen_w//2-400+31,self.screen_h//2-240+57*x),Rect(109*(x-1),2160,109,45))
			if self.menu8==x:
				self.screen.blit(self.menu0,(self.screen_w//2-271+31,self.screen_h//2-240+57*x),Rect(109,1800,109,45))
			else:
				self.screen.blit(self.menu0,(self.screen_w//2-271+31,self.screen_h//2-240+57*x),Rect(0,1800,109,45))
			if self.screen_h//2-183+57*(x-1)<self.mouse_y<self.screen_h//2-183+45+57*(x-1):
				if self.screen_w//2-271+31<self.mouse_x<self.screen_w//2-271+31+109:
					if pg.mouse.get_pressed()==(1,0,0) and self.click_flag == (0,0,0):
						self.click_flag=(1,0,0)
						self.menu8=x
					elif pg.mouse.get_pressed()==(0,0,0):
						self.click_flag=(0,0,0)
		for x in [1,2,3,4]:	
			if x in self.classes:#seleciona quais classes
				self.screen.blit(self.menu0,(self.screen_w//2-80+42,self.screen_h//2-240+57*x),Rect(216,1845+45*x,216,45))
			else:
				self.screen.blit(self.menu0,(self.screen_w//2-80+42,self.screen_h//2-240+57*x),Rect(0,1845+45*x,216,45))
			if self.screen_w//2-80+42<self.mouse_x<self.screen_w//2-80+42+216:#seleciona qual menu
				if self.screen_h//2-240+57*x<self.mouse_y<self.screen_h//2-195+57*x:
					if pg.mouse.get_pressed()==(1,0,0) and self.click_flag == (0,0,0):
						if x in self.classes:
							self.classes.remove(x)
						else:
							self.classes.insert(x-1,x)
						self.click_flag=(1,0,0)
					elif pg.mouse.get_pressed()==(0,0,0):
						self.click_flag=(0,0,0)

		for i,x in enumerate([self.score_time,self.score_fase]):
			self.screen.blit(self.fonte.render(str(x), 1, (255,255,255)),(self.screen_w//2-186-self.fonte.render(str(x), 1, (255,255,255)).get_width()//2,self.screen_h//2-179+57*i))
						
		if self.screen_h//2+150 <self.mouse_y<self.screen_h//2+240: #back
			if self.screen_w//2-54<self.mouse_x<self.screen_w//2+54:
				self.screen.blit(self.menu0,(self.screen_w//2-54,self.screen_h//2+150),Rect(327,720,109,90))
				if pg.mouse.get_pressed()==(1,0,0) and self.click_flag == (0,0,0):
					self.classes.sort()
					self.save_options()
					self.menu=3
					if platform.system()=='Linux':
						self.pub.publish("CL"+" ".join([str(x) for x in self.classes]))
					self.click_flag=(1,0,0)
				elif pg.mouse.get_pressed()==(0,0,0):
					self.click_flag=(0,0,0)
			else:
				self.screen.blit(self.menu0,(self.screen_w//2-54,self.screen_h//2+150),Rect(218,720,109,90))
		else:
			self.screen.blit(self.menu0,(self.screen_w//2-54,self.screen_h//2+150),Rect(218,720,109,90))
			
	def menu_4(self):  #calibration guide
		self.screen.fill((127,127,127))
		self.nickname0=self.fonte.render("The calibration session is to generate data to calibrate", 1, (255,255,255))
		self.nickname1=self.fonte.render("the characteristics extraction and classification algorithms", 1, (255,255,255))
		self.nickname2=self.fonte.render("each task will last for 12 seconds", 1, (255,255,255))
		self.screen.blit(self.nickname0,(self.screen_w//2 - self.nickname0.get_width()//2,self.screen_h//2 - 22))
		self.screen.blit(self.nickname1,(self.screen_w//2 - self.nickname1.get_width()//2,self.screen_h//2 +18))
		self.screen.blit(self.nickname2,(self.screen_w//2 - self.nickname2.get_width()//2,self.screen_h//2 +58))
		pg.display.update()
		pg.time.wait(2300)
		#self.task(3)
		self.menu=3

	def menu_5(self):  #new calibration
		if self.screen_h//2-90<self.mouse_y<self.screen_h//2+90:    #start buttom
			if self.screen_w//2-109<self.mouse_x<self.screen_w//2+109:
				self.screen.blit(self.menu0,(self.screen_w//2-109,self.screen_h//2-90),Rect(218,1350,218,180))
				if pg.mouse.get_pressed()==(1,0,0) and self.click_flag == (0,0,0):
					pg.mouse.set_visible(False)
					self.screen.fill((127,127,127))
					pg.display.update()
					if platform.system()=='Linux':
						self.pub.publish('XX')
					for element in self.lista0:
						self.task(element)
					self.click_flag=(1,0,0)
					pg.mouse.set_visible(True)
				elif pg.mouse.get_pressed()==(0,0,0):
					self.click_flag=(0,0,0)
			else:
				self.screen.blit(self.menu0,(self.screen_w//2-109,self.screen_h//2-90),Rect(0,1350,218,180))
		else:
			self.screen.blit(self.menu0,(self.screen_w//2-109,self.screen_h//2-90),Rect(0,1350,218,180))
		if self.screen_h//2+110 <self.mouse_y<self.screen_h//2+200:   #back buttom
			if self.screen_w//2-54<self.mouse_x<self.screen_w//2+54:
				self.screen.blit(self.menu0,(self.screen_w//2-54,self.screen_h//2+110),Rect(327,720,109,90))
				if pg.mouse.get_pressed()==(1,0,0) and self.click_flag == (0,0,0):
					self.menu=3
					self.click_flag=(1,0,0)
				elif pg.mouse.get_pressed()==(0,0,0):
					self.click_flag=(0,0,0)
			else:
				self.screen.blit(self.menu0,(self.screen_w//2-54,self.screen_h//2+110),Rect(218,720,109,90))
		else:
			self.screen.blit(self.menu0,(self.screen_w//2-54,self.screen_h//2+110),Rect(218,720,109,90))

	def callback(self,msg):
		if msg.data[0:4]=="TY-1" and self.ghostpos_y>-5:
			self.ghostpos_y-=1
		elif msg.data[0:4]=="TY+1" and self.ghostpos_y<5:
			self.ghostpos_y+=1
		elif msg.data[0:4]=="TX-1" and self.ghostpos_x>-5:
			self.ghostpos_x-=1
		elif msg.data[0:4]=="TX+1" and self.ghostpos_x<5:
			self.ghostpos_x+=1

	def task(self,i):
		self.beep.play()
		pg.time.wait(100)
		self.screen.blit(self.signs,(self.screen_w//2 - 158, self.screen_h//2 - 148),Rect(0,0,316,296))
		pg.display.update()
		pg.time.wait(int(self.alert_time)-200)
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
		pg.time.wait(int(self.break_time))

	def save_options(self):
		file=open(self.globalpath + "/users/" + self.user + "/" + "options.txt",'w')
		file.write(self.alert_time + '\n')
		file.write(self.cue_time + '\n')
		file.write(self.task_time + '\n')
		file.write(self.break_time + '\n')
		file.write(" ".join([str(x) for x in self.classes])+"\n")
		file.write(self.trials+"\n")
		file.write(self.score_time+"\n")
		file.write(self.score_fase+"\n")
		file.close()

	def load_options(self):
		file=open(self.globalpath + "/users/" + self.user + "/" + "options.txt",'r')
		self.alert_time = file.readline()[0:-1]
		self.cue_time = file.readline()[0:-1]
		self.task_time = file.readline()[0:-1]
		self.break_time = file.readline()[0:-1]
		self.classes=[int(x) for x in file.readline()[0:-1].split(" ")]
		self.trials=file.readline()[0:-1]
		self.score_time=file.readline()[0:-1]
		self.score_fase=file.readline()[0:-1]
		file.close()
		
	def menu_6(self): #training
		self.screen.fill((0,0,0))
		if self.time_toscore<=0:
			self.menu6=0
		self.screen.blit(self.fonte.render("Score "+str(self.score), 1, (255,255,255)),(self.screen_w//2+300-self.fonte.render("Score "+str(self.score), 1, (255,255,255)).get_width()//2,80))
		self.screen.blit(self.fonte.render("Nivel "+str(self.nivel), 1, (255,255,255)),(self.screen_w//2+300-self.fonte.render("Nivel "+str(self.nivel), 1, (255,255,255)).get_width()//2,40))
		if self.menu6==0:
			if self.fase==0:
				self.playtime=0
				if self.classes[self.nivel]==1:
					self.ghostpos_x=0
					self.ghostpos_y=-4
					self.starpos_x=0
					self.starpos_y=4
				elif self.classes[self.nivel]==2:
					self.ghostpos_x=0
					self.ghostpos_y=4
					self.starpos_x=0
					self.starpos_y=-4
				elif self.classes[self.nivel]==3:
					self.ghostpos_x=-4
					self.ghostpos_y=0
					self.starpos_x=4
					self.starpos_y=0
				elif self.classes[self.nivel]==4:
					self.ghostpos_x=4
					self.ghostpos_y=0
					self.starpos_x=-4
					self.starpos_y=0
			self.menu6=1
		self.time_toscore=float(self.score_time)-self.playtime//1
		self.screen.blit(self.fonte.render("Time "+str(self.time_toscore), 1, (255,255,255)),(self.screen_w//2+300-self.fonte.render("Nivel "+str(self.time_toscore), 1, (255,255,255)).get_width()//2,120))
		self.screen.blit(self.ghost0,(self.screen_w//2-77//2+self.ghostpos_x*77,self.screen_h//2-77//2+self.ghostpos_y*77),Rect(0,0,77,77))
		self.screen.blit(self.star,(self.screen_w//2-77//2+self.starpos_x*77,self.screen_h//2-77//2+self.starpos_y*77),Rect(0,0,77,77))	
		if self.ghostpos_x==self.starpos_x and self.ghostpos_y==self.starpos_y:
			self.menu6=0
			self.score+=1
			self.file.write(str(int(self.score_time) - self.time_toscore)+"\t"+str(self.classes[self.nivel])+"\n")
			if self.score==int(self.score_fase):
				if self.nivel < len(self.classes)-1:
					self.nivel+=1
					if platform.system()=='Linux':
						self.pub.publish("NI"+str(self.nivel))
					self.score=0
		
			

a=user_interface()
