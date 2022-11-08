import eventManager
import model
import view
import controller

def run():
    evManager = eventManager.EventManager()
    gameModel = model.GameEngine(evManager)
    inputHandler = controller.InputHandler(evManager, gameModel)
    graphics = view.GraphicalView(evManager, gameModel)
    gameModel.run()

if __name__ == '__main__':
    run()
