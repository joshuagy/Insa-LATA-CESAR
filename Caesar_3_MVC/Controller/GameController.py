from Controller.MouseInputHandler import MouseInputHandler
from Controller.KeyboardInputHandler import KeyboardInputHandler

class GameController:
    def __init__(self, evManager, model):
        self.evManager = evManager
        evManager.RegisterListener(self)
        self.model = model
        self.mouseInputHandler = MouseInputHandler(self, evManager, model)
        self.keyboardInputHandler = KeyboardInputHandler(self, evManager, model)