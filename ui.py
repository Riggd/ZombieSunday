#For the handling the UI
#Author list:
#	Luke Martin <ltmartin@bsu.edu>
#	Michael Milkovic <mlmilkovic@bsu.edu>
#	Derek Onay <dsonay@bsu.edu>
#	Ryan Wiesjahn <rwiesjahn@bsu.edu>

import somber as somber_engine
import logging
import config
import json
import time

class UI_Group:
	def __init__(self,somber,level,sprite_group):
		self.somber = somber
		self.level = level
		self.sprite_group = sprite_group
		
		self.elements = []
	
	def create_element(self,sprite,name,x=0,y=0):
		_element = UI_Element(self.somber,self.level,sprite,self.sprite_group,name,x=x,y=y)
		_element.parent = self
		
		self.elements.append(_element)
		
		return _element
	
	def remove_element(self,element):
		logging.debug('[Somber] Removed ui element \'%s\'.' % element.name)
		
		self.elements.remove(element)
	
	def get_element(self,name):
		for element in self.elements:
			if element.name == name:
				return element
		
		raise 'Element \'%s\' does not exist.' % name
	
	def get_clicked_elements(self):
		_clicked_elements = []
		for element in self.elements:
			if element.collides_with_point(self.somber.mouse_pos):
				_clicked_elements.append(element)
		
		return _clicked_elements

class UI_Element(somber_engine.Static_UI):
	def __init__(self,somber,level,sprite,group,name,x=0,y=0):
		somber_engine.Static_UI.__init__(self,sprite,somber=somber,pos=(x,y))
		
		self.name = name
		
		level.add_object(self,group)

	def kill(self):
		self.parent.remove_element(self)
		
		somber_engine.Static_UI.kill(self)

def load_highscores():
	try:
		config.HIGHSCORES = json.loads(open('highscores.txt','r').readline())
		logging.info('[Somber] Loaded highscores')
	except IOError:
		save_highscores()

def save_highscores():
	with open('highscores.txt','w') as e:
		e.write(json.dumps(config.HIGHSCORES))
		logging.info('[Somber] Saved highscores!')

def add_highscore(score,kills):
	date = time.strftime('%m/%d/%y')
	_added = False
	
	if not len(config.HIGHSCORES):
		config.HIGHSCORES.append({'score': score,'kills': kills,'date': date})
		logging.info('[Somber] New highscore!')
		_added = True
	else:
		for entry in config.HIGHSCORES:
			if score>entry['score']:
				config.HIGHSCORES.insert(config.HIGHSCORES.index(entry),{'score': score,'kills': kills,'date': date})
				logging.info('[Somber] New highscore!')
				_added = True
				break
	
	#if len(config.HIGHSCORES)<5:
		#if not _added:
		config.HIGHSCORES.append({'score': score,'kills': kills,'date': date})
	#lse:
	if len(config.HIGHSCORES)>=5:
		config.HIGHSCORES.pop()
	
