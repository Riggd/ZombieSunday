#Bullets
#Author list:
#	Luke Martin <ltmartin@bsu.edu>
#	Michael Milkovic <mlmilkovic@bsu.edu>
#	Derek Onay <dsonay@bsu.edu>
#	Ryan Wiesjahn <rwiesjahn@bsu.edu>

import somber as somber_engine

class Bullet:
	def __init__(self,sprite,somber):
		somber_engine.active.__init__(self,sprite,somber=somber)
