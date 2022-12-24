import pygame
from Model.Menu import Menu 
from Model.Plateau import Plateau
from Model.Walker import Walker
from EventManager.EventManager import EventManager
from EventManager.allEvent import *
from Model.constants import *

class GraphicalView(object):
    """
    Draws the model state onto the screen.
    """

    def __init__(self, evManager, model) -> None:
        """
        evManager (EventManager): Allows posting messages to the event queue.
        model (GameEngine): a strong reference to the game Model.
                
        Attributes:
        isinitialized (bool): pygame is ready to draw.
        screen (pygame.Surface): the screen surface.
        clock (pygame.time.Clock): keeps the fps constant.
        smallfont (pygame.Font): a small font.
        """
        
        self.evManager = evManager
        evManager.RegisterListener(self)
        self.model = model
        self.isinitialized = False
        self.screen = None
        self.clock = None
        self.smallfont = None

    def notify(self, event):
        """
        Receive events posted to the message queue. 
        """

        if isinstance(event, InitializeEvent):
            self.initialize()
        elif isinstance(event, ExitEvent):
            # shut down the pygame graphics
            self.isinitialized = False
            pygame.quit()
        elif isinstance(event, TickEvent):
            if not self.isinitialized:
                return
            currentstate = self.model.state.peek()
            if currentstate == STATE_MENU:
                self.renderMenu()
            if currentstate == STATE_PLAY:
                self.renderGame()
            self.clock.tick(30)

        
    def renderMenu(self) -> None:
        """
        Render the game menu.
        """

        self.model.menu.render()
        pygame.display.flip()
    
    def renderGame(self) -> None:
        """
        Render the game.
        """
        self.model.actualGame.update()
        self.model.actualGame.draw()


    def initialize(self) -> None:
        """
        Set up the pygame graphical display and loads graphical resources.
        """

        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('Game')
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.smallfont = pygame.font.Font(None, 40)
        self.isinitialized = True
        self.model.menu = Menu(self.screen)
        self.model.actualGame = Plateau(self.screen, self.clock, "Plateau", self.screen.get_size()[0], self.screen.get_size()[1])

        #Création de walkers
        Walker(self.model.actualGame.map[19][20], self.model.actualGame)