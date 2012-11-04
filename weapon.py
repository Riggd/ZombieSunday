#Handles weapons (duh)
#Author list:
#	Luke Martin <ltmartin@bsu.edu>
import somber as somber_engine

class Weapon:
	def __init__(self, attachments = [None, None]):
		self.attachments = attachments
		self.type = WeaponType.Default
		
		if attachments.count(Attachment.Multi) == 1:
			if attachments.count(Attachment.Fire) == 1:
				self.type = WeaponType.MultiFire
			elif attachments.count(Attachment.Lob) == 1:
				self.type = WeaponType.MultiLob
			elif attachments.count(Attachment.Force) == 1:
				self.type = WeaponType.MultiForce
			else:
				self.type = WeaponType.Multi
	
		elif attachments.count(Attachment.Fire) == 1:
			if attachments.count(Attachment.Lob) == 1:
				self.type = WeaponType.FireLob
			elif attachments.count(Attachment.Force) == 1:
				self.type = WeaponType.FireForce
			else:
				self.type = WeaponType.Fire
		
		elif attachments.count(Attachment.Lob) == 1:
			if attachments.count(Attachment.Force) == 1:
				self.type = WeaponType.LobForce
			else:
				self.type = WeaponType.Lob
				
		elif attachments.count(Attachment.Force) == 1:
				self.type = WeaponType.Force
		
		elif attachments.count(Attachment.Multi) == 2:
			self.type = WeaponType.MultiMulti
		
		elif attachments.count(Attachment.Fire) == 2:
			self.type = WeaponType.FireFire
		
		elif attachments.count(Attachment.Lob) == 2:
			self.type = WeaponType.lobLob
		
		elif attachments.count(Attachment.Force) == 2:
			self.type = WeaponType.ForceForce

class WeaponType:
	Default, Multi, MultiMulti, MultiFire, MultiLob, MultiForce, Fire, FireFire, FireLob, FireForce, Lob, LobLob, LobForce, Force, ForceForce = range(15)

class Attachment:
	Multi, Fire, Lob, Force = range(4)