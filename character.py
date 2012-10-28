#For the handling of characters, both Player-controlled and NPCs
#Author list:
#	Luke Martin <ltmartin@bsu.edu>
import somber as somber_engine

class Character:
	def __init__(self,sprite,somber):
		somber_engine.active.__init__(self,sprite,somber=somber)
