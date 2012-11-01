#Levels
#Author list:
#	Luke Martin <ltmartin@bsu.edu>
import somber as somber_engine

class Level:
	def __init__(self,somber):
		self.somber = somber
		
		self.level = somber_engine.Level('Title Screen')
		self.level.create_sprite_group('background_0')
		self.level.create_sprite_group('background_1')
		self.level.create_sprite_group('background_2')
		self.level.create_sprite_group('ui')
		
		Background(self.somber,self.level,'background_sky.png','background_0')
		Background(self.somber,self.level,'background_trees_back.png',
											'background_1',y=235)
		Background(self.somber,self.level,'background_trees_fore.png',
											'background_2',y=288)
	
	def add_object(self,object,group_name):
		self.level.add_object(object,group_name)

class Background(somber_engine.Active):
	def __init__(self,somber,level,sprite,z,x=0,y=0):
		somber_engine.Active.__init__(self,sprite,somber=somber,pos=(x,y))
		
		level.add_object(self,z)
