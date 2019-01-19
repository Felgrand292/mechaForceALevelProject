#sprite classes for platform game
import pygame as pg
from settings import *
vec = pg.math.Vector2
class Spritesheet:
	#For loading and parsing spritesheets
	def __init__(self, filename):
		self.spritesheet = pg.image.load(filename).convert()

	def get_image(self, x, y, width, height):
		  # grabs image out of spritesheet
		  image = pg.Surface((width, height))
		  image.blit(self.spritesheet, (0, 0), (x, y, width, height))
		  image = pg.transform.scale(image, (width * 4, height * 4))
		  return image

class Player(pg.sprite.Sprite):
	def __init__(self, game):
		pg.sprite.Sprite.__init__(self)
		self.game = game
		self.walking = False
		self.jumping = False
		self.current_frame = 0
		self.last_update = 0
		self.load_images()
		self.image = self.standing_frames[0]
		self.rect = self.image.get_rect()
		self.rect.center = (WIDTH / 2, HEIGHT / 2)
		self.pos = vec(WIDTH / 2, HEIGHT / 2)
		self.vel = vec(0, 0)
		self.acc = vec(0, 0)

	def load_images(self):
		# >> DO JUMPING ANIMATION <<

		self.standing_frames = [
			self.game.spritesheet.get_image(0, 87, 26, 21),
			self.game.spritesheet.get_image(0, 129, 26, 21),
		]
		self.jumping_frames = [
			self.game.spritesheet.get_image(0, 0, 26, 21),
			self.game.spritesheet.get_image(0, 21, 26, 19),
			self.game.spritesheet.get_image(0, 40, 26, 23),
			self.game.spritesheet.get_image(0, 63, 26, 24),
		]
		self.walking_right_frames = [
			self.game.spritesheet.get_image(0, 129, 26, 21),
			self.game.spritesheet.get_image(0, 171, 26, 20),
			self.game.spritesheet.get_image(0, 211, 26, 21),
			self.game.spritesheet.get_image(0, 253, 26, 20),
			self.game.spritesheet.get_image(0, 293, 26, 21),
			self.game.spritesheet.get_image(0, 335, 26, 20),
			self.game.spritesheet.get_image(0, 375, 26, 21),
			self.game.spritesheet.get_image(0, 417, 26, 20),
		]

		self.walking_left_frames = [
			self.game.spritesheet.get_image(0, 150, 26, 21),
			self.game.spritesheet.get_image(0, 191, 26, 20),
			self.game.spritesheet.get_image(0, 232, 26, 21),
			self.game.spritesheet.get_image(0, 273, 26, 20),
			self.game.spritesheet.get_image(0, 314, 26, 21),
			self.game.spritesheet.get_image(0, 355, 26, 20),
			self.game.spritesheet.get_image(0, 396, 26, 21),
			self.game.spritesheet.get_image(0, 437, 26, 20),
		]


		for frame in self.standing_frames:
			frame.set_colorkey(KEY)
		for frame in self.walking_right_frames:
			frame.set_colorkey(KEY)
		for frame in self.walking_left_frames:
			frame.set_colorkey(KEY)
	def jump(self):
		# jump only if standing on platform
		self.rect.y += 1
		# collision detection
		hits = pg.sprite.spritecollide(self, self.game.platforms, False)
		self.rect.y -= 1
		if hits:
			self.vel.y = -JUMP_HEIGHT
		hits = pg.sprite.spritecollide(self, self.game.set, False)
		self.rect.y -= 1
		if hits:
			self.vel.y = -JUMP_HEIGHT


	def update(self):
		self.animate()
		self.acc = vec(0, PLAYER_GRAV)
		keys = pg.key.get_pressed()
		if keys[pg.K_a]:
			self.acc.x = -PLAYER_ACC
		# key detection
		if keys[pg.K_d]:
			self.acc.x = PLAYER_ACC
		elif self.game.player.rect.right >= WIDTH / 1.2:
			self.acc.x = 0
		
		# Apply friction
		self.acc.x += self.vel.x * PLAYER_FRICTION
		# Equations of motion
		self.vel += self.acc
		if abs(self.vel.x) < 0.1:
			self.vel.x = 0
		self.pos += self.vel + 0.5 * self.acc


		# Wrap around sides
		#if self.pos.x > WIDTH:
		#	self.pos.x= 0
		#if self.pos.x < 0:
		#	self.pos.x = WIDTH

		self.rect.midbottom = self.pos

	def animate(self):
		now = pg.time.get_ticks()
		if self.vel.x !=0:
			self.walking = True
		else:
			self.walking = False
		if not self.jumping and not self.walking:
			if now - self.last_update > 250:
				self.last_update = now
				self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
				bottom = self.rect.bottom
				self.image = self.standing_frames[self.current_frame]
				self.rect = self.image.get_rect()
				self.rect.bottom = bottom

		if self.walking:
			if now - self.last_update > 100:
				self.last_update = now
				self.current_frame = (self.current_frame + 1) % len(self.walking_right_frames)
				bottom = self.rect.bottom
				if self.vel.x > 0:
					self.image = self.walking_right_frames[self.current_frame]

				else:
					self.image = self.walking_left_frames[self.current_frame]
				self.rect = self.image.get_rect()
				self.rect.bottom = bottom


class Platform(pg.sprite.Sprite):
	def __init__ (self, game, x, y, state):
		pg.sprite.Sprite.__init__(self)
		self.game = game
		self.images = [
				self.game.spritesheet.get_image(0, 1161, 32, 13),
				self.game.spritesheet.get_image(0, 1174, 32, 13),
				self.game.spritesheet.get_image(0, 1187, 32, 13)
				]
		self.image = self.images[state]
		#self.image.fill(BLACK)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

class Set(pg.sprite.Sprite):
	def __init__ (self, game, x, y, state):
		pg.sprite.Sprite.__init__(self)
		self.game = game
		self.images = [
				self.game.spritesheet.get_image(0, 1161, 32, 13),
				self.game.spritesheet.get_image(0, 1174, 32, 13),
				self.game.spritesheet.get_image(0, 1187, 32, 13)
				]
		self.image = self.images[state]
		#self.image.fill(BLACK)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

class StartBackground(pg.sprite.Sprite):
	def __init__(self, image_file, location):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.image.load(image_file)
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = location

class IntroChar(pg.sprite.Sprite):
	def __init__(self, game, location):
		pg.sprite.Sprite.__init__(self)
		self.game = game
		self.key = False
		self.current_frame = 0
		self.last_update = 0
		self.load_intro()
		self.image = self.intro_frames[0]
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = location
		#self.anim = True
		#while self.anim:
			#self.animation()

	def load_intro(self):
		self.intro_frames = [
			self.game.spritesheet.get_image(0, 457, 32, 32),
			self.game.spritesheet.get_image(0, 489, 32, 32),
			self.game.spritesheet.get_image(0, 521, 32, 32),
			self.game.spritesheet.get_image(0, 553, 32, 32),
			self.game.spritesheet.get_image(0, 585, 32, 32),
			self.game.spritesheet.get_image(0, 617, 32, 32),
			self.game.spritesheet.get_image(0, 649, 32, 32),
			self.game.spritesheet.get_image(0, 681, 32, 32),
			self.game.spritesheet.get_image(0, 713, 32, 32),
			self.game.spritesheet.get_image(0, 745, 32, 32),
			self.game.spritesheet.get_image(0, 777, 32, 32),
			self.game.spritesheet.get_image(0, 809, 32, 32),
			self.game.spritesheet.get_image(0, 841, 32, 32),
			self.game.spritesheet.get_image(0, 873, 32, 32),
			self.game.spritesheet.get_image(0, 905, 32, 32),
			self.game.spritesheet.get_image(0, 937, 32, 32),
			self.game.spritesheet.get_image(0, 969, 32, 32),
			self.game.spritesheet.get_image(0, 1001, 32, 32),
			self.game.spritesheet.get_image(0, 1033, 32, 32),
			self.game.spritesheet.get_image(0, 1065, 32, 32),
			self.game.spritesheet.get_image(0, 1097, 32, 32),
			self.game.spritesheet.get_image(0, 1129, 32, 32),
		]

		for frame in self.intro_frames:
			frame.set_colorkey(KEY)

	def update(self):
		#self.game = game
		#self.anim = True
		#self.frames = 0

		now = pg.time.get_ticks()
		if now - self.last_update > 100:
			self.last_update = now
			self.current_frame = (self.current_frame + 1) % len(self.intro_frames)
			self.image = self.intro_frames[self.current_frame]


