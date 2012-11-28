# Bullets
# Author list:
# 	Luke Martin <ltmartin@bsu.edu>
# 	Michael Milkovic <mlmilkovic@bsu.edu>
# 	Derek Onay <dsonay@bsu.edu>
# 	Ryan Wiesjahn <rwiesjahn@bsu.edu>

import somber as somber_engine
from weapon import *

class Bullet(somber_engine.Active):
	def __init__(self, somber, x=0, y=0, from_player=True, sprite='sprites/bullets/bullet_default.png'):
		for player in somber.current_level.get_sprite_group('player'):
			self.player = player
			self.level = player.level
		if from_player:
			x += self.player.pos[0] + (self.player.sprite.get_width() * self.player.direction)
			y += self.player.pos[1] + (self.player.sprite.get_height() / 2)
		somber_engine.Active.__init__(self, sprite, somber=somber, pos=(x, y))
		self.level.add_object(self, 'bullets')
		
		self.timer = 0
		self.damage = 0
		self.duration = 0
		self.hspeed = 0
		
		if self.player.direction == 0:
			self.hspeed = -self.hspeed
		
	def update(self):
		self.hit()
		self.time()
		somber_engine.Active.update(self)
		
	def time(self):
		if self.timer < self.duration:
			self.timer += self.player.delta_speed
		else:
			self.kill()
		
	def hit(self):
		pass
				
class DefaultBullet(Bullet):
	def __init__(self, somber, x_offset=0, y_offset=0, direction=1):
		Bullet.__init__(self, somber, x_offset, y_offset)
		self.duration = 1
		self.hspeed = 600
		self.damage = 10
		
		self.hspeed = (self.hspeed + abs(self.player.hspeed)) * direction
		if self.player.direction == 0:
			self.hspeed = -self.hspeed
		
	def update(self):
		Bullet.update(self)
		
	def hit(self):
		for zombie in self.level.get_sprite_group('zombies'):
			if self.collides_with(zombie):
				self.kill()
				zombie.health[0] -= self.damage

class LobBullet(Bullet):
	def __init__(self, somber, x_offset=0, y_offset=0, direction=1):
		Bullet.__init__(self, somber, x_offset, y_offset, sprite='sprites/bullets/bullet_lob.png')
		self.duration = 1
		self.hspeed = 500
		self.vspeed = -500
		self.gravity = 20
		self.damage = 10
		
		self.hspeed = (self.hspeed + abs(self.player.hspeed)) * direction
		if self.player.direction == 0:
			self.hspeed = -self.hspeed
		
	def update(self):
		Bullet.update(self)
		
	def hit(self):
		if self.collides_with_group(self.level.get_sprite_group('ground')):
			Explosion(self.somber, self.pos[0] - 150, self.pos[1] - 112)
			self.kill()

class Explosion(Bullet):
	def __init__(self, somber, x=0, y=0, direction=1):
		Bullet.__init__(self, somber, x, y, from_player=False, sprite='sprites/bullets/explosion.png')
		self.has_hit = False
		self.duration = 1
		self.hspeed = 0
		self.damage = 40
		
	def update(self):
		Bullet.update(self)
		
	def hit(self):
		if not self.has_hit:
			self.has_hit = True
			for zombie in self.level.get_sprite_group('zombies'):
				if self.collides_with(zombie):
					zombie.health[0] -= self.damage

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

class ForceBullet(somber_engine.Active):
	def __init__(self, somber, x_offset=0, y_offset=0, direction=1):
		sprite = 'sprites/bullets/bullet_force.png'
		x = x_offset + character.pos[0] + (character.sprite.get_width() * character.direction)
		y = y_offset + character.pos[1] + (character.sprite.get_height() / 2)
		somber_engine.Active.__init__(self, sprite, somber=somber, pos=(x, y))
		character.level.add_object(self, 'bullets')
		self.character = character
		self.level = character.level
		self.hspeed = (600 + abs(character.hspeed)) * direction
		self.damage = 10
		self.duration = 1
		self.timer = 0
		
		if character.direction == 0:
			self.hspeed = -self.hspeed
			self.flip_horizontally()
		
	def update(self):
		self.hit()
		somber_engine.Active.update(self)
		
	def hit(self):
		for zombie in self.level.get_sprite_group('zombies'):
			if self.collides_with(zombie):
				self.kill()
				zombie.health[0] -= self.damage
