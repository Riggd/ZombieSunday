# For the handling of characters, both Player-controlled and NPCs
# Author list:
# 	Luke Martin <ltmartin@bsu.edu>
# 	Michael Milkovic <mlmilkovic@bsu.edu>
# 	Derek Onay <dsonay@bsu.edu>
# 	Ryan Wiesjahn <rwiesjahn@bsu.edu>

import somber as somber_engine
from weapon import *
import config
import random

class Entity(somber_engine.Active):
	def __init__(self, somber, level, sprite_group, x=0, y=0, sprite='sprites/player/player_right_0.png'):
		somber_engine.Active.__init__(self, sprite, somber=somber, pos=(x, y))
		level.add_object(self, sprite_group)
		self.somber = somber
		self.level = level
		self.sprite_group = sprite_group
		self.attacking = False
		self.hspeed_max = config.ENTITY_HSPEED
		self.vspeed_max = config.ENTITY_VSPEED
		self.gravity = config.ENTITY_GRAVITY
		self.direction = 1
		self.health = [1, config.ENTITY_HEALTH]
		self.health[0] = self.health[1]
		
		# Effects
		self.push_speed = 0
		self.fire_object = None
	
	def update(self):
		if not self.level.complete and not self.level.dead and not self.level.out_of_time:
			somber_engine.Active.update(self)
	
	def collision(self):
		if self.pos[0] < 0:
			self.pos[0] = 0
		if self.pos[0] > config.GROUND_WIDTH * (config.LEVEL_SIZE - 1):
			self.pos[0] = config.GROUND_WIDTH * (config.LEVEL_SIZE - 1)
					
		if self.collides_with_group(self.level.get_sprite_group('ground')):
			self.pos[1] = config.GROUND_POS[1] - 150 + 1
			if self.vspeed > 0:
				self.vspeed = 0
			self.gravity = 0
		else:
			self.gravity = config.ENTITY_GRAVITY
	
	def animate(self):
		if self.hspeed != 0:
			if self.direction == 1:
				if not self.get_animation() == 'move_right':
					self.set_animation('move_right')
			else:
				if not self.get_animation() == 'move_left':
					self.set_animation('move_left')
		else:
			if self.direction == 1:
				if not self.attacking:
					if not self.get_animation() == 'idle_right':
						self.set_animation('idle_right')
				else:
					if not self.get_animation() == 'attack_right':
						self.set_animation('attack_right')
			else:
				if not self.attacking:
					if not self.get_animation() == 'idle_left':
						self.set_animation('idle_left')
				else:
					if not self.get_animation() == 'attack_left':
						self.set_animation('attack_left')

class Character(Entity):
	def __init__(self, somber, level, sprite_group, x=0, y=0):
		Entity.__init__(self, somber, level, sprite_group, x, y)
		self.weapon = Weapon(somber, self, [None, None])
		self.hspeed_max = config.PLAYER_HSPEED
		self.health = [1, config.PLAYER_HEALTH]
		self.health[0] = self.health[1]
		self.score = 0
		self.zombies_killed = 0
		self.supplies = [0, config.PLAYER_SUPPLY_MAX]
		self.total_supplies = [0, config.SUPPLY_GOAL + (config.SUPPLY_GOAL_MOD * self.level.stage)]
		
		self.scavanging = False
		self.dropping_off = False
		self.scavanging_timer = 0
		
		self.add_animation('idle_right', 15, ['sprites/player/player_right_0.png'])
		self.add_animation('idle_left', 15, ['sprites/player/player_left_0.png'])
		self.add_animation('move_right', 15, ['sprites/player/player_right_0.png', 'sprites/player/player_right_1.png'])
		self.add_animation('move_left', 15, ['sprites/player/player_left_0.png', 'sprites/player/player_left_1.png'])
		self.set_animation('idle_right')
	
	def update(self):
		if not self.level.complete and not self.level.dead and not self.level.out_of_time:
			self.weapon.update(self.delta_speed)
			Entity.collision(self)
			self.change_direction()
			Entity.animate(self)
			self.scavange_timer()
			self.drop_off_timer()
			Entity.update(self)
		else:
			self.set_movement(None)
	
	def action(self):
		self.scavange_building()
		self.collect_item()
	
	def collision(self):
		Entity.collision(self)
			
	def change_direction(self):
		if self.hspeed > 0:
			self.direction = 1
		if self.hspeed < 0:
			self.direction = -1
	
	def collect_item(self):
		for item in self.somber.current_level.get_sprite_group('items'):
			if self.collides_with(item):
				item.collect()
				break
	
	def scavange_building(self):
		for building in self.somber.current_level.get_sprite_group('buildings'):
			if self.collides_with(building.door):
				if not building.home:
					if not building.scavanged and not self.scavanging and self.supplies[0] != self.supplies[1]:
						self.somber.play_sound(config.SOUND_DOOR)
						building.scavanged = True
						self.scavanging = True
				else:
					if not self.scavanging and self.supplies[0] > 0:
						self.somber.play_sound(config.SOUND_DOOR)
						self.dropping_off = True
					
	
	def scavange_timer(self):
		if self.scavanging:
			self.scavanging_timer += self.delta_speed
			self.pos[1] = -400
			self.set_movement(None)
			self.gravity = 0
			self.hspeed = 0
			self.vspeed = 0
			if self.scavanging_timer >= config.SCAVANGE_DURATION:
				self.scavanging = False
				self.add_supplies()
				self.score += config.SCAVANGE_SCORE + (config.SCAVANGE_SCORE_MOD * self.level.stage)
				self.scavanging_timer = 0
				self.pos[1] = config.PLAYER_POS[1]
				self.set_movement('horizontal')
				self.somber.play_sound(config.SOUND_DOOR)
				
	def drop_off_timer(self):
		if self.dropping_off:
			self.scavanging_timer += self.delta_speed
			self.pos[1] = -400
			self.set_movement(None)
			self.gravity = 0
			self.hspeed = 0
			self.vspeed = 0
			if self.scavanging_timer >= config.SCAVANGE_DURATION:
				self.dropping_off = False
				self.add_total_supplies()
				self.scavanging_timer = 0
				self.pos[1] = config.PLAYER_POS[1]
				self.set_movement('horizontal')
				self.somber.play_sound(config.SOUND_DOOR)
	
	def add_total_supplies(self):
		if (self.supplies[0] + self.total_supplies[0]) > self.total_supplies[1]:
			self.total_supplies[0] = self.total_supplies[1]
		else:
			self.total_supplies[0] +=self.supplies[0]
			self.supplies[0] = 0
	
	def add_supplies(self):
		supply_amount = random.randint(config.SUPPLY_RANGE[0], config.SUPPLY_RANGE[1])
		if (self.supplies[0] + supply_amount) > self.supplies[1]:
			self.supplies[0] = self.supplies[1]
		else:
			self.supplies[0] += supply_amount
					
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
		for player in self.level.get_sprite_group('player'):
			self.player = player
		self.attack_timer = 0
		self.health = [1, config.ZOMBIE_HEALTH + (config.ZOMBIE_HEALTH_MOD * self.level.stage)]
		self.health[0] = self.health[1]
		self.damage = config.ZOMBIE_DAMAGE + (config.ZOMBIE_DAMAGE_MOD * self.level.stage)
		self.attack_rate = config.ZOMBIE_ATTACK_RATE * pow(config.ZOMBIE_ATTACK_RATE_MOD, self.level.stage)
		self.hspeed_max = config.ZOMBIE_HSPEED + (config.ZOMBIE_HSPEED_MOD * self.level.stage)
		self.hspeed = self.hspeed_max
		self.score = config.ZOMBIE_SCORE + (config.ZOMBIE_SCORE_MOD * self.level.stage)
		
		self.add_animation('idle_right', 15, ['sprites/zombie/zombie_right_0.png'])
		self.add_animation('idle_left', 15, ['sprites/zombie/zombie_left_0.png'])
		self.add_animation('move_right', 15, ['sprites/zombie/zombie_right_0.png', 'sprites/zombie/zombie_right_1.png'])
		self.add_animation('move_left', 15, ['sprites/zombie/zombie_left_0.png', 'sprites/zombie/zombie_left_1.png'])
		self.add_animation('attack_right', 15, ['sprites/zombie/zombie_right_0.png', 'sprites/zombie/zombie_right_2.png'])
		self.add_animation('attack_left', 20, ['sprites/zombie/zombie_left_0.png', 'sprites/zombie/zombie_left_2.png'])
		self.set_animation('idle_right')
		
	def update(self):
		if not self.level.complete and not self.level.dead and not self.level.out_of_time:
			self.timer()
			Entity.collision(self)
			self.ai()
			Entity.animate(self)
			self.die()
			self.effects()
			Entity.update(self)
		
	def ai(self):
		padding = 20
		self.attacking = False
		if self.pos[0] + self.sprite.get_width() < self.player.pos[0] + padding:
			self.hspeed = self.hspeed_max
			self.direction = 1
		elif self.pos[0] > self.player.pos[0] + self.player.sprite.get_width() - padding:
			self.hspeed = -self.hspeed_max
			self.direction = -1
		else:
			self.hspeed = 0
			if self.collides_with(self.player):
				self.attack()
				self.attacking = True
	
	def timer(self):
		if self.attack_timer < self.attack_rate:
			self.attack_timer += self.delta_speed
			
	def attack(self):
		if self.attack_timer >= self.attack_rate:
			if self.player.health[0] - self.damage < 0:
				self.player.health[0] = 0
			else:
				self.player.health[0] -= self.damage
			self.attack_timer = 0
			
	def effects(self):
		if self.push_speed != 0:
			if not self.collides_with_group(self.level.get_sprite_group('ground')):
				self.hspeed = self.push_speed
			else:
				self.push_speed = 0					
				
	def die(self):
		if self.health[0] <= 0:
			self.kill()
			if self.fire_object != None:
				self.fire_object.kill()
			self.add_scores()
			self.somber.play_sound(config.SOUND_ZOMBIE_YELL)
	
	def add_scores(self):
		self.player.score += self.score
		self.player.zombies_killed += 1
			
