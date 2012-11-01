import somber as somber_engine
import character
import weapon
import bullet
import level
import ui
import os

win_size = (800,600)

somber = somber_engine.Somber(name='Zombie Sunday',win_size=win_size)
somber.resource_dir = os.path.join('sprites')

def callback():
	pass

#Level setup
somber.set_background_color((150,150,150))
TITLE_SCREEN = level.create_title_screen(somber)

#UI setup
main_ui = ui.UI_Group(somber,TITLE_SCREEN,'ui')
main_ui.create_element('zombie_sunday_logo.png',x=55,y=20)

somber.change_level('Title Screen')
somber.run(callback)