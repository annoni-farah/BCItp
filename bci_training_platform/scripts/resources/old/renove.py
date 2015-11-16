#!/usr/bin/env python
import os, sys, rospy, pygame as pg
from random import shuffle
from pygame.locals import *
from std_msgs.msg import String



class user_interface:
	def __init__(self):
		pg.init()
		rospy.init_node('listener', anonymous=True)
		rospy.Subscriber('canal5', String, self.callback)
		self.pub=rospy.Publisher('manager_gui', String, queue_size=100)
		self.screen= pg.display.set_mode((700,500),HWSURFACE|DOUBLEBUF|RESIZABLE)#|pg.FULLSCREEN)
		self.screen_w, self.screen_h=self.screen.get_size()
		self.mouse_x, self.mouse_y=0,0
		self.globalpath=os.path.abspath(os.path.dirname(__file__))
		print(self.globalpath)
		self.back=pg.transform.smoothscale(pg.image.load(self.globalpath+"/uresources/back.jpg"),(self.screen_w,self.screen_h))
		self.menu=0
		self.fps=15
		self.fonte=pg.font.Font(self.globalpath+"/uresources/ubuntu.bold.ttf", 33)
		self.user=""
		self.beep = pg.mixer.Sound(self.globalpath+"/uresources/reoubeep.ogg")
		self.users_list=self.globalpath+"/uresources/users_list.txt"
		self.click_flag=(0,0,0)
		self.menu_pos=[[0+self.screen_w//6 - 218//2,self.screen_w//3 +self.screen_w//6 - 218//2]]
		self.menu0=pg.image.load(self.globalpath+"/uresources/menu0.png")
		self.signs=pg.image.load(self.globalpath+"/uresources/signs.png")
		self.sessions_cont=1
		self.clock=pg.time.Clock()
		self.playtime=0.0
		self.loop()

	def loop(self):
		while True:
			self.handler()
			self.draw()
			self.d=self.clock.tick(self.fps)
			#self.playtime += self.d / 1000.0
			#print(self.playtime)

	def handler(self):
		for event in pg.event.get():
			if event.type==QUIT:
				pg.quit(); sys.exit()
			elif event.type==VIDEORESIZE:
				self.screen= pg.display.set_mode(event.size,HWSURFACE|DOUBLEBUF|RESIZABLE)
				self.screen_w, self.screen_h=self.screen.get_size()
				self.back=pg.transform.smoothscale(pg.image.load("back.jpg"),(self.screen_w,self.screen_h))
			elif event.type==KEYDOWN:
				if event.key==K_ESCAPE:
					pg.quit();sys.exit()
				if self.menu==1:
					if len(self.user)<21:
						if 64<event.key<91 or 96<event.key<123 or event.key==95 or 47<event.key<58:
							self.user=self.user+chr(event.key)
					if event.key==K_BACKSPACE and len(self.user)>0:
						self.user=self.user[0:-1]

	def draw(self):
		self.screen.blit(self.back,(0,0))
		self.mouse_x, self.mouse_y=pg.mouse.get_pos()
		if self.menu==0:
			self.menu_0()
		elif self.menu==1:
			self.menu_1()
		elif self.menu==2:
			self.menu_0()
		elif self.menu==3:
			self.menu_3()
		elif self.menu==4:
			self.menu_4()
		elif self.menu==5:
			self.menu_5()
		pg.display.update()

	def menu_0(self):
		if self.screen_h//2 - 90<self.mouse_y<self.screen_h//2 + 90:
			for i in range(3):
				if i*self.screen_w//3+self.screen_w//6-109<self.mouse_x<i*self.screen_w//3+self.screen_w//6+109:
					self.screen.blit(self.menu0,(i*self.screen_w//3+self.screen_w//6-109,self.screen_h//2-90),Rect(218,180*i,218,180))
					if pg.mouse.get_pressed()==(1,0,0) and self.click_flag == (0,0,0):
						if i==0:    self.menu=1
						if i==1:    self.menu=0
						if i==2:    pg.quit();sys.exit()
						self.click_flag=(1,0,0)
					elif pg.mouse.get_pressed()==(0,0,0):
						self.click_flag=(0,0,0)
				else:
					self.screen.blit(self.menu0,(i*self.screen_w//3+self.screen_w//6-109,self.screen_h//2-90),Rect(0,180*i,218,180))
		else:
			for i in range(3):
				self.screen.blit(self.menu0,(i*self.screen_w//3+self.screen_w//6-109,self.screen_h//2-90),Rect(0,180*i,218,180))

	def menu_1(self):
		self.screen.blit(self.menu0,(self.screen_w//2-218,self.screen_h//2 - 180),Rect(0,540,436,90))
		self.screen.blit(self.menu0,(self.screen_w//2-218,self.screen_h//2 - 45),Rect(0,630,436,90))
		self.nickname=self.fonte.render(str(self.user), 1, (255,255,255))
		self.screen.blit(self.nickname,(self.screen_w//2 - self.nickname.get_width()//2,self.screen_h//2 - 22))

		if self.screen_h//2 - 45 < self.mouse_y < self.screen_h//2 +45:
			if self.screen_w//2-218 - 121 < self.mouse_x< self.screen_w//2-218 - 12:
				self.screen.blit(self.menu0,(self.screen_w//2-218-121,self.screen_h//2 - 45),Rect(327,720,109,90))
				if pg.mouse.get_pressed()==(1,0,0) and self.click_flag == (0,0,0):
					self.menu=0
					self.click_flag=(1,0,0)
				elif pg.mouse.get_pressed()==(0,0,0):
					self.click_flag=(0,0,0)
			else:
				self.screen.blit(self.menu0,(self.screen_w//2-218-121,self.screen_h//2 - 45),Rect(218,720,109,90))
			if self.screen_w//2+218 + 12 < self.mouse_x< self.screen_w//2+218 + 121:
				self.screen.blit(self.menu0,(self.screen_w//2+218+12,self.screen_h//2 - 45),Rect(109,720,109,90))
				if pg.mouse.get_pressed()==(1,0,0) and self.click_flag == (0,0,0):
					try:
						file=open(self.users_list,'r')
					except:
						file=open(self.users_list,'w')
						file=open(self.users_list,'r')

					for line in file.readlines():
						if line == (str(self.user)+'\n'):
							self.menu=3
							break
					self.click_flag=(1,0,0)
				elif pg.mouse.get_pressed()==(0,0,0):
					self.click_flag=(0,0,0)
			else:
				self.screen.blit(self.menu0,(self.screen_w//2+218+12,self.screen_h//2 - 45),Rect(0,720,109,90))
		else:
			self.screen.blit(self.menu0,(self.screen_w//2-218-121,self.screen_h//2 - 45),Rect(218,720,109,90))
			self.screen.blit(self.menu0,(self.screen_w//2+218+12,self.screen_h//2 - 45),Rect(0,720,109,90))

	def menu_3(self):
		if self.screen_h//2-200<self.mouse_y<self.screen_h//2-110:
			if self.screen_w//2-218<self.mouse_x<self.screen_w//2+218:
				self.screen.blit(self.menu0,(self.screen_w//2-218,self.screen_h//2-200),Rect(0,900,436,90))
				if pg.mouse.get_pressed()==(1,0,0) and self.click_flag == (0,0,0):
					self.menu=5
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

	def menu_4(self):
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

	def menu_5(self):
		if self.screen_h//2-90<self.mouse_y<self.screen_h//2+90:
			if self.screen_w//2-109<self.mouse_x<self.screen_w//2+109:
				self.screen.blit(self.menu0,(self.screen_w//2-109,self.screen_h//2-90),Rect(218,1350,218,180))
				if pg.mouse.get_pressed()==(1,0,0) and self.click_flag == (0,0,0):
					pg.mouse.set_visible(False)
					self.lista0=[1,2]*self.sessions_cont
					shuffle(self.lista0)
					self.screen.fill((127,127,127))
					pg.display.update()
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
		if self.screen_h//2+110 <self.mouse_y<self.screen_h//2+200:
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

	def callback(data):
	    global i, flag
	    i = data.data
	    flag=1

def callback(data):
	pass

def user_interface():
    global pub
    rospy.init_node('user_interface', anonymous=True)
    rospy.Subscriber('canal5', String, callback)
    pub=rospy.Publisher('manager_gui', String, queue_size=100)
	print("done")
	#a=user_interface()


user_interface()
