from EventManager.Event import Event
from EventManager.allEvent import QuitEvent, TickEvent, QuitEvent
import pygame

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

		if event.key == pygame.K_ESCAPE:
				self.evManager.Post(QuitEvent())
