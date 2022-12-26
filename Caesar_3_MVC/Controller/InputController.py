import pygame
from Controller.MouseInputHandler import MouseInputHandler
from Controller.KeyboardInputHandler import KeyboardInputHandler
from EventManager.Event import Event
from EventManager.allEvent import *

class InputController: 
	def __init__(self, evManager, model):
		self.evManager = evManager
		evManager.RegisterListener(self)
		self.model = model

		self.mouseInputHandler = MouseInputHandler(evManager, model)
		self.keyboardInputHandler = KeyboardInputHandler(evManager, model)

	def notify(self, event: Event) -> None:
		"""
		Receive events posted to the message queue. 
		Handles only TickEvent events.
		"""

		if isinstance(event, TickEvent):
				# Called for each game tick. We check our mouse inputs here.
				for event in pygame.event.get():
						if event.type == pygame.QUIT:
								self.evManager.Post(ExitEvent())
						if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
								self.mouseInputHandler.handleInput(event)
						if event.type == pygame.KEYDOWN:
								self.keyboardInputHandler.handleInput(event)
						self.mouseInputHandler.checkEveryButton(event)
							