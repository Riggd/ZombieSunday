# Handles weapons (duh)
# Author list:
# 	Luke Martin <ltmartin@bsu.edu>
# 	Michael Milkovic <mlmilkovic@bsu.edu>
# 	Derek Onay <dsonay@bsu.edu>
# 	Ryan Wiesjahn <rwiesjahn@bsu.edu>
# LobForce

import somber as somber_engine
from bullet import *

class Weapon:
	def __init__(self, somber, character, attachments=[None, None]):
		self.somber = somber
		self.attachments = attachments
		self.type = WeaponType.Default
		self.character = character
		self.firefire_check = False
		self.ammo = [0, 5000]
		self.ammo[0] = self.ammo[1]
		self.ammo_consumption = 1
		self.rate = 0
		self.timer = self.rate
		
		self.set_weapon_type()
	
	def set_weapon_type(self):
		if self.attachments.count(Attachment.Speed) == 1:
			if self.attachments.count(Attachment.Fire) == 1:
				self.type = WeaponType.SpeedFire
				self.rate = 1
				self.ammo_consumption = 1
			elif self.attachments.count(Attachment.Lob) == 1:
				self.type = WeaponType.SpeedLob
				self.rate = 2
				self.ammo_consumption = 1
			elif self.attachments.count(Attachment.Force) == 1:
				self.type = WeaponType.SpeedForce
				self.rate = 2
				self.ammo_consumption = 1
			else:
				self.type = WeaponType.Speed
				self.rate = .2
				self.ammo_consumption = 1
	
		elif self.attachments.count(Attachment.Fire) == 1:
			if self.attachments.count(Attachment.Lob) == 1:
				self.type = WeaponType.FireLob
				self.rate = 2.5
				self.ammo_consumption = 1
			elif self.attachments.count(Attachment.Force) == 1:
				self.type = WeaponType.FireForce
				self.rate = 2
				self.ammo_consumption = 1
			else:
				self.type = WeaponType.Fire
				self.rate = 2
				self.ammo_consumption = 5
		
		elif self.attachments.count(Attachment.Lob) == 1:
			if self.attachments.count(Attachment.Force) == 1:
				self.type = WeaponType.LobForce
				self.rate = 2
				self.ammo_consumption = 1
			else:
				self.type = WeaponType.Lob
				self.rate = 2
				self.ammo_consumption = 1
				
		elif self.attachments.count(Attachment.Force) == 1:
				self.type = WeaponType.Force
				self.rate = 1.5
				self.ammo_consumption = 1
		
		elif self.attachments.count(Attachment.Speed) == 2:
			self.type = WeaponType.SpeedSpeed
			self.rate = .1
			self.ammo_consumption = 1
		
		elif self.attachments.count(Attachment.Fire) == 2:
			self.type = WeaponType.FireFire
			self.rate = -1
			self.ammo_consumption = 1
		
		elif self.attachments.count(Attachment.Lob) == 2:
			self.type = WeaponType.LobLob
			self.rate = 3
			self.ammo_consumption = 1
		
		elif self.attachments.count(Attachment.Force) == 2:
			self.type = WeaponType.ForceForce
			self.rate = 2
			self.ammo_consumption = 1
			
		elif self.attachments.count(None) == 2:
			self.type = WeaponType.Default
			self.rate = .5
			self.ammo_consumption = 1
		
		self.timer = self.rate
			
	def update(self, delta):
		self.weapon_timer(delta)
	
	def weapon_timer(self, delta):
		if self.timer < self.rate:
			self.timer += delta
		
	def fire(self):
		if self.ammo[0] - self.ammo_consumption >= 0:
			if self.rate > -5:
				if self.timer >= self.rate:
					self.create_bullet()
					self.ammo[0] -= self.ammo_consumption
					self.timer = 0
	
	def create_bullet(self):
		#self.somber.play_sound(os.path.join('sounds','revolver-1.wav'))
		
		if self.type == WeaponType.Speed:
			SpeedBullet(self.somber)
		elif self.type == WeaponType.Fire:
			FireBullet(self.somber)
		elif self.type == WeaponType.Lob:
			LobBullet(self.somber)
		elif self.type == WeaponType.Force:
			ForceBullet(self.somber)
		elif self.type == WeaponType.SpeedSpeed:
			SpeedSpeedBullet(self.somber)
		elif self.type == WeaponType.SpeedFire:
			SpeedFireBullet(self.somber)
		elif self.type == WeaponType.SpeedLob:
			SpeedLobBullet(self.somber)
		elif self.type == WeaponType.SpeedForce:
			SpeedForceBullet(self.somber)
		elif self.type == WeaponType.FireFire:
			if not self.firefire_check:
				FireFireBullet(self.somber)
				self.firefire_check = True
		elif self.type == WeaponType.FireLob:
			FireLobBullet(self.somber)
		elif self.type == WeaponType.FireForce:
			FireForceBullet(self.somber)
		elif self.type == WeaponType.LobLob:
			LobLobBullet(self.somber)
		elif self.type == WeaponType.LobForce:
			LobForceBullet(self.somber)
		elif self.type == WeaponType.ForceForce:
			ForceForceBullet(self.somber)
		else:
			DefaultBullet(self.somber)

			
class WeaponType:
	Default, Speed, SpeedSpeed, SpeedFire, SpeedLob, SpeedForce, Fire, FireFire, FireLob, FireForce, Lob, LobLob, LobForce, Force, ForceForce = range(15)

class Attachment:
	Speed, Fire, Lob, Force = range(4)
