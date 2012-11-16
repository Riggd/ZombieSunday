#Author list:
#	Luke Martin <ltmartin@bsu.edu>
#	Michael Milkovic <mlmilkovic@bsu.edu>
#	Derek Onay <dsonay@bsu.edu>
#	Ryan Wiesjahn <rwiesjahn@bsu.edu>

# Testing a change. Again

import somber as somber_engine
from character import *
import weapon
import bullet
import config
import level
import sys
import ui
import os

somber = somber_engine.Somber(name='Zombie Sunday',
	win_size=config.WINDOW_SIZE,
	fps=config.FPS)
somber.set_resource_directory('sprites')

def callback():
	somber.write('ProggySquare.ttf',
		(0,0),
		'Camera: X=%s, Y=%s' % (somber.camera_pos[0],somber.camera_pos[1]),
		color=(0,0,0))
	
	somber.write('ProggySquare.ttf',
		(0,10),
		'FPS: %s' % int(somber.current_fps),
		color=(0,0,0))

#Level setup
somber.set_background_color((150,150,150))
somber.add_font('ProggySquare.ttf',16)
TITLE_SCREEN = level.Title_Screen(somber).create_level()
ENDLESS_LEVEL = level.Endless_Level(somber).create_level()

if '-testlevel' in sys.argv:
	somber.change_level('Endless Level')
else:
	somber.change_level('Title Screen')

somber.run(callback)