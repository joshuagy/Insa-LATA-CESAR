from EventManager.EventManager import EventManager
from Model import model
from View import view
from Controller.InputController import InputController 

if __name__ == '__main__':
    evManager = EventManager()
    gameModel = model.GameEngine(evManager)
    inputHandler = InputController(evManager, gameModel)
    graphics = view.GraphicalView(evManager, gameModel)
    gameModel.run()
