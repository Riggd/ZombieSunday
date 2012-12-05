# Author list:
# 	Luke Martin <ltmartin@bsu.edu>
# 	Michael Milkovic <mlmilkovic@bsu.edu>
# 	Derek Onay <dsonay@bsu.edu>
# 	Ryan Wiesjahn <rwiesjahn@bsu.edu>

import somber as somber_engine
from entity import *
from items import *
import random
import weapon
import bullet
import config
import level
import sys
import ui
import os

somber = somber_engine.Somber(name=config.TITLE,
	win_size=config.WINDOW_SIZE,
	fps=config.FPS)
somber.set_resource_directory(config.RES_DIR)

def callback():
	print_ui()

def print_ui():
	if TITLE_SCREEN != somber.current_level:
		for player in somber.current_level.get_sprite_group('player'):
			somber.write('Lombriz',
				(config.WEAPON_STR_POS[0], config.WEAPON_STR_POS[1]),
				'%s /  %s' % (int(player.weapon.ammo[0]), int(player.weapon.ammo[1])),
				color=(65, 65, 65))
			
			somber.write('Lombriz',
				(config.HEALTH_STR_POS[0], config.HEALTH_STR_POS[1]),
				'%s /  %s' % (int(player.health[0]), int(player.health[1])),
				color=(233, 32, 20))
			
			somber.write('Lombriz',
				(config.SUPPLY_STR_POS[0], config.SUPPLY_STR_POS[1]),
				'%s /  %s' % (int(player.supplies[0]), int(player.supplies[1])),
				color=(16, 164, 156))
			
			somber.write('Lombriz',
				(config.CLOCK_STR_POS[0], config.CLOCK_STR_POS[1]),
				'%s' % somber.current_level.clock(),
				color=(231, 95, 46))
			
			somber.write('Lombriz',
				(config.TOTAL_SUPPLY_STR_POS[0], config.TOTAL_SUPPLY_STR_POS[1]),
				'%s /  %s' % (int(player.total_supplies[0]), int(player.total_supplies[1])),
				color=(16, 164, 156))
			
			somber.write('Lombriz',
				(config.LEVEL_STR_POS[0], config.LEVEL_STR_POS[1]),
				'Level:  %s' % int(somber.current_level.stage + 1),
				color=(233, 32, 20))
			
			somber.write('Lombriz',
				(config.SCORE_STR_POS[0], config.SCORE_STR_POS[1]),
				'Score: %s' % int(player.score),
				color=(233, 32, 20))
			
			somber.write('Lombriz',
				(config.KILLS_STR_POS[0], config.KILLS_STR_POS[1]),
				'Kills: %s' % int(player.zombies_killed),
				color=(233, 32, 20))

def debug():
	text_padding = 180
	somber.write('Proggy',
		(0, 0),
		'FPS: %s' % int(somber.current_fps),
		color=(0, 0, 0))

	somber.write('Proggy',
		(text_padding, 0),
		'Camera: X=%s, Y=%s' % (somber.camera_pos[0], somber.camera_pos[1]),
		color=(0, 0, 0))
	
	if TITLE_SCREEN != somber.current_level:
		for player in somber.current_level.get_sprite_group('player'):
			somber.write('Proggy',
				(0, 15),
				'Player: X=%s, Y=%s' % (int(player.pos[0]), int(player.pos[1])),
				color=(0, 0, 0))
			somber.write('Proggy',
				(text_padding, 15),
				'Health: %s / %s' % (int(player.health[0]), int(player.health[1])),
				color=(0, 0, 0))
			somber.write('Proggy',
				(0, 30),
				'Supplies: %s / %s' % (int(player.supplies[0]), int(player.supplies[1])),
				color=(0, 0, 0))
			somber.write('Proggy',
				(text_padding, 30),
				'Total Supplies: %s / %s' % (int(player.total_supplies[0]), int(player.total_supplies[1])),
				color=(0, 0, 0))
			somber.write('Proggy',
				(0, 45),
				'Weapon: %s, %s' % (str(player.weapon.attachments[0]), str(player.weapon.attachments[1])),
				color=(0, 0, 0))
			somber.write('Proggy',
				(text_padding, 45),
				'Ammo: %s, %s' % (int(player.weapon.ammo[0]), int(player.weapon.ammo[1])),
				color=(0, 0, 0))
			somber.write('Proggy',
				(0, 60),
				'Score: %s' % int(player.score), 
				color=(0, 0, 0))
			somber.write('Proggy',
				(text_padding, 60),
				'Heads Taken: %s' % int(player.zombies_killed), 
				color=(0, 0, 0))
			somber.write('Proggy',
				(0, 75),
				'Level: %s' % somber.current_level.stage,
				color=(0, 0, 0))
			somber.write('Proggy',
				(text_padding, 75),
				'Clock: %s' % somber.current_level.clock(),
				color=(0, 0, 0))

# Level setup
somber.set_background_color((150, 150, 150))
somber.add_font('Proggy', config.FONT_PROGGY, 16)
somber.add_font('Lombriz', config.FONT_LOMBRIZ, 24)
TITLE_SCREEN = level.Title_Screen(somber).create_level()
#somber.play_music(os.path.join('res','sounds','squired.xm'))

somber.change_level(TITLE_SCREEN)

somber.run(callback)
