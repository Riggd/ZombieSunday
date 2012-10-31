import somber as somber_engine
import character
import weapon
import bullet
import level
import ui
import os

win_size = (640,480)

somber = somber_engine.Somber(name='Zombie Sunday',win_size=win_size)
somber.resource_dir = os.path.join('sprites')
#somber.add_font('ProggyClean.ttf',16)

def callback():
	pass

#Somber setup
#Somber creates two sprite groups by default (0 and 1)
somber.create_group() #Layer 2 - Additional background layer (hills)
somber.create_group() #Layer 3 - Clouds
somber.create_group() #Layer 4 - Player
somber.create_group() #Layer 5 - UI

#Level setup
somber.set_background_color((150,150,150))
level.Level(somber)

#UI setup
main_ui = ui.UI_Group(somber,5)
main_ui.create_element('zombie_sunday_logo.png')

somber.run(callback)