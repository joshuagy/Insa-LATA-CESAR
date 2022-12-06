from Controller.MouseInputHandler import MouseInputHandler
from Controller.KeyboardInputHandler import KeyboardInputHandler

class GameController:
    def __init__(self, evManager, model):
        self.evManager = evManager
        evManager.RegisterListener(self)
        self.model = model

    def initGame():
        pass