# Author list:
# 	Luke Martin <ltmartin@bsu.edu>
# 	Michael Milkovic <mlmilkovic@bsu.edu>
# 	Derek Onay <dsonay@bsu.edu>
# 	Ryan Wiesjahn <rwiesjahn@bsu.edu>

import somber as somber_engine
from entity import *
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
	debug()

def debug():
	somber.write(config.FONT,
		(0, 0),
		'FPS: %s' % int(somber.current_fps),
		color=(0, 0, 0))

	somber.write(config.FONT,
		(0, 10),
		'Camera: X=%s, Y=%s' % (somber.camera_pos[0], somber.camera_pos[1]),
		color=(0, 0, 0))
	
	if ENDLESS_LEVEL == somber.current_level:
		for player in somber.current_level.get_sprite_group('player'):
			somber.write(config.FONT,
				(0, 20),
				'Player: X=%s, Y=%s' % (int(player.pos[0]), int(player.pos[1])),
				color=(0, 0, 0))
			somber.write(config.FONT,
				(0, 30),
				'Weapon: %s, %s' % (str(player.weapon.attachments[0]), str(player.weapon.attachments[1])),
				color=(0, 0, 0))

# Level setup
somber.set_background_color((150, 150, 150))
somber.add_font(config.FONT, 16)
TITLE_SCREEN = level.Title_Screen(somber).create_level()
ENDLESS_LEVEL = level.Endless_Level(somber).create_level()

if '-testlevel' in sys.argv:
	somber.change_level('Endless Level')
else:
	somber.change_level('Title Screen')

somber.run(callback)
