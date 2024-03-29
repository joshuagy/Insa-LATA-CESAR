from EventManager.allEvent import *
from Model.constants import *
from Model.Music import *
from Model.SoundMixer import *

class GameEngine(object):
	"""
	Tracks the game state.
	"""

	def __init__(self, evManager):
		"""
		evManager (EventManager): Allows posting messages to the event queue.
		
		Attributes:
		running (bool): True while the en:ine is online. Changed via QuitEvent().
		"""
		
		self.evManager = evManager
		evManager.RegisterListener(self)
		self.running = False
		self.state = StateMachine()

		self.musicMixer = Music()
		self.musicMixer.play()

		self.soundMixer = SoundMixer()

		self.introScene = None
		self.menu = None
		self.actualGame = None
	
	def notify(self, event):
		"""
		Called by an event in the message queue. 
		"""

		if isinstance(event, ExitEvent):
				self.running = False
		if isinstance(event, StateChangeEvent):
				# pop request
				if not event.state:
						# false if no more states are left
						if not self.state.pop():
								self.evManager.Post(ExitEvent())
				else:
						# push a new state on the stack
						self.state.push(event.state)
						self.musicMixer.changeMusic(event.state)
        
	def run(self):
		"""
		Starts the game engine loop.

		This pumps a Tick event into the message queue for each loop.
		The loop ends when this object hears a QuitEvent in notify(). 
		"""
		self.running = True
		self.evManager.Post(InitializeEvent())

		# initialize initial state as STATE_INTRO_SCENE
		self.state.push(STATE_INTRO_SCENE)
		
		while self.running:
				newTick = TickEvent()
				self.evManager.Post(newTick)
		print("a")
		if self.actualGame.multiplayer:
			self.actualGame.multiplayer.delete()



class StateMachine(object):
	"""
	Manages a stack based state machine.
	peek(), pop() and push() perform as traditionally expected.
	peeking and popping an empty stack returns None.
	"""

	def __init__ (self):
		self.statestack = []

	def peek(self):
		"""
		Returns the current state without altering the stack.
		Returns None if the stack is empty.
		"""
		try:
				return self.statestack[-1]
		except IndexError:
				# empty stack
				return None

	def pop(self):
		"""
		Returns the current state and remove it from the stack.
		Returns None if the stack is empty.
		"""
		try:
				self.statestack.pop()
				return len(self.statestack) > 0
		except IndexError:
				# empty stack
				return None

	def push(self, state):
		"""
		Push a new state onto the stack.
		Returns the pushed value.
		"""
		self.statestack.append(state)
		return state