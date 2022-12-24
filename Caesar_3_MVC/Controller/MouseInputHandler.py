import pygame
from Model.constants import *
from Model.control_panel import *
from EventManager.Event import Event
from EventManager.allEvent import StateChangeEvent, TickEvent, QuitEvent
from Model.Plateau import Plateau, cell_size

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
                if(self.clicked):
                        # get current state
                        self.finalClickCoordinate = pygame.mouse.get_pos()
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
        #Handle the buttons of the control panel
        overlays_button.handle_event(event)
        hide_control_panel_button.handle_event(event)
        display_control_panel_button.handle_event(event)
        advisors_button.handle_event(event)
        empire_map_button.handle_event(event)
        assignement_button.handle_event(event)
        compass_button.handle_event(event)
        arrow_rotate_counterclockwise.handle_event(event)
        arrow_rotate_clockwise.handle_event(event)
        build_housing_button.handle_event(event)
        clear_land_button.handle_event(event)
        build_roads_button.handle_event(event)
        water_related_structures.handle_event(event)
        health_related_structures.handle_event(event)
        religious_structures.handle_event(event)
        education_structures.handle_event(event)
        entertainment_structures.handle_event(event)
        administration_or_government_structures.handle_event(event)
        engineering_structures.handle_event(event)
        security_structures.handle_event(event)
        industrial_structures.handle_event(event)
        undo_button.handle_event(event)
        message_view_button.handle_event(event)
        see_recent_troubles_button.handle_event(event)

        #Pelle
        if self.clicked:
            x, y = self.initialMouseCoordinate
            world_x = x - self.model.actualGame.camera.vect.x - self.model.actualGame.surface_cells.get_width() / 2
            world_y = y - self.model.actualGame.camera.vect.y

            cart_y = (2 * world_y - world_x) / 2
            cart_x = cart_y + world_x
            grid_x1 = int(cart_x // cell_size)
            grid_y1 = int(cart_y // cell_size)

            x, y = event.pos
            world_x = x - self.model.actualGame.camera.vect.x - self.model.actualGame.surface_cells.get_width() / 2
            world_y = y - self.model.actualGame.camera.vect.y

            cart_y = (2 * world_y - world_x) / 2
            cart_x = cart_y + world_x
            grid_x2 = int(cart_x // cell_size)
            grid_y2 = int(cart_y // cell_size)
        
            if grid_x1 <0:
                grid_x1 = 0
            if grid_x2 <0:
                grid_x2 = 0
            if grid_y1 <0:
                grid_y1 = 0
            if grid_y2 <0:
                grid_y2 = 0

            if grid_x1 > self.model.actualGame.nbr_cell_x-1:
                grid_x1 = self.model.actualGame.nbr_cell_x-1
            if grid_x2 > self.model.actualGame.nbr_cell_x-1:
                grid_x2 = self.model.actualGame.nbr_cell_x-1
            if grid_y1 > self.model.actualGame.nbr_cell_y-1:
                grid_y1 = self.model.actualGame.nbr_cell_y-1
            if grid_y2 > self.model.actualGame.nbr_cell_y-1:
                grid_y2 = self.model.actualGame.nbr_cell_y-1

            if grid_x1 > grid_x2:
                temp = grid_x1
                grid_x1 = grid_x2
                grid_x2 = temp

            if grid_y1 > grid_y2:
                temp = grid_y1
                grid_y1 = grid_y2
                grid_y2 = temp

            for xi in range(grid_x1, grid_x2+1):
                for yi in range(grid_y1, grid_y2+1):
                        self.model.actualGame.map[xi][yi].sprite = "land1"
                        self.model.actualGame.map[xi][yi].collision = 0
            self.model.actualGame.collision_matrix = self.model.actualGame.create_collision_matrix()
        
                
            