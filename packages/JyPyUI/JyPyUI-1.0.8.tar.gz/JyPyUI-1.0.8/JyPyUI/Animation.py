import pygame
import os




class MultImage(pygame.sprite.Sprite):
	def __init__(self, dir_images):
		pygame.sprite.Sprite.__init__(self)
		self.padding = {'x':200,'y':200}
		self.pos = {'x':0,'y':0}
		self.sprites = []
		self.anim = 0
		self.cont = 0
		self.cont_max = 3
		self.active = False
		if os.path.exists(dir_images) and os.path.isdir(dir_images):
			images = os.listdir(dir_images)
			for image in images:
				self.image= pygame.image.load(os.path.join(dir_images, image))
				self.sprites.append(self.image)
		self.image = self.sprites[self.anim]
		self.image = pygame.transform.scale(self.image, (self.padding['x'],self.padding['y']))
		self.rect = self.image.get_rect()
		self.rect.topleft = self.pos['x'],self.pos['y']
	def ActiveAnimation(self):
		self.active = True
	def DefaultAnimation(self):
		self.active = False			
	def update(self):
		if self.active:
			self.cont += 1
		if self.cont >self.cont_max:
			self.cont = 0
			self.anim += 1
		if self.anim >=len(self.sprites):
			self.anim = 0
		self.image = self.sprites[self.anim]
		self.image = pygame.transform.scale(self.image, (self.padding['x'],self.padding['y']))
		self.rect = self.image.get_rect()
		self.rect.topleft = self.pos['x'],self.pos['y']
		
class FramesImage(pygame.sprite.Sprite):   
    def __init__(self, image, frames,quadro):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []
        self.app = pygame
        self.pos = {'x': 0, 'y': 0}
        self.padding={'x':200,'y':200}
        self.frame_y = quadro
        self.image = self.app.image.load(image)
        self.frames = frames
        self.anim = 0
        self.cont = 0
        self.cont_max = 3
        self.active = False

        # Calcula a largura dos quadros com base na imagem original
        frame_width = self.image.get_width() // self.frames

        for i in range(self.frames):
            # Calcula as coordenadas de corte corretamente
            x = i * frame_width
            sprite = self.image.subsurface(pygame.Rect(x, 0, frame_width, self.frame_y))
            self.sprites.append(sprite)

        self.image = self.sprites[self.anim]
        self.image = pygame.transform.scale(self.image, (self.padding['x'],self.padding['y']))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos['x'], self.pos['y']
    def ActiveAnimation(self):
    	self.active = True
    def DefaultAnimation(self):
    	self.active = False
    def update(self):
       if self.active:
       	self.cont += 1
       if self.cont > self.cont_max:
       	self.cont =0
       	self.anim +=1
       if self.anim >= len(self.sprites):
       	self.anim = 0
       self.image = self.sprites[self.anim]
       self.image = pygame.transform.scale(self.image, (self.padding['x'],self.padding['y']))
       self.rect = self.image.get_rect()
       self.rect.topleft = self.pos['x'], self.pos['y']
       	
class GroupAnimation:
	def __init__(self, image_anim):
		self.Group = pygame.sprite.Group()
		self.Group.add(image_anim)
		