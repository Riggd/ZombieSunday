# Levels
# Author list:
# 	Luke Martin <ltmartin@bsu.edu>
# 	Michael Milkovic <mlmilkovic@bsu.edu>
# 	Derek Onay <dsonay@bsu.edu>
# 	Ryan Wiesjahn <rwiesjahn@bsu.edu>

import somber as somber_engine
import random
import ui
from entity import *
from items import *

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
		Sun(self.somber, self, 'sprites/background/sun.png', 'sun', x=self.somber.win_size[0] - 250, y=20)
		Background(self.somber, self, 'sprites/background/trees_back.png', 'background_1', y=self.somber.win_size[1] - 245)
		Background(self.somber, self, 'sprites/background/trees_fore.png', 'background_2', y=self.somber.win_size[1] - 192)
		Cloud(self.somber, self, 'sprites/background/cloud_1.png', 'clouds', x=self.somber.win_size[0] - 100, y=10)
		Cloud(self.somber, self, 'sprites/background/cloud_2.png', 'clouds', x=self.somber.win_size[0] / 2, y=200)
		Cloud(self.somber, self, 'sprites/background/cloud_3.png', 'clouds', y=100)
		Background(self.somber, self, 'sprites/foreground/ground.png', 'ground', y=self.somber.win_size[1] - 96)
		
		self.main_ui = ui.UI_Group(self.somber, self, 'ui')
		self.main_ui.create_element('sprites/ui/logo_zombie_sunday.png', 'logo', x=(self.somber.win_size[0] / 2) - 338, y=30)
		self.main_ui.create_element('sprites/ui/ui_start_game.png', 'start', x=(self.somber.win_size[0] / 2) - 165, y=220)
		
		self.level = self
		
		self.setup()
		
		return self.level
	
	def setup(self):
		self.somber.bind_key('m1', self.mouse_down)
		
		self.dummy = Dummy(self.somber, self, 'sprites/foreground/dummy.png', 'dummy', x=self.somber.win_size[0] / 2, y=400)
		self.dummy.hspeed = 100
		
		for group in self.level.sprite_groups:
			_speed = -(self.level.sprite_groups.index(group) * 8)
			
			for sprite in group['group']:				
				if group['name'] == 'clouds':
					sprite.hspeed = -(random.randrange(2, 6) * 8)
	
	def on_change_to(self):
		self.somber.camera_follow(self.dummy)
					
	def mouse_down(self, button):
		for element in self.main_ui.get_clicked_elements():
			if element.name == 'start':
				self.somber.change_level('Endless Level')
	
	def update(self, delta):
		self.somber.camera_pos[0] = self.somber.camera_pos[0] + 1

class Endless_Level(somber_engine.Level):
	def __init__(self, somber):
		somber_engine.Level.__init__(self, somber, 'Endless Level')
		self.level_size = 10
		self.ground_size = 1600
		self.zombie_timer = 0

	def create_level(self):
		self.create_sprite_group('background_0', scroll_speed=0)
		self.create_sprite_group('background_1', scroll_speed=0.2, group=somber_engine.BackgroundParallaxGroup)
		self.create_sprite_group('background_2', scroll_speed=0.3, group=somber_engine.BackgroundParallaxGroup)
		self.create_sprite_group('sun', group=somber_engine.StaticBackgroundGroup)
		self.create_sprite_group('clouds', group=somber_engine.StaticBackgroundGroup)
		self.create_sprite_group('ground')
		self.create_sprite_group('ladders')
		self.create_sprite_group('buildings')
		self.create_sprite_group('player')
		self.create_sprite_group('bullets')
		self.create_sprite_group('items')
		self.create_sprite_group('zombies')
		self.create_sprite_group('ui')
		
		Static_Background(self.somber, self, 'sprites/background/sky.png', 'background_0')
		
		Background(self.somber, self, 'sprites/background/trees_back.png', 'background_1', y=self.somber.win_size[1] - 245)
		Background(self.somber, self, 'sprites/background/trees_fore.png', 'background_2', y=self.somber.win_size[1] - 192)
		
		Sun(self.somber, self, 'sprites/background/sun.png', 'sun', x=self.somber.win_size[0] - 250, y=20)
		
		Cloud(self.somber, self, 'sprites/background/cloud_1.png', 'clouds', x=self.somber.win_size[0] - 100, y=10)
		Cloud(self.somber, self, 'sprites/background/cloud_2.png', 'clouds', x=self.somber.win_size[0] / 2, y=200)
		Cloud(self.somber, self, 'sprites/background/cloud_3.png', 'clouds', y=100)
		
		
		for tile in range(0, self.level_size):
			Platform(self.somber, self, 'sprites/foreground/ground.png', 'ground', x=tile * self.ground_size, y=self.somber.win_size[1] - 96)
		
		House(self.somber, self, 'sprites/foreground/home.png', 'buildings', x=5, y=self.somber.win_size[1] - 525)
		
		distance = 0
		while True:
			distance += random.randint(12, 20) * 100
			if distance < self.level_size * self.ground_size:
				House(self.somber, self, 'sprites/foreground/house.png', 'buildings', x=distance, y=self.somber.win_size[1] - 572)
			else:
				break
			
		
		self.level = self
		self.setup()
		
		return self
	
	def setup(self):
		self.player = Character(self.somber, self, 'sprites/player/player_right_0.png', 'player', x=10, y=self.somber.win_size[1] - 246)
		self.player.hspeed_max = 500
		self.player.vspeed_max = 30
		self.player.gravity = 3
		self.player.set_movement('horizontal')

		for group in self.level.sprite_groups:
			for sprite in group['group']:
				if group['name'] == 'clouds':
					sprite.hspeed = -(random.randint(2, 6) * 8)
					
		Item(self.somber, x=200, y=340)
	
	def on_change_to(self):
		self.somber.camera_follow(self.player)
	
	def update(self, delta):
		self.spawn_zombies(delta)
	
	def spawn_zombies(self, delta):
		self.zombie_timer += delta
		zombie_time = 5
		if self.zombie_timer > zombie_time:
			self.zombie_timer -= zombie_time
			side = 1
			extra = 200
			if self.somber.camera_pos[0] > 200:
				side = random.randint(0, 1)
				if side == 0:
					extra = -extra
			Zombie(self.somber, self, 'sprites/zombie/zombie_right_0.png', 'zombies', x=self.somber.camera_pos[0] + (self.somber.win_size[0] * side) + extra, y=self.somber.win_size[1] - 246)

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

class Ladder(somber_engine.Active):
	def __init__(self, somber, level, sprite, sprite_group, x=0, y=0):
		somber_engine.Active.__init__(self, sprite, somber=somber, pos=(x, y))
		
		self.level = level
		self.sprite_group = sprite_group
		self.set_pos((x, y))
		
		level.add_object(self, sprite_group)
		
class House(somber_engine.Active):
	def __init__(self, somber, level, sprite, sprite_group, x=0, y=0):
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
