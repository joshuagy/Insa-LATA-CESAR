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
from Model.Buildings.UrbanPlanning import *
from Model.Buildings.RessourceBuilding import *

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
        self.pause_move_button()
        if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                        self.clicked = True
                        self.initialMouseCoordinate = pygame.mouse.get_pos()

                        self.pause_menu(event)

        elif event.type == pygame.MOUSEBUTTONUP:
                if(self.clicked):
                        # get current state
                        self.finalClickCoordinate = pygame.mouse.get_pos()
                        currentstate = self.model.state.peek()
                        if currentstate == STATE_INTRO_SCENE:
                                self.handleMouseEventsStateIntroScene(event)
                        if currentstate == STATE_MENU:
                                self.handleMouseEventsStateMenu(event)
                        if currentstate == STATE_PLAY:
                                self.handleMouseEventsStatePlay(event)
                if event.button == 1:
                        self.clicked = False
                        self.initialMouseCoordinate = None

        #  Preview clear land
        else:
            temp = pygame.mouse.get_pos()
            if temp != self.initialMouseCoordinate:
                self.handleMouseMouvementWhenClicked(event)

        # Handle all hover
        self.hoverEvent(event)

    def hoverEvent(self, event):
        mousePos = event.pos 
        currentstate = self.model.state.peek()
        controlsCurrentState = self.model.actualGame.controls.getCurrentState()

        if currentstate == STATE_INTRO_SCENE:
            self.handleHoverEventIntroScene(mousePos)
        elif currentstate == STATE_MENU:
            self.handleHoverEventMenu(mousePos)
        elif currentstate == STATE_PLAY:
            self.checkEveryButton(event)
            if controlsCurrentState == 'default':
                self.model.actualGame.foreground.initForegroundGrid()
                if self.isMousePosInGrid(mousePos):
                    (x, y) = self.mousePosToGridPos(mousePos)
                    self.model.actualGame.foreground.addEffect(x, y, 'default')
            
    def handleHoverEventIntroScene(self, mousePos):
        self.model.introScene.handleHoverEvent(mousePos)

    def handleHoverEventMenu(self, mousePos):
        self.model.menu.handleHoverEvent(mousePos)

    def handleMouseEventsStateIntroScene(self, event):
        """
        Handles intro scene mouse events.
        """
        feedBack = self.model.introScene.handleMouseInput(event)
        self.evManager.Post(feedBack)

    def handleMouseEventsStateMenu(self, event):
        """
        Handles menu mouse events.
        """
        feedBack = self.model.menu.handleMouseInput(event)
        self.evManager.Post(feedBack)

    def pause_move_button(self):
        if self.model.pause_menu.Exit_rect.collidepoint(pygame.mouse.get_pos()) and self.model.pause_menu.pause :
            self.model.pause_menu.passed[0]=True
            if self.model.pause_menu.Exit_rect.y == self.model.pause_menu.Exit_rectyinit:
                self.model.pause_menu.Exit_rect.y = self.model.pause_menu.Exit_rectyinit - 2
        else:
            self.model.pause_menu.passed[0] = False
            self.model.pause_menu.Exit_rect.y = self.model.pause_menu.Exit_rectyinit




        if self.model.pause_menu.Continue_rect.collidepoint(pygame.mouse.get_pos()) and self.model.pause_menu.pause :
            self.model.pause_menu.passed[1] = True
            if self.model.pause_menu.Continue_rect.y == self.model.pause_menu.Continue_rectyinit:
                self.model.pause_menu.Continue_rect.y =self.model.pause_menu.Continue_rectyinit - 2
        else:
            self.model.pause_menu.passed[1] = False
            self.model.pause_menu.Continue_rect.y = self.model.pause_menu.Continue_rectyinit


        if self.model.pause_menu.Savegame_rect.collidepoint(pygame.mouse.get_pos()) and self.model.pause_menu.pause :
            self.model.pause_menu.passed[2] = True
            if self.model.pause_menu.Savegame_rect.y == self.model.pause_menu.Savegame_rectyinit:
                self.model.pause_menu.Savegame_rect.y = self.model.pause_menu.Savegame_rectyinit - 2
        else:
            self.model.pause_menu.passed[2] = False
            self.model.pause_menu.Savegame_rect.y = self.model.pause_menu.Savegame_rectyinit


        if self.model.pause_menu.Replay_rect.collidepoint(pygame.mouse.get_pos()) and self.model.pause_menu.pause :
            self.model.pause_menu.passed[3] = True
            if self.model.pause_menu.Replay_rect.y == self.model.pause_menu.Replay_rectyinit:
                self.model.pause_menu.Replay_rect.y = self.model.pause_menu.Replay_rectyinit - 2
        else:
            self.model.pause_menu.passed[3] = False
            self.model.pause_menu.Replay_rect.y = self.model.pause_menu.Replay_rectyinit








    def pause_menu(self,event):
        if self.model.pause_menu.Exit_rect.collidepoint(event.pos) and self.model.pause_menu.pause:
            self.model.pause_menu.exit()

        if self.model.pause_menu.Continue_rect.collidepoint(event.pos) and self.model.pause_menu.pause:
            self.model.pause_menu.pause = False
            self.model.actualGame.pause = False

        if self.model.pause_menu.Savegame_rect.collidepoint(event.pos) and self.model.pause_menu.pause:
            pass

        if self.model.pause_menu.Replay_rect.collidepoint(event.pos) and self.model.pause_menu.pause:
            self.model.actualGame.restart = True
            self.model.actualGame.update()
            self.model.pause_menu.pause = False
            self.model.actualGame.pause = False


    def checkEveryButton(self, event):
        """
            Check if a button has been pressed
        """
        
        #Handle the buttons of the control panel
        
        event.pos = (event.pos[0] - (self.model.actualGame.width - big_gap_menu.dim[0]), event.pos[1] - 24)
        for button in self.model.actualGame.controls.listOfButtons:
            button.handle_event(event)

    def handleMouseEventsStatePlay(self, event):
        """
        Handles game mouse events
        """

        mousePosRelative = (event.pos[0] - (self.model.actualGame.width - big_gap_menu.dim[0] - 1758.0) - 1758.0, event.pos[1] -24)
        controlsCurrentState = self.model.actualGame.controls.getCurrentState()

        # Pelle 
        if controlsCurrentState == 'clearLand' and not self.model.actualGame.controls.clear_land_button.rect.collidepoint(mousePosRelative):
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
            
            self.model.actualGame.clearLand(grid_x1, grid_x2, grid_y1, grid_y2)
            
        # Routes
        elif controlsCurrentState == 'buildRoads' and not self.model.actualGame.controls.build_roads_button.rect.collidepoint(mousePosRelative):
            grid_x1, grid_y1 = self.mousePosToGridPos(self.initialMouseCoordinate)
            grid_x2, grid_y2 = self.mousePosToGridPos(event.pos)
        
            pattern = 0
            if grid_x1 > grid_x2:
                pattern += 1

            if grid_y1 > grid_y2:
                pattern += 2

            if self.model.actualGame.map[grid_x1][grid_y1].sprite not in list_of_undestructible and self.model.actualGame.map[grid_x2][grid_y2].sprite not in list_of_undestructible:
                match(pattern):
                    case 0:
                        for xi in range(grid_x1, grid_x2+1):
                            if self.model.actualGame.map[xi][grid_y2].road == None and self.model.actualGame.map[xi][grid_y2].structure == None and self.model.actualGame.map[xi][grid_y2].sprite not in list_of_collision:
                                Route(self.model.actualGame.map[xi][grid_y2], self.model.actualGame)

                        for yi in range(grid_y1, grid_y2+1):
                            if self.model.actualGame.map[grid_x1][yi].road == None and self.model.actualGame.map[grid_x1][yi].structure == None and self.model.actualGame.map[grid_x1][yi].sprite not in list_of_collision:
                                Route(self.model.actualGame.map[grid_x1][yi], self.model.actualGame)
                    case 1:
                        for xi in range(grid_x1, grid_x2-1, -1):
                            if self.model.actualGame.map[xi][grid_y1].road == None and self.model.actualGame.map[xi][grid_y1].structure == None and self.model.actualGame.map[xi][grid_y1].sprite not in list_of_collision:
                                Route(self.model.actualGame.map[xi][grid_y1], self.model.actualGame)
                        for yi in range(grid_y1, grid_y2+1):
                            if self.model.actualGame.map[grid_x2][yi].road == None and self.model.actualGame.map[grid_x2][yi].structure == None and self.model.actualGame.map[grid_x2][yi].sprite not in list_of_collision:
                                Route(self.model.actualGame.map[grid_x2][yi], self.model.actualGame)
                    case 2:
                        for xi in range(grid_x1, grid_x2+1):
                            if self.model.actualGame.map[xi][grid_y1].road == None and self.model.actualGame.map[xi][grid_y1].structure == None and self.model.actualGame.map[xi][grid_y1].sprite not in list_of_collision:
                                Route(self.model.actualGame.map[xi][grid_y1], self.model.actualGame)
                        for yi in range(grid_y1, grid_y2-1, -1):
                            if self.model.actualGame.map[grid_x2][yi].road == None and self.model.actualGame.map[grid_x2][yi].structure == None and self.model.actualGame.map[grid_x2][yi].sprite not in list_of_collision:
                                Route(self.model.actualGame.map[grid_x2][yi], self.model.actualGame)
                    case 3:
                        for xi in range(grid_x1, grid_x2-1, -1):
                            if self.model.actualGame.map[xi][grid_y2].road == None and self.model.actualGame.map[xi][grid_y2].structure == None and self.model.actualGame.map[xi][grid_y2].sprite not in list_of_collision:
                                Route(self.model.actualGame.map[xi][grid_y2], self.model.actualGame)
                        for yi in range(grid_y1, grid_y2-1, -1):
                            if self.model.actualGame.map[grid_x1][yi].road == None and self.model.actualGame.map[grid_x1][yi].structure == None and self.model.actualGame.map[grid_x1][yi].sprite not in list_of_collision:
                                Route(self.model.actualGame.map[grid_x1][yi], self.model.actualGame)

                self.model.actualGame.collision_matrix = self.model.actualGame.create_collision_matrix()
            
        # #Buildings
        # #HousingSpot
        elif controlsCurrentState == 'buildHousing' and not self.model.actualGame.controls.build_housing_button.rect.collidepoint(mousePosRelative):
            grid_x1, grid_y1 = self.mousePosToGridPos(event.pos)

            for xcr in range (grid_x1-2,grid_x1+3,1) :
                for ycr in range (grid_y1-2,grid_y1+3,1) :
                    if 0<=xcr<self.model.actualGame.nbr_cell_x and 0<=ycr<self.model.actualGame.nbr_cell_y:
                        if not self.model.actualGame.map[grid_x1][grid_y1].road and not self.model.actualGame.map[grid_x1][grid_y1].structure and self.model.actualGame.map[grid_x1][grid_y1].sprite not in list_of_collision:
                            if self.model.actualGame.map[xcr][ycr].road:
                                HousingSpot(self.model.actualGame.map[grid_x1][grid_y1], self.model.actualGame)
    
        # #Prefecture     
        elif controlsCurrentState == 'securityStructures' and not self.model.actualGame.controls.security_structures.rect.collidepoint(mousePosRelative):
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
                    if self.model.actualGame.map[xi][yi].getConnectedToRoad() > 0 :
                        if not self.model.actualGame.map[xi][yi].road and not self.model.actualGame.map[xi][yi].structure and self.model.actualGame.map[xi][yi].sprite not in list_of_collision:
                            Prefecture(self.model.actualGame.map[xi][yi],self.model.actualGame,(1,1),"Prefecture",1)

        # #Engineer
        elif controlsCurrentState == 'buildEngineerPost' and not self.model.actualGame.controls.engineering_structures.rect.collidepoint(mousePosRelative):
        
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
                    if self.model.actualGame.map[xi][yi].getConnectedToRoad() > 0 :
                        if not self.model.actualGame.map[xi][yi].road and not self.model.actualGame.map[xi][yi].structure and self.model.actualGame.map[xi][yi].sprite not in list_of_collision:
                            EnginnerPost(self.model.actualGame.map[xi][yi],self.model.actualGame,(1,1),"EngineerPost",1)

        #Well
        if self.model.actualGame.controls.water_related_structures.clicked and not self.model.actualGame.controls.water_related_structures.rect.collidepoint((event.pos[0] - 1758.0, event.pos[1] - 24)):
        
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
                    if not self.model.actualGame.map[xi][yi].road and not self.model.actualGame.map[xi][yi].structure and self.model.actualGame.map[xi][yi].sprite not in list_of_collision:
                        Well(self.model.actualGame.map[xi][yi],self.model.actualGame,"Well")

        #Senate
        if self.model.actualGame.controls.administration_or_government_structures.clicked and not self.model.actualGame.controls.administration_or_government_structures.rect.collidepoint(event.pos):
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
            
            #Vérifier qu'on a pas déjà un Sénat
            for ms in self.model.actualGame.structures :
                if ms.desc == "Senate" :
                    return
            #Vérifier que toutes les cases sont disponibles :
            for xi in range(grid_x1, grid_x2+1):
                for yi in range(grid_y1, grid_y2+1):
                    for xccl in range(xi, xi+5, 1) :
                        for yccl in range(yi, yi-5, -1 ) :
                            if self.model.actualGame.map[xccl][yccl].road or self.model.actualGame.map[xccl][yccl].structure or self.model.actualGame.map[xccl][yccl].sprite in list_of_collision:
                                return
            Senate(self.model.actualGame.map[xi][yi],self.model.actualGame,(5,5),"Senate")

        #Farm
        if self.model.actualGame.controls.industrial_structures.clicked and not self.model.actualGame.controls.industrial_structures.rect.collidepoint(event.pos):
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
            
            #Vérifier que toutes les cases sont disponibles :
            for xi in range(grid_x1, grid_x2+1):
                for yi in range(grid_y1, grid_y2+1):
                    for xccl in range(xi, xi+3, 1) :
                        for yccl in range(yi-1, yi-2, -1 ) :
                            if self.model.actualGame.map[xccl][yccl].road or self.model.actualGame.map[xccl][yccl].structure or self.model.actualGame.map[xccl][yccl].sprite in list_of_collision:
                                return
            WheatFarm(self.model.actualGame.map[xi][yi],self.model.actualGame,(1,1),"WheatFarm")
 
                                    
        #Overlay part
        # if fire_overlay.clicked:
        #     pass


    def isMousePosInGrid(self, mousePos):
        x, y = mousePos
        world_x = x - self.model.actualGame.camera.vect.x - self.model.actualGame.surface_cells.get_width() / 2
        world_y = y - self.model.actualGame.camera.vect.y

        cart_y = (2 * world_y - world_x) / 2
        cart_x = cart_y + world_x
        grid_x1 = int(cart_x // cell_size)
        grid_y1 = int(cart_y // cell_size)

        if grid_x1 < 0 or grid_y1 <0:
            return False
            
        elif grid_x1 > self.model.actualGame.nbr_cell_x-1 or grid_y1 > self.model.actualGame.nbr_cell_y-1:
            return False
        else:
            return True



    def mousePosToGridPos(self, mousePos):
        x, y = mousePos
        world_x = x - self.model.actualGame.camera.vect.x - self.model.actualGame.surface_cells.get_width() / 2
        world_y = y - self.model.actualGame.camera.vect.y

        cart_y = (2 * world_y - world_x) / 2
        cart_x = cart_y + world_x
        grid_x1 = int(cart_x // cell_size)
        grid_y1 = int(cart_y // cell_size)

        if grid_x1 <0:
            grid_x1 = 0
        
        if grid_y1 <0:
            grid_y1 = 0
   
        if grid_x1 > self.model.actualGame.nbr_cell_x-1:
            grid_x1 = self.model.actualGame.nbr_cell_x-1
        if grid_y1 > self.model.actualGame.nbr_cell_y-1:
            grid_y1 = self.model.actualGame.nbr_cell_y-1

        return (grid_x1, grid_y1)

    def handleMouseMouvementWhenClicked(self, event):
        """ Here we are going to manage the movement of the mouse"""

        controlsCurrentState = self.model.actualGame.controls.getCurrentState()

        # clearLand State (Pelle)
        if controlsCurrentState == 'clearLand':
            self.model.actualGame.foreground.initForegroundGrid()
            # and self.initialMouseCoordinate != None
            if self.clicked:
                grid_x1, grid_y1 = self.mousePosToGridPos(self.initialMouseCoordinate)
                grid_x2, grid_y2 = self.mousePosToGridPos(event.pos)
            
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
                        self.model.actualGame.foreground.addEffect(xi, yi, 'activeClearLand')
            
            elif self.isMousePosInGrid(event.pos):
                (x, y) = self.mousePosToGridPos(event.pos)
                self.model.actualGame.foreground.addEffect(x, y, 'defaultClearLand')

        if controlsCurrentState == 'buildHousing':
            self.model.actualGame.foreground.initForegroundGrid()
            if self.clicked:
                grid_x1, grid_y1 = self.mousePosToGridPos(self.initialMouseCoordinate)
                grid_x2, grid_y2 = self.mousePosToGridPos(event.pos)
            
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
                            for xcr in range (xi-2,xi+3,1) :
                                for ycr in range (yi-2,yi+3,1) :
                                    if 0<=xcr<self.model.actualGame.nbr_cell_x and 0<=ycr<self.model.actualGame.nbr_cell_y:
                                        if not self.model.actualGame.map[xi][yi].road and not self.model.actualGame.map[xi][yi].structure and self.model.actualGame.map[xi][yi].sprite not in list_of_collision:
                                            if self.model.actualGame.map[xcr][ycr].road :
                                                HousingSpot(self.model.actualGame.map[xi][yi],self.model.actualGame)
                            
            elif self.isMousePosInGrid(event.pos):
                (x, y) = self.mousePosToGridPos(event.pos)
                self.model.actualGame.foreground.addEffect(x, y, 'default')

        if controlsCurrentState == 'buildRoads':
            self.model.actualGame.foreground.initForegroundGrid()
            if self.clicked:
                grid_x1, grid_y1 = self.mousePosToGridPos(self.initialMouseCoordinate)
                grid_x2, grid_y2 = self.mousePosToGridPos(event.pos)
            
                pattern = 0
                if grid_x1 > grid_x2:
                    pattern += 1

                if grid_y1 > grid_y2:
                    pattern += 2

                if self.model.actualGame.map[grid_x1][grid_y1].sprite not in list_of_undestructible and self.model.actualGame.map[grid_x2][grid_y2].sprite not in list_of_undestructible:
                    match(pattern):
                        case 0:
                            for xi in range(grid_x1, grid_x2+1):
                                if self.model.actualGame.map[xi][grid_y2].road == None and self.model.actualGame.map[xi][grid_y2].structure == None and self.model.actualGame.map[xi][grid_y2].sprite not in list_of_collision:
                                    Route(self.model.actualGame.map[xi][grid_y2], self.model.actualGame)

                            for yi in range(grid_y1, grid_y2+1):
                                if self.model.actualGame.map[grid_x1][yi].road == None and self.model.actualGame.map[grid_x1][yi].structure == None and self.model.actualGame.map[grid_x1][yi].sprite not in list_of_collision:
                                    Route(self.model.actualGame.map[grid_x1][yi], self.model.actualGame)
                        case 1:
                            for xi in range(grid_x1, grid_x2-1, -1):
                                if self.model.actualGame.map[xi][grid_y1].road == None and self.model.actualGame.map[xi][grid_y1].structure == None and self.model.actualGame.map[xi][grid_y1].sprite not in list_of_collision:
                                    Route(self.model.actualGame.map[xi][grid_y1], self.model.actualGame)
                            for yi in range(grid_y1, grid_y2+1):
                                if self.model.actualGame.map[grid_x2][yi].road == None and self.model.actualGame.map[grid_x2][yi].structure == None and self.model.actualGame.map[grid_x2][yi].sprite not in list_of_collision:
                                    Route(self.model.actualGame.map[grid_x2][yi], self.model.actualGame)
                        case 2:
                            for xi in range(grid_x1, grid_x2+1):
                                if self.model.actualGame.map[xi][grid_y1].road == None and self.model.actualGame.map[xi][grid_y1].structure == None and self.model.actualGame.map[xi][grid_y1].sprite not in list_of_collision:
                                    Route(self.model.actualGame.map[xi][grid_y1], self.model.actualGame)
                            for yi in range(grid_y1, grid_y2-1, -1):
                                if self.model.actualGame.map[grid_x2][yi].road == None and self.model.actualGame.map[grid_x2][yi].structure == None and self.model.actualGame.map[grid_x2][yi].sprite not in list_of_collision:
                                    Route(self.model.actualGame.map[grid_x2][yi], self.model.actualGame)
                        case 3:
                            for xi in range(grid_x1, grid_x2-1, -1):
                                if self.model.actualGame.map[xi][grid_y2].road == None and self.model.actualGame.map[xi][grid_y2].structure == None and self.model.actualGame.map[xi][grid_y2].sprite not in list_of_collision:
                                    Route(self.model.actualGame.map[xi][grid_y2], self.model.actualGame)
                            for yi in range(grid_y1, grid_y2-1, -1):
                                if self.model.actualGame.map[grid_x1][yi].road == None and self.model.actualGame.map[grid_x1][yi].structure == None and self.model.actualGame.map[grid_x1][yi].sprite not in list_of_collision:
                                    Route(self.model.actualGame.map[grid_x1][yi], self.model.actualGame)

                    self.model.actualGame.collision_matrix = self.model.actualGame.create_collision_matrix()

                    self.model.actualGame.foreground.addEffect(grid_x2, grid_y2, 'activeBuildRoads') 

            elif self.isMousePosInGrid(event.pos):
                (x, y) = self.mousePosToGridPos(event.pos)
                self.model.actualGame.foreground.addEffect(x, y, 'default') 
                # for xi in range(grid_x1, grid_x2+1):
                #     for yi in range(grid_y1, grid_y2+1):
                #         self.model.actualGame.foreground.addEffect(xi, yi, 'activeBuildRoads')
            