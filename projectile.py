from __future__ import division
import pygame as pg
from settings import *
from sprite import *

class playerProjectile(pg.sprite.Sprite):
	# The Players projectile attack (sprite and collisions)
	def __init__(self, game):
		pg.sprite.Sprite.__init__(self)
		self.game = game
		self.image = self.game.spritesheet.get_image(0, 1200, 32, 32)#.set_colorkey(KEY)
		self.rect = self.image.get_rect()

	def fire(self, posx, posy):
		self.targetX, self.targetY = pg.mouse.get_pos()
		self.rect.center = (float(posx), float(posy))
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

class plusProjectile(pg.sprite.Sprite):
	# The Players perpendicular projectile attack (sprite and collisions)
	def __init__(self, game):
                pg.sprite.Sprite.__init__(self)
		self.game = game
		self.image = self.game.spritesheet.get_image(0, 1200, 32, 32)#.set_colorkey(KEY)
		self.rect = self.image.get_rect()

	def fireleft(self, posx, posy):
                self.rect.center = posx,posy
                if self.rect.x > 0:
                        self.rect.x = self.rect.x - 1
                else:
                        self.kill()
	def fireright(self, posx, posy):
                self.rect.center = posx,posy
                if self.rect.x < WIDTH:
                        self.rect.x = self.rect.x + 1
                else:
                        self.kill()
	def fireup(self, posx, posy):
                self.rect.center = posx,posy
                if self.rect.y > 0:
                        self.rect.y = self.rect.y - 1
                else:
                        self.kill()
	def firedown(self, posx, posy):
                self.rect.center = posx,posy
                if self.rect.y < HEIGHT:
                        self.rect.y = self.rect.y + 1
                else:
                        self.kill()
	def fire(self, posx, posy):
                self.fireleft(posx, posy)
                self.fireright(posx, posy)
                self.fireup(posx, posy)
                self.firedown(posx, posy)
                
                
