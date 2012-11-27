# Bullets
# Author list:
# 	Luke Martin <ltmartin@bsu.edu>
# 	Michael Milkovic <mlmilkovic@bsu.edu>
# 	Derek Onay <dsonay@bsu.edu>
# 	Ryan Wiesjahn <rwiesjahn@bsu.edu>

import somber as somber_engine
from weapon import *

class Bullet(somber_engine.Active):
	def __init__(self, somber, character, x_offset=0, y_offset=0, direction=1):
		sprite = 'sprites/bullets/bullet_default.png'
		x = x_offset + character.pos[0] + (character.sprite.get_width() * character.direction)
		y = y_offset + character.pos[1] + (character.sprite.get_height() / 2)
		somber_engine.Active.__init__(self, sprite, somber=somber, pos=(x, y))
		character.level.add_object(self, 'bullets')
		self.character = character
		self.level = character.level
		self.hspeed = (600 + abs(character.hspeed)) * direction
		self.damage = 10
		
		if character.direction == 0:
			self.hspeed = -self.hspeed
		
	def update(self):
		self.hit()
		somber_engine.Active.update(self)
		
	def hit(self):
		for zombie in self.level.get_sprite_group('zombies'):
			if self.collides_with(zombie):
				self.kill()
				zombie.health[0] -= self.damage
				
class LobBullet(somber_engine.Active):
	def __init__(self, somber, character, x_offset=0, y_offset=0):
		sprite = 'sprites/bullets/bullet_default.png'
		x = x_offset + character.pos[0] + (character.sprite.get_width() * character.direction)
		y = y_offset + character.pos[1] + (character.sprite.get_height() / 2)
		somber_engine.Active.__init__(self, sprite, somber=somber, pos=(x, y))
		character.level.add_object(self, 'bullets')
		self.character = character
		self.level = character.level
		self.hspeed = 500
		self.vspeed = -500
		self.gravity = 20

		if character.direction == 0:
			self.hspeed = -self.hspeed
		
	def update(self):
		self.hit()
		somber_engine.Active.update(self)

	def hit(self):
		if self.collides_with_group(self.level.get_sprite_group('ground')):
			self.kill()
			Explosion(self.somber, self.character, self.pos[0] - 150, self.pos[1] - 147)
				
class Explosion(somber_engine.Active):
	def __init__(self, somber, character, x=0, y=0):
		sprite = 'sprites/bullets/explosion.png'
		somber_engine.Active.__init__(self, sprite, somber=somber, pos=(x, y))
		character.level.add_object(self, 'bullets')
		self.character = character
		self.level = character.level
		self.damage = 40
		self.duration = 1
		self.timer = 0
		
		self.hit()
		
	def update(self):
		self.time()
		somber_engine.Active.update(self)

	def hit(self):
		for zombie in self.level.get_sprite_group('zombies'):
			if self.collides_with(zombie):
				zombie.health[0] -= self.damage
	
	def time(self):
		if self.timer < self.duration:
			self.timer += self.character.delta_speed
		else:
			self.kill()

class FireBullet(somber_engine.Active):
	def __init__(self, somber, character):
		sprite = 'sprites/bullets/bullet_fire.png'
		x = character.pos[0] + (character.sprite.get_width() * character.direction)
		y = character.pos[1] + (character.sprite.get_height() / 2) - 82
		somber_engine.Active.__init__(self, sprite, somber=somber, pos=(x, y))
		character.level.add_object(self, 'bullets')
		self.character = character
		self.level = character.level
		self.damage = 2
		
	def update(self):
		self.hit()
		somber_engine.Active.update(self)
		
	def hit(self):
		for zombie in self.level.get_sprite_group('zombies'):
			if self.collides_with(zombie):
				zombie.health[0] -= self.damage
