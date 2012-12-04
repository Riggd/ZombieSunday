# Levels
# Author list:
# 	Luke Martin <ltmartin@bsu.edu>
# 	Michael Milkovic <mlmilkovic@bsu.edu>
# 	Derek Onay <dsonay@bsu.edu>
# 	Ryan Wiesjahn <rwiesjahn@bsu.edu>

import somber as somber_engine
import random
import ui
import os
from entity import *
from items import *
from weapon import *

class Title_Screen(somber_engine.Level):
	def __init__(self, somber):
		somber_engine.Level.__init__(self, somber, 'Title Screen')
	
	def create_level(self):
		self.create_sprite_group('background_0', scroll_speed=0)
		self.create_sprite_group('background_1', scroll_speed=0.2, group=somber_engine.BackgroundParallaxGroup)
		self.create_sprite_group('background_2', scroll_speed=0.3, group=somber_engine.BackgroundParallaxGroup)
		self.create_sprite_group('sun', group=somber_engine.StaticBackgroundGroup)
		self.create_sprite_group('clouds', group=somber_engine.StaticBackgroundGroup)
		self.create_sprite_group('ground', scroll_speed=1, group=somber_engine.BackgroundParallaxGroup)
		self.create_sprite_group('dummy')
		self.create_sprite_group('ui', group=somber_engine.StaticGroup)
		
		Static_Background(self.somber, self, 'sprites/background/sky.png', 'background_0')
		Sun(self.somber, self, 'sprites/background/sun.png', 'sun', x=config.SUN_POS[0], y=config.SUN_POS[1])
		Background(self.somber, self, 'sprites/background/trees_back.png', 'background_1', x=config.BACKGROUND_1_POS[0], y=config.BACKGROUND_1_POS[1])
		Background(self.somber, self, 'sprites/background/trees_fore.png', 'background_2', x=config.BACKGROUND_2_POS[0], y=config.BACKGROUND_2_POS[1])
		Cloud(self.somber, self, 'sprites/background/cloud_1.png', 'clouds', x=config.CLOUD_1_POS[0], y=config.CLOUD_1_POS[1])
		Cloud(self.somber, self, 'sprites/background/cloud_2.png', 'clouds', x=config.CLOUD_2_POS[0], y=config.CLOUD_2_POS[1])
		Cloud(self.somber, self, 'sprites/background/cloud_3.png', 'clouds', x=config.CLOUD_3_POS[0], y=config.CLOUD_3_POS[1])
		Background(self.somber, self, 'sprites/foreground/ground.png', 'ground', x=config.GROUND_POS[0], y=config.GROUND_POS[1])
		
		self.main_ui = ui.UI_Group(self.somber, self, 'ui')
		self.main_ui.create_element('sprites/ui/logo_zombie_sunday.png', 'logo', x=config.LOGO_POS[0], y=config.LOGO_POS[1])
		self.main_ui.create_element('sprites/ui/ui_start_game.png', 'start', x=config.BUTTON_START_POS[0], y=config.BUTTON_START_POS[1])
		
		self.level = self
		
		self.setup()
		
		return self.level
	
	def setup(self):
		self.dummy = Dummy(self.somber, self, 'sprites/foreground/dummy.png', 'dummy', x=self.somber.win_size[0] / 2, y=400)
		self.dummy.hspeed = config.TITLE_SCROLL_SPEED
		
		for group in self.level.sprite_groups:
			_speed = -(self.level.sprite_groups.index(group) * 8)
			
			for sprite in group['group']:				
				if group['name'] == 'clouds':
					sprite.hspeed = -(random.randrange(2, 6) * 8)
	
	def update(self, delta):
		pass
	
	def on_change_to(self):
		self.somber.camera_follow(self.dummy)
		self.somber.bind_key('m1', self.mouse_down)
		self.somber.bind_key('\r', self.start_game)
					
	def mouse_down(self, button):
		for element in self.main_ui.get_clicked_elements():
			if element.name == 'start':
				self.start_game()
	
	def start_game(self):
		ENDLESS_LEVEL = Endless_Level(self.somber).create_level()
		self.somber.change_level('Endless Level')

class Endless_Level(somber_engine.Level):
	def __init__(self, somber, stage=0):
		somber_engine.Level.__init__(self, somber, 'Endless Level')
		self.stage = stage
		self.zombie_timer = 0

	def create_level(self):
		self.create_sprite_group('background_0', scroll_speed=0)
		self.create_sprite_group('background_1', scroll_speed=0.2, group=somber_engine.BackgroundParallaxGroup)
		self.create_sprite_group('background_2', scroll_speed=0.3, group=somber_engine.BackgroundParallaxGroup)
		self.create_sprite_group('sun', group=somber_engine.StaticBackgroundGroup)
		self.create_sprite_group('clouds', group=somber_engine.StaticBackgroundGroup)
		self.create_sprite_group('ground')
		self.create_sprite_group('buildings')
		self.create_sprite_group('doors')
		self.create_sprite_group('bullets')
		self.create_sprite_group('items')
		self.create_sprite_group('player')
		self.create_sprite_group('zombies')
		self.create_sprite_group('explosions')
		self.create_sprite_group('ui')
		
		Static_Background(self.somber, self, 'sprites/background/sky.png', 'background_0')
		Sun(self.somber, self, 'sprites/background/sun.png', 'sun', x=config.SUN_POS[0], y=config.SUN_POS[1])
		Background(self.somber, self, 'sprites/background/trees_back.png', 'background_1', x=config.BACKGROUND_1_POS[0], y=config.BACKGROUND_1_POS[1])
		Background(self.somber, self, 'sprites/background/trees_fore.png', 'background_2', x=config.BACKGROUND_2_POS[0], y=config.BACKGROUND_2_POS[1])
		Cloud(self.somber, self, 'sprites/background/cloud_1.png', 'clouds', x=config.CLOUD_1_POS[0], y=config.CLOUD_1_POS[1])
		Cloud(self.somber, self, 'sprites/background/cloud_2.png', 'clouds', x=config.CLOUD_2_POS[0], y=config.CLOUD_2_POS[1])
		Cloud(self.somber, self, 'sprites/background/cloud_3.png', 'clouds', x=config.CLOUD_3_POS[0], y=config.CLOUD_3_POS[1])
		
		Building(self.somber, self, 'sprites/foreground/home.png', 'buildings', x=config.HOME_POS[0], y=config.HOME_POS[1])
		
		self._init_ground()
		self._init_clouds()
			
		self.level = self
		self.setup()
		
		return self
	
	def _init_ground(self):
		for tile in range(0, config.LEVEL_SIZE):
			Platform(self.somber, self, 'sprites/foreground/ground.png', 'ground', x=tile * config.GROUND_WIDTH, y=config.GROUND_POS[1])
	
	def _init_clouds(self):
		for group in self.sprite_groups:
			for sprite in group['group']:
				if group['name'] == 'clouds':
					sprite.hspeed = -(random.randint(2, 6) * 8)
	
	def setup(self):
		self._setup_player()
		self._setup_buildings()
		
		Zombie(self.somber, self, 'zombies', x=300, y=config.ZOMBIE_POS[1])
					
		self.spawn_ammo()
		self.spawn_attachments()
	
	def _setup_player(self):
		self.player = Character(self.somber, self, 'player', x=config.PLAYER_POS[0], y=config.PLAYER_POS[1])
		self.player.set_movement('horizontal')
		
	def _setup_buildings(self):
		distance = 0
		while distance < config.LEVEL_SIZE * config.GROUND_WIDTH:
			distance += (random.randint(config.BUILDING_RANGE[0], config.BUILDING_RANGE[1]) * config.BUILDING_RANGE[2]) + (config.BUILDING_DISTANCE_MOD * self.stage)
			Building(self.somber, self, 'sprites/foreground/house.png', 'buildings', x=distance, y=config.BUILDING_POS[1])
	
	def _spawn_zombies(self, delta):
		if len(self.get_sprite_group('zombies')) < config.ZOMBIE_MAX + (config.ZOMBIE_MAX_MOD * self.stage):
			self.zombie_timer += delta
			zombie_time = round(config.ZOMBIE_SPAWN_RATE * pow(config.ZOMBIE_SPAWN_RATE_MOD, self.stage), 10)
			if self.zombie_timer > zombie_time:
				self.zombie_timer -= zombie_time
				side = 1
				extra = 200
				if self.somber.camera_pos[0] > extra:
					side = random.randint(0, 1)
					if side == 0:
						extra = -extra
				Zombie(self.somber, self, 'zombies', x=self.somber.camera_pos[0] + (config.WINDOW_SIZE[0] * side) + extra, y=config.ZOMBIE_POS[1])
	
	def spawn_ammo(self): # TEMPORARY
		distance = 0
		while True:
			distance += random.randint(12, 20) * 100
			if distance < config.LEVEL_SIZE * config.GROUND_WIDTH:
				Ammo(self.somber, self.level, x=distance, y=self.somber.win_size[1] - 150)
			else:
				break
			
	def spawn_attachments(self): # TEMPORARY
		distance = 0
		while True:
			distance += random.randint(12, 20) * 100
			if distance < config.LEVEL_SIZE * config.GROUND_WIDTH:
				AttachmentItem(self.somber, self, random.randint(0, 3), x=distance, y=self.somber.win_size[1] - 150)
			else:
				break
	
	def on_change_to(self):
		self.somber.camera_follow(self.player)
		
		self.somber.bind_key(' ', self.player.weapon.fire, repeat=True)
		self.somber.bind_key('e', self.player.collect_item)
		self.somber.bind_key('-', self.player.change_attachment_1)
		self.somber.bind_key('=', self.player.change_attachment_2)
	
	def update(self, delta):
		self._spawn_zombies(delta)
		
class Static_Background(somber_engine.Active):
	def __init__(self, somber, level, sprite, sprite_group, x=0, y=0):
		somber_engine.Active.__init__(self, sprite, somber=somber, pos=(x, y))
		
		self.level = level
		self.sprite_group = sprite_group
		self.static = True
		
		level.add_object(self, sprite_group)

class Background(somber_engine.BackgroundParallax):
	def __init__(self, somber, level, sprite, sprite_group, x=0, y=0):
		somber_engine.BackgroundParallax.__init__(self, sprite, somber=somber, pos=(x, y))
		
		self.level = level
		self.sprite_group = sprite_group
		self.static = False
		
		level.add_object(self, sprite_group)
	
	def update(self):
		somber_engine.BackgroundParallax.update(self)

class Platform(somber_engine.Active):
	def __init__(self, somber, level, sprite, sprite_group, x=0, y=0):
		somber_engine.Active.__init__(self, sprite, somber=somber, pos=(x, y))
		
		self.level = level
		self.sprite_group = sprite_group
		
		level.add_object(self, sprite_group)
	
	def update(self):
		somber_engine.Active.update(self)
		
class Building(somber_engine.Active):
	def __init__(self, somber, level, sprite, sprite_group, x=0, y=0):
		somber_engine.Active.__init__(self, sprite, somber=somber, pos=(x, y))
		
		self.level = level
		self.sprite_group = sprite_group
		self.set_pos((x, y))
		
		level.add_object(self, sprite_group)
		
		Door(somber, self.level, 'sprites/foreground/door.png', 'doors', self, x=x + config.DOOR_POS[0], y=config.DOOR_POS[1])
		
class Door(somber_engine.Active):
	def __init__(self, somber, level, sprite, sprite_group, building, x=0, y=0):
		somber_engine.Active.__init__(self, sprite, somber=somber, pos=(x, y))
		
		self.level = level
		self.sprite_group = sprite_group
		self.set_pos((x, y))
		
		level.add_object(self, sprite_group)

class Cloud(somber_engine.Active):
	def __init__(self, somber, level, sprite, sprite_group, x=0, y=0):
		somber_engine.Active.__init__(self, sprite, somber=somber, pos=(x, y))
		
		self.level = level
		self.sprite_group = sprite_group
		
		level.add_object(self, sprite_group)
	
	def update(self):
		if self.pos[0] + self.sprite.get_width() < 0:
			self.set_pos((self.somber.win_size[0] + 10, self.pos[1]))
		
		somber_engine.Active.update(self)

class Sun(somber_engine.Active):
	def __init__(self, somber, level, sprite, sprite_group, x=0, y=0):
		somber_engine.Active.__init__(self, sprite, somber=somber, pos=(x, y))
		
		self.level = level
		self.sprite_group = sprite_group
		
		level.add_object(self, sprite_group)
		
class Dummy(somber_engine.Active):
	def __init__(self, somber, level, sprite, sprite_group, x=0, y=0):
		somber_engine.Active.__init__(self, sprite, somber=somber, pos=(x, y))
		self.somber = somber
		self.level = level
		self.sprite_group = sprite_group
		level.add_object(self, sprite_group)
		
	def update(self):	
		somber_engine.Active.update(self)
