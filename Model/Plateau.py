import pygame
from Model.Zoom import Zoom
from Model.Camera import Camera
from Model.Case import Case
from View.Menu_map import Menu_map
from Model.Walker import *
from Model.control_panel import *
from Model.constants import *
from Model.Route import Route
from Model.Buildings.Building import BurningBuilding
from Model.Buildings.Building import DamagedBuilding
from Model.Buildings.House import House
from Model.Buildings.House import HousingSpot
from Model.Buildings.House import MergedHouse
from Model.Buildings.UrbanPlanning import Well
from Model.Buildings.UrbanPlanning import Senate
from Model.Buildings.UrbanPlanning import Temple
from Model.Buildings.UrbanPlanning import Colosseum
from Model.Buildings.RessourceBuilding import WheatFarm
from Model.Buildings.RessourceBuilding import WheatPlot
from Model.Buildings.RessourceBuilding import Granary
from Model.Buildings.RessourceBuilding import Market

from Model.Buildings.WorkBuilding import *
from Model.Controls import Controls
from Model.control_panel import TextRender
from Model.TopBar import TopBar
from Model.Foreground import Foreground
from Model.EmpireDate import EmpireDate
from Model.Sauvegarde import *
from random import *

counter=1

class Plateau():
    def __init__(self, screen, clock, name, heigth, width, soundMixer, nbr_cell_x=MAP_SIZE, nbr_cell_y=MAP_SIZE, attractiveness=0, listeCase=[], entities = [], structures = [], cityHousesList = [], cityHousingSpotsList = [], burningBuildings = []):
        
        self.screen = screen
        self.clock = clock
        self.minimalFont = pygame.font.SysFont(None, 20)
        self.soundMixer = soundMixer
        self.width, self.height = self.screen.get_size()
        self.camera = Camera(self.width, self.height)
        self.running = True
        self.zoomed = True
        self.menu_map = Menu_map(self.width,self.height)

        self.name = name
        self.heigthScreen = heigth
        self.widthScreen = width
        self.nbr_cell_x = nbr_cell_x
        self.nbr_cell_y = nbr_cell_y

        self.surface_cells = pygame.Surface((nbr_cell_x * cell_size * 2, nbr_cell_y * cell_size  + 2 * cell_size )).convert_alpha()
        

        #Load de tous les sprites
        self.image = self.load_cases_images()
        self.image_route = self.load_routes_images()
        self.image_walkers = self.load_walkers_images()
        self.image_structures = self.load_structures_images()
        self.road_warning_rectangle =load_image("image/UI/menu/roadWarning.png")
        self.loyalty_warning_rectangle =load_image("image/UI/menu/loyaltyWarning.png")

        self.zoom__=Zoom(self.image)

        self.attractiveness = attractiveness
        self.listeCase = listeCase
        self.treasury = START_TREASURY #Trésorerie
        self.population = [0,0,0,0] #Population
        self.empireDate = EmpireDate(self)
        self.roadWarning = False #Affiche un avertissement quand un bâtiment qui a besoin de la route est déconnecté
        self.loyaltyWarning = False #Affiche un avertissement quand un bâtiment a une loyauté faible et pourrait changer de camp
        self.loyAct = 0     #Timer pour l'actualisation de la loyauté
        self.load_savefile("DefaultMap.pickle")
        #Map du début
#       self.load_savefile("testx40.pickle")
        self.map = self.default_map()
        self.foreground = Foreground(self.screen, self.nbr_cell_x, self.nbr_cell_y)

        #Tableau contenant toutes les cases occupées par les walkers
        self.walkers = [[[] for x in range(self.nbr_cell_x)] for y in range(self.nbr_cell_y)]

        #Tableau contenant l'intégralité des walker présents sur la map
        self.entities = [] 

        #Tableau des collisions de la map (pour le moment la map ne contient pas de collision)
        self.collision_matrix = self.create_collision_matrix()

        #Tableau contenant l'intégralité des bâtiments présent sur la map
        self.structures = []
        self.cityHousesList = []
        self.cityHousingSpotsList = []
        self.burningBuildings = {1 : [], 2 : [], 3 : [], 4 : []}

        self.currentSpeed = 100
        self.buttonsFunctions = self.getButtonsFunctions()
        self.controls = Controls(self.screen, self.minimalFont, self.currentSpeed, self.buttonsFunctions, self.soundMixer)

        self.property = 1
        self.topbar = TopBar(self.screen, self.treasury[self.property-1], self.population[self.property-1], self.empireDate)
        self.topbarbol = False

        #Define the position of the button on the full panel button who won't change position after
        # overlays_button.change_pos(self.width-overlays_button.dim[0]-hide_control_panel_button.dim[0]-10,27)
        # hide_control_panel_button.change_pos(self.width-hide_control_panel_button.dim[0]-4,24+5)
        # advisors_button.change_pos(self.width-155,179)
        # empire_map_button.change_pos(self.width-78,179)
        # assignement_button.change_pos(self.width-155,208)
        # compass_button.change_pos(self.width-116,208)
        # arrow_rotate_counterclockwise.change_pos(self.width-78,208)
        # arrow_rotate_clockwise.change_pos(self.width-39,208)                
        # undo_button.change_pos(self.width-149,445)
        # message_view_button.change_pos(self.width-99,445)
        # see_recent_troubles_button.change_pos(self.width-49,445)

        self.pause = False
        self.restart = False
        global counter
        counter = 1
        self.overlayCounter = 0   
        self.property = 1 #ID player
        self.multiplayer = None
        self.modeText = "Singleplayer Mode"

    def save_game(self, filename):
        if filename.split(".")[-1] != "pickle":
            filename += ".pickle"
        print("saving game... in " + filename)
        save = Sauvegarde(self)
        save_object(save, filename)
        print("save !")

    def load_savefile(self, filename : str):
        save = load_object(filename)
        if save == "error":
            return "error"
        #============== CLEAR ==============#

        #Clear Buildings
        """for s in self.structures:
            s.delete()"""
        self.structures = []
        self.cityHousesList = []
        self.cityHousingSpotsList = []
        self.burningBuildings = {1 : [], 2 : [], 3 : [], 4 : []}

        #Clear Walkers
        """for e in self.entities:
            e.delete()"""
        self.walkers = [[[] for x in range(self.nbr_cell_x)] for y in range(self.nbr_cell_y)]
        self.entities = []
        #Clear Cases
        """for x in range(self.nbr_cell_x):
            for y in range(self.nbr_cell_y):
                if self.map[x][y].road :
                    self.map[x][y].road.delete()
                self.map[x][y].delete()"""
        self.map = []

        #============== LOAD ==============#

        # Cases
        for cell_x in range(self.nbr_cell_x):
            self.map.append([])
            for cell_y in range(self.nbr_cell_y):
                cells_to_map = self.cells_to_map(save.map[cell_x][cell_y]["x"], save.map[cell_x][cell_y]["y"], save.map[cell_x][cell_y]["sprite"], save.map[cell_x][cell_y]["indexSprite"])
                self.map[cell_x].append(cells_to_map)
                cells_to_map.feature = save.map[cell_x][cell_y]["feature"]
                #Surface cell
                render_pos = cells_to_map.render_pos
                self.surface_cells.blit(self.image["land"][1], (render_pos[0] + self.surface_cells.get_width()/2, render_pos[1]))
        #Routes
        for cell_x in range(self.nbr_cell_x):
            for cell_y in range(self.nbr_cell_y):
                if save.map[cell_x][cell_y]["road"]:
                    Route(self.map[cell_x][cell_y], self)
        #Buildings
        for s in save.structures:
            match(s["type"]):
                case "HousingSpot":
                    HousingSpot(self.map[s["x"]][s["y"]], self, s["type"], s["property"],s["nb_immigrant"])
                case "SmallTent" | "LargeTent":
                    House(self.map[s["x"]][s["y"]], self, s["size"], s["type"], s["entertainLvl"], s["wheat"], s["nbHab"], s["nbHabMax"], s["religiousAccess"], s["property"], s["fireRisk"], s["collapseRisk"])
                case "SmallTent2" | "LargeTent2" | "SmallShack" | "LargeShack":
                    MergedHouse(self.map[s["x"]][s["y"]], self, s["size"], s["type"],s["wheat"], s["nbHab"], [self.map[s["case1_x"]][s["case1_y"]], self.map[s["case2_x"]][s["case2_y"]], self.map[s["case3_x"]][s["case3_y"]]], s["property"], s["fireRisk"], s["collapseRisk"])
                case "Prefecture":
                    Prefecture(self.map[s["x"]][s["y"]], self, s["size"], s["type"], s["active"], s["property"], s["fireRisk"], s["collapseRisk"])
                case "EngineerPost":
                    EnginnerPost(self.map[s["x"]][s["y"]], self, s["size"], s["type"], s["active"], s["property"], s["fireRisk"], s["collapseRisk"])   
                case "Well":
                    Well(self.map[s["x"]][s["y"]], self, s["size"], s["type"],s["property"])
                case "BurningBuilding":
                    BurningBuilding(self.map[s["x"]][s["y"]], self, s["type"], s["size"], s["property"], s["fireRisk"], s["collapseRisk"], s["timeBurning"])
                case "Ruins" | "BurnedRuins":
                    DamagedBuilding(self.map[s["x"]][s["y"]], self, s["type"], s["size"], s["property"], s["fireRisk"], s["collapseRisk"])
                case "Senate" :
                    Senate(self.map[s["x"]][s["y"]], self, s["size"], s["type"],s["property"])
                case "WheatFarm" :
                    WheatFarm(self.map[s["x"]][s["y"]], self, s["size"], s["type"], s["property"], s["storedQuant"], s["growingQuant"])
                case "Market" :
                    Market(self.map[s["x"]][s["y"]], self, s["size"], s["type"], s["property"], s["storedWheat"])
                case "Granary" :
                    Granary(self.map[s["x"]][s["y"]], self, s["size"], s["type"], s["property"], s["storedWheat"])
                case "Temple" :
                    Temple(self.map[s["x"]][s["y"]], self, s["size"], s["type"], s["property"])
                case "Colosseum" :
                    Colosseum(self.map[s["x"]][s["y"]], self, s["size"], s["type"], s["property"])

        
        #Walker
        #Immigrant
        for e in save.entities:
            match(e["type"]):
                case "Citizen":
                    Citizen(self.map[e["x"]][e["y"]], self, e["name"], e["ttw"], e["action"], e["direction"], e["path"])
                case "Prefet":
                    Prefet(self.map[e["x"]][e["y"]], self,self.map[e["workplace_x"]][e["workplace_y"]].structure, e["name"], e["rest"], e["ttw"], e["action"], e["direction"], self.map[e["target_x"]][e["target_y"]].structure, e["path"])
                case "Engineer":
                    Engineer(self.map[e["x"]][e["y"]], self,self.map[e["workplace_x"]][e["workplace_y"]].structure, e["name"], e["rest"], e["ttw"], e["action"], e["direction"], e["path"])
                case "Immigrant":
                    Immigrant(self.map[e["x"]][e["y"]], self, self.map[e["target_x"]][e["target_y"]], e["name"], e["ttw"], e["action"], e["direction"], e["path"])
                case "CartPusher":
                    CartPusher(self.map[e["x"]][e["y"]], self,self.map[e["workplace_x"]][e["workplace_y"]].structure, e["name"], e["mode"], e["rest"], e["ttw"], e["action"], e["direction"], e["path"])
                case "MarketTrader":
                    MarketTrader(self.map[e["x"]][e["y"]], self,self.map[e["workplace_x"]][e["workplace_y"]].structure,e["mode"], e["wheat"], e["name"], e["rest"], e["ttw"], e["action"], e["direction"], e["path"])
        
        #Ville
        self.create_collision_matrix()
        self.attractiveness = save.attractiveness
        self.treasury = save.treasury
        self.population = save.population
        
    def default_map(self):
        '''Generate a map filled with grass'''
        self.map = []
        for cell_x in range(self.nbr_cell_x):
            self.map.append([])
            for cell_y in range(self.nbr_cell_y):
                sprite = self.choose_image()[0]
                cells_to_map = self.cells_to_map(cell_x, cell_y, sprite, randint(0, 57))
                self.map[cell_x].append(cells_to_map)
                render_pos = cells_to_map.render_pos
                self.surface_cells.blit(self.image["land"][1], (render_pos[0] + self.surface_cells.get_width()/2, render_pos[1]))
        return self.map

    
    def choose_image(self):
        image=""
        global counter
        if counter<=MAP_SIZE**2:
            image=["land"]
            counter+=1
        return image
    
    def cells_to_map(self, cell_x, cell_y, sprite, indexSprite):

        rectangle_cell = [
            (cell_x * cell_size , cell_y * cell_size ),
            (cell_x * cell_size  + cell_size , cell_y * cell_size ),
            (cell_x * cell_size  + cell_size , cell_y * cell_size  + cell_size ),
            (cell_x * cell_size , cell_y * cell_size  + cell_size )
        ]

        isometric_cell = [self.cartesian_to_isometric(x, y) for x, y in rectangle_cell]

        nouvelle_case = Case(cell_x, cell_y, rectangle_cell, isometric_cell, [min([x for x, y in isometric_cell]), min([y for x, y in isometric_cell])], sprite = sprite, indexSprite=indexSprite)
        return nouvelle_case
        
    def cartesian_to_isometric(self, x, y):
            return x - y,(x + y)/2

    def zoom(self,X__,bol):
        if bol:
            global cell_size
            global counter
            counter=1
            cell_size *= X__
            self.zoom__.set_zoom(X__)
            self.surface_cells.fill((0,0,0))
            self.surface_cells = pygame.Surface((self.nbr_cell_x * cell_size * 2, self.nbr_cell_y * cell_size + 2 * cell_size)).convert_alpha()
            self.map=self.default_map()

    def set_self_num(self):
        self.num=1
    def load_cases_images(self):

        land = list(load_image(f"image/Case/Lands/Land{i}.png") for i in range(58))

        tree = list(load_image(f"image/Case/Trees/Tree{i}.png") for i in range(32))

        rock = list(load_image(f"image/Case/Rocks/Rock{i}.png") for i in range(14))

        sign = list(load_image(f"image/Case/Signs/Land3a_000{i}.png") for i in range(87, 89))

        water = list(load_image(f"image/Case/Water/Water{i}.png") for i in range(37))

        red = pygame.image.load("image/C3/red.png").convert_alpha()
        red = pygame.transform.scale(red, (red.get_width() / 2, red.get_height() / 2))

        base_overlay = pygame.image.load("image/C3/Land2a_00004.png").convert_alpha()
        base_overlay = pygame.transform.scale(base_overlay, (base_overlay.get_width() / 2, base_overlay.get_height() / 2))

        return {"land" : land, "tree" : tree, "rock": rock, "water":water, "sign":sign, "red":red, "base_overlay":base_overlay}
    def load_routes_images(self):
        
        west = load_image("image/Routes/Land2a_00104.png")
        east = load_image("image/Routes/Land2a_00102.png")
        east_west = load_image("image/Routes/Land2a_00094.png")
        south = load_image("image/Routes/Land2a_00101.png")
        south_west = load_image("image/Routes/Land2a_00100.png")
        south_east = load_image("image/Routes/Land2a_00097.png")
        south_east_west = load_image("image/Routes/Land2a_00109.png")
        north = load_image("image/Routes/Land2a_00105.png")
        north_west = load_image("image/Routes/Land2a_00099.png")
        north_south = load_image("image/Routes/Land2a_00095.png")
        north_south_west = load_image("image/Routes/Land2a_00108.png")
        north_east = load_image("image/Routes/Land2a_00098.png")
        north_east_west = load_image("image/Routes/Land2a_00107.png")
        north_south_east = load_image("image/Routes/Land2a_00106.png")
        north_south_east_west = load_image("image/Routes/Land2a_00110.png")

        return {0: north, 1: west, 2: south, 3: south_west, 4: east, 5: east_west, 6: south_east,
                7: south_east_west, 8: north, 9: north_west, 10: north_south, 11: north_south_west,
                12: north_east, 13: north_east_west, 14: north_south_east, 15: north_south_east_west}
    def load_walkers_images(self):
        """walker_sprite[Type_Walker(String)][Action(Int)][Direction(Int)]""" #Directions : 1 -> North  2 -> East   3 -> South  4 -> West

        #====== Citizens ======#
        citizen = {1 : create_liste_sprites_walker("Citizen", "Walk", 12)}

        #====== Prefet ======#
        prefet = {1 : create_liste_sprites_walker("Prefet", "Walk", 12), 2 : create_liste_sprites_walker("Prefet", "FarmerWalk", 12), 3 : create_liste_sprites_walker("Prefet", "Throw", 6)}

        #====== Immigrant ======#
        immigrant = {1 : create_liste_sprites_walker("Immigrant", "Walk", 12)}

        #====== Chariot ======#
        chariot = {1 : create_liste_sprites_walker("Chariot", "Walk", 1)}

        #====== Engineer ======#
        engineer = {1 : create_liste_sprites_walker("Engineer", "Walk", 12)}

        #====== CartPusher ======#
        cartPusher = {1 : create_liste_sprites_walker("CartPusher", "Walk", 12)}

        #====== Cart ======#
        cart = {1 : create_liste_sprites_walker("Cart", "Empty", 1), 2 : create_liste_sprites_walker("Cart", "Full", 1)}

        #====== MarketTrader ======#
        marketTrader = {1 : create_liste_sprites_walker("MarketTrader", "Walk", 12)}

        return {"Citizen" : citizen, "Prefet" : prefet, "Immigrant" : immigrant, "Chariot" : chariot, "Engineer" : engineer, "CartPusher" : cartPusher, "Cart" : cart, "MarketTrader" : marketTrader}
    def load_structures_images(self):

        hss = load_image("image/Buildings/Housng1a_00045.png")
        st1s = load_image("image/Buildings/Housng1a_00001.png")
        st2s = load_image("image/Buildings/Housng1a_00005.png")
        lt1s = load_image("image/Buildings/Housng1a_00004.png")
        lt2s = load_image("image/Buildings/Housng1a_00006.png")
        sss = load_image("image/Buildings/Housng1a_00011.png")
        lss = load_image("image/Buildings/Housng1a_00017.png")
        ps = load_image("image/Buildings/Security_00001.png")
        eps = load_image("image/Buildings/transport_00056.png")
        ws = load_image("image/Buildings/Utilitya_00001.png")
        bsts = list(load_image(f"image/Buildings/BurningBuilding/BurningBuildingFrame{i}.png") for i in range(1, 9))
        burnruinss = load_image("image/Buildings/BurningBuilding/Land2a_00187.png")
        ruinss = load_image("image/Buildings/Land2a_00111.png")
        sens = load_image("image/Buildings/Govt_00004.png")
        whfas = load_image("image/Buildings/Farm/Commerce_00012.png")
        whpls = list(load_image(f"image/Buildings/Farm/Plot{i}.png") for i in range(0,5))
        marks = load_image("image/Buildings/Commerce_00001.png")
        granatops = load_image("image/Buildings/Granary/Gtop.png")
        granabases = load_image("image/Buildings/Granary/Gbase.png")
        granabs = list(load_image(f"image/Buildings/Granary/b{i}.png")for i in range(0,4))
        granals = list(load_image(f"image/Buildings/Granary/l{i}.png")for i in range(0,7))
        temples = list(load_image(f"image/Buildings/Security_000{i}.png") for i in range(11,15))
        colosseums = load_image("image/Buildings/entertainment_00036.png")
        

        return {"HousingSpot" : hss, "SmallTent" : st1s, "SmallTent2" : st2s, "LargeTent" : lt1s, "LargeTent2" : lt2s, "Prefecture" : ps, "EngineerPost" : eps, "Well" : ws, 
                "BurningBuilding" : bsts, "Ruins" : ruinss, "BurnedRuins" : burnruinss, "Senate" : sens, "WheatFarm" : whfas, "WheatPlot" : whpls, "Market" : marks, "GranaryTop" : granatops,
                "GranaryBase" : granabases, "GranaryRoom" : granabs, "GranaryLev" : granals, "Temple" : temples, "SmallShack" : sss, "LargeShack" : lss, "Colosseum" : colosseums }
 
    def getButtonsFunctions(self):
        return {
            'increaseSpeed': self.increaseSpeed,
            'decreaseSpeed': self.decreaseSpeed,
        }

    def increaseSpeed(self):
        if self.currentSpeed >= 0 and self.currentSpeed < 500:
            if self.currentSpeed >= 100:
                self.currentSpeed += 100
            else: 
                self.currentSpeed += 10 

        self.soundMixer.playEffect("clickEffect")
    
    def decreaseSpeed(self):
        if self.currentSpeed > 10:
            if self.currentSpeed > 100:
                self.currentSpeed -= 100
            else:
                self.currentSpeed -= 10 
        self.soundMixer.playEffect("clickEffect")

    def clearLand(self, grid_x1, grid_x2, grid_y1, grid_y2, property):
        for xi in range(grid_x1, grid_x2+1):
                for yi in range(grid_y1, grid_y2+1):
                        if self.map[xi][yi].sprite not in list_of_undestructible:
                            if self.map[xi][yi].sprite != "land":
                                self.map[xi][yi].sprite = "land"
                                self.map[xi][yi].indexSprite = randint(0, 57)
                            if self.map[xi][yi].road and self.map[xi][yi].road.property == property:
                                self.map[xi][yi].road.delete()
                                self.treasury[self.property-1] = self.treasury[self.property-1] - DESTRUCTION_COST
                            if self.map[xi][yi].structure and self.map[xi][yi].structure.property == property :
                                if self.map[xi][yi].structure.desc != "BurningBuilding" :
                                    self.map[xi][yi].structure.delete()
                                    self.treasury[self.property-1] = self.treasury[self.property-1] - DESTRUCTION_COST
                                   
        self.collision_matrix = self.create_collision_matrix()
        self.foreground.initForegroundGrid()

    def buildRoads(self, pattern, grid_x1, grid_x2, grid_y1, grid_y2, property):
        match(pattern):
            case 0:
                for xi in range(grid_x1, grid_x2+1):
                    if self.map[xi][grid_y2].road == None and self.map[xi][grid_y2].structure == None and self.map[xi][grid_y2].sprite not in list_of_collision:
                        Route(self.map[xi][grid_y2], self, property)

                for yi in range(grid_y1, grid_y2+1):
                    if self.map[grid_x1][yi].road == None and self.map[grid_x1][yi].structure == None and self.map[grid_x1][yi].sprite not in list_of_collision:
                        Route(self.map[grid_x1][yi], self, property)
            case 1:
                for xi in range(grid_x1, grid_x2-1, -1):
                    if self.map[xi][grid_y1].road == None and self.map[xi][grid_y1].structure == None and self.map[xi][grid_y1].sprite not in list_of_collision:
                        Route(self.map[xi][grid_y1], self, property)
                for yi in range(grid_y1, grid_y2+1):
                    if self.map[grid_x2][yi].road == None and self.map[grid_x2][yi].structure == None and self.map[grid_x2][yi].sprite not in list_of_collision:
                        Route(self.map[grid_x2][yi], self, property)
            case 2:
                for xi in range(grid_x1, grid_x2+1):
                    if self.map[xi][grid_y1].road == None and self.map[xi][grid_y1].structure == None and self.map[xi][grid_y1].sprite not in list_of_collision:
                        Route(self.map[xi][grid_y1], self, property)
                for yi in range(grid_y1, grid_y2-1, -1):
                    if self.map[grid_x2][yi].road == None and self.map[grid_x2][yi].structure == None and self.map[grid_x2][yi].sprite not in list_of_collision:
                        Route(self.map[grid_x2][yi], self, property)
            case 3:
                for xi in range(grid_x1, grid_x2-1, -1):
                    if self.map[xi][grid_y2].road == None and self.map[xi][grid_y2].structure == None and self.map[xi][grid_y2].sprite not in list_of_collision:
                        Route(self.map[xi][grid_y2], self, property)
                for yi in range(grid_y1, grid_y2-1, -1):
                    if self.map[grid_x1][yi].road == None and self.map[grid_x1][yi].structure == None and self.map[grid_x1][yi].sprite not in list_of_collision:
                        Route(self.map[grid_x1][yi], self, property)
        
        self.collision_matrix = self.create_collision_matrix()

    def buildHousingSpot(self, grid_x1, grid_x2, grid_y1, grid_y2, property):
        for xi in range(grid_x1, grid_x2+1):
            for yi in range(grid_y1, grid_y2+1):
                for xcr in range (xi-2,xi+3,1) :
                    for ycr in range (yi-2,yi+3,1) :
                        if 0<=xcr<self.nbr_cell_x and 0<=ycr<self.nbr_cell_y:
                            if not self.map[xi][yi].road and not self.map[xi][yi].structure and self.map[xi][yi].sprite not in list_of_collision and self.map[xi][yi].sprite not in list_of_undestructible:
                                if self.map[xcr][ycr].road :
                                    if self.treasury[self.property-1] > HOUSE_COST :
                                        HousingSpot(self.map[xi][yi], self, property=property)
    
    def buildPrefecture(self, grid_x1, grid_x2, grid_y1, grid_y2, property):
        for xi in range(grid_x1, grid_x2+1):
            for yi in range(grid_y1, grid_y2+1):
                if self.map[xi][yi].getConnectedToRoad() > 0 :
                    if not self.map[xi][yi].road and not self.map[xi][yi].structure and self.map[xi][yi].sprite not in list_of_collision:
                        if self.treasury[self.property-1] > PREFECTURE_COST :
                            Prefecture(self.map[xi][yi],self,(1,1),"Prefecture",1, property)

    def buildEngineerPost(self, grid_x1, grid_x2, grid_y1, grid_y2, property):
        for xi in range(grid_x1, grid_x2+1):
            for yi in range(grid_y1, grid_y2+1):
                if self.map[xi][yi].getConnectedToRoad() > 0 :
                    if not self.map[xi][yi].road and not self.map[xi][yi].structure and self.map[xi][yi].sprite not in list_of_collision:
                        if self.treasury[self.property-1] > ENGINEERPOST_COST :
                            EnginnerPost(self.map[xi][yi],self,(1,1),"EngineerPost",1, property)
    
    def buildWell(self, grid_x1, grid_x2, grid_y1, grid_y2, property):
        for xi in range(grid_x1, grid_x2+1):
                for yi in range(grid_y1, grid_y2+1):
                    if not self.map[xi][yi].road and not self.map[xi][yi].structure and self.map[xi][yi].sprite not in list_of_collision:
                        if self.treasury[self.property-1] > WELL_COST :
                            Well(self.map[xi][yi],self,(1,1),"Well", property)
    
    def buildSenate(self, grid_x1, grid_x2, grid_y1, grid_y2, property):
        for xi in range(grid_x1, grid_x2+1):
            for yi in range(grid_y1, grid_y2+1):
                for xccl in range(xi, xi+5, 1) :
                    for yccl in range(yi, yi-5, -1 ) :
                        if self.map[xccl][yccl].road or self.map[xccl][yccl].structure or self.map[xccl][yccl].sprite in list_of_collision:
                            return
        #Vérifier qu'on a pas déjà un Sénat
        for ms in self.structures :
            if ms.desc == "Senate" and ms.property == self.property:
                return
        if self.treasury[self.property-1] > SENATE_COST :
            Senate(self.map[xi][yi],self,(5,5),"Senate", property)

    def buildFarm(self, grid_x1, grid_x2, grid_y1, grid_y2, property):
        #Vérifier que toutes les cases sont disponibles :
        for xi in range(grid_x1, grid_x2+1):
            for yi in range(grid_y1, grid_y2+1):
                for xccl in range(xi-1, xi+2, 1) :
                    for yccl in range(yi-1, yi+2, 1 ) :
                        if self.map[xccl][yccl].road or self.map[xccl][yccl].structure or self.map[xccl][yccl].sprite in list_of_collision:
                            return
        if self.treasury[self.property-1] > WHEATFARM_COST :
            WheatFarm(self.map[xi][yi],self,(2,2),"WheatFarm", property)
            
    def buildGranary(self, grid_x1, grid_x2, grid_y1, grid_y2, property):
        #Vérifier que toutes les cases sont disponibles :
        for xi in range(grid_x1, grid_x2+1):
            for yi in range(grid_y1, grid_y2+1):
                for xccl in range(xi, xi-3, -1) :
                    for yccl in range(yi, yi-3, -1 ) :
                        if self.map[xccl][yccl].road or self.map[xccl][yccl].structure or self.map[xccl][yccl].sprite in list_of_collision:
                            return
        if self.treasury[self.property-1] > GRANARY_COST :
            Granary(self.map[xi][yi],self,(3,3),"Granary", property)
            
    def buildMarket(self, grid_x1, grid_x2, grid_y1, grid_y2, property):
        for xi in range(grid_x1, grid_x2+1):
            for yi in range(grid_y1, grid_y2+1):
                for xccl in range(xi, xi+2, 1) :
                    for yccl in range(yi, yi-2, -1 ) :
                        if self.map[xccl][yccl].road or self.map[xccl][yccl].structure or self.map[xccl][yccl].sprite in list_of_collision:
                            return
        if self.treasury[self.property-1] > MARKET_COST :
            Market(self.map[xi][yi],self,(2,2),"Market", property)

    def buildTemple(self, grid_x1, grid_x2, grid_y1, grid_y2, property):
        #Vérifier que toutes les cases sont disponibles :
        for xi in range(grid_x1, grid_x2+1):
            for yi in range(grid_y1, grid_y2+1):
                for xccl in range(xi, xi+2, 1) :
                    for yccl in range(yi, yi-2, -1 ) :
                        if self.map[xccl][yccl].road or self.map[xccl][yccl].structure or self.map[xccl][yccl].sprite in list_of_collision:
                            return
        if self.treasury[self.property-1] > TEMPLE_COST :
            Temple(self.map[xi][yi],self,(2,2),"Temple", property)

    def buildColosseum(self, grid_x1, grid_x2, grid_y1, grid_y2, property):
        for xi in range(grid_x1, grid_x2+1):
            for yi in range(grid_y1, grid_y2+1):
                for xccl in range(xi, xi+5, 1) :
                    for yccl in range(yi, yi-5, -1 ) :
                        if self.map[xccl][yccl].road or self.map[xccl][yccl].structure or self.map[xccl][yccl].sprite in list_of_collision:
                            return
        #Vérifier que personne n'a construit un sanctuaire
        for ms in self.structures :
            if ms.desc == "Sanctuary":
                return
        if self.treasury[self.property-1] > COLOSSEUM_COST :
            Colosseum(self.map[xi][yi],self,(5,5),"Colosseum", property)

    def update(self):
        if self.restart:

            self.entities.clear()
            self.listeCase.clear()
            self.structures.clear()
            self.cityHousesList.clear()
            self.cityHousingSpotsList.clear()
            self.burningBuildings.clear()

        if not self.pause:
            
            self.camera.update()
            self.controls.update(self.currentSpeed)
            self.topbar.update(self.treasury[self.property-1], self.population[self.property-1], self.empireDate)

            #Update de la position des walkers
            currentSpeedFactor = self.currentSpeed/100
            for e in self.entities: e.update(currentSpeedFactor)
            for hs in self.cityHousingSpotsList: hs.generateImmigrant(currentSpeedFactor)
            for i in range(1, 4):
                for bb in self.burningBuildings[i]: bb.update(currentSpeedFactor)
            self.roadWarning=False
            self.loyaltyWarning=False
            if self.loyAct >= 1000 :        #On actualise la loyauté seulement tous les 1000 ticks sinon le jeu tourne à 3 FPS
                self.loyAct = 0
                self.actualizeInf()
            else : self.loyAct = self.loyAct+1
            for b in self.structures :
                if isinstance(b,Building) : 
                    b.riskCheck(self.currentSpeed)   # Vérifie et incrémente les risques d'incendies et d'effondrement
                    b.loyaltyUpdate()                # Vérifie la loyauté du bâtiment
                if isinstance(b,WorkBuilding): b.delay()
                if isinstance(b,WheatFarm) or isinstance(b,Granary) or isinstance(b,Market ) : b.update(self.currentSpeed)     #Actualize Food Chain Buildings
                self.nearbyRoadsCheck(b)                    #Supprime les maisons/hs et désactive les wb s'il ne sont pas connectés à la route
            self.population[self.property-1] = 0
            for h in self.cityHousesList:
                h.udmCheck()   # Vérifie les upgrades, downgrades et merge d'habitations
                if h.property == self.property :
                    self.population[self.property-1] = self.population[self.property-1] + h.nbHab
            self.empireDate.update()

    def nearbyRoadsCheck(self, b):     #Supprime les maisons/hs et désactive les wb s'il ne sont pas connectés à la route
        for xcr in range (b.case.x-2,b.case.x+3,1) :
            for ycr in range (b.case.y-2,b.case.y+3,1) :
                    if 0<=xcr<self.nbr_cell_x and 0<=ycr<self.nbr_cell_y:
                        if self.map[xcr][ycr].road :
                            return
        
        if isinstance(b,HousingSpot) or isinstance(b,House) :
            b.delete()
        if isinstance(b,WorkBuilding) and b.active==True :
            b.active = False

    def actualizeInf(self) :
        for x in range(self.nbr_cell_x):
            for y in range(self.nbr_cell_y):
                self.map[x][y].setPlayerInfluence(self, self.property)

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.surface_cells, (self.camera.vect.x, self.camera.vect.y))

        # UPDATE RISK VALUE
        # DRAW OVERLAY
        # Overlay part
        # Fire
        # Hidding the overlay by default
        if self.overlayCounter == 30:
            if self.foreground.getOverlayName() == "fire":
                self.foreground.initOverlayGrid()
                for x in range(MAP_SIZE):
                    for y in range(MAP_SIZE):
                        temp = self.map[x][y].structure
                        if isinstance(temp, Building) and not isinstance(temp, BurningBuilding):
                            self.foreground.addOverlayInfo(x, y, temp.get_fireRisk())
                self.controls.overlays_button.change_image("image/UI/menu/menu_fire_overlay.png")       

            elif self.foreground.getOverlayName() == "destruct":
                self.foreground.initOverlayGrid()
                for x in range(MAP_SIZE):
                    for y in range(MAP_SIZE):
                        temp = self.map[x][y].structure
                        if isinstance(temp, Building) and not isinstance(temp, BurningBuilding):
                            self.foreground.addOverlayInfo(x, y, temp.get_collapseRisk())
                self.controls.overlays_button.change_image("image/UI/menu/menu_collapse_overlay.png")

            elif self.foreground.getOverlayName() == "influence":
                self.foreground.initOverlayGrid()
                for x in range(MAP_SIZE):
                    for y in range(MAP_SIZE):
                        temp = self.map[x][y]
                        self.foreground.addOverlayInfo(x, y, temp.getInfluenceDifIndex())
                self.controls.overlays_button.change_image("image/UI/menu/menu_influence_overlay.png")       
            
            elif self.foreground.getOverlayName() == None:
                self.controls.overlays_button.change_image("image/UI/menu/menu_overlay_button.png")       

            self.overlayCounter = 0

        sprite = "base_overlay"

        # DRAW CELLS

        for cell_x in range(self.nbr_cell_x):
            for cell_y in range(self.nbr_cell_y):
                render_pos =  self.map[cell_x][cell_y].render_pos
                id_image = None
                image = None
                # DRAW DEFAULT CELLS
                if not self.map[cell_x][cell_y].road and not self.map[cell_x][cell_y].structure:
                    id_image = self.map[cell_x][cell_y].sprite
                    index_image = self.map[cell_x][cell_y].indexSprite
                    if type(id_image) != str:
                        print("id_image is not a string:", id_image)
                    image = self.image[id_image][index_image]
                    self.screen.blit(image,
                                (render_pos[0] + self.surface_cells.get_width()/2 + self.camera.vect.x,
                                render_pos[1] - (image.get_height() - cell_size) + self.camera.vect.y))
                
                # DRAW ROADS
                if self.map[cell_x][cell_y].road:
                    id_image = self.map[cell_x][cell_y].road.sprite
                    image = self.image_route[id_image]
                    self.screen.blit(image,
                                    (render_pos[0] + self.surface_cells.get_width()/2 + self.camera.vect.x,
                                    render_pos[1] - (image.get_height() - cell_size) + self.camera.vect.y))
                # DRAW OVERLAY
                elif self.foreground.getOverlayInfo(cell_x, cell_y) != None:
                    match self.foreground.getOverlayInfo(cell_x, cell_y):
                        case 0:
                            effectedImage = self.foreground.putGreen(self.image[sprite].copy())
                            self.screen.blit(effectedImage,
                                            ([min([x for x, y in self.map[cell_x][cell_y].isometric_cell]), min([y for x, y in self.map[cell_x][cell_y].isometric_cell])][0] + self.surface_cells.get_width()/2 + self.camera.vect.x,
                                            [min([x for x, y in self.map[cell_x][cell_y].isometric_cell]), min([y for x, y in self.map[cell_x][cell_y].isometric_cell])][1] - (self.image[sprite].get_height() - cell_size) + self.camera.vect.y))
                        
                        case 1:
                            effectedImage = self.foreground.putGreenYellow(self.image[sprite].copy())
                            self.screen.blit(effectedImage,
                                            ([min([x for x, y in self.map[cell_x][cell_y].isometric_cell]), min([y for x, y in self.map[cell_x][cell_y].isometric_cell])][0] + self.surface_cells.get_width()/2 + self.camera.vect.x,
                                            [min([x for x, y in self.map[cell_x][cell_y].isometric_cell]), min([y for x, y in self.map[cell_x][cell_y].isometric_cell])][1] - (self.image[sprite].get_height() - cell_size) + self.camera.vect.y))
                        
                        case 2:
                            effectedImage = self.foreground.putYellow(self.image[sprite].copy())
                            self.screen.blit(effectedImage,
                                            ([min([x for x, y in self.map[cell_x][cell_y].isometric_cell]), min([y for x, y in self.map[cell_x][cell_y].isometric_cell])][0] + self.surface_cells.get_width()/2 + self.camera.vect.x,
                                            [min([x for x, y in self.map[cell_x][cell_y].isometric_cell]), min([y for x, y in self.map[cell_x][cell_y].isometric_cell])][1] - (self.image[sprite].get_height() - cell_size) + self.camera.vect.y))
                        
                        case 3:
                            effectedImage = self.foreground.putYellowOrange(self.image[sprite].copy())
                            self.screen.blit(effectedImage,
                                            ([min([x for x, y in self.map[cell_x][cell_y].isometric_cell]), min([y for x, y in self.map[cell_x][cell_y].isometric_cell])][0] + self.surface_cells.get_width()/2 + self.camera.vect.x,
                                            [min([x for x, y in self.map[cell_x][cell_y].isometric_cell]), min([y for x, y in self.map[cell_x][cell_y].isometric_cell])][1] - (self.image[sprite].get_height() - cell_size) + self.camera.vect.y))
                        
                        case 4:
                            effectedImage = self.foreground.putOrange(self.image[sprite].copy())
                            self.screen.blit(effectedImage,
                                            ([min([x for x, y in self.map[cell_x][cell_y].isometric_cell]), min([y for x, y in self.map[cell_x][cell_y].isometric_cell])][0] + self.surface_cells.get_width()/2 + self.camera.vect.x,
                                            [min([x for x, y in self.map[cell_x][cell_y].isometric_cell]), min([y for x, y in self.map[cell_x][cell_y].isometric_cell])][1] - (self.image[sprite].get_height() - cell_size) + self.camera.vect.y))
                        
                        case 5:
                            effectedImage = self.foreground.putOrangeRed(self.image[sprite].copy())
                            self.screen.blit(effectedImage,
                                            ([min([x for x, y in self.map[cell_x][cell_y].isometric_cell]), min([y for x, y in self.map[cell_x][cell_y].isometric_cell])][0] + self.surface_cells.get_width()/2 + self.camera.vect.x,
                                            [min([x for x, y in self.map[cell_x][cell_y].isometric_cell]), min([y for x, y in self.map[cell_x][cell_y].isometric_cell])][1] - (self.image[sprite].get_height() - cell_size) + self.camera.vect.y))

                        case 6:
                            effectedImage = self.foreground.putRed(self.image[sprite].copy())
                            self.screen.blit(effectedImage,
                                            ([min([x for x, y in self.map[cell_x][cell_y].isometric_cell]), min([y for x, y in self.map[cell_x][cell_y].isometric_cell])][0] + self.surface_cells.get_width()/2 + self.camera.vect.x,
                                            [min([x for x, y in self.map[cell_x][cell_y].isometric_cell]), min([y for x, y in self.map[cell_x][cell_y].isometric_cell])][1] - (self.image[sprite].get_height() - cell_size) + self.camera.vect.y))

                        case -1:
                            effectedImage = self.foreground.putGrey(self.image[sprite].copy())
                            self.screen.blit(effectedImage,
                                            ([min([x for x, y in self.map[cell_x][cell_y].isometric_cell]), min([y for x, y in self.map[cell_x][cell_y].isometric_cell])][0] + self.surface_cells.get_width()/2 + self.camera.vect.x,
                                            [min([x for x, y in self.map[cell_x][cell_y].isometric_cell]), min([y for x, y in self.map[cell_x][cell_y].isometric_cell])][1] - (self.image[sprite].get_height() - cell_size) + self.camera.vect.y))

                # DRAW DEFAULT CELLS   
                elif not self.map[cell_x][cell_y].road and not self.map[cell_x][cell_y].structure:
                    id_image = self.map[cell_x][cell_y].sprite
                    index_image = self.map[cell_x][cell_y].indexSprite
                    image = self.image[id_image][index_image]
                    self.screen.blit(image,
                                (render_pos[0] + self.surface_cells.get_width()/2 + self.camera.vect.x,
                                render_pos[1] - (image.get_height() - cell_size) + self.camera.vect.y))
                    
                # DRAW STRUCTURES
                elif isinstance(self.map[cell_x][cell_y].structure, BurningBuilding):
                    self.screen.blit(self.image_structures["BurningBuilding"][int(self.map[cell_x][cell_y].structure.index_sprite)], 
                                (render_pos[0] + self.surface_cells.get_width()/2 + self.camera.vect.x,
                                    render_pos[1] - (self.image_structures["BurningBuilding"][int(self.map[cell_x][cell_y].structure.index_sprite)].get_height() - cell_size) + self.camera.vect.y))
                elif isinstance(self.map[cell_x][cell_y].structure, WheatPlot):
                    self.screen.blit(self.image_structures["WheatPlot"][self.map[cell_x][cell_y].structure.level], 
                                    (render_pos[0] + self.surface_cells.get_width()/2 + self.camera.vect.x,
                                        render_pos[1] - (self.image_structures["WheatPlot"][self.map[cell_x][cell_y].structure.level].get_height() - cell_size) + self.camera.vect.y))
                
                elif isinstance(self.map[cell_x][cell_y].structure, Granary):
                    if self.map[cell_x][cell_y].structure.case == self.map[cell_x][cell_y] :
                        self.screen.blit(self.image_structures["GranaryBase"], 
                                        (render_pos[0] + self.surface_cells.get_width()/2 + self.camera.vect.x -55 ,    #-55
                                            render_pos[1] - (self.image_structures["GranaryBase"].get_height() - cell_size) + self.camera.vect.y)) #+50
                    
                        self.screen.blit(self.image_structures["GranaryTop"], 
                                            (render_pos[0] + self.surface_cells.get_width()/2 + self.camera.vect.x - 25, #-5
                                            render_pos[1] - (self.image_structures["GranaryTop"].get_height() - cell_size) + self.camera.vect.y-10)) #+35
                        """    
                            for gl in range(0,self.map[cell_x][cell_y].structure.levelB) :
                                self.screen.blit(self.image_structures["GranaryRoom"][gl], 
                                            (render_pos[0] + self.surface_cells.get_width()/2 + self.camera.vect.x,
                                                render_pos[1] - (self.image_structures["GranaryRoom"][gl].get_height() - cell_size) + self.camera.vect.y))
                        """
                        self.screen.blit(self.image_structures["GranaryLev"][self.map[cell_x][cell_y].structure.levelV], 
                                        (render_pos[0] + self.surface_cells.get_width()/2 + self.camera.vect.x +25,
                                            render_pos[1] - (self.image_structures["GranaryLev"][self.map[cell_x][cell_y].structure.levelV].get_height() - cell_size) + self.camera.vect.y))

                        #storedQuantTxt = TextRender(str(self.map[cell_x][cell_y].structure.storedWheat),(20,20),(0,0,0)).img_scaled
                        #self.screen.blit(storedQuantTxt,(render_pos[0] + self.surface_cells.get_width()/2 + self.camera.vect.x,
                        #                    render_pos[1] - (self.image_structures["GranaryTop"].get_height() - cell_size) + self.camera.vect.y))
                                    
                elif isinstance(self.map[cell_x][cell_y].structure, Temple) :
                    if self.map[cell_x][cell_y].structure.case == self.map[cell_x][cell_y] :
                        self.screen.blit(self.image_structures["Temple"][self.map[cell_x][cell_y].structure.property-1], 
                                        (render_pos[0] + self.surface_cells.get_width()/2 + self.camera.vect.x,
                                            render_pos[1] - (self.image_structures["Temple"][self.map[cell_x][cell_y].structure.property-1].get_height() - cell_size) + self.camera.vect.y))
                    
                elif self.map[cell_x][cell_y].structure.case == self.map[cell_x][cell_y] :
                    id_image = self.map[cell_x][cell_y].structure.desc
                    original_image = self.image_structures[id_image]
                    image = original_image.copy()

                    filt = pygame.Surface(image.get_size(), pygame.SRCALPHA)
                    if self.map[cell_x][cell_y].structure.property == 1:
                        filt.fill((255, 255, 255, 255))
                    elif self.map[cell_x][cell_y].structure.property == 2:
                        filt.fill((255, 155, 155, 255))
                    elif self.map[cell_x][cell_y].structure.property == 3:
                        filt.fill((155, 255, 155, 255))
                    elif self.map[cell_x][cell_y].structure.property == 4:
                        filt.fill((155, 155, 255, 255))

                    filtered_image = image.copy()
                    filtered_image.blit(filt, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

                    self.screen.blit(
                        filtered_image,
                        (render_pos[0] + self.surface_cells.get_width()/2 + self.camera.vect.x,
                        render_pos[1] - (filtered_image.get_height() - cell_size) + self.camera.vect.y)
                    )

                    #if isinstance(self.map[cell_x][cell_y].structure, House) :
                    #    nbHabTxt = TextRender(str(self.map[cell_x][cell_y].structure.nbHab),(20,20),(0,0,0)).img_scaled
                    #    self.screen.blit(nbHabTxt,(render_pos[0] + self.surface_cells.get_width()/2 + self.camera.vect.x,
                    #                        render_pos[1] - (self.image_structures[id_image].get_height() - cell_size) + self.camera.vect.y))
                    #if isinstance(self.map[cell_x][cell_y].structure, WheatFarm) :
                    #    grQuantTxt = TextRender(str(self.map[cell_x][cell_y].structure.growingQuant),(20,20),(0,0,0)).img_scaled
                    #    self.screen.blit(grQuantTxt,(render_pos[0] + self.surface_cells.get_width()/2 + self.camera.vect.x,
                    #                        render_pos[1] - (self.image_structures[id_image].get_height() - cell_size) + self.camera.vect.y))

                # DRAW PREVIEWED CELLS AND HOVERED CELLS
                if not self.pause: 
                    if self.foreground.hasEffect(cell_x, cell_y) and image != None:
                        effectedImage = self.foreground.getEffectedImage(id_image, image.copy(), cell_x, cell_y)
                        self.screen.blit(effectedImage,
                                        (render_pos[0] + self.surface_cells.get_width()/2 + self.camera.vect.x,
                                        render_pos[1] - (effectedImage.get_height() - cell_size) + self.camera.vect.y))

                # DRAW WALKERS
                for e in self.walkers[cell_x][cell_y]:
                    self.screen.blit(self.image_walkers[e.type][e.action][e.direction][int(e.index_sprite)],
                                        (render_pos[0] + self.surface_cells.get_width()/2 + self.camera.vect.x,
                                            render_pos[1] - (self.image_walkers[e.type][e.action][e.direction][int(e.index_sprite)].get_height() - cell_size) + self.camera.vect.y))
                
        
        self.overlayCounter += 1    
        self.topbar.render()
        self.controls.render()
     
        if self.roadWarning : self.screen.blit(self.road_warning_rectangle,(500,30))
        if self.loyaltyWarning : self.screen.blit(self.loyalty_warning_rectangle,(500,30))

        fpsText = self.minimalFont.render(f"FPS: {self.clock.get_fps():.0f}", 1, (255, 255, 255), (0, 0, 0))
        propertyText = self.minimalFont.render(f"Player: {self.property}", 1, (255, 255, 255), (0, 0, 0))

        self.screen.blit(fpsText, (0, self.screen.get_height() - fpsText.get_height()))
        self.screen.blit(propertyText, (0, self.screen.get_height() - fpsText.get_height() - propertyText.get_height()))
        self.screen.blit(self.minimalFont.render(self.modeText, 1, (255, 255, 255), (0, 0, 0)), (0, self.screen.get_height() - fpsText.get_height() - propertyText.get_height() - 20))

        # if state_control_panel=="reduced":

        #     self.screen.blit(small_gap_menu.img_scaled, (self.width-small_gap_menu.dim[0], 24))


        #     display_control_panel_button.update()
        #     display_control_panel_button.change_pos(self.width-display_control_panel_button.dim[0]-5,28)
        #     display_control_panel_button.draw(self.screen)

        #     build_housing_button.update()
        #     build_housing_button.change_pos(self.width-build_housing_button.dim[0]-1,24+32)
        #     build_housing_button.draw(self.screen)

        #     clear_land_button.update()
        #     clear_land_button.change_pos(self.width-clear_land_button.dim[0]-1,24+67)
        #     clear_land_button.draw(self.screen)

        #     build_roads_button.update()
        #     build_roads_button.change_pos(self.width-build_roads_button.dim[0]-1,24+102)
        #     build_roads_button.draw(self.screen)


        #     water_related_structures.update()
        #     water_related_structures.change_pos(self.width-water_related_structures.dim[0]-1,24+137)
        #     water_related_structures.draw(self.screen)

        #     health_related_structures.update()
        #     health_related_structures.change_pos(self.width-health_related_structures.dim[0]-1,24+172)
        #     health_related_structures.draw(self.screen)

        #     religious_structures.update()
        #     religious_structures.change_pos(self.width-religious_structures.dim[0]-1,24+207)
        #     religious_structures.draw(self.screen)

        #     education_structures.update()
        #     education_structures.change_pos(self.width-education_structures.dim[0]-1,24+242)
        #     education_structures.draw(self.screen)

        #     entertainment_structures.update()
        #     entertainment_structures.change_pos(self.width-entertainment_structures.dim[0]-1,24+277)
        #     entertainment_structures.draw(self.screen)

        #     administration_or_government_structures.update()
        #     administration_or_government_structures.change_pos(self.width-administration_or_government_structures.dim[0]-1,24+312)
        #     administration_or_government_structures.draw(self.screen)

        #     engineering_structures.update()
        #     engineering_structures.change_pos(self.width-engineering_structures.dim[0]-1,24+347)
        #     engineering_structures.draw(self.screen)

        #     security_structures.update()
        #     security_structures.change_pos(self.width-security_structures.dim[0]-1,24+382)
        #     security_structures.draw(self.screen)

        #     industrial_structures.update()
        #     industrial_structures.change_pos(self.width-industrial_structures.dim[0]-1,24+417)
        #     industrial_structures.draw(self.screen)


    def create_collision_matrix(self):
        collision_matrix = [[1000 for x in range(self.nbr_cell_x)] for y in range(self.nbr_cell_y)]
        #La suite sera pour quand on aura un système de collision
        for x in range(self.nbr_cell_x):
            for y in range(self.nbr_cell_y):
                if self.map[x][y].collision:
                    collision_matrix[y][x] = 0
                if self.map[x][y].road:
                    collision_matrix[y][x] = 1
        return collision_matrix

    def draw_menu_File(self):
        if self.topbar.File_bol:
            self.screen.blit(self.topbar.File_menu_Rm, self.topbar.File_menu_Rm_rect)
            self.screen.blit(self.topbar.File_menu_Sg, self.topbar.File_menu_Sg_rect)
            self.screen.blit(self.topbar.File_menu_Eg, self.topbar.File_menu_Eg_rect)

def load_image(path):
    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(image, (image.get_width() / 2, image.get_height() / 2))

def create_liste_sprites_walker(type, action, nb_frame):
    direction = {1 : "UpRight", 2 : "DownRight", 3 : "DownLeft", 4 : "UpLeft"}
    return {j : list(load_image(f"image/Walkers/{type}/{action}/{direction[j]}/{type}{action}{direction[j]}Frame{i}.png") for i in range(1, nb_frame+1)) for j in range(1, 5)}
