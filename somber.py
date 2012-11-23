import logging
import pygame
import sys
import os
from pygame.locals import *

logger = logging.getLogger()
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_formatter = logging.Formatter('[%(asctime)s] %(message)s')

ch = logging.StreamHandler()
ch.setFormatter(console_formatter)
logger.addHandler(ch)

hdlr = logging.FileHandler('debug.txt')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.DEBUG)

__author__  = 'flags'
__contact__ = 'jetstarforever@gmail.com'
__license__ = 'WTFPLv2'
__version__ = '0.2'
__about__   = '2d game engine using PyGame'

class StaticBackgroundGroup(pygame.sprite.Group):
	def draw(self,surface):
		spritedict = self.spritedict
		surface_blit = surface.blit
		dirty = self.lostsprites
		self.lostsprites = []
		dirty_append = dirty.append
		
		for s in self.sprites():
			r = spritedict[s]
			
			newrect = surface_blit(s.image, s.rect)
			
			if r is 0:
				dirty_append(newrect)
			else:
				if newrect.colliderect(r):
					dirty_append(newrect.union(r))
				else:
					dirty_append(newrect)
					dirty_append(r)
			spritedict[s] = newrect
		return dirty

class BackgroundParallaxGroup(pygame.sprite.Group):
	def draw(self,surface):
		spritedict = self.spritedict
		surface_blit = surface.blit
		dirty = self.lostsprites
		self.lostsprites = []
		dirty_append = dirty.append
		
		for s in self.sprites():
			r = spritedict[s]
			_scroll_x = s.somber.camera_pos[0] * s.scroll_speed
			
			_pos = (s.rect.topleft[0]-_scroll_x,
				s.rect.topleft[1]-s.somber.camera_pos[1])
			_posright = (s.rect.topright[0]-_scroll_x,
				s.rect.topright[1]-s.somber.camera_pos[1])
			_posdown = (s.rect.bottomright[0]-_scroll_x,
				s.rect.bottomright[1]-s.somber.camera_pos[1])
			
			for i in range(0,abs(int(_pos[0])/(s.rect.width/2))+2):
				newrect = surface_blit(s.image,(_pos[0]+(s.rect.width*i),_pos[1]))
				dirty_append(newrect)

			spritedict[s] = newrect
		return dirty

class StaticGroup(StaticBackgroundGroup):
	pass

class ActiveGroup(pygame.sprite.Group):
	"""'Give me $20' -flags, 2012"""
	def draw(self,surface):
		spritedict = self.spritedict
		surface_blit = surface.blit
		dirty = self.lostsprites
		self.lostsprites = []
		dirty_append = dirty.append
		
		for s in self.sprites():
			r = spritedict[s]
			if s.static:
				newrect = surface_blit(s.image, s.rect)
			else:
				_scroll_x = s.somber.camera_pos[0]-(s.somber.camera_pos[0]*(s.scroll_speed*.1))
				
				_pos = (s.rect.topleft[0]-_scroll_x,
					s.rect.topleft[1]-s.somber.camera_pos[1])
				_posright = (s.rect.topright[0]-_scroll_x,
					s.rect.topright[1]-s.somber.camera_pos[1])
				_posdown = (s.rect.bottomright[0]-_scroll_x,
					s.rect.bottomright[1]-s.somber.camera_pos[1])
				
				if _posright[0]<0 or _pos[0]>s.somber.win_size[0]:
					continue
				elif _posdown[1]+16<0 or _posright[1]-8>s.somber.win_size[1]:
					continue
				
				newrect = surface_blit(s.image, _pos)
			
			if r is 0:
				dirty_append(newrect)
			else:
				if newrect.colliderect(r):
					dirty_append(newrect.union(r))
				else:
					dirty_append(newrect)
					dirty_append(r)
			spritedict[s] = newrect
		return dirty

class Somber:
	def __init__(self,name='Somber Engine',win_size=(320,240),fps=60):
		self.name = name
		self.win_size = win_size
		self.fps = fps
		self.current_fps = fps
		self.state = 'running'
		
		#Various
		self.resource_dir = ''
		self.input = {'up':False,
			'down':False,
			'left':False,
			'right':False}
		self.mouse_pos = (0,0)
		self.camera_pos = [0,0]
		self.camera_follows = None
		
		#Lists
		self.fonts = []
		self.dirty_rects = []
		self.sprites = []
		self.keybinds = []
		
		#Start Pygame
		try:
			pygame.init()
			logging.info('[Somber] %s is running.' % name)
		except Exception, e:
			logging.error('[Somber] PyGame init failed with \'%s\'.' % e)

		#Set up our clocks here
		self.clock_fps = pygame.time.Clock()

		#Define the surfaces we'll be drawing to
		self.window = pygame.display.set_mode(self.win_size)
		self.buffer = pygame.Surface(self.win_size)
		self.background = pygame.Surface(self.win_size)
		
		#Set caption
		pygame.display.set_caption(self.name)
		
		#Levels
		self.levels = []
		self.current_level = None
	
	def set_resource_directory(self,directory):
		self.resource_dir = os.path.join(directory)
	
	def create_level(self,level,name='Untitled'):
		self.levels.append({'name': name, 'level': level})
		
		logging.debug('[Somber] Created level of name \'%s\'.' % name)
		
		return True
	
	def change_level(self,name):
		self.set_background_color((50,50,50))
		
		for level in self.levels:
			if level['name'] == name:
				self.current_level = level['level']
				level['level'].on_change_to()
				
				return True
		
		raise Exception('Level \'%s\' does not exist.' % name)
	
	def camera_follow(self,object):
		self.camera_follows = object
	
	def camera_update(self):
		if not self.camera_follows:
			return False
		
		_center_x = int(self.camera_follows.pos[0]-(self.win_size[0]/2))+\
			(self.camera_follows.sprite.get_width()/2)
		
		if _center_x<0: _center_x = 0
		self.camera_pos[0] = _center_x
	
	def get_all_resources(self):
		_ret = []
		
		for root, dirs, files in os.walk(self.resource_dir):
			for infile in files:
				_fname = os.path.join(root, infile)
				file, ext = os.path.splitext(_fname)
				if ext.lower() in ['.jpg','.png']:
					_ret.append(_fname.replace(self.resource_dir+os.sep,''))
		
		return _ret
	
	def bind_key(self,key,callback):
		self.keybinds.append({'key':key,'callback':callback})
	
	def make_rect(self,x,y,w,h):
		return pygame.Rect(x,y,w,h)
	
	def add_active(self,object):
		self.active_objects.add(object)
	
	def add_sprite(self,name):
		try:
			_surface = load_image(os.path.join(self.resource_dir,name))
		except:
			raise Exception('Sprite not found: %s' % os.path.join(self.resource_dir,name))
		
		self.sprites.append({'name':name,'surface':_surface})
		logging.debug('[Somber] Cached new sprite \'%s\'.' % (name))
		
		return _surface
	
	def get_sprite(self,name):
		for sprite in self.sprites:
			if sprite['name'] == name:
				return sprite['surface']
		
		return self.add_sprite(name)
	
	def add_font(self,font,size):
		for _font in self.fonts:
			if _font['name'] == font:
				raise Exception('Font \'%s\' already exists.' % font)
		
		self.fonts.append({'name':font,'size':size,'font':pygame.font.Font(font,size)})
		logging.debug('[Somber] Added font \'%s\'.' % font)
	
	def get_font(self,name):
		for font in self.fonts:
			if font['name']==name:
				return font
		
		return None
	
	def set_background_image(self,name):
		self.background_image = self.get_sprite(name)
		self.background.blit(self.background_image,(0,0))
		self.window.blit(self.background,(0,0))
		
		pygame.display.update()
	
	def set_background_color(self,color):
		self.background.fill(color)
		self.window.blit(self.background,(0,0))
		
		pygame.display.update()
	
	def draw_sprite_in_background(self,sprite,pos):
		self.background.blit(self.get_sprite(sprite),pos)
		
		pygame.display.update()
	
	def write(self,font,pos,text,color=(0,0,0),aa=True):
		_font = self.get_font(font)['font']
		
		self.dirty_rects.append(self.window.blit(_font.render(text, aa, color),pos))
	
	def draw_square(self,pos,color,alpha=255):
		_square = pygame.Surface((pos[2]-pos[0],pos[3]-pos[1]),flags=pygame.SRCALPHA)
		_square.fill((color[0],color[1],color[2],alpha))
		
		self.dirty_rects.append(self.window.blit(_square,(pos[0],pos[1])))
	
	def get_input(self):
		for event in pygame.event.get():
			if event.type == QUIT or event.type == KEYDOWN and event.key in [K_ESCAPE,K_q]:
				pygame.quit()
				sys.exit()
			
			elif event.type == KEYDOWN:
				if event.key == K_UP or event.key == K_KP8 or event.key == K_w:
					self.input['up'] = True
				elif event.key == K_DOWN or event.key == K_KP2 or event.key == K_s:
					self.input['down'] = True
				elif event.key == K_LEFT or event.key == K_KP4 or event.key == K_a:
					self.input['left'] = True
				elif event.key == K_RIGHT or event.key == K_KP6 or event.key == K_d:
					self.input['right'] = True
				elif event.key == K_KP7:
					self.input['upleft'] = True
				elif event.key == K_KP9:
					self.input['upright'] = True
				elif event.key == K_KP1:
					self.input['downleft'] = True
				elif event.key == K_KP3:
					self.input['downright'] = True
				
				for entry in self.keybinds:
					if len(entry['key'])==1 and ord(entry['key']) == event.key:
						entry['callback']()
			
			elif event.type == KEYUP:
				if event.key == K_UP or event.key == K_KP8 or event.key == K_w:
					self.input['up'] = False
				elif event.key == K_DOWN or event.key == K_KP2 or event.key == K_s:
					self.input['down'] = False
				elif event.key == K_LEFT or event.key == K_KP4 or event.key == K_a:
					self.input['left'] = False
				elif event.key == K_RIGHT or event.key == K_KP6 or event.key == K_d:
					self.input['right'] = False
				elif event.key == K_KP7:
					self.input['upleft'] = False
				elif event.key == K_KP9:
					self.input['upright'] = False
				elif event.key == K_KP1:
					self.input['downleft'] = False
				elif event.key == K_KP3:
					self.input['downright'] = False
			
			elif event.type == MOUSEMOTION:
				self.mouse_pos = tuple(event.pos)
			
			elif event.type == MOUSEBUTTONDOWN:
				for entry in self.keybinds:
					if entry['key']=='m1':
						entry['callback'](event.button)
	
	def run(self,callback):	
		while self.state=='running':
			if not self.current_level:
				continue
				
			milliseconds = self.clock_fps.tick(self.fps)
			seconds = milliseconds / 1000.0
			
			self.get_input()
			
			self.update(seconds)
			self.camera_update()
			self.render()
			callback()
			
			self.current_fps = self.clock_fps.get_fps()
			
			#Update the screen
			pygame.display.update(self.dirty_rects)
			
			self.dirty_rects = []
	
	def update(self,delta):
		#Update level
		self.current_level.update(delta)
		
		#Update all groups
		for group in self.current_level.sprite_groups:
			#TODO: Update all, then clear?
			for sprite in group['group']:
				sprite.delta_speed = delta
			
			group['group'].update()
			group['group'].clear(self.window,self.background)
	
	def render(self):
		#Draw all groups
		for group in self.current_level.sprite_groups:
			self.dirty_rects.extend(group['group'].draw(self.window))

class General(pygame.sprite.Sprite):
	def __init__(self,sprite,pos=None):
		self.sprite = sprite
		
		self.pos = list(pos)
		self.start_pos = list(pos)
		self.static = False
		self.z = 0
		
		self.movement = None
		
		self.alpha = 255
		self.last_alpha = 255
		
		self.animations = {}
		self.animation = None
		self.animation_index = 0
		
		self.image = self.sprite
		self.rect = self.image.get_bounding_rect()
		self.image.blit(self.image,(0,0))
		self.rect.topleft = self.pos

		pygame.sprite.Sprite.__init__(self)
	
	def add_animation(self,name,time,sprites):
		if name in self.animations.keys():
			raise Exception('Object already has animation \'%s\'.' % name)
		
		for sprite in sprites:
			self.somber.get_sprite(sprite)
		
		self.animations[name] = {'sprites': sprites[:],
			'time': time,
			'time_max': time}
		
		logging.debug('[Somber] Created new animation \'%s\'.' % name)
	
	def set_animation(self,animation):
		self.animation = animation
		self.animation_index = 0
		
		self.set_sprite(self.animations[self.animation]['sprites'][0])
	
	def play_animation(self):
		if not self.animation:
			return False
		
		if self.animations[self.animation]['time']:
			self.animations[self.animation]['time'] -= 1
		else:
			if self.animation_index < len(self.animations[self.animation]['sprites'])-1:
				self.animation_index += 1
			else:
				self.animation_index = 0
				
			self.set_sprite(self.animations[self.animation]['sprites'][self.animation_index])
			self.animations[self.animation]['time'] =\
				self.animations[self.animation]['time_max']
	
	def get_animation(self):
		return self.animation
	
	def set_sprite(self,sprite):
		self.sprite = self.somber.get_sprite(sprite)
		self.image = self.sprite
		self.image.blit(self.sprite,(0,0))
	
	def set_alpha(self,val):
		self.image1 = self.image.copy()
		self.image1.set_alpha(val)
		self.image.blit(self.image1,(0,0))
	
	def set_pos(self,pos,set_start=False):
		self.rect.topleft = list(pos)
		self.pos = list(pos)
		
		if set_start:
			self.start_pos = list(pos)
	
	def collides_with_point(self,pos):
		return self.rect.collidepoint(pos)
	
	def collide_at(self,pos,other):
		return other.rect.collidepoint((pos))
	
	def collides_with(self,object):
		if self.rect.colliderect(object.rect): return True
		
		return False
	
	def collides_with_group(self,group):
		_collides = pygame.sprite.spritecollide(self,group,False)
		if _collides:
			return _collides
		
		return False
	
	def collides_with_group_at(self,group_name,point):
		_found_group = False
		
		for group in self.somber.current_level.sprite_groups:
			if group['name'] == group_name:
				_found_group = True
				
				for sprite in group['group']:
					if sprite.rect.collidepoint((point)):
						return True
		
		if _found_group:
			return False
		else:
			raise Exception('Sprite group %s does not exist!' % group_name)
	
	def update(self):
		if self.animation:
			self.play_animation()
	
	def destroy(self):
		pass

class Static(General):
	def __init__(self,sprite=None,pos=(0,0),somber=None):
		if not somber:
			raise Exception('No somber callback set!')
		
		self.somber = somber
		self.sprite = somber.get_sprite(sprite)
		self.static = True
		
		General.__init__(self,sprite=self.sprite,pos=pos)

class Background(General):
	def __init__(self,sprite=None,pos=(0,0),somber=None):
		if not somber:
			raise Exception('No somber callback set!')
		
		self.somber = somber
		self.sprite = somber.get_sprite(sprite)
		
		General.__init__(self,sprite=self.sprite,pos=pos)

class BackgroundParallax(Background):
	def __init__(self,sprite=None,pos=(0,0),somber=None):
		if not somber:
			raise Exception('No somber callback set!')
		
		self.somber = somber
		self.sprite = somber.get_sprite(sprite)
		
		General.__init__(self,sprite=self.sprite,pos=pos)
		
		self.parallax = True

class Active(General):
	def __init__(self,sprite,pos=(0,0),somber=None):
		if not somber:
			raise Exception('No somber callback set!')
		
		self.somber = somber
		self.sprite = somber.get_sprite(sprite)
		
		General.__init__(self,sprite=self.sprite,pos=pos)
		
		self.hspeed = 0
		self.hspeed_max = 0
		self.hspeed_min = 0
		self.hfriction_move = 0
		self.hfriction_stop = 0
		
		self.vspeed = 0
		self.vspeed_max = 0
		self.vspeed_min = 0
		
		self.delta_speed = 0
		
		self.x_limit_min = None
		self.x_limit_max = None
		
		self.y_limit_min = None
		self.y_limit_max = None
		
		self.gravity = 0
		self.parallax = False
	
	def set_movement(self,type):
		if type in ['horizontal','vertical','ortho']:
			self.movement = type
		elif type == None:
			self.movement = None
		else:
			raise Exception('Invalid movement type: \'%s\'' % type)
	
	def update(self):
		if self.movement=='horizontal':
			if self.somber.input['right']:
				if self.hfriction_move and self.hspeed<self.hspeed_max:
					self.hspeed += self.hfriction_move
				else:
					self.hspeed = self.hspeed_max
			elif self.somber.input['left']:
				if self.hfriction_move and self.hspeed>-self.hspeed_max:
					self.hspeed -= self.hfriction_move
				else:
					self.hspeed = -self.hspeed_max
			else:
				if self.hfriction_stop:
					if self.hspeed>0:
						self.hspeed -= self.hfriction_stop
					elif self.hspeed<0:
						self.hspeed += self.hfriction_stop
				else:
					self.hspeed = self.hspeed_min
		elif self.movement=='vertical':
			if self.somber.input['right']: self.vspeed = self.vspeed_max
			elif self.somber.input['left']: self.vspeed = -self.vspeed_max
			else: self.vspeed = self.vspeed_min
		
		if not self.x_limit_max == None:
			if self.rect.topright[0]>self.x_limit_max:
				if self.hspeed>0:
					self.hspeed = 0
		
		if not self.x_limit_min == None:	
			if self.pos[0]<self.x_limit_min:
				if self.hspeed<0:
					self.hspeed = 0
					
		if not self.y_limit_max == None:
			if self.rect.bottomleft[1]>self.y_limit_max:
				if self.vspeed>0:
					self.vspeed = 0
		
		if not self.y_limit_min == None:	
			if self.pos[1]<self.y_limit_min:
				if self.vspeed<0:
					self.vspeed = 0
		
		self.vspeed+=self.gravity
		
		if not self.alpha == self.last_alpha:
			self.set_alpha(self.alpha)
		
		self.last_alpha = self.alpha
		self.pos[0] += self.hspeed * self.delta_speed
		self.pos[1] += self.vspeed * self.delta_speed
		#print self.hspeed,nx
		
		self.rect.topleft = [round(self.pos[0],0),round(self.pos[1],0)]
		#print self.rect.topleft
		
		General.update(self)
	
	def destroy(self):
		active.remove(self)
		
		general.destroy(self)

class Particle(Active):
	def __init__(self,sprite=None,pos=(0,0),gravity=0.05,alpha=255,velocity=(0,0)):
		active.__init__(self,sprite=sprite,pos=pos)
		
		self.set_alpha(alpha)
		self.gravity = gravity
		
		self.hspeed = velocity[0]
		self.vspeed = velocity[1]
	
	def update(self):
		self.alpha-=2
		
		if self.alpha<=0: self.destroy()
		
		if self.pos[0]<0 or self.pos[0]>win_size[0]\
			or self.pos[1]<0 or self.pos[1]>win_size[1]:
			self.destroy()
		
		active.update(self)

class Level:
	def __init__(self,somber,name):
		self.somber = somber
		self.name = name
		
		somber.create_level(self,name=name)
		
		self.sprite_groups = []
	
	def get_sprite_group(self,group_name):
		for _group in self.sprite_groups:
			if _group['name'] == group_name:
				return _group['group']
		
		raise Exception('Sprite group %s does not exist!' % group_name)
	
	def get_sprite_group_z_level(self,group_name):
		for _group in self.sprite_groups:
			if _group['name'] == group_name:
				return self.sprite_groups.index(_group)
		
		raise Exception('Sprite group %s does not exist!' % group_name)
	
	def create_sprite_group(self,name,z=-1,scroll_speed=0,group=ActiveGroup):
		if z == -1:
			z = len(self.sprite_groups)
		
		_group = group()
		
		self.sprite_groups.insert(z,{'name': name, 'group': _group, 'scroll_speed':scroll_speed})
		
		return _group
	
	def add_object(self,object,group_name):
		for _group in self.sprite_groups:
			if _group['name'] == group_name:
				object.scroll_speed = _group['scroll_speed']
				_group['group'].add(object)
				
				return True
		
		raise Exception('Sprite group %s does not exist!' % group_name)

	def on_change_to(self):
		pass
	
	def update(self):
		pass

def load_image(name):
	try:
		image = pygame.image.load(name)
	except:
		raise Exception('Could not find: %s' % name)
	
	if name.count('.png'):
		image=image.convert_alpha()
	else:
		image=image.convert()
		image.set_colorkey((255,255,255))
	
	return image

class UI_Group:
	def __init__(self,somber,level,sprite_group):
		self.somber = somber
		self.level = level
		self.sprite_group = sprite_group
		
		self.elements = []
	
	def create_element(self,sprite,name,x=0,y=0):
		_element = UI_Element(self.somber,self.level,sprite,self.sprite_group,name,x=x,y=y)
		
		self.elements.append(_element)
	
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

class UI_Element(Static):
	def __init__(self,somber,level,sprite,group,name,x=0,y=0):
		Static.__init__(self,sprite,somber=somber,pos=(x,y))
		
		self.name = name
		
		level.add_object(self,group)