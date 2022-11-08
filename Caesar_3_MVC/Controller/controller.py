import pygame
from Model import model
from EventManager.eventManager import *


class InputHandler: 
	def __init__(self, evManager, model):
		self.evManager = evManager
		evManager.RegisterListener(self)
		self.model = model

		self.mouseInputHandler = MouseInputHandler(self)
		self.keyboardInputHandler = KeyboardInputHandler(self)

	def notify(self, event: Event) -> None:
		"""
		Receive events posted to the message queue. 
		Handles only TickEvent events.
		"""

		if isinstance(event, TickEvent):
				# Called for each game tick. We check our mouse inputs here.
				for event in pygame.event.get():
						if event.type == pygame.QUIT:
								self.evManager.Post(QuitEvent())
						if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
								self.mouseInputHandler.handleInput(event)
						if event.type == pygame.KEYDOWN:
								self.keyboardInputHandler.handleInput(event)

class MouseInputHandler:
	"""
	Handles mouse input.
	"""
	def __init__(self, InputHandler: InputHandler) -> None:
		self.inputHandler = InputHandler
		self.evManager = self.inputHandler.evManager
		self.model = self.inputHandler.model

		self.clicked = False

	def handleInput(self, event: Event) -> None:
		"""
		Receive events posted to the message queue. 
		"""

		if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1: 
						self.clicked = True
		if event.type == pygame.MOUSEBUTTONUP:
				if(self.clicked):
						# get current state
						currentstate = self.model.state.peek()
						if currentstate == model.STATE_INTRO:
								self.handleMouseEventsStateIntro(event)
						if currentstate == model.STATE_MENU:
								self.handleMouseEventsStateMenu(event)

				if event.button == 1:
						self.clicked = False

	def handleMouseEventsStateIntro(self, event):
		"""
		Handles intro mouse events.
		"""
		# left click launchs menu
		self.evManager.Post(StateChangeEvent(model.STATE_MENU))

	def handleMouseEventsStateMenu(self, event):
		"""
		Handles menu mouse events.
		"""
		# left click exits
		self.evManager.Post(StateChangeEvent(model.STATE_PLAY))

class KeyboardInputHandler:
	"""
	Handles keyboard input.
	"""
	def __init__(self, InputHandler: InputHandler) -> None:
		self.inputHandler = InputHandler
		self.evManager = self.inputHandler.evManager
		self.model = self.inputHandler.model

	def handleInput(self, event: Event) -> None:
		"""
		Receive events posted to the message queue. 
		"""

		if event.key == pygame.K_ESCAPE:
				self.evManager.Post(QuitEvent())