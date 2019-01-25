from __future__ import division
import pygame as pg
from settings import *
from sprite import *

class playerProjectile(pg.sprite.Sprite):
	# The Players projectile attack (sprite and collisions)
	def __init__(self, game):
		pg.sprite.Sprite.__init__(self)
		self.game = game
		self.load_images()
		self.image = self.standing_frames[0]
		self.rect = self.image.get_rect()

	def load_images(self):

		self.standing_frames = [
			self.game.spritesheet.get_image(0, 1200, 7, 7)
		]
		for frame in self.standing_frames:
			frame.set_colorkey(KEY)
		
	def fire(self, posx, posy):
		self.targetX, self.targetY = pg.mouse.get_pos()
		self.rect.center = (float(posx), float(posy-25))
		print(self.targetX, self.targetY)
		self.travx = float(self.targetX) - self.rect.x
		self.travy = float(self.targetY) - self.rect.y
		#self.travx = self.selfx - self.targetX
		#self.travy = self.selfy - self.targetY
		self.projGrad = self.travy / self.travx
		print(posx, posy)
		print(self.travx, self.travy)
		print(self.projGrad)
		self.fired = True
		col = pg.sprite.spritecollide(self, self.game.platforms, False)
		while col == False:
			col = pg.sprite.spritecollide(self, self.game.platforms, False)
		self.kill()
	def update(self):
		# 4 IF-Statements to fix projectile gradient
                        # Top Right Sector:
		if self.travx >= 0 and self.travy < 0:
			if self.projGrad >= 1 or self.projGrad <= -1:
				self.rect.x = self.rect.x + 1
				self.rect.y = self.rect.y + self.projGrad
			else:
				self.smalGrad = 1 / self.projGrad
				round(self.smalGrad)
				self.rect.y = self.rect.y - 1
				self.rect.x = self.rect.x - self.smalGrad
			# Bottom Right Sector:
		if self.travx >= 0 and self.travy >= 0:
			if self.projGrad >= 1 or self.projGrad <= -1:
				self.rect.x = self.rect.x + 1
				self.rect.y = self.rect.y + self.projGrad
			else:
				self.smalGrad = 1 / self.projGrad
				round(self.smalGrad)
				self.rect.y = self.rect.y + 1
				self.rect.x = self.rect.x + self.smalGrad
                        # Top Left Sector:
		if self.travx < 0 and self.travy < 0:
			if self.projGrad >= 1 or self.projGrad <= -1:
				self.rect.x = self.rect.x - 1
				self.rect.y = self.rect.y - self.projGrad
			else:
				self.smalGrad = 1 / self.projGrad
				round(self.smalGrad)
				self.rect.y = self.rect.y - 1
				self.rect.x = self.rect.x - self.smalGrad
                        # Bottom Left Sector:
		if self.travx < 0 and self.travy >= 0:
			if self.projGrad >= 1 or self.projGrad <= -1:
				self.rect.x = self.rect.x - 1
				self.rect.y = self.rect.y - self.projGrad
			else:
				self.smalGrad = 1 / self.projGrad
				round(self.smalGrad)
				self.rect.y = self.rect.y + 1
				self.rect.x = self.rect.x + self.smalGrad
		#Does collision-y things:
		hits = pg.sprite.spritecollide(self, self.game.platforms, False)
		if hits:
			# >increment DDA missed shots here<
			self.kill()
		# Used to kill projectiles at edge of screen:
		if self.rect.x <= 0:
			self.kill()
			self.fired = False
		if self.rect.y <= 0:
			self.kill()
			self.fired = False
		if self.rect.x >= WIDTH:
			self.kill()
			self.fired = False
		if self.rect.y >= HEIGHT:
			self.kill()
			self.fired = False

class plusProjectilel(pg.sprite.Sprite):
	# The Players plus projectile attack (LEFT) (sprite and collisions)
	def __init__(self, game):
		pg.sprite.Sprite.__init__(self)
		self.game = game
		self.load_images()
		self.image = self.standing_frames[0]
		self.rect = self.image.get_rect()

	def load_images(self):

		self.standing_frames = [
			self.game.spritesheet.get_image(0, 1200, 7, 7)
		]
		for frame in self.standing_frames:
			frame.set_colorkey(KEY)
		
	def fire(self, posx, posy):
		self.rect.center = posx, (posy-25)
		print("CHECK2")
	def update(self):
		hits = pg.sprite.spritecollide(self, self.game.platforms, False)
		if hits:
			self.kill()
		if self.rect.x > 0:
			self.rect.x = self.rect.x - 8
			print("CHECK3")
		else:
			print("END")
			self.kill()

class plusProjectiler(pg.sprite.Sprite):
	# The Players plus projectile attack (RIGHT) (sprite and collisions)
	def __init__(self, game):
		pg.sprite.Sprite.__init__(self)
		self.game = game
		self.load_images()
		self.image = self.standing_frames[0]
		self.rect = self.image.get_rect()

	def load_images(self):

		self.standing_frames = [
			self.game.spritesheet.get_image(0, 1200, 7, 7)
		]
		for frame in self.standing_frames:
			frame.set_colorkey(KEY)

	def fire(self, posx, posy):
		self.rect.center = posx, (posy-25)
	def update(self):
		hits = pg.sprite.spritecollide(self, self.game.platforms, False)
		if hits:
			self.kill()
		if self.rect.x < WIDTH:
			self.rect.x = self.rect.x + 8
		else:
			self.kill()

class plusProjectileu(pg.sprite.Sprite):
	# The Players plus projectile attack (UP) (sprite and collisions)
	def __init__(self, game):
		pg.sprite.Sprite.__init__(self)
		self.game = game
		self.load_images()
		self.image = self.standing_frames[0]
		self.rect = self.image.get_rect()

	def load_images(self):

		self.standing_frames = [
			self.game.spritesheet.get_image(0, 1200, 7, 7)
		]
		for frame in self.standing_frames:
			frame.set_colorkey(KEY)
		
	def fire(self, posx, posy):
		self.rect.center = posx, (posy-25)
	def update(self):
		hits = pg.sprite.spritecollide(self, self.game.platforms, False)
		if hits:
			self.kill()
		if self.rect.y > 0:
			self.rect.y = self.rect.y - 8
		else:
			self.kill()

class plusProjectiled(pg.sprite.Sprite):
	# The Players plus projectile attack (DOWN) (sprite and collisions)
	def __init__(self, game):
		pg.sprite.Sprite.__init__(self)
		self.game = game
		self.load_images()
		self.image = self.standing_frames[0]
		self.rect = self.image.get_rect()

	def load_images(self):

		self.standing_frames = [
			self.game.spritesheet.get_image(0, 1200, 7, 7)
		]
		for frame in self.standing_frames:
			frame.set_colorkey(KEY)
		
	def fire(self, posx, posy):
		self.rect.center = posx, (posy-25)
	def update(self):
		hits = pg.sprite.spritecollide(self, self.game.platforms, False)
		if hits:
			self.kill()
		if self.rect.y < HEIGHT:
			self.rect.y = self.rect.y + 8
		else:
			self.kill()
