# For the handling of characters, both Player-controlled and NPCs
# Author list:
# 	Luke Martin <ltmartin@bsu.edu>
# 	Michael Milkovic <mlmilkovic@bsu.edu>
# 	Derek Onay <dsonay@bsu.edu>
# 	Ryan Wiesjahn <rwiesjahn@bsu.edu>

import somber as somber_engine
from weapon import *

class Character(somber_engine.Active):
	def __init__(self, somber, level, sprite, sprite_group, x=0, y=0):
		somber_engine.Active.__init__(self, sprite, somber=somber, pos=(x, y))
		self.somber = somber
		self.level = level
		self.sprite_group = sprite_group
		self.hspeed_max_default = 300
		self.climb_speed = 100
		self.direction = 1
		self.health = [1, 100]
		self.health[0] = self.health[1]
		self.fire_timer = 1
		level.add_object(self, sprite_group)
		
		self.climbing = False
		self.add_animation('idle_right', 15, ['sprites/player/player_right_0.png'])
		self.add_animation('idle_left', 15, ['sprites/player/player_left_0.png'])
		self.add_animation('move_right', 15, ['sprites/player/player_right_0.png', 'sprites/player/player_right_1.png'])
		self.add_animation('move_left', 15, ['sprites/player/player_left_0.png', 'sprites/player/player_left_1.png'])
		self.set_animation('idle_right')
		
		self.weapon = Weapon(somber, self, [Attachment.Multi, Attachment.Multi])
	
	def update(self):
		self.change_direction()
		self.check_climbing()
		self.collision()
		self.animate()
		self.weapon_timer()
		
		somber_engine.Active.update(self)
		
	def weapon_timer(self):
		if self.fire_timer < self.weapon.rate:
			self.fire_timer += self.delta_speed
		
	def fire(self):
		if self.fire_timer >= self.weapon.rate:
			self.weapon.fire()
			self.fire_timer = 0
		
	def check_climbing(self):
		if self.collides_with_group(self.level.get_sprite_group('ladders')):
			if self.somber.input['up']:
				self.climbing = True
				self.vspeed = -self.climb_speed
			elif self.somber.input['down']:
				self.climbing = True
				self.vspeed = self.climb_speed
			else:
				self.vspeed = 0
		else:
			self.climbing = False
			self.gravity = 3
			
		if self.collides_with_group_at('ground', (self.rect.bottomleft[0], self.rect.bottomleft[1])):
			self.climbing = False
			
		if self.climbing:				
			self.hspeed_max = 0
		else:
			self.hspeed_max = self.hspeed_max_default
		
	def collision(self):
		if self.pos[0] < 0:
			self.pos[0] = 0
		
		if self.pos[0] > self.level.ground_size * (self.level.level_size - 1):
			self.pos[0] = self.level.ground_size * (self.level.level_size - 1)
			
		if not self.climbing:
			if self.collides_with_group(self.level.get_sprite_group('ground')):
				if self.vspeed > 0:
					self.vspeed = 0
				self.gravity = 0
			else:
				self.gravity = 3
		else:
			self.gravity = 0
			
	def change_direction(self):
		if self.hspeed > 0:
			self.direction = 1
		if self.hspeed < 0:
			self.direction = 0
			
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
		
class Zombie(somber_engine.Active):
	def __init__(self, somber, level, sprite, sprite_group, x=0, y=0):
		somber_engine.Active.__init__(self, sprite, somber=somber, pos=(x, y))
		self.somber = somber
		self.level = level
		self.sprite_group = sprite_group
		level.add_object(self, sprite_group)
		
		self.health = [1, 100]
		self.health[0] = self.health[1]
		self.direction = 1
		self.pre_hspeed = 75
		self.hspeed = self.pre_hspeed
		
		self.add_animation('idle_right', 15, ['sprites/zombie/zombie_right_0.png'])
		self.add_animation('idle_left', 15, ['sprites/zombie/zombie_left_0.png'])
		self.add_animation('move_right', 15, ['sprites/zombie/zombie_right_0.png', 'sprites/zombie/zombie_right_1.png'])
		self.add_animation('move_left', 15, ['sprites/zombie/zombie_left_0.png', 'sprites/zombie/zombie_left_1.png'])
		self.set_animation('idle_right')
		
	def update(self):	
		self.change_speed()
		self.collision()
		self.animate()
		self.die()

		somber_engine.Active.update(self)
		
	def change_speed(self):
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
			
	def collision(self):
		if self.pos[0] < 0:
			self.pos[0] = 0
			
		if self.collides_with_group(self.level.get_sprite_group('ground')):
			if self.vspeed > 0:
				self.vspeed = 0
			self.gravity = 0
		else:
			self.gravity = 3
		
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
	def die(self):
		if self.health[0] <= 0:
			self.kill()
