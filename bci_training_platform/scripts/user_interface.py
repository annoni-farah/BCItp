#!/usr/bin/env python
import os, sys, rospy, pygame as pg
from random import shuffle
from pygame.locals import *
from std_msgs.msg import String



class user_interface:
	def __init__(self):
		pg.init()
		rospy.init_node('listener', anonymous=True)
		rospy.Subscriber('manager_gui', String, self.callback)
		self.pub=rospy.Publisher('manager_gui', String, queue_size=100)
		self.screen= pg.display.set_mode((700,500),HWSURFACE|DOUBLEBUF|RESIZABLE)#|pg.FULLSCREEN)
		self.screen_w, self.screen_h=self.screen.get_size()
		self.mouse_x, self.mouse_y=0,0
		self.globalpath=os.path.abspath(os.path.dirname(__file__))
		print(self.globalpath)
		self.back=pg.transform.smoothscale(pg.image.load(self.globalpath+"/uresources/back.jpg"),(self.screen_w,self.screen_h))
		self.menu=0
		self.fps=20
		self.fonte=pg.font.Font(self.globalpath+"/uresources/ubuntu.bold.ttf", 33)
		self.user=""
		self.beep = pg.mixer.Sound(self.globalpath+"/uresources/reoubeep.ogg")
		self.users_list=self.globalpath+"/uresources/users_list.txt"
		self.click_flag=(0,0,0)
		self.menu_pos=[[0+self.screen_w//6 - 218//2,self.screen_w//3 +self.screen_w//6 - 218//2]]
		self.menu0=pg.image.load(self.globalpath+"/uresources/menu0.png")
		self.signs=pg.image.load(self.globalpath+"/uresources/signs.png")
		self.sessions_cont=5
		self.lista0=[3,4]*self.sessions_cont    #task list
		shuffle(self.lista0)
		self.ghost0=pg.image.load(self.globalpath+"/uresources/red_ghost.png")
		self.save()
		self.enter=0
		self.clock=pg.time.Clock()
		self.playtime=0.0
		self.ghostpos_y=0
		self.ghostpos_x=0
		self.loop()

	def save(self):
		self.file0 = open(self.globalpath + "/marcas.txt",'w')
		for index,element in enumerate(self.lista0):
			self.file0.write(str(index*12*250)+"\t"+str(element)+"\n")
		self.file0.close()

	def loop(self): #main loop
		while True:
			self.handler()
			self.draw()
			self.d=self.clock.tick(self.fps)
			#self.playtime += self.d / 1000.0
			#print(self.playtime)

	def handler(self): #handler of events
		for event in pg.event.get():
			if event.type==QUIT:
				self.pub.publish("DY");pg.quit(); sys.exit()
			elif event.type==VIDEORESIZE:
				self.screen= pg.display.set_mode(event.size,HWSURFACE|DOUBLEBUF|RESIZABLE)
				self.screen_w, self.screen_h=self.screen.get_size()
				self.back=pg.transform.smoothscale(pg.image.load(self.globalpath+"/uresources/back.jpg"),(self.screen_w,self.screen_h))
			elif event.type==KEYDOWN:
				if event.key==K_ESCAPE:
					if self.menu!=6:
						pg.quit();sys.exit()
					else:
						self.menu=3
						self.pub.publish('XY')
						self.ghostpos_x=0
						self.ghostpos_y=0
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
					elif event.key==K_LEFT and self.ghostpos_x>-5:
						self.ghostpos_x-=1
					elif event.key==K_RIGHT and self.ghostpos_x<5:
						self.ghostpos_x+=1
					pg.event.clear()

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
		pg.display.update()

	def menu_0(self): #first menu [login, new user, exit]
		if self.screen_h//2 - 90<self.mouse_y<self.screen_h//2 + 90:
			for i in range(3):
				if i*self.screen_w//3+self.screen_w//6-109<self.mouse_x<i*self.screen_w//3+self.screen_w//6+109:
					self.screen.blit(self.menu0,(i*self.screen_w//3+self.screen_w//6-109,self.screen_h//2-90),Rect(218,180*i,218,180))
					if pg.mouse.get_pressed()==(1,0,0) and self.click_flag == (0,0,0):
						if i==0:    self.menu=1
						if i==1:    self.menu=2
						if i==2:    self.pub.publish("DY");pg.quit();sys.exit()
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
								self.pub.publish("UN"+str(self.user))
								break
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

	def menu_3(self):  #user menu [new calibration, guide, training, back]
		if self.screen_h//2-200<self.mouse_y<self.screen_h//2-110:
			if self.screen_w//2-218<self.mouse_x<self.screen_w//2+218:
				self.screen.blit(self.menu0,(self.screen_w//2-218,self.screen_h//2-200),Rect(0,900,436,90))
				if pg.mouse.get_pressed()==(1,0,0) and self.click_flag == (0,0,0):
					self.menu=5
					self.pub.publish("NC")
					self.click_flag=(1,0,0)
				elif pg.mouse.get_pressed()==(0,0,0):
					self.click_flag=(0,0,0)
			else:
				self.screen.blit(self.menu0,(self.screen_w//2-218,self.screen_h//2-200),Rect(0,810,436,90))
			if self.screen_w//2+218+10<self.mouse_x<self.screen_w//2+218+100:
				self.screen.blit(self.menu0,(self.screen_w//2+218+10,self.screen_h//2-200),Rect(109,990,109,90))
				if pg.mouse.get_pressed()==(1,0,0) and self.click_flag == (0,0,0):
					self.menu=4
					self.click_flag=(1,0,0)
				elif pg.mouse.get_pressed()==(0,0,0):
					self.click_flag=(0,0,0)
			else:
				self.screen.blit(self.menu0,(self.screen_w//2+218+10,self.screen_h//2-200),Rect(0,990,109,90))
		else:
			self.screen.blit(self.menu0,(self.screen_w//2-218,self.screen_h//2-200),Rect(0,810,436,90))
			self.screen.blit(self.menu0,(self.screen_w//2+218+10,self.screen_h//2-200),Rect(0,990,109,90))
		if self.screen_h//2-70<self.mouse_y<self.screen_h//2+20:
			if self.screen_w//2-218<self.mouse_x<self.screen_w//2+218:
				self.screen.blit(self.menu0,(self.screen_w//2-218,self.screen_h//2-70),Rect(0,1170,436,90))
				if pg.mouse.get_pressed()==(1,0,0) and self.click_flag == (0,0,0):
					self.menu=6
					self.pub.publish('TR')
					pg.time.wait(200)
					self.pub.publish('XX')
					self.click_flag=(1,0,0)
				elif pg.mouse.get_pressed()==(0,0,0):
					self.click_flag=(0,0,0)
			else:
				self.screen.blit(self.menu0,(self.screen_w//2-218,self.screen_h//2-70),Rect(0,1080,436,90))
		else:
			self.screen.blit(self.menu0,(self.screen_w//2-218,self.screen_h//2-70),Rect(0,1080,436,90))
		if self.screen_h//2+110 <self.mouse_y<self.screen_h//2+200:
			if self.screen_w//2-54<self.mouse_x<self.screen_w//2+54:
				self.screen.blit(self.menu0,(self.screen_w//2-54,self.screen_h//2+110),Rect(327,720,109,90))
				if pg.mouse.get_pressed()==(1,0,0) and self.click_flag == (0,0,0):
					self.menu=0
					self.user=""
					self.click_flag=(1,0,0)
				elif pg.mouse.get_pressed()==(0,0,0):
					self.click_flag=(0,0,0)
			else:
				self.screen.blit(self.menu0,(self.screen_w//2-54,self.screen_h//2+110),Rect(218,720,109,90))
		else:
			self.screen.blit(self.menu0,(self.screen_w//2-54,self.screen_h//2+110),Rect(218,720,109,90))

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
		pg.time.wait(2300)
		self.screen.fill((127,127,127))
		pg.time.wait(100)
		self.screen.blit(self.signs,(self.screen_w//2 - 158, self.screen_h//2 - 148),Rect(i*316,0,316,296))
		pg.display.update()
		pg.time.wait(1500)
		self.screen.fill((127,127,127))
		pg.display.update()
		pg.time.wait(4000)
		self.screen.blit(self.signs,(self.screen_w//2 - 158, self.screen_h//2 - 148),Rect(5*316,0,316,296))
		pg.display.update()
		pg.time.wait(4000)

	def menu_6(self):
		self.screen.fill((0,0,0))
		self.screen.blit(self.ghost0,(self.screen_w//2-77//2+self.ghostpos_x*77,self.screen_h//2-77//2+self.ghostpos_y*77),Rect(0,0,77,77))

a=user_interface()
