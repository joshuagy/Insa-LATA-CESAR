import pygame
from Model import model, Plateau
from EventManager.EventManager import EventManager
from EventManager.allEvent import *
from Scenes.introScene import IntroScene


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
        self.game = None
    
    def notify(self, event):
        """
        Receive events posted to the message queue. 
        """

        if isinstance(event, InitializeEvent):
            self.initialize()
        elif isinstance(event, QuitEvent):
            # shut down the pygame graphics
            self.isinitialized = False
            pygame.quit()
        elif isinstance(event, TickEvent):
            if not self.isinitialized:
                return
            currentstate = self.model.state.peek()
            if currentstate == model.STATE_INTRO:
                self.renderIntro()
            if currentstate == model.STATE_MENU:
                self.renderMenu()
            if currentstate == model.STATE_PLAY:
                self.renderGame()
            self.clock.tick(30)
    
    def renderScene(self, scene):

        pygame.display.flip()
    def renderIntro(self) -> None:
        """
        Render the game intro.
        """
        self.screen.fill((255, 0, 0))
        somewords = self.smallfont.render(
                    'game intro', 
                    True, (0, 255, 0))
        self.screen.blit(somewords, (0, 0))
        pygame.display.flip()
        
    def renderMenu(self) -> None:
        """
        Render the game menu.
        """

        self.screen.fill((0, 255, 0))
        somewords = self.smallfont.render(
                    'game menu', 
                    True, (0, 0, 255))
        self.screen.blit(somewords, (0, 0))
        pygame.display.flip()
    
    def renderGame(self) -> None:
        """
        Render the game.
        """
        pygame.init() 
        pygame.mixer.init() # For sound
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        clock = pygame.time.Clock()
        self.game = Plateau.Plateau(screen, clock, "Plateau", self.screen.get_size()[0], self.screen.get_size()[1])

        while True:
            self.game.run()

    def initialize(self) -> None:
        """
        Set up the pygame graphical display and loads graphical resources.
        """

        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('Game')
        self.screen = pygame.display.set_mode((200, 200))
        self.clock = pygame.time.Clock()
        self.smallfont = pygame.font.Font(None, 40)
        self.isinitialized = True
