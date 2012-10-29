import somber as somber_engine
import character
import weapon
import bullet
import level
import os

win_size = (640,480)

somber = somber_engine.Somber(name='Zombie Sunday',win_size=win_size)
somber.resource_dir = os.path.join('sprites')
#somber.add_font('ProggyClean.ttf',16)

def callback():
	pass

somber.set_background_color((150,150,150))
somber.run(callback)