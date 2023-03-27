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
		elif currentstate == STATE_SAVE_SCENE:
			self.handleKeyboardEventsStateSaveScene(event)
		elif currentstate == STATE_JOIN_IP_SCENE:
			self.handleKeyboardEventsStateJoinIPScene(event)
		elif event.key == pygame.K_ESCAPE:
			self.evManager.Post(ExitEvent())

	def handleKeyboardEventsStateSaveScene(self, event):
		feedback = self.model.saveScene.handleKeyboardInput(event)
		self.evManager.Post(feedback)

	def handleKeyboardEventsStateJoinIPScene(self, event):
		feedback = self.model.menu.joinIPScene.handleKeyboardInput(event)
		self.evManager.Post(feedback)

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
			elif event.key == pygame.K_ESCAPE and self.model.actualGame.pause:
				self.model.pause_menu.pause = False
				self.model.actualGame.pause = False

		#if event.type == pygame.KEYDOWN:
		#	if event.key == pygame.K_2:
		#		if cell_size==30:
		#			self.zoomed=True
		#			x,y=pygame.mouse.get_pos()
		#			self.model.actualGame.camera.vect=pygame.Vector2(self.model.actualGame.camera.vect.x-x-200, self.model.actualGame.camera.vect.y-y)
		#			self.model.actualGame.camera.get_cell_size(60)
		#			self.model.actualGame.zoom(2,self.model.actualGame.zoomed)
		#			cell_size=60
		#			self.model.actualGame.zoomed=False

		#if event.type == pygame.KEYDOWN:
		#	if event.key == pygame.K_1:
		#		if cell_size==60:
		#			self.model.actualGame.zoomed=True
		#			self.model.actualGame.camera.vect = pygame.Vector2(-700,-100)
		#			cell_size=30
		#			self.model.actualGame.camera.get_cell_size(30)
		#			self.model.actualGame.zoom(0.5,self.model.actualGame.zoomed)
		#			self.model.actualGame.zoomed=False
		

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_c:
				self.model.actualGame.save_game("test.pickle")
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_v:
				self.model.actualGame.load_savefile("test.pickle")
		
		#Creative mode
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_KP0:
				self.model.actualGame.controls.setCurrentState("land")

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_KP1:
				self.model.actualGame.controls.setCurrentState("tree")
		
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_KP2:
				self.model.actualGame.controls.setCurrentState("rock")
		
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_KP3:
				self.model.actualGame.controls.setCurrentState("water")
