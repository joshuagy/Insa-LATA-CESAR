from EventManager.Event import Event
from EventManager.allEvent import QuitEvent, TickEvent, QuitEvent
from Model.model import STATE_ABOUT, STATE_HELP, STATE_INTRO, STATE_MENU, STATE_PLAY
import pygame
import sys

cell_size = 30

class KeyboardInputHandler:
	"""
	Handles keyboard input.
	"""
	def __init__(self, evManager, model) -> None:
		self.evManager = evManager
		self.model = model

	def handleInput(self, event: Event) -> None:
		"""
		Receive events posted to the message queue. 
		"""
		currentstate = self.model.state.peek()
		if currentstate == STATE_PLAY:
			self.handleKeyboardEventsStatePlay(event)

		elif event.key == pygame.K_ESCAPE:
			self.evManager.Post(QuitEvent())

	def handleKeyboardEventsStatePlay(self, event):
		"""
		Handles game keyboard events
		"""
		global cell_size
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()


		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_2:
				if cell_size==30:
					self.zoomed=True
					x,y=pygame.mouse.get_pos()
					self.model.actualGame.camera.vect=pygame.Vector2(self.model.actualGame.camera.vect.x-x-200, self.model.actualGame.camera.vect.y-y)
					self.model.actualGame.camera.get_cell_size(60)
					self.model.actualGame.zoom(2,self.model.actualGame.zoomed)
					cell_size=60
					self.model.actualGame.zoomed=False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_1:
				if cell_size==60:
					self.model.actualGame.zoomed=True
					self.model.actualGame.camera.vect = pygame.Vector2(-700,-100)
					cell_size=30
					self.model.actualGame.camera.get_cell_size(30)
					self.model.actualGame.zoom(0.5,self.model.actualGame.zoomed)
					self.model.actualGame.zoomed=False