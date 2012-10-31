#Levels
#Author list:
#	Luke Martin <ltmartin@bsu.edu>
import somber as somber_engine

class Level:
	def __init__(self,somber):
		self.somber = somber
		
		Background(self.somber,'background_sky.png',0)
		Background(self.somber,'background_trees_back.png',1,y=235)
		Background(self.somber,'background_trees_fore.png',2,y=288)

class Background(somber_engine.active):
	def __init__(self,somber,sprite,z,x=0,y=0):
		somber_engine.active.__init__(self,sprite,somber=somber,pos=(x,y))
		
		somber.add_object(self,z)
