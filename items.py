# Items
# Author list:
# 	Luke Martin <ltmartin@bsu.edu>
# 	Michael Milkovic <mlmilkovic@bsu.edu>
# 	Derek Onay <dsonay@bsu.edu>
# 	Ryan Wiesjahn <rwiesjahn@bsu.edu>

import somber as somber_engine
import weapon
from entity import *

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
		self.weapon = self.player.weapon
		self.rounds = 50
		
	def update(self):
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

class AttachmentSpeed(Item):
	def __init__(self, somber, level, x=0, y=0):
		Item.__init__(self, somber, level, x, y, sprite='sprites/items/item_speed.png')
		self.weapon = self.player.weapon
		self.attachments = self.player.weapon.attachments
		
	def update(self):
		Item.update(self)
		
	def collect(self):
		if self.collides_with(self.player):
			self.set_attachment()
			self.kill()
			
	def set_attachment(self):
		if self.attachments[0] == None:
			 self.attachments[0] = weapon.Attachment.Speed
		else:
			self.attachments[1] = weapon.Attachment.Speed
				
		self.weapon.set_weapon_type()
			
class AttachmentFire(Item):
	def __init__(self, somber, level, x=0, y=0):
		Item.__init__(self, somber, level, x, y, sprite='sprites/items/item_fire.png')
		self.weapon = self.player.weapon
		self.attachments = self.player.weapon.attachments
		
	def update(self):
		Item.update(self)
		
	def collect(self):
		if self.collides_with(self.player):
			self.set_attachment()
			self.kill()
			
	def set_attachment(self):
		if self.attachments[0] == None:
			 self.attachments[0] = weapon.Attachment.Fire
		else:
			self.attachments[1] = weapon.Attachment.Fire
				
		self.weapon.set_weapon_type()

class AttachmentLob(Item):
	def __init__(self, somber, level, x=0, y=0):
		Item.__init__(self, somber, level, x, y, sprite='sprites/items/item_lob.png')
		self.weapon = self.player.weapon
		self.attachments = self.player.weapon.attachments
		
	def update(self):
		Item.update(self)
		
	def collect(self):
		if self.collides_with(self.player):
			self.set_attachment()
			self.kill()
			
	def set_attachment(self):
		if self.attachments[0] == None:
			 self.attachments[0] = weapon.Attachment.Lob
		else:
			self.attachments[1] = weapon.Attachment.Lob
				
		self.weapon.set_weapon_type()

class AttachmentForce(Item):
	def __init__(self, somber, level, x=0, y=0):
		Item.__init__(self, somber, level, x, y, sprite='sprites/items/item_force.png')
		self.weapon = self.player.weapon
		self.attachments = self.player.weapon.attachments
		
	def update(self):
		Item.update(self)
		
	def collect(self):
		if self.collides_with(self.player):
			self.set_attachment()
			self.kill()
			
	def set_attachment(self):
		if self.attachments[0] == None:
			 self.attachments[0] = weapon.Attachment.Force
		else:
			self.attachments[1] = weapon.Attachment.Force
				
		self.weapon.set_weapon_type()
		
