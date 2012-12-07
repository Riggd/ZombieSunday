# Items
# Author list:
# 	Luke Martin <ltmartin@bsu.edu>
# 	Michael Milkovic <mlmilkovic@bsu.edu>
# 	Derek Onay <dsonay@bsu.edu>
# 	Ryan Wiesjahn <rwiesjahn@bsu.edu>

import somber as somber_engine
from weapon import *
from entity import *
import config

class Item(somber_engine.Active):
	def __init__(self, somber, level, x=0, y=0, sprite='sprites/items/item_default.png'):
		somber_engine.Active.__init__(self, sprite, somber=somber, pos=(x, y))
		for player in level.get_sprite_group('player'):
			self.player = player
		self.level = level
		self.level.add_object(self, 'items')
		
	def update(self):
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
		Item.__init__(self, somber, level, x, y, sprite='sprites/items/item_ammo.png')
		self.weapon = self.player.weapon
		self.rounds = 50
		
	def update(self):
		self.collect()
		Item.update(self)
		
	def collect(self):
		if self.collides_with(self.player):
			self.add_ammo()			
			self.kill()
			
	def add_ammo(self):
		self.add_ammo = 0
		
		if self.weapon.ammo[0] < self.weapon.ammo[1]:
			self.add_ammo = self.rounds
		
		if (self.add_ammo + self.weapon.ammo[0]) > self.weapon.ammo[1]:
			self.add_ammo = 0
			self.weapon.ammo[0] = self.weapon.ammo[1]
			
		else:
			self.weapon.ammo[0] += self.add_ammo
			
class AttachmentItem(Item):
	def __init__(self, somber, level, attachment, x=0, y=0):
		if attachment == Attachment.Speed:
			self.sprite = 'sprites/items/item_speed.png'
		elif attachment == Attachment.Fire:
			self.sprite = 'sprites/items/item_fire.png'
		elif attachment == Attachment.Force:
			self.sprite = 'sprites/items/item_force.png'
		elif attachment == Attachment.Lob:
			self.sprite = 'sprites/items/item_lob.png'
			
		Item.__init__(self, somber, level, x, y, sprite=self.sprite)
		self.attachment = attachment
		self.weapon = self.player.weapon
		
	def update(self):
		Item.update(self)
		
	def collect(self):
		self.set_attachment()
		self.kill()
			
	def set_attachment(self):
		if self.weapon.attachments[0] == None:
			 self.weapon.attachments[0] = self.attachment
		elif self.weapon.attachments[1] == None:
			self.weapon.attachments[1] = self.attachment
		else:
			self.weapon.attachments[0] = self.weapon.attachments[1]
			self.weapon.attachments[1] = self.attachment
				
		self.weapon.set_weapon_type()
		
class SalvagedGoods(Item):
	def __init__(self, somber, level, x, y):
		self.sprite = 'sprites/items/item_salvaged.png'
		Item.__init__(self, somber, level, x, y, sprite=self.sprite)
		
	def update(self):
		Item.update(self)
		
	def collect(self):
		if self.collides_with(self.player):
			self.kill()		
		
		