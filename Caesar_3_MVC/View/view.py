import pygame
from Model.Menu import Menu 
from Model.IntroScene import IntroScene 
from Model.Plateau import Plateau
from Model.Walker import *
from EventManager.EventManager import EventManager
from EventManager.allEvent import *
from Model.constants import *
from Model.MiniMap import MiniMap
from Model.Menu_pause import *

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
            exit()
        elif isinstance(event, TickEvent):
            if not self.isinitialized:
                return
            currentstate = self.model.state.peek()
            if currentstate == STATE_INTRO_SCENE:
                self.renderIntroScene();
            elif currentstate == STATE_MENU:
                self.renderMenu()
            elif currentstate == STATE_PLAY:
                self.renderGame()
            self.clock.tick(60)
            print(self.clock.get_fps())
            #print("FPS:", int(self.clock.get_fps()))

    
    def renderIntroScene(self) -> None:
        """
        Render the intro scene.
        """
        
        self.model.introScene.render()
        pygame.display.flip()

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
        if self.model.actualGame.restart:
            self.initialize()
        self.model.actualGame.update()
        self.model.actualGame.draw()
        self.model.mini_map.draw_position(self.model.actualGame.screen, self.model.actualGame.camera,self.model.actualGame.map,self.model.actualGame.nbr_cell_x,self.model.actualGame.nbr_cell_y,self.model.actualGame.image)
        self.model.pause_menu.draw_pause_menu()
        self.model.actualGame.restart=False

        pygame.display.flip()



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
        self.model.introScene = IntroScene(self.screen)
        self.model.menu = Menu(self.screen)
        self.model.actualGame = Plateau(self.screen, self.clock, "Plateau", self.screen.get_size()[0], self.screen.get_size()[1])
        self.model.mini_map = MiniMap(self.screen.get_width(), self.screen.get_height(), 40 * cell_size * 2, 40 * cell_size + 2 * cell_size)
        self.model.pause_menu=Pausemenu(self.screen.get_width(),self.screen.get_height(),self.screen)

        #Création de walkers
        #for _ in range(1) : Immigrant(self.model.actualGame.map[19][38], self.model.actualGame, self.model.actualGame.map[19][20])