# Platformer Project
import pygame as pg
import random
from settings import *
from sprite import *
from projectile import *
from os import path
import time

class Game:
	def __init__(self):
		# initialize game window, etc.
		pg.init()
		pg.mixer.init()
		self.death = 0
		# initial window settings
		self.screen = pg.display.set_mode((WIDTH, HEIGHT))
		pg.display.set_caption(TITLE)
		self.clock = pg.time.Clock()
		self.running = True
		self.font_name = pg.font.match_font(FONT_NAME)
		self.load_data()

	def load_data(self):
		#load DDA file and graphic/sound
		self.dir = path.dirname(__file__)
		img_dir = path.join(self.dir, 'img')
		with open(path.join(self.dir, DEATHs_FILE), 'r') as f:
			try:
				self.totaldeath = int(f.read())
			except:
				self.totaldeath = 0
		with open(path.join(self.dir, DEATH_FILE), 'r') as f:
			try:
				self.totaldeath = int(f.read())
			except:
				self.totaldeath = 0
		# Load Spritesheet image
		self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))
        # Streamlining the creation of platforms and scenery
	def make_platform(self, x, y, name, state):
		name = Platform(self, x, y, state)
		self.all_sprites.add(name)
		self.platforms.add(name)


	def make_set(self, x, y, name, state):
		name = Set(self, x, y, state)
		self.all_sprites.add(name)
		self.platforms.add(name)
		#self.set.add(name)

	def new(self):
		# Start new game
		self.all_sprites = pg.sprite.Group()
		self.platforms = pg.sprite.Group()
		self.set = pg.sprite.Group()
		self.player = Player(self)
		self.all_sprites.add(self.player)
		self.make_set(150, HEIGHT - 64, 21, 0)
		self.make_set(WIDTH - 150, HEIGHT - 64, 22, 0)
		self.make_platform(WIDTH / 2 + 200, HEIGHT * 3 /4, 5, 0)
		self.make_platform(WIDTH / 2 - 50, HEIGHT * 3 / 4, 11, 0)
		self.make_platform(WIDTH / 2 + 14, HEIGHT * 3 / 4, 12, 2)
		self.run() 


	def run(self):
		# Game loop
		self.playing = True
		while self.playing:
			self.clock.tick(FPS)
			self.events()
			self.update()
			self.draw()

	def update(self):
		# Game loop - Update
		self.all_sprites.update()
		# check if player hits a platform
		if self.player.vel.y > 0:
			hits = pg.sprite.spritecollide(self.player, self.platforms, False)
			if hits:
					self.player.pos.y = hits[0].rect.top + 1
					self.player.vel.y = 0

		# Checking if player is on scenery
		if self.player.vel.y > 0:
			hits = pg.sprite.spritecollide(self.player, self.set, False)
			if hits:
					self.player.pos.y = hits[0].rect.top + 1
					self.player.vel.y = 0


		# If player reaches right quarter
		if self.player.rect.right >= WIDTH / 1.2:
			self.player.pos.x -= max(abs(self.player.vel.x),6)
			for plat in self.platforms:
				plat.rect.x -= max(abs(self.player.vel.x),6)
				if plat.rect.right <= 0:
					plat.kill()
			for plat in self.set:
				plat.rect.x -= max(abs(self.player.vel.x),6)
				if plat.rect.right  <= 0:
					plat.kill()

		if self.player.rect.top > HEIGHT:
			self.death += 1
			self.playing = False


		# Stop player from going backwards
		if self.player.rect.left <= 0:
			self.player.vel.x = -2*self.player.vel.x

	def events(self):
		# Game loop - Events
		for event in pg.event.get():

			# for shutdown
			if event.type == pg.QUIT:
				if self.playing:
					self.playing = False
				self.running = False
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_w:
					self.player.jump()
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_SPACE:
					print(self.player.pos.x, self.player.pos.y)
					self.proj = playerProjectile(self)
					self.proj.fire(self.player.pos.x, self.player.pos.y)
					self.all_sprites.add(self.proj)

	def draw(self):
		#Game loop - draw
		self.screen.fill(CYAN)
		self.all_sprites.draw(self.screen)

		# Draw death variable to screen
		self.draw_text(str(self.death), 22, WHITE, WIDTH / 2, 15)

		# after all drawing, flip display
		pg.display.flip()

	def show_start_screen(self):
		# Game start screen
		self.intro_sprites = pg.sprite.Group()
		self.intro = IntroChar(self, [WIDTH / 4, HEIGHT / 2 + 75])
		self.intro_sprites.add(self.intro)
		self.intro_sprites.update()
		self.BackGround = StartBackground('img/bgimage.png', [0,0])
		self.screen.fill(WHITE)
		self.screen.blit(self.BackGround.image, self.BackGround.rect)
		self.screen.blit(self.intro.image, self.intro.rect)
		# For testing if DDA file works:
		#self.draw_text("Total Deaths: " + str(self.totaldeath), 22, WHITE, WIDTH / 2, 15)
		timer = 0
		pg.display.flip()
		self.wait_for_key()
		self.intro_sprites.update()


	def show_go_screen(self):
		self.screen.fill(BLACK)
		# Game over screen
		if not self.running:
			return
                # Increasing "Death Value (Total)"
		self.totaldeath += 1 
		with open(path.join(self.dir, DEATHs_FILE), 'w') as f:
			f.write(str(self.totaldeath))
		with open(path.join(self.dir, DEATH_FILE), 'w') as f:
			f.write(str(self.death))
		pg.display.flip()
		time.sleep(2)
		self.wait_for_key()
		

	def wait_for_key(self):
		# Used in menues		
		waiting = True
		while waiting:
			self.clock.tick(FPS)
			for event in pg.event.get():
				if event.type == pg.QUIT:
					waiting = False
					self.running = False
				if event.type == pg.KEYUP:
					waiting = False

	def draw_text(self, text, size, color, x, y):
		font = pg.font.Font(self.font_name, size)
		text_surface = font.render(text, True, color)
		text_rect = text_surface.get_rect()
		text_rect.midtop = (x, y)
		self.screen.blit(text_surface, text_rect)


g = Game()
g.show_start_screen()
while g.running:
	g.new()
	g.show_go_screen()


pg.quit()
