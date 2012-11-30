# Items
# Author list:
# 	Luke Martin <ltmartin@bsu.edu>
# 	Michael Milkovic <mlmilkovic@bsu.edu>
# 	Derek Onay <dsonay@bsu.edu>
# 	Ryan Wiesjahn <rwiesjahn@bsu.edu>

import somber as somber_engine
import weapon

class Item(somber_engine.Active):
	def __init__(self, somber, level, x=0, y=0, sprite='sprites/items/item_default.png'):
		somber_engine.Active.__init__(self, sprite, somber=somber, pos=(x, y))
		for player in level.get_sprite_group('player'):
			self.player = player
		self.level = level
		self.level.add_object(self, 'items')
		
	def update(self):
		self.collect()
		somber_engine.Active.update(self)
		
	def collect(self):
		pass
				
class DefaultItem(Item):
	def __init__(self, somber, level, x=0, y=0):
		Item.__init__(self, somber, level, x, y, sprite='sprites/items/item_default.png')
		
	def update(self):
		Item.update(self)
		
	def collect(self):
		if self.collides_with(self.player):
			self.kill()
			print 'Collected Item!'

class Ammo(Item):
	def __init__(self, somber, level, x=0, y=0):
		Item.__init__(self, somber, level, x, y, sprite='sprites/items/item_default.png')
		
	def update(self):
		Item.update(self)
		
	def collect(self):
		if self.collides_with(self.player):
			self.kill()
