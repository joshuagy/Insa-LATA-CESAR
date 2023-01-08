from EventManager.Event import Event
from EventManager.allEvent import *
from Model.constants import *
import pygame
import sys

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
		if currentstate == STATE_INTRO_SCENE:
			self.handleKeyboardEventsStateIntroScene(event)
		elif currentstate == STATE_PLAY:
			self.handleKeyboardEventsStatePlay(event)

		elif event.key == pygame.K_ESCAPE:
			self.evManager.Post(ExitEvent())

	def handleKeyboardEventsStateIntroScene(self, event):
		self.model.introScene.handleKeyboardInput(event)

	def handleKeyboardEventsStatePlay(self, event):
		"""
		Handles game keyboard events
		"""
		global cell_size
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE and not self.model.actualGame.pause:
				self.model.pause_menu.pause = True
				self.model.actualGame.pause = True
			elif event.key == pygame.K_ESCAPE and self.model.actualGame.pause :
				self.model.pause_menu.pause = False
				self.model.actualGame.pause = False



