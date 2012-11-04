import somber as somber_engine
from character import *
import weapon
import bullet
import level
import ui
import os

win_size = (1024,600)

somber = somber_engine.Somber(name='Zombie Sunday',win_size=win_size,fps=120)
somber.resource_dir = os.path.join('sprites')

def callback():
	pass

#Level setup
somber.set_background_color((150,150,150))
TITLE_SCREEN = level.Title_Screen(somber).create_level()
ENDLESS_LEVEL = level.Endless_Level(somber).create_level()

#Player STUFF
player = Character(somber,ENDLESS_LEVEL,'player.png','player',x=10,y=400)
player.hspeed_max = 250
player.set_movement('horizontal')

somber.camera_follow(player)

#UI setup
main_ui = ui.UI_Group(somber,TITLE_SCREEN,'ui')
main_ui.create_element('logo_zombie_sunday.png',x=55,y=100)

somber.change_level('Endless Level')
somber.run(callback)