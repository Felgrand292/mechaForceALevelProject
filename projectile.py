from __future__ import division
import pygame as pg
from settings import *
from sprite import *

class playerProjectile(pg.sprite.Sprite):										#Creates the projectile sprite that the player will fire as standard
	# The Players projectile attack (sprite and collisions)
	def __init__(self, game):
		pg.sprite.Sprite.__init__(self)
		self.game = game
		self.load_images()
		self.image = self.standing_frames[0]
		self.rect = self.image.get_rect()

	def load_images(self):														#Loading images for the sprite

		self.standing_frames = [
			self.game.spritesheet.get_image(0, 1200, 7, 7)
		]
		for frame in self.standing_frames:
			frame.set_colorkey(KEY)
		
	def fire(self, posx, posy):													#Doing positional maths with y=mx+c to fire in direction of mouse. Explained more below
		self.targetX, self.targetY = pg.mouse.get_pos()
		self.rect.center = (float(posx), float(posy-25))
		print(self.targetX, self.targetY)
		self.travx = float(self.targetX) - self.rect.x 							#These two variables (travx,travy) hold the value of the difference in x and y coordinates
		self.travy = float(self.targetY) - self.rect.y 							# of the mouse and the players sprite.
		self.projGrad = self.travy / self.travx									#A gradient of the line between the two is then determined by travy/travx 
		print(posx, posy)														# This tells us how much y will need to be changed per every x coord moved
		print(self.travx, self.travy)
		print(self.projGrad)
		self.fired = True
	def update(self):
		# 4 IF-Statements to fix projectile gradient
                        # Top Right Sector:										 Detects if projectile is aimed in the top right corner of the display
		if self.travx >= 0 and self.travy < 0:
			if self.projGrad >= 1 or self.projGrad <= -1:
				self.rect.x = self.rect.x + 1
				self.rect.y = self.rect.y + self.projGrad
			else:
				self.smalGrad = 1 / self.projGrad								#If the gradient is anything between 1 and -1, the sprite cannot be moved less than a pixel,
				round(self.smalGrad)											#To solve this, we divide 1 by the gradient, to get the value x must be moved for incrementing y
				self.rect.y = self.rect.y - 1
				self.rect.x = self.rect.x - self.smalGrad
						# Bottom Right Sector:									 Detects if projectile is aimed in the bottom right corner of the display
		if self.travx >= 0 and self.travy >= 0:
			if self.projGrad >= 1 or self.projGrad <= -1:
				self.rect.x = self.rect.x + 1
				self.rect.y = self.rect.y + self.projGrad
			else:
				self.smalGrad = 1 / self.projGrad
				round(self.smalGrad)
				self.rect.y = self.rect.y + 1
				self.rect.x = self.rect.x + self.smalGrad
                        # Top Left Sector:										 Detects if projectile is aimed in the top left corner of the display
		if self.travx < 0 and self.travy < 0:
			if self.projGrad >= 1 or self.projGrad <= -1:
				self.rect.x = self.rect.x - 1
				self.rect.y = self.rect.y - self.projGrad
			else:
				self.smalGrad = 1 / self.projGrad
				round(self.smalGrad)
				self.rect.y = self.rect.y - 1
				self.rect.x = self.rect.x - self.smalGrad
                        # Bottom Left Sector:									 Detects if projectile is aimed in the bottom left corner of the display
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
		hits = pg.sprite.spritecollide(self, self.game.platforms, False)		#Detects if the projectile collides with anything other than a player, and kills the projectile
		if hits:
			# >increment DDA missed shots here<
			self.kill()															#Leaves room to implement DDA features in the final iteration
		hits = pg.sprite.spritecollide(self, self.game.set, False)
		if hits:
			# >increment DDA missed shots here<
			self.kill()
		hits = pg.sprite.spritecollide(self, self.game.setsky, False)
		if hits:
			# >increment DDA missed shots here<
			self.kill()

		if self.rect.x <= 0:													# Used to kill projectiles at edge of screen
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

class plusProjectilel(pg.sprite.Sprite):										#Creates 1/4 projectile sprites needed for the "+" shaped attack
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
		hits = pg.sprite.spritecollide(self, self.game.set, False)
		if hits:
			# >increment DDA missed shots here<
			self.kill()
		hits = pg.sprite.spritecollide(self, self.game.setsky, False)
		if hits:
			# >increment DDA missed shots here<
			self.kill()
		if self.rect.x > 0:
			self.rect.x = self.rect.x - 8
			print("CHECK3")
		else:
			print("END")
			self.kill()

class plusProjectiler(pg.sprite.Sprite):										#Creates 2/4 projectile sprites needed for the "+" shaped attack
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
		hits = pg.sprite.spritecollide(self, self.game.set, False)
		if hits:
			# >increment DDA missed shots here<
			self.kill()
		hits = pg.sprite.spritecollide(self, self.game.setsky, False)
		if hits:
			# >increment DDA missed shots here<
			self.kill()
		if self.rect.x < WIDTH:
			self.rect.x = self.rect.x + 8
		else:
			self.kill()

class plusProjectileu(pg.sprite.Sprite):										#Creates 3/4 projectile sprites needed for the "+" shaped attack
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
		hits = pg.sprite.spritecollide(self, self.game.set, False)
		if hits:
			# >increment DDA missed shots here<
			self.kill()
		hits = pg.sprite.spritecollide(self, self.game.setsky, False)
		if hits:
			# >increment DDA missed shots here<
			self.kill()
		if self.rect.y > 0:
			self.rect.y = self.rect.y - 8
		else:
			self.kill()

class plusProjectiled(pg.sprite.Sprite):										#Creates 4/4 projectile sprites needed for the "+" shaped attack
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
		hits = pg.sprite.spritecollide(self, self.game.set, False)
		if hits:
			# >increment DDA missed shots here<
			self.kill()
		hits = pg.sprite.spritecollide(self, self.game.setsky, False)
		if hits:
			# >increment DDA missed shots here<
			self.kill()
		if self.rect.y < HEIGHT:
			self.rect.y = self.rect.y + 8
		else:
			self.kill()
