# Levels
# Author list:
# 	Luke Martin <ltmartin@bsu.edu>
# 	Michael Milkovic <mlmilkovic@bsu.edu>
# 	Derek Onay <dsonay@bsu.edu>
# 	Ryan Wiesjahn <rwiesjahn@bsu.edu>

import somber as somber_engine
import pygame
import random
import sys
import ui
import os
import pygame
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
		self.create_sprite_group('background_3', scroll_speed=1, group=somber_engine.BackgroundParallaxGroup)
		self.create_sprite_group('sun', group=somber_engine.StaticBackgroundGroup)
		self.create_sprite_group('clouds', group=somber_engine.StaticBackgroundGroup)
		self.create_sprite_group('ground', scroll_speed=1, group=somber_engine.BackgroundParallaxGroup)
		self.create_sprite_group('dummy')
		self.create_sprite_group('ui', group=somber_engine.StaticGroup)
		self.create_sprite_group('how_to_ui', group=somber_engine.StaticGroup)
		
		Static_Background(self.somber, self, 'sprites/background/sky.png', 'background_0')
		Sun(self.somber, self, 'sprites/background/sun.png', 'sun', x=config.SUN_POS[0], y=config.SUN_POS[1])
		Background(self.somber, self, 'sprites/background/trees_back.png', 'background_1', x=config.BACKGROUND_1_POS[0], y=config.BACKGROUND_1_POS[1])
		Background(self.somber, self, 'sprites/background/trees_fore.png', 'background_2', x=config.BACKGROUND_2_POS[0], y=config.BACKGROUND_2_POS[1])
		Cloud(self.somber, self, 'sprites/background/cloud_1.png', 'clouds', x=config.CLOUD_1_POS[0], y=config.CLOUD_1_POS[1])
		Cloud(self.somber, self, 'sprites/background/cloud_2.png', 'clouds', x=config.CLOUD_2_POS[0], y=config.CLOUD_2_POS[1])
		Cloud(self.somber, self, 'sprites/background/cloud_3.png', 'clouds', x=config.CLOUD_3_POS[0], y=config.CLOUD_3_POS[1])
		Background(self.somber, self, 'sprites/foreground/ground.png', 'ground', x=config.GROUND_POS[0], y=config.GROUND_POS[1])
		Background(self.somber, self, 'sprites/foreground/ground_top.png', 'background_3', x=config.GROUND_TOP_POS[0], y=config.GROUND_TOP_POS[1])
		
		self.main_ui = ui.UI_Group(self.somber, self, 'ui')
		self.how_to_ui = ui.UI_Group(self.somber, self, 'how_to_ui')
		
		self.logo = None
		self.button_start = None
		self.button_how_to = None
		self.button_quit = None
		self.how_to_screen = None
		self.button_back_to_title = None
		
		self.create_main_ui()
				
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
	
	def create_main_ui(self):
		self.logo = self.main_ui.create_element('sprites/ui/logo_zombie_sunday.png', 'logo', x=config.LOGO_POS[0], y=config.LOGO_POS[1])
		self.button_start = self.main_ui.create_element('sprites/ui/button_start_game.png', 'button_start', x=config.BUTTON_START_POS[0], y=config.BUTTON_START_POS[1])
		self.button_how_to = self.main_ui.create_element('sprites/ui/button_how_to.png', 'button_how_to', x=config.BUTTON_HOWTO_POS[0], y=config.BUTTON_HOWTO_POS[1])
		self.button_quit = self.main_ui.create_element('sprites/ui/button_quit_game.png', 'button_quit', x=config.BUTTON_QUIT_POS[0], y=config.BUTTON_QUIT_POS[1])
		
	def create_how_to_ui(self):
		self.how_to_screen = self.main_ui.create_element('sprites/ui/how_to_play_screen.png', 'how_to_screen', x=config.HOW_TO_SCREEN_POS[0], y=config.HOW_TO_SCREEN_POS[1])
		self.button_back_to_title = self.main_ui.create_element('sprites/ui/button_back_to_title.png', 'button_back_to_title', x=config.BUTTON_BACK_TO_TITLE_POS[0], y=config.BUTTON_BACK_TO_TITLE_POS[1])
					
	def mouse_down(self, button):
		for element in self.main_ui.get_clicked_elements():
			if element.name == 'button_start':
				self.somber.play_sound(config.SOUND_BUTTON)
				self.start_game()
			elif element.name == 'button_how_to':
				self.somber.play_sound(config.SOUND_BUTTON)
				self.clear_ui()
				self.create_how_to_ui()
			elif element.name == 'button_back_to_title':
				self.somber.play_sound(config.SOUND_BUTTON)
				self.clear_ui()
				self.create_main_ui()
			elif element.name == 'button_quit':
				self.somber.play_sound(config.SOUND_BUTTON)
				self.somber.quit()
	
	def clear_ui(self):
		for sprite in self.main_ui.elements[:]:
			sprite.kill()
		for sprite in self.how_to_ui.elements[:]:
			sprite.kill()
	
	def start_game(self):
		ENDLESS_LEVEL = Endless_Level(self.somber).create_level()
		self.somber.change_level(ENDLESS_LEVEL)

class Endless_Level(somber_engine.Level):
	def __init__(self, somber, stage=0):
		somber_engine.Level.__init__(self, somber, 'Endless Level')
		self.stage = stage
		self.zombie_timer = 0
		self.level_clock = config.LEVEL_TIME
		self.level_timer = 0
		self.attachment_1_sprite = None
		self.attachment_2_sprite = None
		self.complete = False
		self.dead = False
		self.out_of_time = False

	def create_level(self):
		self.create_sprite_group('background_0', scroll_speed=0)
		self.create_sprite_group('background_1', scroll_speed=0.2, group=somber_engine.BackgroundParallaxGroup)
		self.create_sprite_group('background_2', scroll_speed=0.3, group=somber_engine.BackgroundParallaxGroup)
		self.create_sprite_group('sun', group=somber_engine.StaticBackgroundGroup)
		self.create_sprite_group('clouds', group=somber_engine.StaticBackgroundGroup)
		self.create_sprite_group('ground')
		self.create_sprite_group('ground_top')
		self.create_sprite_group('buildings')
		self.create_sprite_group('doors')
		self.create_sprite_group('bullets')
		self.create_sprite_group('items')
		self.create_sprite_group('player')
		self.create_sprite_group('zombies')
		self.create_sprite_group('explosions')
		self.create_sprite_group('ui_back', group=somber_engine.StaticGroup)
		self.create_sprite_group('ui_fore', group=somber_engine.StaticGroup)
		
		Static_Background(self.somber, self, 'sprites/background/sky.png', 'background_0')
		Sun(self.somber, self, 'sprites/background/sun.png', 'sun', x=config.SUN_POS[0], y=config.SUN_POS[1])
		Background(self.somber, self, 'sprites/background/trees_back.png', 'background_1', x=config.BACKGROUND_1_POS[0], y=config.BACKGROUND_1_POS[1])
		Background(self.somber, self, 'sprites/background/trees_fore.png', 'background_2', x=config.BACKGROUND_2_POS[0], y=config.BACKGROUND_2_POS[1])
		Cloud(self.somber, self, 'sprites/background/cloud_1.png', 'clouds', x=config.CLOUD_1_POS[0], y=config.CLOUD_1_POS[1])
		Cloud(self.somber, self, 'sprites/background/cloud_2.png', 'clouds', x=config.CLOUD_2_POS[0], y=config.CLOUD_2_POS[1])
		Cloud(self.somber, self, 'sprites/background/cloud_3.png', 'clouds', x=config.CLOUD_3_POS[0], y=config.CLOUD_3_POS[1])
		
		Building(self.somber, self, 'sprites/foreground/home.png', 'buildings', home=True, x=config.HOME_POS[0], y=config.HOME_POS[1])
		
		self.main_ui_back = ui.UI_Group(self.somber, self, 'ui_back')
		self.main_ui_back.create_element('sprites/ui/weapon_bg.png', 'weapon_bg', x=config.WEAPON_BG_POS[0], y=config.WEAPON_BG_POS[1])
		self.main_ui_back.create_element('sprites/ui/health_bg.png', 'health_bg', x=config.HEALTH_BG_POS[0], y=config.HEALTH_BG_POS[1])
		self.main_ui_back.create_element('sprites/ui/supply_bg.png', 'supply_bg', x=config.SUPPLY_BG_POS[0], y=config.SUPPLY_BG_POS[1])
		self.main_ui_back.create_element('sprites/ui/supply_bg.png', 'total_supply_bg', x=config.TOTAL_SUPPLY_BG_POS[0], y=config.TOTAL_SUPPLY_BG_POS[1])
		
		self.main_ui_fore = ui.UI_Group(self.somber, self, 'ui_fore')
		self.health_bar = self.main_ui_fore.create_element('sprites/ui/health_bar.png', 'health_bar', x=config.HEALTH_BAR_POS[0], y=config.HEALTH_BAR_POS[1])
		self.supply_bar = self.main_ui_fore.create_element('sprites/ui/supply_bar.png', 'supply_bar', x=config.SUPPLY_BAR_POS[0], y=config.SUPPLY_BAR_POS[1])
		self.total_supply_bar = self.main_ui_fore.create_element('sprites/ui/supply_bar.png', 'total_supply_bar', x=config.TOTAL_SUPPLY_BAR_POS[0], y=config.TOTAL_SUPPLY_BAR_POS[1])
		
		self.attachment_1 = None
		self.attachment_2 = None
		self.box_bg = self.button_next_level = None
		
		self._init_ground()
		self._init_clouds()
			
		self.level = self
		self.setup()
		
		return self
	
	def _init_ground(self):
		for tile in range(0, config.LEVEL_SIZE):
			Platform(self.somber, self, 'sprites/foreground/ground.png', 'ground', x=tile * config.GROUND_WIDTH, y=config.GROUND_POS[1])
			Platform(self.somber, self, 'sprites/foreground/ground_top.png', 'ground_top', x=tile * config.GROUND_WIDTH, y=config.GROUND_TOP_POS[1])
	
	def _init_clouds(self):
		for group in self.sprite_groups:
			for sprite in group['group']:
				if group['name'] == 'clouds':
					sprite.hspeed = -(random.randint(2, 6) * 8)
	
	def setup(self):
		self._setup_player()
		self._setup_buildings()
					
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
				if random.randint(0,1) == 0:
					self.somber.play_sound(config.SOUND_ZOMBIE_GROAN)
				#else:
				#	self.somber.play_sound(config.SOUND_ZOMBIE_GROAN_2)
				Zombie(self.somber, self, 'zombies', x=self.somber.camera_pos[0] + (config.WINDOW_SIZE[0] * side) + extra, y=config.ZOMBIE_POS[1])
	
	def clock_timer(self, delta):
		self.level_timer += delta
		if self.level_timer >= 1:
			self.level_timer -= 1
			self.level_clock -= 1
	
	def clock(self):
		string = str(int(self.level_clock / 60)) + ':'
		seconds = str(self.level_clock % 60)
		if int(seconds) < 10:
			seconds =  '0' + seconds
		string += seconds
		return string
	
	def update_ui(self):
		health_value = round(float(self.player.health[0]) / float(self.player.health[1]), 2) * self.health_bar.sprite.get_width()
		supply_value = round(float(self.player.supplies[0]) / float(self.player.supplies[1]), 2) * self.supply_bar.sprite.get_width()
		total_supply_value = round(float(self.player.total_supplies[0]) / float(self.player.total_supplies[1]), 2) * self.total_supply_bar.sprite.get_width()
		
		if health_value < 0:
			health_value = 0
		if supply_value < 0:
			supply_value = 0
		if total_supply_value < 0:
			total_supply_value = 0
		
		self.health_bar.set_value(health_value)
		self.supply_bar.set_value(supply_value)
		self.total_supply_bar.set_value(total_supply_value)
		
		if self.player.weapon.attachments[0] == Attachment.Speed and self.attachment_1_sprite != Attachment.Speed:
			self.attachment_1_sprite = Attachment.Speed
			if self.attachment_1 != None:
				self.attachment_1.kill()
			self.attachment_1 = self.main_ui_fore.create_element('sprites/ui/attachment_speed.png', 'attachment_1', x=config.ATTACHMENT_1_POS[0], y=config.ATTACHMENT_1_POS[1])
		elif self.player.weapon.attachments[0] == Attachment.Fire and self.attachment_1_sprite != Attachment.Fire:
			self.attachment_1_sprite = Attachment.Fire
			if self.attachment_1 != None:
				self.attachment_1.kill()
			self.attachment_1 = self.main_ui_fore.create_element('sprites/ui/attachment_fire.png', 'attachment_1', x=config.ATTACHMENT_1_POS[0], y=config.ATTACHMENT_1_POS[1])
		elif self.player.weapon.attachments[0] == Attachment.Lob and self.attachment_1_sprite != Attachment.Lob:
			self.attachment_1_sprite = Attachment.Lob
			if self.attachment_1 != None:
				self.attachment_1.kill()
			self.attachment_1 = self.main_ui_fore.create_element('sprites/ui/attachment_lob.png', 'attachment_1', x=config.ATTACHMENT_1_POS[0], y=config.ATTACHMENT_1_POS[1])
		elif self.player.weapon.attachments[0] == Attachment.Force and self.attachment_1_sprite != Attachment.Force:
			self.attachment_1_sprite = Attachment.Force
			if self.attachment_1 != None:
				self.attachment_1.kill()
			self.attachment_1 = self.main_ui_fore.create_element('sprites/ui/attachment_force.png', 'attachment_1', x=config.ATTACHMENT_1_POS[0], y=config.ATTACHMENT_1_POS[1])
		elif self.player.weapon.attachments[0] == None and self.attachment_1_sprite != None:
			self.attachment_1_sprite = None
			if self.attachment_1 != None:
				self.attachment_1.kill()
			self.attachment_1 = self.main_ui_fore.create_element('sprites/foreground/dummy.png', 'attachment_1', x=config.ATTACHMENT_1_POS[0], y=config.ATTACHMENT_1_POS[1])
		
		if self.player.weapon.attachments[1] == Attachment.Speed and self.attachment_2_sprite != Attachment.Speed:
			self.attachment_2_sprite = Attachment.Speed
			if self.attachment_2 != None:
				self.attachment_2.kill()
			self.attachment_2 = self.main_ui_fore.create_element('sprites/ui/attachment_speed.png', 'attachment_2', x=config.ATTACHMENT_2_POS[0], y=config.ATTACHMENT_2_POS[1])
		elif self.player.weapon.attachments[1] == Attachment.Fire and self.attachment_2_sprite != Attachment.Fire:
			self.attachment_2_sprite = Attachment.Fire
			if self.attachment_2 != None:
				self.attachment_2.kill()
			self.attachment_2 = self.main_ui_fore.create_element('sprites/ui/attachment_fire.png', 'attachment_2', x=config.ATTACHMENT_2_POS[0], y=config.ATTACHMENT_2_POS[1])
		elif self.player.weapon.attachments[1] == Attachment.Lob and self.attachment_2_sprite != Attachment.Lob:
			self.attachment_2_sprite = Attachment.Lob
			if self.attachment_2 != None:
				self.attachment_2.kill()
			self.attachment_2 = self.main_ui_fore.create_element('sprites/ui/attachment_lob.png', 'attachment_2', x=config.ATTACHMENT_2_POS[0], y=config.ATTACHMENT_2_POS[1])
		elif self.player.weapon.attachments[1] == Attachment.Force and self.attachment_2_sprite != Attachment.Force:
			self.attachment_2_sprite = Attachment.Force
			if self.attachment_2 != None:
				self.attachment_2.kill()
			self.attachment_2 = self.main_ui_fore.create_element('sprites/ui/attachment_force.png', 'attachment_2', x=config.ATTACHMENT_2_POS[0], y=config.ATTACHMENT_2_POS[1])
		elif self.player.weapon.attachments[1] == None and self.attachment_2_sprite != None:
			self.attachment_2_sprite = None
			if self.attachment_2 != None:
				self.attachment_2.kill()
			self.attachment_2 = self.main_ui_fore.create_element('sprites/foreground/dummy.png', 'attachment_2', x=config.ATTACHMENT_2_POS[0], y=config.ATTACHMENT_2_POS[1])		
	
	def spawn_ammo(self):
		distance = 0
		while True:
			distance += random.randint(config.ITEM_AMMO_RANGE[0], config.ITEM_AMMO_RANGE[1]) * config.ITEM_AMMO_RANGE[2]
			if distance < config.LEVEL_SIZE * config.GROUND_WIDTH:
				Ammo(self.somber, self.level, x=distance, y=self.somber.win_size[1] - 150)
			else:
				break
			
	def spawn_attachments(self):
		distance = 0
		while True:
			distance += random.randint(config.ITEM_ATTACHMENT_RANGE[0], config.ITEM_ATTACHMENT_RANGE[1]) * config.ITEM_ATTACHMENT_RANGE[2]
			if distance < config.LEVEL_SIZE * config.GROUND_WIDTH:
				AttachmentItem(self.somber, self, random.randint(0, 3), x=distance, y=config.ATTACHMENT_POS[1])
			else:
				break
	
	def on_change_to(self):
		self.somber.camera_follow(self.player)
		
		self.somber.bind_key(' ', self.player.weapon.fire, repeat=True)
		self.somber.bind_key('m1', self.mouse_down)
		self.somber.bind_key('e', self.player.action)
		self.somber.bind_key('-', self.player.change_attachment_1)
		self.somber.bind_key('=', self.player.change_attachment_2)
		self.somber.bind_key(']', self.change_stage)
		
	def mouse_down(self, button):
		for element in self.main_ui_fore.get_clicked_elements():
			if element.name == 'button_next_level':
				self.somber.play_sound(config.SOUND_BUTTON)
				self.change_stage()
			if element.name == 'button_exit_to_title':
				TITLE_SCREEN = Title_Screen(self.somber).create_level()
				self.somber.change_level(TITLE_SCREEN)
	
	def change_stage(self):
		self.complete = False
		self.clear_level()
		ENDLESS_LEVEL = Endless_Level(self.somber, self.stage + 1).create_level()
		ENDLESS_LEVEL.player.score = self.player.score + (self.level_clock * config.TIME_SCORE)
		ENDLESS_LEVEL.player.zombies_killed = self.player.zombies_killed
		self.somber.change_level(ENDLESS_LEVEL)
	
	def complete_level(self):
		if self.player.total_supplies[0] == self.player.total_supplies[1]:
			self.complete = True
			self.create_level_complete_ui()
	
	def fail_level(self):
		if self.player.health[0] == 0:
			self.dead = True
			self.create_level_fail_ui()
		if self.level_clock <= 0:
			self.level_clock = 0
			self.out_of_time = True
			self.create_level_fail_ui()
	
	def create_level_complete_ui(self):
		self.box_bg = self.main_ui_back.create_element('sprites/ui/box_2_bg.png', 'box_bg', x=config.BOX_2_BG_POS[0], y=config.BOX_2_BG_POS[1])
		self.button_next_level = self.main_ui_fore.create_element('sprites/ui/button_next_level.png', 'button_next_level', x=config.BUTTON_NEXT_LEVEL_POS[0], y=config.BUTTON_NEXT_LEVEL_POS[1])
		ui.add_highscore(self.player.score,self.player.zombies_killed,'derp')
	
	def create_level_fail_ui(self):
		self.box_bg = self.main_ui_back.create_element('sprites/ui/box_2_bg.png', 'box_bg', x=config.BOX_2_BG_POS[0], y=config.BOX_2_BG_POS[1])
		if self.out_of_time:
			self.fail_title = self.main_ui_fore.create_element('sprites/ui/title_out_of_time.png', 'fail_title', x=config.LVL_FAIL_OUT_OF_TIME_POS[0], y=config.LVL_FAIL_OUT_OF_TIME_POS[1])
		else:
			self.fail_title = self.main_ui_fore.create_element('sprites/ui/title_you_died.png', 'fail_title', x=config.LVL_FAIL_YOU_DIED_POS[0], y=config.LVL_FAIL_YOU_DIED_POS[1])
		self.button_exit_to_title = self.main_ui_fore.create_element('sprites/ui/button_exit_to_title.png', 'button_exit_to_title', x=config.BUTTON_EXIT_TO_TITLE_POS[0], y=config.BUTTON_EXIT_TO_TITLE_POS[1])
		ui.add_highscore(self.player.score,self.player.zombies_killed,'derp')
	
	def update(self, delta):
		if not self.complete and not self.dead and not self.out_of_time:
			self.update_ui()
			self.clock_timer(delta)
			self._spawn_zombies(delta)
			self.complete_level()
			self.fail_level()
	
	def clear_level(self):
		for group in self.sprite_groups:
			for sprite in group['group']:
				sprite.kill()
		
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
	def __init__(self, somber, level, sprite, sprite_group, home=False, x=0, y=0):
		somber_engine.Active.__init__(self, sprite, somber=somber, pos=(x, y))		
		level.add_object(self, sprite_group)
		
		self.level = level
		self.sprite_group = sprite_group
		self.set_pos((x, y))
		self.scavanged = False
		self.home = home
		self.door = Door(somber, self.level, 'sprites/foreground/door.png', 'doors', self, x=x + config.DOOR_POS[0], y=config.DOOR_POS[1])
		
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
