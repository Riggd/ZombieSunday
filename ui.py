#For the handling the UI
#Author list:
#	Luke Martin <ltmartin@bsu.edu>
import somber as somber_engine

class UI_Group:
	def __init__(self,somber,z):
		self.somber = somber
		self.z = z
		
		self.elements = []
	
	def create_element(self,sprite,x=0,y=0):
		_element = UI_Element(self.somber,sprite,x=x,y=y,z=self.z)
		
		self.elements.append(_element)

class UI_Element(somber_engine.active):
	def __init__(self,somber,sprite,x=0,y=0,z=0):
		somber_engine.active.__init__(self,sprite,somber=somber,pos=(x,y))
		
		somber.add_object(self,z=z)