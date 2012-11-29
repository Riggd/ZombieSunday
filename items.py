# Items
# Author list:
# 	Luke Martin <ltmartin@bsu.edu>
# 	Michael Milkovic <mlmilkovic@bsu.edu>
# 	Derek Onay <dsonay@bsu.edu>
# 	Ryan Wiesjahn <rwiesjahn@bsu.edu>

import somber as somber_engine

class Item(somber_engine.Active):
	def __init__(self, somber, x=0, y=0, sprite='sprites/items/item_default.png'):
		somber_engine.Active.__init__(self, sprite, somber=somber, pos=(x, y))
		for player in somber.current_level.get_sprite_group('player'):
			self.player = player
			self.level = player.level

		self.level.add_object(self, 'items')
		
		self.timer = 0
		
	def update(self):
		self.collect()
		self.time()
		somber_engine.Active.update(self)
		
	def time(self):
		if self.timer < self.duration:
			self.timer += self.player.delta_speed
		else:
			self.kill()
		
	def collect(self):
		pass
				
class DefaultItem(Item):
	def __init__(self, somber, x=0, y=0):
		Item.__init__(self, somber, x, y)
		
	def update(self):
		Item.update(self)
		
	def collect(self):
		for player in self.current_level.get_sprite_group('player'):
			if self.collides_with(self.player):
				self.kill()
				print 'Collected Item!'
