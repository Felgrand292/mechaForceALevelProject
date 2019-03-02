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
		self.font_name = pg.font.match_font(FONT_NAME)							#Sets in-game font
		self.load_data()

	def load_data(self):
		#load DDA file and graphic/sound
		self.dir = path.dirname(__file__)
		img_dir = path.join(self.dir, 'img')									#Opens image file for use in sprites
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
		self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))			#Imports image as a spritesheet
		

	def make_platform(self, x, y, name, state):									#Function used for making the platform sprites
		name = Platform(self, x, y, state)
		self.all_sprites.add(name)
		self.platforms.add(name)


	def make_set(self, x, y, name, state):										#Function used for making the scenery sprites
		name = Set(self, x, y, state)
		self.all_sprites.add(name)
		self.set.add(name)

	def make_setsky(self, x, y, name, state):									#Function used for making the ceiling scenery sprites
		name = Set(self, x, y, state)
		self.all_sprites.add(name)
		self.setsky.add(name)

	def make_success(self, x, y, name):											#Function used to make the sprite that registers the completion of a level
		name = Complete(self, x, y)
		self.all_sprites.add(name)
		self.complete.add(name)

	def new(self):
        #def new(self, levelNum):       Handed from menu input function
		# Start new game 														#Calls the level function, creates groups for sprites, resets gunState to 0 and runs the level
                
		self.all_sprites = pg.sprite.Group()
		self.platforms = pg.sprite.Group()
		self.set = pg.sprite.Group()
		self.setsky = pg.sprite.Group()
		self.complete = pg.sprite.Group()
		levelNum = "4"															#To test for loading levels without menu, adjust value here
		self.loadLevel(levelNum)
		self.backdrop = pg.image.load('img/back'+levelNum+'.png').convert()
		self.backcoordx = 0
		self.gunState = 0														#Used to track what weapon the player is using
		self.run()

	def loadLevel(self, levelNum):
                self.level = []													# Loads level from a given number of levels, including platforms, scenery, player and enemies
                self.world = []
                x = 0
                y = 0
                self.success = 0
                self.levelload = open("levels/level"+levelNum+".txt", "r")     	#Opens tilemap text file
                print("CHECKARRAY")
                for l in self.levelload:                               			#Converts text file to 2D array
                    self.level.append(l)
                    #print("CHECKAPPEND")
                for row in self.level:
                	#print("CHECKROW")
                	for col in row:
                		#print("CHECKCOL")
                		if col == "L":                           				#Forms sprites for unclimbable scenery
                			sett = self.make_setsky(x, y, 0, 0)
                			self.world.append(sett)
                			print("CHECKS")
                		if col == "A":                          				#Forms sprites for alternate scenery
                			sett = self.make_setsky(x, y, 0, 0)
                			self.world.append(sett)
                			print("CHECKS")
                		if col == "P":                           				#Forms sprites for platforms
                			plat = self.make_platform(x, y, 0, 0)
                			self.world.append(plat)
                			#print("CHECKP")
                		if col == "S":                           				#Forms sprites for scenery
                			sett = self.make_set(x, y, 0, 0)
                			self.world.append(sett)
                			print("CHECKS")
                		if col == "B":                           				#Forms sprites for bedrock textures
                			sett = self.make_set(x, y, 0, 0)
                			self.world.append(sett)
                			#print("CHECKB")
                		if col == "U":                           				#Forms sprites for players
                			self.player = Player(self, x, y)
                			self.all_sprites.add(self.player)
                			print("CHECKU")
                		if col == "C":                           				#Forms sprites for victory detection
                			success = self.make_success(x, y, 0)
                			self.world.append(success)
                			print("CHECKC")
                		"""if col == "W":                        				#Forms sprites for walking enemy		(Commented out for later implementation, in enemy iteration)
                			self.walker = Walker(self, x, y)
                			self.all_sprites.add(self.walker)
                		if col == "G":                           				#Forms sprites for shooting enemy		(Commented out for later implementation, in enemy iteration)
                			self.shooter = Shooter(self, x, y)
                			self.all_sprites.add(self.shooter)"""
                		x += 64
                	y += 64
                	x = 0
                
                                        

	def run(self):
		# Game loop																Game loops continously updates all sprites, as well as checking for events and drawing them to the display
		self.playing = True
		while self.playing:
			self.clock.tick(FPS)
			self.events()
			self.update()
			self.draw()

	def update(self):
		# Game loop - update 													Updates all sprites and checks for specific conditions, like if the player is on a platform, for example
		self.all_sprites.update()
		# check if player hits a platform
		if self.player.vel.y > 0:
			hits = pg.sprite.spritecollide(self.player, self.platforms, False)
			if hits:
					self.player.pos.y = hits[0].rect.top + 1
					self.player.vel.y = 0

		# Checking if player is on scenery (If so, keep them on that y coordinate)
		if self.player.vel.y > 0:
			hits = pg.sprite.spritecollide(self.player, self.set, False)
			if hits:
					self.player.pos.y = hits[0].rect.top + 1
					self.player.vel.y = 0


		# If player reaches right quarter (If so, move all sprites except player to scroll level)
		if self.player.rect.right >= WIDTH / 1.2:
			self.player.pos.x -= max(abs(self.player.vel.x),6)					#Nulifies the players current movement so that the player runs in place, while the level moves.
			self.backcoordx -= 0.7*max(abs(self.player.vel.x),6)					
			for plat in self.platforms:
				plat.rect.x -= max(abs(self.player.vel.x),6)					#Moves all platforms
				if plat.rect.right <= 0:										#Kills platforms if they go off screen to the left
					plat.kill()
			for plat in self.set:
				plat.rect.x -= max(abs(self.player.vel.x),6)					#Moves all scenery
				if plat.rect.right  <= 0:										#Kills scenery sprites that go off screen to the left
					plat.kill()
			for plat in self.setsky:
				plat.rect.x -= max(abs(self.player.vel.x),6)					#Moves all ceiling scenery
				if plat.rect.right  <= 0:										#Kills all ceiling scenery sprites that go of screen to the left
					plat.kill()
			for plat in self.complete:
				plat.rect.x -= max(abs(self.player.vel.x),6)					#Moves all ceiling scenery
				if plat.rect.right  <= 0:										#Kills all ceiling scenery sprites that go of screen to the left
					plat.kill()

		if self.player.rect.top > HEIGHT:										#Kills player if they fall off the level
			self.death += 1
			self.playing = False


		# Stop player from going backwards
		if self.player.rect.left <= 0:
			self.player.vel.x = -2*self.player.vel.x							#Inverts players velocity to stop them going backwards at the left edge of the screen
		hits = pg.sprite.spritecollide(self.player, self.setsky, False)			#Inverts players x and y velocity to stop them from clipping into the ceilings (setsky)
		if hits:
			self.player.vel.y = -1*self.player.vel.y
			self.player.vel.x = -1.5*self.player.vel.x
		if self.success == 1:													#Added to increment recogition of completion of a level
			#Add SQLite cos here to increment current level record
			return
	def events(self):
		# Game loop - events 													Handles PyGames range of possible events
		for event in pg.event.get():

			# for shutdown
			if event.type == pg.QUIT:											#If red cross on window is clicked, close game
				if self.playing:
					self.playing = False
				self.running = False
			if event.type == pg.KEYDOWN:										#If "w" is pressed, jump
				if event.key == pg.K_w:
					self.player.jump()
			if event.type == pg.KEYDOWN:										#If "space" is pressed, fire the weapon that matches the gunState of the player
				if event.key == pg.K_SPACE:
					if self.gunState == 1:										#Fires all 4 projectiles for the "+" shaped attack
						self.plusProjL = plusProjectilel(self)
						self.all_sprites.add(self.plusProjL)
						self.plusProjL.fire(self.player.pos.x, self.player.pos.y)
						self.plusProjR = plusProjectiler(self)
						self.all_sprites.add(self.plusProjR)
						self.plusProjR.fire(self.player.pos.x, self.player.pos.y)
						self.plusProjU = plusProjectileu(self)
						self.all_sprites.add(self.plusProjU)
						self.plusProjU.fire(self.player.pos.x, self.player.pos.y)
						self.plusProjD = plusProjectiled(self)
						self.all_sprites.add(self.plusProjD)
						self.plusProjD.fire(self.player.pos.x, self.player.pos.y)
					if self.gunState == 0:										#Fires the normal projectile attack
						print(self.player.pos.x, self.player.pos.y)
						self.proj = playerProjectile(self)
						self.proj.fire(self.player.pos.x, self.player.pos.y)
						self.all_sprites.add(self.proj)
			#Shifting gun states for attacks									#Shifts gunState allowing the player to switch weapons
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_UP:
					self.gunState = self.gunState + 1
					print(self.gunState)
					if self.gunState == 3:
						self.gunState = 0
						print(self.gunState)
					if self.gunState == -1:
						self.gunState = 2
						print(self.gunState)
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_DOWN:
					self.gunState = self.gunState - 1
					if self.gunState == 3:
						self.gunState = 0
					if self.gunState == -1:
						self.gunState = 2





	def draw(self):
		#Game loop - Draw 														#Draws all sprites and graphics to the display
		self.rel_backcoordx = self.backcoordx % self.backdrop.get_rect().width	#Creates and draws repeated moving background slower than scenery to give perspective.
		
		self.screen.blit(self.backdrop, (self.rel_backcoordx - self.backdrop.get_rect().width, 0))
		if self.rel_backcoordx < WIDTH:
			self.screen.blit(self.backdrop, (self.rel_backcoordx, 0))
		self.all_sprites.draw(self.screen)

		# Draw death variable to screen
		self.draw_text(str(self.death), 22, WHITE, WIDTH / 2, 15)

		# after all drawing, flip display
		pg.display.flip()

	def show_start_screen(self):
		# Game start screen 													#Shows the game start screen that features the logo of the game
		self.intro_sprites = pg.sprite.Group()
		self.intro = IntroChar(self, [WIDTH / 4, HEIGHT / 2 + 75])
		self.intro_sprites.add(self.intro)
		self.BackGround = StartBackground('img/bgimage.png', [0,0])
		self.screen.fill(WHITE)
		self.introRun()															#Runs the introduction animation
		self.intro.kill()														#Removes all introduction sprites to load levels
		pg.display.flip()
		self.wait_for_key()														#Waits for player to press any key before moving on
		self.running = True 													#Starts the game

	def introRun(self):
		self.startup = True
		while self.startup:
			self.clock.tick(15)
			for event in pg.event.get():
				if event.type == pg.QUIT:											#If red cross on window is clicked, close game
					pg.quit()
			self.intro_sprites.update()
			self.screen.blit(self.BackGround.image, self.BackGround.rect)
			self.intro_sprites.draw(self.screen)
			pg.display.flip()
		


	def show_go_screen(self):
		self.screen.fill(BLACK)
		# Game over screen
		if not self.running:
			return

		self.totaldeath += 1 
		with open(path.join(self.dir, DEATHs_FILE), 'w') as f:
                        #f.write(str(self.totaldeath + self.levelNum))
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

        #def menu(self)
                #>Used to load menu after start screen before level us loaded/Used and level select<
                #Up^ Downv arrows used to change scene
                #Enter used to select, then gives levelNum to "g.new()"
                #Can I just put "g.new()" in here to pass variable?


g = Game()
g.show_start_screen()
#g.menu()				>>CREATE A SECOND GAME LOOP LIKE START SCREEN TO MAKE MENU WORK<<
while g.running:
	g.new()
	g.show_go_screen()


pg.quit()
