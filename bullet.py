# Bullets
# Author list:
# 	Luke Martin <ltmartin@bsu.edu>
# 	Michael Milkovic <mlmilkovic@bsu.edu>
# 	Derek Onay <dsonay@bsu.edu>
# 	Ryan Wiesjahn <rwiesjahn@bsu.edu>

import somber as somber_engine
import os
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
		self.sprite_group = 'explosions'
			
		self.x_offset = x
		self.y_offset = y
		if from_player:
			self.set_pos_to_entity(self.player)
		self.level.add_object(self, self.sprite_group)
		
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
			self.remove()
			
	def remove(self):
		self.kill()
		
	def hit(self):
		pass
	
	def set_pos_to_entity(self, entity):
		x = entity.pos[0]
		y = self.y_offset + entity.pos[1] - (self.sprite.get_height() / 2) + (entity.sprite.get_height() / 2) - 14
		if entity.direction == 1:
			x += entity.sprite.get_width() + self.x_offset
		else:
			x += -self.sprite.get_width() - self.x_offset
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
		self.damage = 8

		self.hspeed = (self.hspeed + abs(self.player.hspeed)) * self.direction
		
	def update(self):
		Bullet.update(self)
		
	def hit(self):
		for zombie in self.level.get_sprite_group('zombies'):
			if self.collides_with(zombie):
				self.kill()
				zombie.health[0] -= self.damage

class SpeedSpeedBullet(Bullet):
	def __init__(self, somber, x=0, y=0):
		Bullet.__init__(self, somber, x, y)
		self.duration = 1
		self.hspeed = 1800
		self.damage = 5

		self.hspeed = (self.hspeed + abs(self.player.hspeed)) * self.direction
		
	def update(self):
		Bullet.update(self)
		
	def hit(self):
		for zombie in self.level.get_sprite_group('zombies'):
			if self.collides_with(zombie):
				self.kill()
				zombie.health[0] -= self.damage
				
class SpeedFireBullet(Bullet):
	def __init__(self, somber, x=0, y=0):
		Bullet.__init__(self, somber, x, y, sprite='sprites/bullets/bullet_fire_0.png')
		self.add_animation('anim', 10, ['sprites/bullets/bullet_fire_0.png', 'sprites/bullets/bullet_fire_1.png'])
		self.set_animation('anim')
		
		self.duration = 1
		self.hspeed = 700
		self.damage = 6
		
		if self.direction < 0:
			self.set_animation('anim',flip_horizontally=True)
		else:
			self.set_animation('anim')
			
		self.hspeed = (self.hspeed + abs(self.player.hspeed)) * self.direction
		
	def update(self):
		Bullet.update(self)
		
	def hit(self):
		for zombie in self.level.get_sprite_group('zombies'):
			if self.collides_with(zombie):
				self.kill()
				zombie.health[0] -= self.damage
				if zombie.fire_object != None:
					zombie.fire_object.kill()
				fire = Fire(self.somber, zombie)
				zombie.fire_object = fire
				
class SpeedLobBullet(Bullet):
	def __init__(self, somber, x=0, y=0):
		Bullet.__init__(self, somber, x, y, sprite='sprites/bullets/bullet_lob.png')
		self.duration = 1
		self.hspeed = 700
		self.vspeed = -400
		self.gravity = 50

		self.hspeed = (self.hspeed + abs(self.player.hspeed)) * self.direction
		
	def update(self):
		Bullet.update(self)
		
	def hit(self):
		if self.collides_with_group(self.level.get_sprite_group('ground')):
			Explosion(self.somber, x=self.pos[0] - 150, y=self.somber.win_size[1] - 238)
			self.kill()

class SpeedForceBullet(Bullet):
	def __init__(self, somber, x=0, y=0):
		Bullet.__init__(self, somber, x, y, sprite='sprites/bullets/bullet_force.png')
		
		self.duration = .7
		self.hspeed = 1000
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
				
class FireBullet(Bullet):
	def __init__(self, somber, x=0, y=0):
		Bullet.__init__(self, somber, x, y, sprite='sprites/bullets/bullet_fire_0.png')
		self.add_animation('anim', 10, ['sprites/bullets/bullet_fire_0.png', 'sprites/bullets/bullet_fire_1.png'])
		
		if self.direction < 0:
			self.set_animation('anim',flip_horizontally=True)
		else:
			self.set_animation('anim')
		
		self.duration = .7
		self.hspeed = 300
		self.damage = 10
		
		self.hspeed = (self.hspeed + abs(self.player.hspeed)) * self.direction
		
	def update(self):
		Bullet.update(self)
		
	def hit(self):
		for zombie in self.level.get_sprite_group('zombies'):
			if self.collides_with(zombie):
				self.kill()
				zombie.health[0] -= self.damage
				if zombie.fire_object != None:
					zombie.fire_object.kill()
				Fire(self.somber, zombie)
				
class FireFireBullet(Bullet):
	def __init__(self, somber, x=0, y=0):
		y=-25
		Bullet.__init__(self, somber, x, y, sprite='sprites/bullets/bullet_firefire.png')
		self.add_animation('anim', 10, ['sprites/bullets/bullet_firefire.png'])
		
		self.duration = 0
		self.hspeed = 300
		self.damage = 1
		
		self.hspeed = (self.hspeed + abs(self.player.hspeed)) * self.direction
		
	def update(self):
		Bullet.set_pos_to_entity(self, self.player)
		self.flip()
		Bullet.update(self)
		
	def flip(self):
		if self.player.direction <= 0:
			self.set_animation('anim',flip_horizontally=True)
		else:
			self.set_animation('anim')
		
	def hit(self):
		for zombie in self.level.get_sprite_group('zombies'):
			if self.collides_with(zombie):
				zombie.health[0] -= self.damage
				if zombie.fire_object != None:
					zombie.fire_object.kill()
				Fire(self.somber, zombie)
	
	def remove(self):
		if not self.somber.input[' ']:
			Bullet.remove(self)
			self.player.weapon.firefire_check = False

class FireLobBullet(Bullet):
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
			Explosion(self.somber, x=self.pos[0] - 150, y=self.somber.win_size[1] - 238, set_fire=True)
			self.kill()

class FireForceBullet(Bullet):
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
				zombie.push_speed = self.hspeed + (100 * self.direction)
				zombie.vspeed = -220
				zombie.push_duration = self.duration
				if zombie.fire_object != None:
					zombie.fire_object.kill()
				Fire(self.somber, zombie)
	
class Fire(Bullet):
	def __init__(self, somber, entity, duration=3, hit_rate=.5, x=0, y=0):
		x = -110
		y = -22
		Bullet.__init__(self, somber, x, y, from_player=False, sprite='sprites/fire/fire_0.png')
		self.entity = entity
		self.entity.fire_object = self
		self.hit_rate = hit_rate
		self.duration = duration
		self.hit_timer = 0
		self.damage = 10
		
	def update(self):
		Bullet.set_pos_to_entity(self, self.entity)
		Bullet.update(self)
		
	def hit(self):
		if self.hit_timer >= self.hit_rate:
			self.entity.health[0] -= self.damage
			self.hit_timer -= self.hit_rate
			print "FIRE!"
		self.hit_timer += self.delta_speed
		
	def remove(self):
		self.entity.fire_object = None
		Bullet.remove(self)

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
			Explosion(self.somber, x=self.pos[0] - 150, y=self.somber.win_size[1] - 238)
			self.kill()
			
class LobLobBullet(Bullet):
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
			Explosion(self.somber, x=self.pos[0] - 244, y=self.somber.win_size[1] - 327, big=True)
			self.kill()
			
class LobForceBullet(Bullet):
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
			Explosion(self.somber, x=self.pos[0] - 150, y=self.somber.win_size[1] - 238, push=True)
			self.kill()

class Explosion(Bullet):
	def __init__(self, somber, x=0, y=0, big=False, set_fire=False, push=False):
		self.sprite='sprites/bullets/explosion_small.png'
		if big:
			self.sprite='sprites/bullets/explosion_big.png'
		Bullet.__init__(self, somber, x, y,from_player=False, sprite=self.sprite)
		self.set_fire = set_fire
		self.push = push
		self.has_hit = False
		self.sprite_group = 'explosions'
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
					if self.set_fire:
						if zombie.fire_object != None:
							zombie.fire_object.kill()
						Fire(self.somber, zombie)
					if self.push:
						zombie.pos[1] = self.somber.win_size[1] - zombie.sprite.get_height() - 500
						zombie_pos = zombie.pos[0] + (zombie.sprite.get_width() / 2)
						explosion_pos = self.pos[0] + (self.sprite.get_width() / 2)
						direction = 1
						if zombie_pos <= explosion_pos:
							direction = -1
						zombie.push_speed = 600
						zombie.vspeed = -2020

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
				zombie.vspeed = -220
				zombie.push_speed = self.hspeed + (100 * self.direction)

class ForceForceBullet(Bullet):
	def __init__(self, somber, x=0, y=0):
		Bullet.__init__(self, somber, x, y, sprite='sprites/bullets/bullet_force.png')
		
		self.duration = .8
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
				zombie.vspeed = -400
				zombie.push_speed = self.hspeed + (300 * self.direction)