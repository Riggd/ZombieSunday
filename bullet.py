#Bullets
#Author list:
#	Luke Martin <ltmartin@bsu.edu>
import somber as somber_engine

class Bullet:
	def __init__(self,sprite,somber):
		somber_engine.active.__init__(self,sprite,somber=somber)