#Levels
#Author list:
#	Luke Martin <ltmartin@bsu.edu>
import somber as somber_engine

def create_title_screen(somber):
	_level = somber.create_level('Title Screen')
	
	_level.create_sprite_group('background_0')
	_level.create_sprite_group('background_1')
	_level.create_sprite_group('background_2')
	_level.create_sprite_group('player')
	_level.create_sprite_group('ui')
	
	Background(somber,_level,'background_sky.png','background_0')
	Background(somber,_level,'background_trees_back.png','background_1',y=280)
	Background(somber,_level,'background_trees_fore.png','background_2',y=409)
	
	return _level

class Background(somber_engine.Active):
	def __init__(self,somber,level,sprite,sprite_group,x=0,y=0):
		somber_engine.Active.__init__(self,sprite,somber=somber,pos=(x,y))
		
		self.hspeed = -level.get_sprite_group_z_level(sprite_group)
		
		level.add_object(self,sprite_group)
