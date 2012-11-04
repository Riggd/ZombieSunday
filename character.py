#For the handling of characters, both Player-controlled and NPCs
#Author list:
#	Luke Martin <ltmartin@bsu.edu>
import somber as somber_engine
from weapon import *

class Character(somber_engine.Active):
	def __init__(self,somber,level,sprite,sprite_group,x=0,y=0):
		somber_engine.Active.__init__(self,sprite,somber=somber,pos=(x,y))
		self.level = level
		self.sprite_group = sprite_group
		level.add_object(self,sprite_group)
		
		self.weapon = Weapon()
	
	def update(self):
		somber_engine.Active.update(self)