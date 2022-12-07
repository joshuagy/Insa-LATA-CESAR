import pygame
from Model.constants import *
from EventManager.Event import Event
from EventManager.allEvent import StateChangeEvent, TickEvent, QuitEvent

cell_size = 30

class MouseInputHandler:
    """
    Handles mouse input.
    """
    def __init__(self, evManager, model) -> None:
        self.evManager = evManager
        self.model = model
        self.clicked = False
        self.initialMouseCoordinate = False
        self.finalClickCoordinate = False

    def handleInput(self, event: Event) -> None:
        """
        Receive events posted to the message queue. 
        """

        if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                        self.clicked = True
                        self.initialMouseCoordinate = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONUP:
                self.finalClickCoordinate = pygame.mouse.get_pos()
                if(self.clicked):
                        # get current state
                        currentstate = self.model.state.peek()
                        if currentstate == STATE_MENU:
                                self.handleMouseEventsStateMenu(event)
                        if currentstate == STATE_PLAY:
                                self.handleMouseEventsStatePlay(event)
                if event.button == 1:
                        self.clicked = False

    def handleMouseEventsStateMenu(self, event):
        """
        Handles menu mouse events.
        """

        mousePos = event.pos
        feedBack = self.model.menu.handleInput(mousePos)
        print(feedBack)
        self.evManager.Post(feedBack)

    def handleMouseEventsStatePlay(self, event):
        """
        Handles game mouse events
        """
        pass