#Bullets
#Author list:
#	Luke Martin <ltmartin@bsu.edu>
#	Michael Milkovic <mlmilkovic@bsu.edu>
#	Derek Onay <dsonay@bsu.edu>
#	Ryan Wiesjahn <rwiesjahn@bsu.edu>

import somber as somber_engine
from weapon import *

class Bullet:
	def __init__(self,somber,sprite,weapon):
		somber_engine.active.__init__(self,sprite,somber=somber)
		self.type = weapon.type