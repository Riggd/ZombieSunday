#For the handling of characters, both Player-controlled and NPCs
#Author list:
#	Luke Martin <ltmartin@bsu.edu>
import somber as somber_engine
from weapon import *

class Character(somber_engine.Active):
	def __init__(self,somber,level,sprite,sprite_group,x=0,y=0):
		somber_engine.Active.__init__(self,sprite,somber=somber,pos=(x,y))
		self.somber = somber
		self.level = level
		self.sprite_group = sprite_group
		level.add_object(self,sprite_group)
		
		self.climbing = False
		
		self.weapon = Weapon()
	
	def update(self):
		if self.collides_with_group(self.level.get_sprite_group('ladders')):
			if self.somber.input['up']:
				self.climbing = True
				self.vspeed = -50
			elif self.somber.input['down']:
				self.climbing = True
				self.vspeed = 50
			else:
				self.vspeed = 0
		else:
			self.climbing = False
		
		if not self.climbing:
			if self.collides_with_group(self.level.get_sprite_group('tiles')):
				if self.vspeed > 0:
					self.vspeed = 0
				self.gravity = 0
			else:
				self.gravity = 3
		else:
			self.gravity = 0
		
		somber_engine.Active.update(self)