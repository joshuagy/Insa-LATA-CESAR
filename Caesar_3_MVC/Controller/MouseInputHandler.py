import pygame
from Model.constants import *
from Model.control_panel import *
from EventManager.Event import Event
from EventManager.allEvent import StateChangeEvent, TickEvent, QuitEvent
from Model.Plateau import Plateau, cell_size
from Model.Route import Route
from Model.Buildings.Building import *
from Model.Buildings.House import *
from Model.Buildings.WorkBuilding import *

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
        elif event.type == pygame.MOUSEBUTTONUP:
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
                        self.initialMouseCoordinate = None
        #  Preview clear land
        elif event.type == pygame.MOUSEMOTION:
            temp = pygame.mouse.get_pos()
            if temp != self.initialMouseCoordinate and self.clicked:
                self.handleMouseMouvement(event)

    def handleMouseEventsStateMenu(self, event):
        """
        Handles menu mouse events.
        """

        mousePos = event.pos
        feedBack = self.model.menu.handleInput(mousePos)
        print(feedBack)
        self.evManager.Post(feedBack)

    def checkEveryButton(self, event):
        """
            Check if a button has been pressed
        """
        
        #Handle the buttons of the control panel
        for button in list_of_buttons:
            button.handle_event(event)

    def handleMouseEventsStatePlay(self, event):
        """
        Handles game mouse events
        """
        #Pelle
        if clear_land_button.clicked and not clear_land_button.rect.collidepoint(event.pos):
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
                        if self.model.actualGame.map[xi][yi].sprite not in list_of_undestructible:
                            self.model.actualGame.map[xi][yi].sprite = "land1"
                            self.model.actualGame.map[xi][yi].collision = 0
                            if self.model.actualGame.map[xi][yi].road :
                                self.model.actualGame.map[xi][yi].road.delete()
                                # Informe toutes les cases adjacentes qu'elles ne sont plus connectées à la route 
                                # (Sauf bien sûr si elles sont connectées à une autre route)
                                for xa in range(xi-1,xi+1,1):
                                    for ya in range(yi-1, yi+1, 1):
                                        self.model.actualGame.map[xa][ya].changeConnectedToRoad(-1)
                                      
                            if self.model.actualGame.map[xi][yi].building :
                              self.model.actualGame.map[xi][yi].building.delete()
                           
                            if self.model.actualGame.map[xi][yi].building :
                                self.model.actualGame.map[xi][yi].building.delete()

                            
            self.model.actualGame.collision_matrix = self.model.actualGame.create_collision_matrix()
            for xi in range(len(self.model.actualGame.previewMap)):
                for yi in range(len(self.model.actualGame.previewMap[0])):
                        self.model.actualGame.previewMap[xi][yi] = None
        
                
        #Routes
        if build_roads_button.clicked and not build_roads_button.rect.collidepoint(event.pos):
        
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

            pattern = 0
            if grid_x1 > grid_x2:
                pattern += 1

            if grid_y1 > grid_y2:
                pattern += 2

            if self.model.actualGame.map[grid_x1][grid_y1].sprite not in list_of_undestructible and self.model.actualGame.map[grid_x2][grid_y2].sprite not in list_of_undestructible:

                match(pattern):
                    case 0:
                        for xi in range(grid_x1, grid_x2+1):
                            if self.model.actualGame.map[xi][grid_y2].road == None:
                                Route(self.model.actualGame.map[xi][grid_y2], self.model.actualGame)

                        for yi in range(grid_y1, grid_y2+1):
                            if self.model.actualGame.map[grid_x1][yi].road == None:
                                Route(self.model.actualGame.map[grid_x1][yi], self.model.actualGame)
                    case 1:
                        for xi in range(grid_x1, grid_x2-1, -1):
                            if self.model.actualGame.map[xi][grid_y1].road == None:
                                Route(self.model.actualGame.map[xi][grid_y1], self.model.actualGame)
                        for yi in range(grid_y1, grid_y2+1):
                            if self.model.actualGame.map[grid_x2][yi].road == None:
                                Route(self.model.actualGame.map[grid_x2][yi], self.model.actualGame)
                    case 2:
                        for xi in range(grid_x1, grid_x2+1):
                            if self.model.actualGame.map[xi][grid_y1].road == None:
                                Route(self.model.actualGame.map[xi][grid_y1], self.model.actualGame)
                        for yi in range(grid_y1, grid_y2-1, -1):
                            if self.model.actualGame.map[grid_x2][yi].road == None:
                                Route(self.model.actualGame.map[grid_x2][yi], self.model.actualGame)
                    case 3:
                        for xi in range(grid_x1, grid_x2-1, -1):
                            if self.model.actualGame.map[xi][grid_y2].road == None:
                                Route(self.model.actualGame.map[xi][grid_y2], self.model.actualGame)
                        for yi in range(grid_y1, grid_y2-1, -1):
                            if self.model.actualGame.map[grid_x1][yi].road == None:
                                Route(self.model.actualGame.map[grid_x1][yi], self.model.actualGame)
                            
            self.model.actualGame.collision_matrix = self.model.actualGame.create_collision_matrix()
            
        #Building

        if build_housing_button.clicked and not build_housing_button.rect.collidepoint(event.pos):
        
        #Mouse Selection :
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

            #Building Construction :
            for xi in range(grid_x1, grid_x2+1):
                for yi in range(grid_y1, grid_y2+1):
                    for xcr in range (xi-2,xi+2,1) :
                        for ycr in range (yi-2,yi+2,1) :
                            if not self.model.actualGame.map[xi][yi].road and not self.model.actualGame.map[xi][yi].building:
                                if self.model.actualGame.map[xcr][ycr].getConnectedToRoad() > 0 :
                                    HousingSpot(self.model.actualGame.map[xi][yi],self.model.actualGame)

                
        if security_structures.clicked and not security_structures.rect.collidepoint(event.pos):
        
        #Mouse Selection :
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

            #Building Construction :
            for xi in range(grid_x1, grid_x2+1):
                for yi in range(grid_y1, grid_y2+1):
                    for xcr in range (xi-1,xi+1,1) :
                        for ycr in range (yi-1,yi+1,1) :
                            if self.model.actualGame.map[xcr][ycr].getConnectedToRoad() > 0 :
                                if not self.model.actualGame.map[xi][yi].road and not self.model.actualGame.map[xi][yi].building:
                                    newPrefect = Prefet(self.model.actualGame.map[xi][yi],self.model.actualGame,"Prefectus")
                                    Prefecture(self.model.actualGame.map[xi][yi],self.model.actualGame,(1,1),"Prefecture",newPrefect,1)
                                    
                                    

                                

    def handleMouseMouvement(self, event):
        """ Here we are going to manage the movement of the mouse"""
        #Pelle
        if clear_land_button.clicked and not clear_land_button.rect.collidepoint(event.pos) and self.initialMouseCoordinate != None:
            for xi in range(len(self.model.actualGame.previewMap)):
                for yi in range(len(self.model.actualGame.previewMap[0])):
                        self.model.actualGame.previewMap[xi][yi] = None
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
                    self.model.actualGame.previewMap[xi][yi] = "red"

