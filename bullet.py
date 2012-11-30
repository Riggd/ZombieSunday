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
		somber_engine.Active.__init__(self, sprite, somber=somber, pos=(x, y))
		for player in somber.current_level.get_sprite_group('player'):
			self.player = player
			self.level = player.level
		if self.player.direction == 1:
			self.direction = 1
		else:
			self.direction = -1
			
		self.x_offset = x
		self.y_offset = y
		if from_player:
			self.set_pos_to_entity(self.player)
		self.level.add_object(self, 'bullets')
		
		self.timer = 0
		self.damage = 0
		self.duration = 0
		self.hspeed = 0
		
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
	
	def set_pos_to_entity(self, entity):
		x = entity.pos[0]
		y = self.y_offset + entity.pos[1] - (self.sprite.get_height() / 2) + (entity.sprite.get_height() / 2) - 14
		if entity.direction == 1:
			x += entity.sprite.get_width() + self.x_offset
		else:
			x += -self.x_offset - self.sprite.get_width()
		self.pos[0] = x
		self.pos[1] = y
				
class DefaultBullet(Bullet):
	def __init__(self, somber, x=0, y=0):
		Bullet.__init__(self, somber, x, y)
		self.duration = 1
		self.hspeed = 800
		self.damage = 20
		
		self.hspeed = (self.hspeed + abs(self.player.hspeed)) * self.direction
		
	def update(self):
		Bullet.update(self)
		
	def hit(self):
		for zombie in self.level.get_sprite_group('zombies'):
			if self.collides_with(zombie):
				self.kill()
				zombie.health[0] -= self.damage
				
class SpeedBullet(Bullet):
	def __init__(self, somber, x=0, y=0):
		Bullet.__init__(self, somber, x, y)
		self.duration = 1
		self.hspeed = 1000
		self.damage = 5

		self.hspeed = (self.hspeed + abs(self.player.hspeed)) * self.direction
		
	def update(self):
		Bullet.update(self)
		
	def hit(self):
		for zombie in self.level.get_sprite_group('zombies'):
			if self.collides_with(zombie):
				self.kill()
				zombie.health[0] -= self.damage

class LobBullet(Bullet):
	def __init__(self, somber, x=0, y=0):
		Bullet.__init__(self, somber, x, y, sprite='sprites/bullets/bullet_lob.png')
		self.duration = 1
		self.hspeed = 500
		self.vspeed = -500
		self.gravity = 20

		self.hspeed = (self.hspeed + abs(self.player.hspeed)) * self.direction
		
	def update(self):
		Bullet.update(self)
		
	def hit(self):
		if self.collides_with_group(self.level.get_sprite_group('ground')):
			Explosion(self.somber, self.pos[0] - 150, self.pos[1] - 112)
			self.kill()

class Explosion(Bullet):
	def __init__(self, somber, x=0, y=0):
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

class FireBullet(Bullet):
	def __init__(self, somber, x=0, y=0):
		x = -150
		Bullet.__init__(self, somber, x, y, sprite='sprites/bullets/bullet_fire_0.png')
		self.add_animation('anim', 10, ['sprites/bullets/bullet_fire_0.png', 'sprites/bullets/bullet_fire_1.png'])
		self.set_animation('anim')
		
		self.duration = .7
		self.hspeed = 300
		self.damage = 40
		
		if self.direction < 0:
			self.flip_horizontally()
		self.hspeed = (self.hspeed + abs(self.player.hspeed)) * self.direction
		
	def update(self):
		Bullet.update(self)
		
	def hit(self):
		for zombie in self.level.get_sprite_group('zombies'):
			if self.collides_with(zombie):
				self.kill()
				zombie.health[0] -= self.damage
				Fire(self.somber, zombie)
	
class Fire(Bullet):
	def __init__(self, somber, entity, x=0, y=0):
		Bullet.__init__(self, somber, x, y, from_player=False, sprite='sprites/fire/fire_0.png')
		self.entity = entity
		self.hit_timer = 0
		self.hit_rate = .5
		self.duration = 10
		self.damage = 1
		
	def update(self):
		Bullet.set_pos_to_entity(self, self.entity)
		Bullet.update(self)
		
	def hit(self):
		if self.hit_timer >= self.hit_rate:
			self.entity.health[0] -= self.damage
			self.hit_timer -= self.hit_rate
			print "FIRE!"
		self.hit_timer += self.delta_speed

class ForceBullet(Bullet):
	def __init__(self, somber, x=0, y=0):
		Bullet.__init__(self, somber, x, y, sprite='sprites/bullets/bullet_force.png')
		
		self.duration = .7
		self.hspeed = 500
		self.damage = 0
		
		if self.direction < 0:
			self.flip_horizontally()
		self.hspeed = self.hspeed * self.direction
		
	def update(self):
		Bullet.update(self)
		
	def hit(self):
		for zombie in self.level.get_sprite_group('zombies'):
			if self.collides_with(zombie):
				zombie.push_speed = self.hspeed
				zombie.vspeed = -100
				zombie.push_duration = self.duration
