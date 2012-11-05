#Levels
#Author list:
#	Luke Martin <ltmartin@bsu.edu>
import somber as somber_engine
import random
from character import *

class Title_Screen(somber_engine.Level):
	def __init__(self,somber):
		somber_engine.Level.__init__(self,somber,'Title Screen')
	
	def create_level(self):
		self.create_sprite_group('background_0')
		self.create_sprite_group('background_1')
		self.create_sprite_group('background_2')
		self.create_sprite_group('player')
		self.create_sprite_group('ui')
		
		Background(self.somber,self,'background_sky.png','background_0')
		Background(self.somber,self,'background_trees_back.png','background_1',y=330)
		Sun(self.somber,self,'background_sun.png','background_1',x=620,y=5)
		Cloud(self.somber,self,'background_cloud_1.png','background_2',x=660,y=10)
		Cloud(self.somber,self,'background_cloud_2.png','background_2',x=540,y=200)
		Cloud(self.somber,self,'background_cloud_3.png','background_2',y=90)
		Background(self.somber,self,'background_trees_fore.png','background_2',y=390)
		Background(self.somber,self,'foreground_grass.png','player',y=515)
		
		self.level = self
		
		self.setup()
		
		return self.level
	
	def setup(self):
		for group in self.level.sprite_groups:
			_speed = -(self.level.sprite_groups.index(group)*8)
			
			for sprite in group['group']:
				sprite.hspeed = _speed
	
	def update(self):
		pass

class Endless_Level(somber_engine.Level):
	def __init__(self,somber):
		somber_engine.Level.__init__(self,somber,'Endless Level')

	def create_level(self):
		self.create_sprite_group('background_0')
		self.create_sprite_group('clouds')
		self.create_sprite_group('background_1')
		self.create_sprite_group('background_2')
		self.create_sprite_group('player')
		self.create_sprite_group('tiles',z=4)
		self.create_sprite_group('ladders',z=5)
		self.create_sprite_group('ui')
		
		Background(self.somber,self,'background_sky.png','background_0')
		Background(self.somber,self,'background_trees_back.png','background_1',y=330)
		Sun(self.somber,self,'background_sun.png','background_1',x=620,y=5)
		Cloud(self.somber,self,'background_cloud_1.png','clouds',x=660,y=10)
		Cloud(self.somber,self,'background_cloud_2.png','clouds',x=540,y=200)
		Cloud(self.somber,self,'background_cloud_3.png','clouds',y=90)
		Background(self.somber,self,'background_trees_fore.png','background_2',y=390)
		Background(self.somber,self,'foreground_grass.png','tiles',y=515)
		Background(self.somber,self,'foreground_grass.png','tiles',x=320,y=387)
		Ladder(self.somber,self,'ladder.png','ladders',x=300,y=451)
		Ladder(self.somber,self,'ladder.png','ladders',x=300,y=387)
		
		self.level = self
		
		self.setup()
		
		return self
	
	def setup(self):
		pass
	
	def update(self):
		for group in self.level.sprite_groups:
			if group['name'] in ['player','tiles','ladders']:
				continue
			
			_layer = self.level.sprite_groups.index(group)
			
			if group['name'] == 'clouds':
				_scroll_x = self.somber.camera_pos[0]-((self.somber.camera_pos[0]/9)*_layer)
				
				for sprite in group['group']:
					sprite.set_pos((_scroll_x+sprite.start_pos[0],sprite.rect.topleft[1]))
			else:
				_scroll_x = self.somber.camera_pos[0]-((self.somber.camera_pos[0]/9)*_layer)
				
				for sprite in group['group']:
					sprite.set_pos((_scroll_x,sprite.rect.topleft[1]))

class Background(somber_engine.Active):
	def __init__(self,somber,level,sprite,sprite_group,x=0,y=0):
		somber_engine.Active.__init__(self,sprite,somber=somber,pos=(x,y))
		
		self.level = level
		self.sprite_group = sprite_group
		
		level.add_object(self,sprite_group)
	
	def update(self):
		if self.pos[0]<=-self.sprite.get_width()/2:
			self.set_pos((self.pos[0]+(self.sprite.get_width()/2),self.pos[1]))
		
		somber_engine.Active.update(self)

class Ladder(somber_engine.Active):
	def __init__(self,somber,level,sprite,sprite_group,x=0,y=0):
		somber_engine.Active.__init__(self,sprite,somber=somber,pos=(x,y))
		
		self.level = level
		self.sprite_group = sprite_group
		self.set_pos((x,y))
		
		level.add_object(self,sprite_group)

class Cloud(somber_engine.Active):
	def __init__(self,somber,level,sprite,sprite_group,x=0,y=0):
		somber_engine.Active.__init__(self,sprite,somber=somber,pos=(x,y))
		
		self.level = level
		self.sprite_group = sprite_group
		
		level.add_object(self,sprite_group)
	
	def update(self):
		#if self.pos[0]<-self.sprite.get_width():
		#	self.set_pos((800,self.pos[1]))
		
		somber_engine.Active.update(self)

class Sun(somber_engine.Active):
	def __init__(self,somber,level,sprite,sprite_group,x=0,y=0):
		somber_engine.Active.__init__(self,sprite,somber=somber,pos=(x,y))
		
		self.level = level
		self.sprite_group = sprite_group
		
		level.add_object(self,sprite_group)