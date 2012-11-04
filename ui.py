#For the handling the UI
#Author list:
#	Luke Martin <ltmartin@bsu.edu>
import somber as somber_engine

class UI_Group:
	def __init__(self,somber,level,sprite_group):
		self.somber = somber
		self.level = level
		self.sprite_group = sprite_group
		
		self.elements = []
	
	def create_element(self,sprite,x=0,y=0):
		_element = UI_Element(self.somber,self.level,sprite,self.sprite_group,x=x,y=y)
		
		self.elements.append(_element)

class UI_Element(somber_engine.Active):
	def __init__(self,somber,level,sprite,group,x=0,y=0):
		somber_engine.Active.__init__(self,sprite,somber=somber,pos=(x,y))
		
		level.add_object(self,group)