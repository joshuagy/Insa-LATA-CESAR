import pygame
import random
from Model.constants import *
from Model.control_panel import *
from EventManager.Event import Event
from EventManager.allEvent import StateChangeEvent, LoadSave, MultiplayerStart
from Model.Plateau import Plateau, cell_size
from Model.Route import Route
from Model.Buildings.Building import *
from Model.Buildings.House import *
from Model.Buildings.WorkBuilding import *
from Model.Buildings.UrbanPlanning import *
from Model.Buildings.RessourceBuilding import *
from Model.Multiplayer import *
from Model.TopBar import TopBar

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
        currentstate = self.model.state.peek()
        if event.type == pygame.MOUSEBUTTONDOWN:
                self.clicked = True
                self.initialMouseCoordinate = pygame.mouse.get_pos()
                
                self.topbar(event)
                
                if currentstate == STATE_PLAY:
                    self.handleMouseButtonDownEventStatePlay(event)


        elif event.type == pygame.MOUSEBUTTONUP:
                if(self.clicked):
                        self.finalClickCoordinate = pygame.mouse.get_pos()
                        
                        if currentstate == STATE_INTRO_SCENE:
                                self.handleMouseEventsStateIntroScene(event)
                        elif currentstate == STATE_MENU:
                                self.handleMouseEventsStateMenu(event)
                        elif currentstate == STATE_PLAY and self.model.pause_menu.pause:
                                self.pause_menu(event)
                        elif currentstate == STATE_PLAY:
                                self.handleMouseButtonUpEventStatePlay(event)
                        elif currentstate == STATE_SAVE_SCENE:
                                self.handleMouseEventsStateSaveScene(event)
                        elif currentstate == STATE_OPEN_TO_LAN_SCENE:
                                self.handleMouseEventsStateOpenToLanScene(event)
                if event.button == 1:
                        self.clicked = False
                        self.initialMouseCoordinate = None

        #  Preview clear land
        else:
            temp = pygame.mouse.get_pos()
            if temp != self.initialMouseCoordinate:
                self.handleMouseMouvement(event)

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

    def handleMouseEventsStateSaveScene(self, event):
        feedBack = self.model.saveScene.handleMouseInput(event)
        self.evManager.Post(feedBack)
    
    def handleMouseEventsStateOpenToLanScene(self, event):
        feedBack = self.model.openToLanScene.handleMouseInput(event)
        self.evManager.Post(feedBack)

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
        if isinstance(feedBack, LoadSave):
            self.model.saveScene.userInput = feedBack.saveName.split('.')[0]
            self.model.actualGame.load_savefile(feedBack.saveName)
            self.evManager.Post(StateChangeEvent(STATE_PLAY))
        elif isinstance(feedBack, MultiplayerStart):
            self.model.actualGame.multiplayer = Multiplayer(self.model.actualGame, feedBack.ipaddr, feedBack.portext, feedBack.portint, 1)
            self.model.actualGame.load_savefile("DefaultMap.pickle")
            self.evManager.Post(StateChangeEvent(STATE_PLAY))
        elif isinstance(feedBack, StateChangeEvent):
            if feedBack.state == STATE_PLAY:
                self.model.saveScene.userInput = ""                
                #Just uncomment the line below to have a defined map, otherwise it will be full of grass
                self.model.actualGame.load_savefile("DefaultMap.pickle")
            self.evManager.Post(feedBack)
        else:
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
            self.model.pause_menu.pause = False
            self.model.actualGame.pause = False
            if self.model.actualGame.multiplayer:
                self.model.actualGame.multiplayer.stop()
                print("stop")
            self.evManager.Post(StateChangeEvent(STATE_MENU))

        if self.model.pause_menu.Continue_rect.collidepoint(event.pos) and self.model.pause_menu.pause:
            self.model.pause_menu.pause = False
            self.model.actualGame.pause = False

        if self.model.pause_menu.Savegame_rect.collidepoint(event.pos) and self.model.pause_menu.pause:
           self.evManager.Post(StateChangeEvent(STATE_SAVE_SCENE))

        if self.model.pause_menu.Replay_rect.collidepoint(event.pos) and self.model.pause_menu.pause:
            self.model.actualGame.restart = True
            self.model.actualGame.update()
            self.model.pause_menu.pause = False
            self.model.actualGame.pause = False

    def topbar(self, event):

        if self.model.actualGame.topbar.File_rect.collidepoint(event.pos) and not self.model.actualGame.topbar.File_bol:
            self.model.actualGame.topbar.File_bol = True
            self.model.actualGame.draw_menu_File

        elif self.model.actualGame.topbar.File_menu_Eg_rect.collidepoint(event.pos) and self.model.actualGame.topbar.File_bol:
            self.model.pause_menu.pause = False
            self.model.actualGame.pause = False
            self.m
            self.evManager.Post(StateChangeEvent(STATE_MENU))

        elif self.model.actualGame.topbar.File_menu_Sg_rect.collidepoint(event.pos) and self.model.actualGame.topbar.File_bol:
            self.evManager.Post(StateChangeEvent(STATE_SAVE_SCENE))

        elif self.model.actualGame.topbar.File_menu_Rm_rect.collidepoint(
                event.pos) and self.model.actualGame.topbar.File_bol:
            self.model.actualGame.restart = True
            self.model.actualGame.update()
        elif self.model.actualGame.topbar.OpenToLan_rect.collidepoint(
                event.pos):
            self.evManager.Post(StateChangeEvent(STATE_OPEN_TO_LAN_SCENE))


        else:
            self.model.actualGame.topbar.File_bol = False


    def checkEveryButton(self, event):
        """
            Check if a button has been pressed
        """
        
        #Handle the buttons of the control panel
        
        event.pos = (event.pos[0] - (self.model.actualGame.width - big_gap_menu.dim[0]), event.pos[1] - 24)
        for button in self.model.actualGame.controls.listOfButtons:
            button.handle_event(event)

    def handleMouseButtonDownEventStatePlay(self, event):
        pass

    def handleMouseButtonUpEventStatePlay(self, event):
        """
        Handles game mouse events
        """
        property = self.model.actualGame.property
        self.model.actualGame.foreground.initOverlayGrid()

        mousePosRelative = (event.pos[0] - (self.model.actualGame.width - big_gap_menu.dim[0] - 1758.0) - 1758.0, event.pos[1] -24)
        controlsCurrentState = self.model.actualGame.controls.getCurrentState()
        
        message = input("Enter your protocol message: ")
        self.wrapper(message)
        print(event.pos)

        if self.model.actualGame.controls.overlays_button.rect.collidepoint(mousePosRelative):
            if self.model.actualGame.foreground.getOverlayName() == "fire":
                self.model.actualGame.foreground.setOverlayName("destruct")

            elif self.model.actualGame.foreground.getOverlayName() == "destruct":
                self.model.actualGame.actualizeInf()
                self.model.actualGame.foreground.setOverlayName("influence")

            elif self.model.actualGame.foreground.getOverlayName() == "influence":
                self.model.actualGame.foreground.setOverlayName(None)
            
            elif self.model.actualGame.foreground.getOverlayName() == None:
                self.model.actualGame.foreground.setOverlayName("fire")

        if self.model.actualGame.controls.mouseInStaticSurface(event.pos):
            return
        
            
        # Pelle 
        if controlsCurrentState == 'clearLand' and not self.model.actualGame.controls.clear_land_button.rect.collidepoint(mousePosRelative):
            x1, y1 = self.initialMouseCoordinate
            x2, y2 = event.pos

            self.pelle(x1, y1, x2, y2)

            if grid_y1 > grid_y2:
                temp = grid_y1
                grid_y1 = grid_y2
                              
                grid_y2 = temp
            
            self.model.actualGame.clearLand(grid_x1, grid_x2, grid_y1, grid_y2, property)
            self.model.actualGame.soundMixer.playEffect('buildEffect')
            if self.model.actualGame.multiplayer:
                self.model.actualGame.multiplayer.send(f"SCL.{grid_x1}.{grid_y1}.{grid_x2}.{grid_y2}.{property}")
        # Routes
        elif controlsCurrentState == 'buildRoads' and not self.model.actualGame.controls.build_roads_button.rect.collidepoint(mousePosRelative):
            x1, y1 = self.initialMouseCoordinate
            x2, y2 = event.pos

            self.roads(x1, y1, x2, y2)

        # #Buildings
        # #HousingSpot
        elif controlsCurrentState == 'buildHousing' and not self.model.actualGame.controls.build_housing_button.rect.collidepoint(mousePosRelative):
            x2, y2 = event.pos
            x1, y1 = self.initialMouseCoordinate
            
            self.house(x1, y1, x2, y2)
    
        # #Prefecture     
        elif controlsCurrentState == 'securityStructures' and not self.model.actualGame.controls.security_structures.rect.collidepoint(mousePosRelative):
            x2, y2 = event.pos
            x1, y1 = self.initialMouseCoordinate
            self.prefet(x1, y1, x2, y2)
           
        # #Engineer
        elif controlsCurrentState == 'buildEngineerPost' and not self.model.actualGame.controls.engineering_structures.rect.collidepoint(mousePosRelative):
            x2, y2 = event.pos
            x1, y1 = self.initialMouseCoordinate
            self.engineering_structure(x1, y1, x2, y2)
           
        #Well
        if self.model.actualGame.controls.water_related_structures.clicked and not self.model.actualGame.controls.water_related_structures.rect.collidepoint((event.pos[0] - 1758.0, event.pos[1] - 24)):
            x2, y2 = event.pos
            x1, y1 = self.initialMouseCoordinate
            self.well(x1, y1, x2, y2)
          
        #Senate
        if self.model.actualGame.controls.administration_or_government_structures.clicked and not self.model.actualGame.controls.administration_or_government_structures.rect.collidepoint(event.pos):
            x2, y2 = event.pos
            x1, y1 = self.initialMouseCoordinate
            self.senate(x1, y1, x2, y2)
        #Farm
        if self.model.actualGame.controls.industrial_structures.clicked and not self.model.actualGame.controls.industrial_structures.rect.collidepoint(event.pos):
            x2, y2 = event.pos
            x1, y1 = self.initialMouseCoordinate
            self.farm(x1, y1, x2, y2)
        #Granary
        if self.model.actualGame.controls.message_view_button.clicked and not self.model.actualGame.controls.message_view_button.rect.collidepoint(event.pos):
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
            
            self.model.actualGame.buildGranary(grid_x1, grid_x2, grid_y1, grid_y2, property)
            self.model.actualGame.soundMixer.playEffect('buildEffect')
            if self.model.actualGame.multiplayer:
                self.model.actualGame.multiplayer.send(f"SBGr.{grid_x1}.{grid_y1}.{grid_x2}.{grid_y2}.{property}")
        #Market
        if self.model.actualGame.controls.see_recent_troubles_button.clicked and not self.model.actualGame.controls.see_recent_troubles_button.rect.collidepoint(event.pos):
            x2, y2 = event.pos
            x1, y1 = self.initialMouseCoordinate
            market(self, x1, y1, x2, y2)
                                    
        if self.model.actualGame.controls.religious_structures.clicked and not self.model.actualGame.controls.religious_structures.rect.collidepoint(event.pos):
            
            x2, y2 = event.pos
            x1, y1 = self.initialMouseCoordinate
            god_structure(self, x1, y1, x2, y2)

        #Overlay part
        # if fire_overlay.clicked:
        #     pass


        #Creative Mode
        if controlsCurrentState == 'land' or controlsCurrentState == 'tree' or controlsCurrentState == 'rock' or controlsCurrentState == 'water':
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
                        if controlsCurrentState == 'land' :
                            self.model.actualGame.map[xi][yi].sprite = "land"
                            self.model.actualGame.map[xi][yi].indexSprite = randint(0, 57)
                        elif controlsCurrentState == 'tree' :
                            self.model.actualGame.map[xi][yi].sprite = "tree"
                            self.model.actualGame.map[xi][yi].indexSprite = randint(0, 31)
                        elif controlsCurrentState == 'rock' :
                            self.model.actualGame.map[xi][yi].sprite = "rock"
                            self.model.actualGame.map[xi][yi].indexSprite = randint(0, 7)
                        elif controlsCurrentState == 'water' :
                            self.model.actualGame.map[xi][yi].sprite = "water"
                            for i in range(xi-1, xi+2):
                                for j in range(yi-1, yi+2):
                                    if i >= 0 and i < self.model.actualGame.nbr_cell_x and j >= 0 and j < self.model.actualGame.nbr_cell_y:
                                        if self.model.actualGame.map[i][j].sprite == "water":
                                            self.water(i,j)

                        if self.model.actualGame.map[xi][yi].road :
                            self.model.actualGame.map[xi][yi].road.delete()
                        if self.model.actualGame.map[xi][yi].structure :
                            self.model.actualGame.map[xi][yi].structure.delete()
            
            self.model.actualGame.collision_matrix = self.model.actualGame.create_collision_matrix()
        
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

    def handleMouseMouvement(self, event):
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
                self.model.actualGame.foreground.addEffect(x, y, 'activeClearLand')

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
                            edited = False
                            for xcr in range (xi-2,xi+3,1) :
                                for ycr in range (yi-2,yi+3,1) :
                                    if 0<=xcr<self.model.actualGame.nbr_cell_x and 0<=ycr<self.model.actualGame.nbr_cell_y:
                                        if not self.model.actualGame.map[xi][yi].road and not self.model.actualGame.map[xi][yi].structure and self.model.actualGame.map[xi][yi].sprite not in list_of_collision and self.model.actualGame.map[xi][yi].sprite not in list_of_undestructible:
                                            if self.model.actualGame.map[xcr][ycr].road :
                                                self.model.actualGame.foreground.addEffect(xi, yi, 'activeBuildHouse')
                                                edited = True
                            if not edited:
                                self.model.actualGame.foreground.addEffect(xi, yi, 'wrong')

            elif self.isMousePosInGrid(event.pos):
                (x, y) = self.mousePosToGridPos(event.pos)
                for xcr in range (x-2,x+3,1) :
                    for ycr in range (y-2,y+3,1) :
                        if 0<=xcr<self.model.actualGame.nbr_cell_x and 0<=ycr<self.model.actualGame.nbr_cell_y:
                            if not self.model.actualGame.map[x][y].road and not self.model.actualGame.map[x][y].structure and self.model.actualGame.map[x][y].sprite not in list_of_collision and self.model.actualGame.map[x][y].sprite not in list_of_undestructible:
                                if self.model.actualGame.map[xcr][ycr].road :
                                    self.model.actualGame.foreground.addEffect(x, y, 'activeBuildHouse')
                                    return
                self.model.actualGame.foreground.addEffect(x, y, 'wrong')
                            

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
                                    self.model.actualGame.foreground.addEffect(xi, grid_y2, 'default') 

                            for yi in range(grid_y1, grid_y2+1):
                                if self.model.actualGame.map[grid_x1][yi].road == None and self.model.actualGame.map[grid_x1][yi].structure == None and self.model.actualGame.map[grid_x1][yi].sprite not in list_of_collision:
                                    self.model.actualGame.foreground.addEffect(grid_x1, yi, 'default') 

                        case 1:
                            for xi in range(grid_x1, grid_x2-1, -1):
                                if self.model.actualGame.map[xi][grid_y1].road == None and self.model.actualGame.map[xi][grid_y1].structure == None and self.model.actualGame.map[xi][grid_y1].sprite not in list_of_collision:
                                    self.model.actualGame.foreground.addEffect(xi, grid_y1, 'default') 
                            for yi in range(grid_y1, grid_y2+1):
                                if self.model.actualGame.map[grid_x2][yi].road == None and self.model.actualGame.map[grid_x2][yi].structure == None and self.model.actualGame.map[grid_x2][yi].sprite not in list_of_collision:
                                    self.model.actualGame.foreground.addEffect(grid_x2, yi, 'default')
                        case 2:
                            for xi in range(grid_x1, grid_x2+1):
                                if self.model.actualGame.map[xi][grid_y1].road == None and self.model.actualGame.map[xi][grid_y1].structure == None and self.model.actualGame.map[xi][grid_y1].sprite not in list_of_collision:
                                    self.model.actualGame.foreground.addEffect(xi, grid_y1, 'default')
                            for yi in range(grid_y1, grid_y2-1, -1):
                                if self.model.actualGame.map[grid_x2][yi].road == None and self.model.actualGame.map[grid_x2][yi].structure == None and self.model.actualGame.map[grid_x2][yi].sprite not in list_of_collision:
                                    self.model.actualGame.foreground.addEffect(grid_x2, yi, 'default')
                        case 3:
                            for xi in range(grid_x1, grid_x2-1, -1):
                                if self.model.actualGame.map[xi][grid_y2].road == None and self.model.actualGame.map[xi][grid_y2].structure == None and self.model.actualGame.map[xi][grid_y2].sprite not in list_of_collision:
                                    self.model.actualGame.foreground.addEffect(xi, grid_y2, 'default')

                            for yi in range(grid_y1, grid_y2-1, -1):
                                if self.model.actualGame.map[grid_x1][yi].road == None and self.model.actualGame.map[grid_x1][yi].structure == None and self.model.actualGame.map[grid_x1][yi].sprite not in list_of_collision:
                                    self.model.actualGame.foreground.addEffect(grid_x1, yi, 'default')

                    self.model.actualGame.collision_matrix = self.model.actualGame.create_collision_matrix()

            elif self.isMousePosInGrid(event.pos):
                (x, y) = self.mousePosToGridPos(event.pos)
                self.model.actualGame.foreground.addEffect(x, y, 'default') 
               
        if controlsCurrentState == 'securityStructures':
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
                        if self.model.actualGame.map[xi][yi].getConnectedToRoad() > 0 and not self.model.actualGame.map[xi][yi].road and not self.model.actualGame.map[xi][yi].road and not self.model.actualGame.map[xi][yi].structure and self.model.actualGame.map[xi][yi].sprite not in list_of_collision:
                            self.model.actualGame.foreground.addEffect(xi, yi, 'activeSecurityStructures')
                        else:
                            self.model.actualGame.foreground.addEffect(xi, yi, 'wrong')
                            

            elif self.isMousePosInGrid(event.pos):
                (x, y) = self.mousePosToGridPos(event.pos)
                if self.model.actualGame.map[x][y].getConnectedToRoad() > 0 and not self.model.actualGame.map[x][y].road and not self.model.actualGame.map[x][y].structure and self.model.actualGame.map[x][y].sprite not in list_of_collision:
                    self.model.actualGame.foreground.addEffect(x, y, 'activeSecurityStructures')
                else:
                    self.model.actualGame.foreground.addEffect(x, y, 'wrong')

        if controlsCurrentState == 'buildEngineerPost':
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
                        edited = False
                        if self.model.actualGame.map[xi][yi].getConnectedToRoad() > 0 and not self.model.actualGame.map[xi][yi].road and not self.model.actualGame.map[xi][yi].structure and self.model.actualGame.map[xi][yi].sprite not in list_of_collision:
                            self.model.actualGame.foreground.addEffect(xi, yi, 'activeEngineerPost')
                        else:
                            self.model.actualGame.foreground.addEffect(xi, yi, 'wrong')

            elif self.isMousePosInGrid(event.pos):
                (x, y) = self.mousePosToGridPos(event.pos)
                if self.model.actualGame.map[x][y].getConnectedToRoad() > 0 and not self.model.actualGame.map[x][y].road and not self.model.actualGame.map[x][y].structure and self.model.actualGame.map[x][y].sprite not in list_of_collision:
                    self.model.actualGame.foreground.addEffect(x, y, 'activeEngineerPost')
                else:
                    self.model.actualGame.foreground.addEffect(x, y, 'wrong')

        if self.model.actualGame.controls.water_related_structures.clicked:
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
                        edited = False
                        if not self.model.actualGame.map[xi][yi].road and not self.model.actualGame.map[xi][yi].structure and self.model.actualGame.map[xi][yi].sprite not in list_of_collision:
                            self.model.actualGame.foreground.addEffect(xi, yi, 'activeAA')
                        else:
                            self.model.actualGame.foreground.addEffect(xi, yi, 'wrong')

            elif self.isMousePosInGrid(event.pos):
                (x, y) = self.mousePosToGridPos(event.pos)
                if not self.model.actualGame.map[x][y].road and not self.model.actualGame.map[x][y].structure and self.model.actualGame.map[x][y].sprite not in list_of_collision:
                    self.model.actualGame.foreground.addEffect(x, y, 'activeAA')
                else:
                    self.model.actualGame.foreground.addEffect(x, y, 'wrong')

    def water(self, x, y) :
        index = 0
        r = random.randint(0, 3)
        if x < self.model.actualGame.nbr_cell_x-1 and y < self.model.actualGame.nbr_cell_y-1: 
            if self.model.actualGame.map[x+1][y+1].sprite == "water":
                index += 128 # + 10000000
        if x < self.model.actualGame.nbr_cell_x-1 and y > 0:
            if self.model.actualGame.map[x+1][y-1].sprite == "water": #
                index += 64 # + 01000000
        if x > 0 and y < self.model.actualGame.nbr_cell_y-1:
            if self.model.actualGame.map[x-1][y+1].sprite == "water":
                index += 32 # + 00100000
        if x > 0 and y > 0:
            if self.model.actualGame.map[x-1][y-1].sprite == "water": #
                index += 16 # + 00010000
        if y < self.model.actualGame.nbr_cell_y-1:
            if self.model.actualGame.map[x][y+1].sprite == "water":
                index += 8 # + 00001000
        if x < self.model.actualGame.nbr_cell_x-1:
            if self.model.actualGame.map[x+1][y].sprite == "water": 
                index += 4 # + 00000100
        if y > 0:
            if self.model.actualGame.map[x][y-1].sprite == "water": #
                index += 2 # + 00000010
        if x > 0:
            if self.model.actualGame.map[x-1][y].sprite == "water": #
                index += 1 # + 00000001 EAST
        table_correspondance = {0 : 0, 
                                87 : 1, 119 : 1, 215 : 1, 252 : 1,
                                206 : 5, 238 : 5, 222 : 5, 254 : 5,
                                173 : 9, 189 : 9, 237 : 9, 253 : 9,
                                59 : 13, 187 : 13, 123 : 13, 251 : 13,
                                70 : 17, 86 : 17, 198 : 17, 214 : 17,
                                140 : 21, 204 : 21, 172 : 21, 236 : 21,
                                41 : 25, 57 : 25, 169 : 25, 185 : 25,
                                19 : 29, 83 : 29, 51 : 29, 115 : 29,
                                223 : 33, 239 : 34, 191 : 35, 127 : 36, }
        index = table_correspondance.get(index, 0)
        if 0 < index < 33:
            index += r
        self.model.actualGame.map[x][y].setSprite("water", index)

    def pelle(self, x1, y1, x2, y2):

        grid_x1, grid_y1 = self.mousePosToGridPos((x1, y1))
        grid_x2, grid_y2 = self.mousePosToGridPos((x2, y2))

        if grid_x1 > grid_x2:
            temp = grid_x1
            grid_x1 = grid_x2
            grid_x2 = temp

        if grid_y1 > grid_y2:
            temp = grid_y1
            grid_y1 = grid_y2
                            
            grid_y2 = temp
        
        self.model.actualGame.clearLand(grid_x1, grid_x2, grid_y1, grid_y2, property)
        self.model.actualGame.soundMixer.playEffect('buildEffect')
    
    def house(self, x1, y1, x2, y2):

        grid_x1, grid_y1 = self.mousePosToGridPos((x1, y1))
        grid_x2, grid_y2 = self.mousePosToGridPos((x2, y2))

        if grid_x1 > grid_x2:
            temp = grid_x1
            grid_x1 = grid_x2
            grid_x2 = temp

        if grid_y1 > grid_y2:
            temp = grid_y1
            grid_y1 = grid_y2
            grid_y2 = temp
            
        self.model.actualGame.buildHousingSpot(grid_x1, grid_y1, grid_x2, grid_y2, property)
        self.model.actualGame.soundMixer.playEffect('buildEffect')

    def engineering_structure(self, x1, y1, x2, y2):
        x, y = x1, y1
        world_x = x - self.model.actualGame.camera.vect.x - self.model.actualGame.surface_cells.get_width() / 2
        world_y = y - self.model.actualGame.camera.vect.y

        cart_y = (2 * world_y - world_x) / 2
        cart_x = cart_y + world_x
        grid_x1 = int(cart_x // cell_size)
        grid_y1 = int(cart_y // cell_size)

        x, y = x2, y2
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
        self.model.actualGame.buildEngineerPost(grid_x1, grid_y1, grid_x2, grid_y2, property)
        self.model.actualGame.soundMixer.playEffect('buildEffect')
    
    def farm(self, x1, y1, x2, y2):
        x, y = x1, y1
        world_x = x - self.model.actualGame.camera.vect.x - self.model.actualGame.surface_cells.get_width() / 2
        world_y = y - self.model.actualGame.camera.vect.y

        cart_y = (2 * world_y - world_x) / 2
        cart_x = cart_y + world_x
        grid_x1 = int(cart_x // cell_size)
        grid_y1 = int(cart_y // cell_size)

        x, y = x1, y2
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
        
        self.model.actualGame.buildFarm(grid_x1, grid_y1, grid_x2, grid_y2, property)
        self.model.actualGame.soundMixer.playEffect('buildEffect')
    
    def prefet(self, x1, y1, x2, y2):
        x, y = x1, y1
        world_x = x - self.model.actualGame.camera.vect.x - self.model.actualGame.surface_cells.get_width() / 2
        world_y = y - self.model.actualGame.camera.vect.y

        cart_y = (2 * world_y - world_x) / 2
        cart_x = cart_y + world_x
        grid_x1 = int(cart_x // cell_size)
        grid_y1 = int(cart_y // cell_size)

        x, y = x2, y2
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
        self.model.actualGame.buildPrefecture(grid_x1, grid_y1, grid_x2, grid_y2, property)
        self.model.actualGame.soundMixer.playEffect('buildEffect')

    def senate(self, x1, y1, x2, y2):
        x, y = x1, y1
        world_x = x - self.model.actualGame.camera.vect.x - self.model.actualGame.surface_cells.get_width() / 2
        world_y = y - self.model.actualGame.camera.vect.y

        cart_y = (2 * world_y - world_x) / 2
        cart_x = cart_y + world_x
        grid_x1 = int(cart_x // cell_size)
        grid_y1 = int(cart_y // cell_size)

        x, y = x2, y2
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
        self.model.actualGame.buildSenate(grid_x1, grid_y1, grid_x2, grid_y2, property)
        self.model.actualGame.soundMixer.playEffect('buildEffect')
    
    def roads(self, x1, y1, x2, y2):
        grid_x1, grid_y1 = self.mousePosToGridPos((x1, y1))
        grid_x2, grid_y2 = self.mousePosToGridPos((x2, y2))
    
        pattern = 0
        if grid_x1 > grid_x2:
            pattern += 1

        if grid_y1 > grid_y2:
            pattern += 2

        if self.model.actualGame.map[grid_x1][grid_y1].sprite not in list_of_undestructible and self.model.actualGame.map[grid_x2][grid_y2].sprite not in list_of_undestructible:
            self.model.actualGame.buildRoads(pattern, grid_x1, grid_x2, grid_y1, grid_y2, property)
            self.model.actualGame.soundMixer.playEffect('buildEffect')

    def well(self, x1, x2, y1, y2):
        x, y =  x1, y1
        world_x = x - self.model.actualGame.camera.vect.x - self.model.actualGame.surface_cells.get_width() / 2
        world_y = y - self.model.actualGame.camera.vect.y

        cart_y = (2 * world_y - world_x) / 2
        cart_x = cart_y + world_x
        grid_x1 = int(cart_x // cell_size)
        grid_y1 = int(cart_y // cell_size)

        x, y = x2, y2
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
        self.model.actualGame.buildWell(grid_x1, grid_y1, grid_x2, grid_y2, property)
        self.model.actualGame.soundMixer.playEffect('buildEffect')

    def god_structure(self, x1, x2, y1, y2):
        x, y = x1, y1
        world_x = x - self.model.actualGame.camera.vect.x - self.model.actualGame.surface_cells.get_width() / 2
        world_y = y - self.model.actualGame.camera.vect.y

        cart_y = (2 * world_y - world_x) / 2
        cart_x = cart_y + world_x
        grid_x1 = int(cart_x // cell_size)
        grid_y1 = int(cart_y // cell_size)

        x, y = x2, y2
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
        
        self.model.actualGame.buildTemple(grid_x1, grid_y1, grid_x2, grid_y2, property)
        self.model.actualGame.soundMixer.playEffect('buildEffect')

    def market(self, x1, x2, y1, y2):
        x, y = x1, y1
        world_x = x - self.model.actualGame.camera.vect.x - self.model.actualGame.surface_cells.get_width() / 2
        world_y = y - self.model.actualGame.camera.vect.y

        cart_y = (2 * world_y - world_x) / 2
        cart_x = cart_y + world_x
        grid_x1 = int(cart_x // cell_size)
        grid_y1 = int(cart_y // cell_size)

        x, y = x2, y2
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
        self.model.actualGame.buildMarket(grid_x1, grid_y1, grid_x2, grid_y2, property)
        self.model.actualGame.soundMixer.playEffect('buildEffect')

    def wrapper(self, message):
        """ Wrapper that recieve message from the network manager and redirect it in the right method """
        message_split = message.split(".")
        
        #Building - Tested
        if message_split[0] == "SCL":
            self.model.actualGame.clearLand(int(message_split[1]), int(message_split[3]), int(message_split[2]), int(message_split[4]), int(message_split[5]))
            self.model.actualGame.soundMixer.playEffect('buildEffect')
        elif message_split[0] == "SBH":
            self.model.actualGame.buildHousingSpot(int(message_split[1]), int(message_split[3]), int(message_split[2]), int(message_split[4]), int(message_split[5]))
            self.model.actualGame.soundMixer.playEffect('buildEffect')
        elif message_split[0] == "SBI":
            self.model.actualGame.buildEngineerPost(int(message_split[1]), int(message_split[3]), int(message_split[2]), int(message_split[4]), int(message_split[5]))
            self.model.actualGame.soundMixer.playEffect('buildEffect')
        elif message_split[0] == "SBF":
            self.model.actualGame.buildFarm(int(message_split[1]), int(message_split[3]), int(message_split[2]), int(message_split[4]), int(message_split[5]))
            self.model.actualGame.soundMixer.playEffect('buildEffect')
        elif message_split[0] == "SBP":
            self.model.actualGame.buildPrefecture(int(message_split[1]), int(message_split[3]), int(message_split[2]), int(message_split[4]), int(message_split[5]))
            self.model.actualGame.soundMixer.playEffect('buildEffect')
        elif message_split[0] == "SBS":
            self.model.actualGame.buildSenate(int(message_split[1]), int(message_split[3]), int(message_split[2]), int(message_split[4]), int(message_split[5]))
            self.model.actualGame.soundMixer.playEffect('buildEffect')
        elif message_split[0] == "SBR":
            self.model.actualGame.buildRoads(int(message_split[5]), int(message_split[1]), int(message_split[3]), int(message_split[2]), int(message_split[4]), int(message_split[6]))
            self.model.actualGame.soundMixer.playEffect('buildEffect')
        elif message_split[0] == "SBW":
            self.model.actualGame.buildWell(int(message_split[1]), int(message_split[3]), int(message_split[2]), int(message_split[4]), int(message_split[5]))
            self.model.actualGame.soundMixer.playEffect('buildEffect')
        elif message_split[0] == "SBGo":
            self.model.actualGame.buildTemple(int(message_split[1]), int(message_split[3]), int(message_split[2]), int(message_split[4]), int(message_split[5]))
            self.model.actualGame.soundMixer.playEffect('buildEffect')
        elif message_split[0] == "SBM":
            self.model.actualGame.buildMarket(int(message_split[1]), int(message_split[3]), int(message_split[2]), int(message_split[4]), int(message_split[5]))
            self.model.actualGame.soundMixer.playEffect('buildEffect')

        # Walker - Appear tested
        elif message_split[0] == "WA":
            if message_split[1] == "0":
                Immigrant(self.model.actualGame.map[int(message_split[2])][int(message_split[3])], self.model.actualGame, self.model.actualGame.map[int(message_split[4])][int(message_split[5])],message_split[6])
            elif message_split[1] == "1":
                Engineer(self.model.actualGame.map[int(message_split[2])][int(message_split[3])], self.model.actualGame, self.model.actualGame.map[int(message_split[4])][int(message_split[5])],message_split[6])
            elif message_split[1] == "2":
                Prefet(self.model.actualGame.map[int(message_split[2])][int(message_split[3])], self.model.actualGame, self.model.actualGame.map[int(message_split[4])][int(message_split[5])],message_split[6])
            elif message_split[1] == "3":
                cartPusher = CartPusher(self.model.actualGame.map[int(message_split[2])][int(message_split[3])], self.model.actualGame, self.model.actualGame.map[int(message_split[4])][int(message_split[5])],message_split[6])
                Cart(self.model.actualGame.map[int(message_split[2])][int(message_split[3])], self.model.actualGame, cartPusher)
            elif message_split[1] == "4":
                Prefet(self.model.actualGame.map[int(message_split[2])][int(message_split[3])], self.model.actualGame, self.model.actualGame.map[int(message_split[4])][int(message_split[5])],message_split[6],message_split[7],message_split[8])
        elif message_split[0] == "WD":
            for walker in self.model.actualGame.walker:
                
