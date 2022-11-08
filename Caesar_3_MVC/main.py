from EventManager import eventManager
from Model import model
from View import view
from Controller import controller

if __name__ == '__main__':
    evManager = eventManager.EventManager()
    gameModel = model.GameEngine(evManager)
    inputHandler = controller.InputHandler(evManager, gameModel)
    graphics = view.GraphicalView(evManager, gameModel)
    gameModel.run()