# Bullets
# Author list:
# 	Luke Martin <ltmartin@bsu.edu>
# 	Michael Milkovic <mlmilkovic@bsu.edu>
# 	Derek Onay <dsonay@bsu.edu>
# 	Ryan Wiesjahn <rwiesjahn@bsu.edu>

import somber as somber_engine
import os
from weapon import *
import config

class Bullet(somber_engine.Active):
	def __init__(self, somber, x=0, y=0, from_player=True, sprite_group='bullets', sprite='sprites/bullets/bullet_default.png'):
		somber_engine.Active.__init__(self, sprite, somber=somber, pos=(x, y))
		for player in somber.current_level.get_sprite_group('player'):
			self.player = player
			self.level = player.level
		if self.player.direction == 1:
			self.direction = 1
		else:
			self.direction = -1
		
		self.sprite_group = sprite_group
		self.timer = 0
		self.x_offset = x
		self.y_offset = y
		if from_player:
			self.set_pos_to_entity(self.player)
		self.level.add_object(self, self.sprite_group)
		
		self.damage = config.DEFAULT_DAMAGE
		self.duration = config.DEFAULT_DURATION
		self.hspeed = config.DEFAULT_HSPEED
		self.add_player_speed = config.DEFAULT_ADD_PLAYER_SPEED
		
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
		if self.add_player_speed:
			self.hspeed += abs(self.player.hspeed)
		self.hspeed *= self.direction
		
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
		self.duration = config.SPEED_DURATION
		self.hspeed = config.SPEED_HSPEED
		self.damage = config.SPEED_DAMAGE
		self.add_player_speed = config.SPEED_ADD_PLAYER_SPEED

		if self.add_player_speed:
			self.hspeed += abs(self.player.hspeed)
		self.hspeed *= self.direction
		
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
		self.duration = config.SPEEDSPEED_DURATION
		self.hspeed = config.SPEEDSPEED_HSPEED
		self.damage = config.SPEEDSPEED_DAMAGE
		self.add_player_speed = config.SPEEDSPEED_ADD_PLAYER_SPEED

		if self.add_player_speed:
			self.hspeed += abs(self.player.hspeed)
		self.hspeed *= self.direction
		
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
		
		self.duration = config.SPEEDFIRE_DURATION
		self.hspeed = config.SPEEDFIRE_HSPEED
		self.damage = config.SPEEDFIRE_DAMAGE
		self.add_player_speed = config.SPEEDFIRE_ADD_PLAYER_SPEED
		
		if self.direction < 0:
			self.set_animation('anim',flip_horizontally=True)
		else:
			self.set_animation('anim')
			
		if self.add_player_speed:
			self.hspeed += abs(self.player.hspeed)
		self.hspeed *= self.direction
		
	def update(self):
		Bullet.update(self)
		
	def hit(self):
		for zombie in self.level.get_sprite_group('zombies'):
			if self.collides_with(zombie):
				self.kill()
				zombie.health[0] -= self.damage
				Fire(self.somber, zombie, damage=config.SPEEDFIRE_FIRE_DAMAGE, duration=config.SPEEDFIRE_FIRE_DURATION, hit_rate=config.SPEEDFIRE_FIRE_RATE)
				
class SpeedLobBullet(Bullet):
	def __init__(self, somber, x=0, y=0):
		Bullet.__init__(self, somber, x, y, sprite='sprites/bullets/bullet_lob.png')
		self.duration = config.SPEEDLOB_DURATION
		self.hspeed = config.SPEEDLOB_HSPEED
		self.vspeed = config.SPEEDLOB_VSPEED
		self.gravity = config.SPEEDLOB_GRAVITY
		self.add_player_speed = config.SPEEDLOB_ADD_PLAYER_SPEED

		if self.add_player_speed:
			self.hspeed += abs(self.player.hspeed)
		self.hspeed *= self.direction
		
	def update(self):
		Bullet.update(self)
		
	def hit(self):
		if self.collides_with_group(self.level.get_sprite_group('ground')):
			Explosion(self.somber, damage=config.SPEEDLOB_EXPLOSION_DAMAGE, duration=config.SPEEDLOB_EXPLOSION_DURATION, x=self.pos[0] - 150, y=self.somber.win_size[1] - 238)
			self.kill()

class SpeedForceBullet(Bullet):
	def __init__(self, somber, x=0, y=0):
		Bullet.__init__(self, somber, x, y, sprite='sprites/bullets/bullet_force.png')
		
		self.duration = config.SPEEDFORCE_DURATION
		self.hspeed = config.SPEEDFORCE_HSPEED
		self.damage = config.SPEEDFORCE_DAMAGE
		self.add_player_speed = config.SPEEDFORCE_ADD_PLAYER_SPEED
		
		if self.direction < 0:
			self.flip_horizontally()
		
		if self.add_player_speed:
			self.hspeed += abs(self.player.hspeed)
		self.hspeed *= self.direction
		
	def update(self):
		Bullet.update(self)
		
	def hit(self):
		for zombie in self.level.get_sprite_group('zombies'):
			if self.collides_with(zombie):
				zombie.push_speed = self.hspeed + (config.SPEEDFORCE_FORCE_HSPEED * self.direction)
				zombie.vspeed = config.SPEEDFORCE_FORCE_VSPEED
				
class FireBullet(Bullet):
	def __init__(self, somber, x=0, y=0):
		Bullet.__init__(self, somber, x, y, sprite='sprites/bullets/bullet_fire_0.png')
		self.add_animation('anim', 10, ['sprites/bullets/bullet_fire_0.png', 'sprites/bullets/bullet_fire_1.png'])
		
		if self.direction < 0:
			self.set_animation('anim',flip_horizontally=True)
		else:
			self.set_animation('anim')
		
		self.duration = config.FIRE_DURATION
		self.hspeed = config.FIRE_HSPEED
		self.damage = config.FIRE_DAMAGE
		self.add_player_speed = config.FIRE_ADD_PLAYER_SPEED
		
		if self.add_player_speed:
			self.hspeed += abs(self.player.hspeed)
		self.hspeed *= self.direction
		
	def update(self):
		Bullet.update(self)
		
	def hit(self):
		for zombie in self.level.get_sprite_group('zombies'):
			if self.collides_with(zombie):
				self.kill()
				zombie.health[0] -= self.damage
				Fire(self.somber, zombie, damage=config.FIRE_FIRE_DAMAGE, duration=config.FIRE_FIRE_DURATION, hit_rate=config.FIRE_FIRE_RATE)
				
class FireFireBullet(Bullet):
	def __init__(self, somber, x=0, y=0):
		y=-25
		Bullet.__init__(self, somber, x, y, sprite='sprites/bullets/bullet_firefire.png')
		self.add_animation('anim', 10, ['sprites/bullets/bullet_firefire.png'])
		
		self.duration = 0
		self.hspeed = 0
		self.damage = config.FIREFIRE_DAMAGE
		
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
				Fire(self.somber, zombie, damage=config.FIREFIRE_FIRE_DAMAGE, duration=config.FIREFIRE_FIRE_DURATION, hit_rate=config.FIREFIRE_FIRE_RATE)
	
	def remove(self):
		if not self.somber.input[' ']:
			Bullet.remove(self)
			self.player.weapon.firefire_check = False

class FireLobBullet(Bullet):
	def __init__(self, somber, x=0, y=0):
		Bullet.__init__(self, somber, x, y, sprite='sprites/bullets/bullet_lob.png')
		self.duration = config.FIRELOB_DURATION
		self.hspeed = config.FIRELOB_HSPEED
		self.vspeed = config.FIRELOB_VSPEED
		self.gravity = config.FIRELOB_GRAVITY
		self.add_player_speed = config.FIRELOB_ADD_PLAYER_SPEED

		if self.add_player_speed:
			self.hspeed += abs(self.player.hspeed)
		self.hspeed *= self.direction
		
	def update(self):
		Bullet.update(self)
		
	def hit(self):
		if self.collides_with_group(self.level.get_sprite_group('ground')):
			Explosion(self.somber, damage=config.FIRELOB_EXPLOSION_DAMAGE, duration=config.FIRELOB_EXPLOSION_DURATION, fire_damage=config.FIRELOB_FIRE_DAMAGE, fire_duration=config.FIRELOB_FIRE_DURATION, fire_rate=config.FIRELOB_FIRE_RATE, x=self.pos[0] - 150, y=self.somber.win_size[1] - 238, set_fire=True)
			self.kill()

class FireForceBullet(Bullet):
	def __init__(self, somber, x=0, y=0):
		Bullet.__init__(self, somber, x, y, sprite='sprites/bullets/bullet_force.png')
		
		self.duration = config.FIREFORCE_DURATION
		self.hspeed = config.FIREFORCE_HSPEED
		self.damage = config.FIREFORCE_DAMAGE
		self.add_player_speed = config.FIREFORCE_ADD_PLAYER_SPEED
		
		if self.direction < 0:
			self.flip_horizontally()
		
		if self.add_player_speed:
			self.hspeed += abs(self.player.hspeed)
		self.hspeed *= self.direction
		
	def update(self):
		Bullet.update(self)
		
	def hit(self):
		for zombie in self.level.get_sprite_group('zombies'):
			if self.collides_with(zombie):
				zombie.push_speed = self.hspeed + (config.FIREFORCE_FORCE_HSPEED * self.direction)
				zombie.vspeed = config.FIREFORCE_FORCE_VSPEED
				Fire(self.somber, zombie, damage=config.FIREFORCE_FIRE_DAMAGE, duration=config.FIREFORCE_FIRE_DURATION, hit_rate=config.FIREFORCE_FIRE_RATE)

class LobBullet(Bullet):
	def __init__(self, somber, x=0, y=0):
		Bullet.__init__(self, somber, x, y, sprite='sprites/bullets/bullet_lob.png')
		self.duration = config.LOB_DURATION
		self.hspeed = config.LOB_HSPEED
		self.vspeed = config.LOB_VSPEED
		self.gravity = config.LOB_GRAVITY
		self.add_player_speed = config.LOB_ADD_PLAYER_SPEED

		if self.add_player_speed:
			self.hspeed += abs(self.player.hspeed)
		self.hspeed *= self.direction
		
	def update(self):
		Bullet.update(self)
		
	def hit(self):
		if self.collides_with_group(self.level.get_sprite_group('ground')):
			Explosion(self.somber, damage=config.LOB_EXPLOSION_DAMAGE, duration=config.LOB_EXPLOSION_DURATION, x=self.pos[0] - 150, y=self.somber.win_size[1] - 238)
			self.kill()
			
class LobLobBullet(Bullet):
	def __init__(self, somber, x=0, y=0):
		Bullet.__init__(self, somber, x, y, sprite='sprites/bullets/bullet_lob.png')
		self.duration = config.LOBLOB_DURATION
		self.hspeed = config.LOBLOB_HSPEED
		self.vspeed = config.LOBLOB_VSPEED
		self.gravity = config.LOBLOB_GRAVITY
		self.add_player_speed = config.LOBLOB_ADD_PLAYER_SPEED

		if self.add_player_speed:
			self.hspeed += abs(self.player.hspeed)
		self.hspeed *= self.direction
		
	def update(self):
		Bullet.update(self)
		
	def hit(self):
		if self.collides_with_group(self.level.get_sprite_group('ground')):
			Explosion(self.somber, damage=config.LOBLOB_EXPLOSION_DAMAGE, duration=config.LOBLOB_EXPLOSION_DURATION, x=self.pos[0] - 244, y=self.somber.win_size[1] - 327, big=True)
			self.kill()
			
class LobForceBullet(Bullet):
	def __init__(self, somber, x=0, y=0):
		Bullet.__init__(self, somber, x, y, sprite='sprites/bullets/bullet_lob.png')
		self.duration = config.LOBFORCE_DURATION
		self.hspeed = config.LOBFORCE_HSPEED
		self.vspeed = config.LOBFORCE_VSPEED
		self.gravity = config.LOBFORCE_GRAVITY
		self.add_player_speed = config.LOBFORCE_ADD_PLAYER_SPEED

		if self.add_player_speed:
			self.hspeed += abs(self.player.hspeed)
		self.hspeed *= self.direction
		
	def update(self):
		Bullet.update(self)
		
	def hit(self):
		if self.collides_with_group(self.level.get_sprite_group('ground')):
			Explosion(self.somber, damage=config.LOBFORCE_EXPLOSION_DAMAGE, duration=config.LOBFORCE_EXPLOSION_DURATION, force_hspeed=config.LOBFORCE_FORCE_HSPEED, force_vspeed=config.LOBFORCE_FORCE_VSPEED, x=self.pos[0] - 150, y=self.somber.win_size[1] - 238, push=True)
			self.kill()

class ForceBullet(Bullet):
	def __init__(self, somber, x=0, y=0):
		Bullet.__init__(self, somber, x, y, sprite='sprites/bullets/bullet_force.png')
		
		self.duration = config.FORCE_DURATION
		self.hspeed = config.FORCE_HSPEED
		self.damage = config.FORCE_DAMAGE
		
		if self.direction < 0:
			self.flip_horizontally()
		
		if self.add_player_speed:
			self.hspeed += abs(self.player.hspeed)
		self.hspeed *= self.direction
		
	def update(self):
		Bullet.update(self)
		
	def hit(self):
		for zombie in self.level.get_sprite_group('zombies'):
			if self.collides_with(zombie):
				zombie.vspeed = config.FORCE_FORCE_VSPEED
				zombie.push_speed = self.hspeed + (config.FORCE_FORCE_HSPEED * self.direction)

class ForceForceBullet(Bullet):
	def __init__(self, somber, x=0, y=0):
		Bullet.__init__(self, somber, x, y, sprite='sprites/bullets/bullet_force.png')
		
		self.duration = config.FORCEFORCE_DURATION
		self.hspeed = config.FORCEFORCE_HSPEED
		self.damage = config.FORCEFORCE_DAMAGE
		
		if self.direction < 0:
			self.flip_horizontally()
		
		if self.add_player_speed:
			self.hspeed += abs(self.player.hspeed)
		self.hspeed *= self.direction
		
	def update(self):
		Bullet.update(self)
		
	def hit(self):
		for zombie in self.level.get_sprite_group('zombies'):
			if self.collides_with(zombie):
				zombie.vspeed = config.FORCEFORCE_FORCE_VSPEED
				zombie.push_speed = self.hspeed + (config.FORCEFORCE_FORCE_HSPEED * self.direction)

class Fire(Bullet):
	def __init__(self, somber, entity, damage=10, duration=3, hit_rate=.5, x=0, y=0):
		x = -110
		y = -22
		Bullet.__init__(self, somber, x, y, from_player=False, sprite='sprites/fire/fire_0.png')
		self.entity = entity
		if entity.fire_object != None:
			entity.fire_object.kill()
		self.entity.fire_object = self
		self.hit_rate = hit_rate
		self.duration = duration
		self.hit_timer = 0
		self.damage = damage
		
	def update(self):
		Bullet.set_pos_to_entity(self, self.entity)
		Bullet.update(self)
		
	def hit(self):
		if self.hit_timer >= self.hit_rate:
			self.entity.health[0] -= self.damage
			self.hit_timer -= self.hit_rate
		self.hit_timer += self.delta_speed
		
	def remove(self):
		self.entity.fire_object = None
		Bullet.remove(self)

class Explosion(Bullet):
	def __init__(self, somber, x=0, y=0, damage=40, duration=1, fire_damage=10, fire_duration=3, fire_rate=.5, force_hspeed=100, force_vspeed=-220, big=False, set_fire=False, push=False):
		self.sprite='sprites/bullets/explosion_small.png'
		if big:
			self.sprite='sprites/bullets/explosion_big.png'
		Bullet.__init__(self, somber, x, y,from_player=False, sprite_group='explosions', sprite=self.sprite)
		self.set_fire = set_fire
		self.push = push
		self.has_hit = False
		self.damage = damage
		self.duration = duration
		self.fire_damage = fire_damage
		self.fire_duration = fire_duration
		self.fire_rate = fire_rate
		self.force_hspeed = force_hspeed
		self.force_vspeed = force_vspeed
		self.hspeed = 0
		
	def update(self):
		Bullet.update(self)
		
	def hit(self):
		if not self.has_hit:
			self.has_hit = True
			for zombie in self.level.get_sprite_group('zombies'):
				if self.collides_with(zombie):
					zombie.health[0] -= self.damage
					if self.set_fire:
						Fire(self.somber, zombie, damage=self.fire_damage, duration=self.fire_duration, hit_rate=self.fire_rate)
					if self.push:
						zombie_pos = zombie.pos[0] + (zombie.sprite.get_width() / 2)
						explosion_pos = self.pos[0] + (self.sprite.get_width() / 2)
						direction = 1
						if zombie_pos <= explosion_pos:
							direction = -1
						zombie.push_speed = self.force_hspeed
						zombie.vspeed = self.force_vspeed