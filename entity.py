# For the handling of characters, both Player-controlled and NPCs
# Author list:
# 	Luke Martin <ltmartin@bsu.edu>
# 	Michael Milkovic <mlmilkovic@bsu.edu>
# 	Derek Onay <dsonay@bsu.edu>
# 	Ryan Wiesjahn <rwiesjahn@bsu.edu>

import somber as somber_engine
from weapon import *
import config

class Entity(somber_engine.Active):
	def __init__(self, somber, level, sprite_group, x=0, y=0, sprite='sprites/player/player_right_0.png'):
		somber_engine.Active.__init__(self, sprite, somber=somber, pos=(x, y))
		level.add_object(self, sprite_group)
		self.somber = somber
		self.level = level
		self.sprite_group = sprite_group
		self.hspeed_max = 100
		self.direction = 1
		self.health = [1, 100]
		self.health[0] = self.health[1]
	
	def update(self):
		somber_engine.Active.update(self)
	
	def collision(self):
		if self.pos[0] < 0:
			self.pos[0] = 0
		if self.pos[0] > self.level.ground_size * (self.level.level_size - 1):
			self.pos[0] = self.level.ground_size * (self.level.level_size - 1)
					
		if self.collides_with_group(self.level.get_sprite_group('ground')):
			if self.vspeed > 0:
				self.vspeed = 0
			self.gravity = 0
		else:
			self.gravity = config.ENTITY_GRAVITY
	
	def animate(self):
		if self.hspeed > 0:
			if not self.get_animation() == 'move_right':
				self.set_animation('move_right')
		elif self.hspeed < 0:
			if not self.get_animation() == 'move_left':
				self.set_animation('move_left')
		elif not self.gravity:
			if not self.get_animation() == 'idle_left' and not self.get_animation() == 'idle_right':
				if self.get_animation() == 'move_left':
					self.set_animation('idle_left')
				else:
					self.set_animation('idle_right')

class Character(Entity):
	def __init__(self, somber, level, sprite_group, x=0, y=0):
		Entity.__init__(self, somber, level, sprite_group, x, y)
		self.weapon = Weapon(somber, self, [Attachment.Force, None])
		self.hspeed_default = 10
		
		self.add_animation('idle_right', 15, ['sprites/player/player_right_0.png'])
		self.add_animation('idle_left', 15, ['sprites/player/player_left_0.png'])
		self.add_animation('move_right', 15, ['sprites/player/player_right_0.png', 'sprites/player/player_right_1.png'])
		self.add_animation('move_left', 15, ['sprites/player/player_left_0.png', 'sprites/player/player_left_1.png'])
		self.set_animation('idle_right')
		
		self.somber.bind_key(' ', self.weapon.fire, repeat=True)
		self.somber.bind_key('-', self.change_attachment_1)
		self.somber.bind_key('=', self.change_attachment_2)
	
	def update(self):
		self.weapon.update(self.delta_speed)
		Entity.collision(self)
		self.change_direction()
		Entity.animate(self)
		Entity.update(self)
		
	def collision(self):
		Entity.collision(self)
			
	def change_direction(self):
		if self.hspeed > 0:
			self.direction = 1
		if self.hspeed < 0:
			self.direction = 0
					
	def change_attachment_1(self):
		attachment = self.weapon.attachments[0]
		if attachment == None:
			attachment = 0
		else:
			attachment += 1
		if attachment > 3:
			attachment = None
		self.weapon.attachments[0] = attachment
		self.weapon.set_weapon_type()
			
	def change_attachment_2(self):
		attachment = self.weapon.attachments[1]
		if attachment == None:
			attachment = 0
		else:
			attachment += 1
		if attachment > 3:
			attachment = None
		self.weapon.attachments[1] = attachment
		self.weapon.set_weapon_type()
		
class Zombie(Entity):
	def __init__(self, somber, level, sprite_group, x=0, y=0):
		Entity.__init__(self, somber, level, sprite_group, x, y, sprite='sprites/zombie/zombie_right_0.png')
		self.pre_hspeed = 100
		self.hspeed = self.pre_hspeed
		
		# Effects
		self.push_speed = 0
		self.push_timer = 0
		self.push_duration = 0
		
		self.add_animation('idle_right', 15, ['sprites/zombie/zombie_right_0.png'])
		self.add_animation('idle_left', 15, ['sprites/zombie/zombie_left_0.png'])
		self.add_animation('move_right', 15, ['sprites/zombie/zombie_right_0.png', 'sprites/zombie/zombie_right_1.png'])
		self.add_animation('move_left', 15, ['sprites/zombie/zombie_left_0.png', 'sprites/zombie/zombie_left_1.png'])
		self.set_animation('idle_right')
		
	def update(self):	
		Entity.collision(self)
		self.change_direction()
		Entity.animate(self)
		self.die()
		self.effects()
		Entity.update(self)
		
	def change_direction(self):
		for player in self.level.get_sprite_group('player'):
			if self.pos[0] > player.pos[0]:
				if self.pos[0] < player.pos[0] + player.sprite.get_width():
					self.direction = 0
				else:
					self.direction = -1
			else:
				if self.pos[0] + self.sprite.get_width() > player.pos[0]:
					self.direction = 0
				self.direction = 1

		self.hspeed = self.direction * self.pre_hspeed			
					
	def effects(self):
		if self.push_speed != 0:
			if not self.collides_with_group(self.level.get_sprite_group('ground')):
				self.hspeed = self.push_speed
			else:
				self.push_speed = 0
				
	def die(self):
		if self.health[0] <= 0:
			self.kill()
