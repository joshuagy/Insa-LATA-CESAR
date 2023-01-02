import pygame
from Model.Zoom import Zoom
from Model.Camera import Camera
from Model.Case import Case
from View.Menu_map import Menu_map
from Model.Walker import Walker
from Model.control_panel import *
from Model.constants import *
from Model.Route import Route
import sys

counter=1

class Plateau():
    def __init__(self, screen, clock, name, heigth, width, nbr_cell_x=40, nbr_cell_y=40, attractiveness=0, listeCase=[], entities = [], buildings = []):
        
        self.screen = screen
        self.clock = clock
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

        #Load de tous les spirtes
        self.image = self.load_cases_images()
        self.image_route = self.load_routes_images()
        self.image_walkers = self.load_walkers_images()
        self.image_buildings = self.load_buildings_images()

        self.zoom__=Zoom(self.image)

        self.attractiveness = attractiveness
        self.listeCase = listeCase

        self.map = self.default_map()
        self.default_road()

        #Tableau contenant l'intégralité des walker présents sur la map
        self.entities = entities

        #Tableau des collisions de la map (pour le moment la map ne contient pas de collision)
        self.collision_matrix = self.create_collision_matrix()

        #Tableau contenant l'intégralité des bâtiments présent sur la map
        self.buildings = buildings

        #Define the position of the button on the full panel button who won't change position after
        overlays_button.change_pos(self.width-overlays_button.dim[0]-hide_control_panel_button.dim[0]-10,27)
        hide_control_panel_button.change_pos(self.width-hide_control_panel_button.dim[0]-4,24+5)
        advisors_button.change_pos(self.width-155,179)
        empire_map_button.change_pos(self.width-78,179)
        assignement_button.change_pos(self.width-155,208)
        compass_button.change_pos(self.width-116,208)
        arrow_rotate_counterclockwise.change_pos(self.width-78,208)
        arrow_rotate_clockwise.change_pos(self.width-39,208)                
        undo_button.change_pos(self.width-149,445)
        message_view_button.change_pos(self.width-99,445)
        see_recent_troubles_button.change_pos(self.width-49,445)

    def default_map(self):

        map = []

        for cell_x in range(self.nbr_cell_x):
            map.append([])
            for cell_y in range(self.nbr_cell_y):
                cells_to_map = self.cells_to_map(cell_x, cell_y)
                map[cell_x].append(cells_to_map)
                render_pos = cells_to_map.render_pos
                self.surface_cells.blit(self.image["land2"], (render_pos[0] + self.surface_cells.get_width()/2, render_pos[1]))
        return map
    def default_road(self):
        for j in range(19, 20):
            for i in range(self.nbr_cell_y):
                Route(self.map[j][i], self)
        
    def cells_to_map(self, cell_x, cell_y):

        rectangle_cell = [
            (cell_x * cell_size , cell_y * cell_size ),
            (cell_x * cell_size  + cell_size , cell_y * cell_size ),
            (cell_x * cell_size  + cell_size , cell_y * cell_size  + cell_size ),
            (cell_x * cell_size , cell_y * cell_size  + cell_size )
        ]

        isometric_cell = [self.cartesian_to_isometric(x, y) for x, y in rectangle_cell]

        sprite=self.choose_image()
        nouvelle_case = Case(cell_x, cell_y, rectangle_cell, isometric_cell, [min([x for x, y in isometric_cell]), min([y for x, y in isometric_cell])], sprite = sprite)
        if sprite.startswith("path"):
            nouvelle_case.sprite = "land1"
            Route(nouvelle_case, self)
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
            self.create_map=self.default_map()

    def set_self_num(self):
        self.num=1
    def choose_image(self):
        image=""
        global counter
        if counter<=1600:

            if (counter>=1 and counter<=10) or(counter>=41 and counter<=50)or(counter>=201 and counter<=207)or (counter>=281 and counter<=286)or(counter>=361 and counter<=364)or (counter>=441 and counter<=443)or (counter>=481 and counter<=483)or (counter>=561 and counter<=562)or (counter>=641 and counter<=642) or (counter in range(21,41,1))or (counter in range(103,121,1))or (counter in range(185,201,1))or (counter in range(267,281,1))or (counter in range(349,361,1))or (counter==1200)or (counter in range(1155,1161,1))or (counter in range(1115,1121))or (counter in range(1075,1081))or (counter==1040):
                image = "tree2"
            elif (counter>=121 and counter<=129)or(counter>=161 and counter<=168)or(counter>=81 and counter<=89) or (counter>=241 and counter<=246)or(counter>=321 and counter<=324) or (counter>=401 and counter<=404)or (counter>=521 and counter<=522)or (counter>=601 and counter<=602)or (counter in range(62,81,1))or (counter in range(144,161,1))or (counter in range(226,241,1))or (counter in range(308,321,1))or (counter in range(390,401,1))or (counter==1440)or (counter in range(1395,1401,1))or (counter in range(1355,1361,1))or (counter in range(1315,1321,1))or (counter in range(1276,1281,1))or (counter==1240):
                image = "tree1"
            elif (counter >= 761 and counter<=800):
                image = "land1" # route
            elif (counter == 721):
                image = "sign2"
            elif (counter == 760):
                image = "sign1"
            elif (counter>=14 and counter<=19) or(counter>=55 and counter<=60)or(counter>=96 and counter<=101)or(counter>=137 and counter<=142)or(counter>=178 and counter<=183)or(counter>=219 and counter<=224)or(counter>=260 and counter<=265)or(counter>=301 and counter<=306)or(counter>=342 and counter<=347)or(counter>=383 and counter<=388)or(counter>=424 and counter<=429)or(counter>=465 and counter<=480)or(counter>=506 and counter<=520)or(counter>=547 and counter<=560)or(counter>=588 and counter<=600)or(counter>=629 and counter<=640)or(counter<=1573 and counter>=1569)or(counter<=1533 and counter>=1529)or(counter<=1493 and counter>=1489)or(counter<=1453 and counter>=1449)or(counter<=1413 and counter>=1409)or(counter<=1373 and counter>=1369)or(counter<=1333 and counter>=1329)or(counter<=1293 and counter>=1281)or(counter<=1253 and counter>=1241)or(counter<=1213 and counter>=1201)or(counter<=1173 and counter>=1161):
                image = "water1"
            elif (counter==20) or (counter==61)or(counter==102)or(counter==143)or(counter==184)or(counter==225)or(counter==266)or(counter==307)or(counter==348)or(counter==389)or(counter>=430 and counter<=440 )or(counter<=1133 and counter>=1121):
                image="water2"
            elif (counter>=669 and counter<=680)or counter==628 or counter==587 or counter==546 or counter==505 or counter==464 or counter==423 or counter==382 or counter==341 or counter==300 or counter==259 or counter==218 or counter==177 or counter==136 or counter==95 or counter==54 or counter==13 or(counter<=1328 and counter>=1321):
                image = "water3"
            elif (counter==1574)or(counter==1534)or(counter==1494)or(counter==1454)or(counter==1414)or(counter==1374)or(counter==1334)or(counter==1294)or(counter==1254)or(counter==1214)or(counter==1174)or(counter==1134):
                image="water4"
            elif (counter==1568)or(counter==1528)or(counter==1488)or(counter==1448)or(counter==1408)or(counter==1368):
                image="water5"
            elif (counter==1590)or(counter==1549)or(counter==1508)or(counter==1467)or(counter==1426)or(counter==1385)or(counter==1384)or(counter==1343)or(counter==1302) or (counter==1298)or (counter==1600)or (counter==1337)or (counter==1376)or (counter==1415)or (counter==1455)or (counter==1495)or (counter==1535)or (counter==1575)or (counter in range(1575,1591)):
                image = "rock1"
            elif (counter==1262) or (counter==1520):
                image="rock2"
            elif (counter in range(681,721,1))or(counter in range(722,760,1)) or(counter in range(681+40*3,720+40*4+1,1)):
                image="tree3"
            elif counter in range(720+40*4,1600,20):
                image="rock3"
            elif counter in range(1,680,20):
                image="rock3"
            else:
                image="land1"
            counter+=1
        return image

    def load_cases_images(self):


        land1 = pygame.image.load("image/C3/Land1a_00116.png").convert_alpha()
        land1 = pygame.transform.scale(land1,(land1.get_width()/2,land1.get_height()/2))
        land2 = pygame.image.load("image/C3/Land1a_00265.png").convert_alpha()
        land2 = pygame.transform.scale(land2, (land2.get_width() / 2, land2.get_height() / 2))



        tree1 = pygame.image.load("image/C3/Land1a_00059.png").convert_alpha()
        tree1 = pygame.transform.scale(tree1,(tree1.get_width()/2,tree1.get_height()/2))
        tree2 = pygame.image.load("image/C3/Land1a_00061.png").convert_alpha()
        tree2 = pygame.transform.scale(tree2, (tree2.get_width() / 2, tree2.get_height() / 2))
        tree3 = pygame.image.load("image/C3/Land1a_00039.png").convert_alpha()
        tree3 = pygame.transform.scale(tree3, (tree3.get_width() / 2, tree3.get_height() / 2))



        rock1 = pygame.image.load("image/C3/Land1a_00292.png").convert_alpha()
        rock1 = pygame.transform.scale(rock1, (rock1.get_width() / 2, rock1.get_height() / 2))
        rock2 = pygame.image.load("image/C3/land3a_00084.png").convert_alpha()
        rock2 = pygame.transform.scale(rock2, (rock2.get_width() / 2, rock2.get_height() / 2))
        rock3 = pygame.image.load("image/C3/Land1a_00223.png").convert_alpha()
        rock3 = pygame.transform.scale(rock3, (rock3.get_width() / 2, rock3.get_height() / 2))


        sign1 = pygame.image.load("image/C3/land3a_00089.png").convert_alpha()
        sign1 = pygame.transform.scale(sign1, (sign1.get_width() / 2, sign1.get_height() / 2))
        sign2 = pygame.image.load("image/C3/land3a_00087.png").convert_alpha()
        sign2 = pygame.transform.scale(sign2, (sign2.get_width() / 2, sign2.get_height() / 2))


        water1 = pygame.image.load("image/C3/Land1a_00122.png").convert_alpha()
        water1 = pygame.transform.scale(water1, (water1.get_width() / 2, water1.get_height() / 2))
        water2 = pygame.image.load("image/C3/Land1a_00132.png").convert_alpha()
        water2 = pygame.transform.scale(water2, (water2.get_width() / 2, water2.get_height() / 2))
        water3 = pygame.image.load("image/C3/Land1a_00141.png").convert_alpha()
        water3 = pygame.transform.scale(water3, (water3.get_width() / 2, water3.get_height() / 2))
        water4 = pygame.image.load("image/C3/Land1a_00146.png").convert_alpha()
        water4 = pygame.transform.scale(water4, (water4.get_width() / 2, water4.get_height() / 2))
        water5 = pygame.image.load("image/C3/Land1a_00154.png").convert_alpha()
        water5 = pygame.transform.scale(water5, (water5.get_width() / 2, water5.get_height() / 2))

        return {"land1": land1,"land2": land2, "tree1": tree1,"tree2": tree2,
                "tree3": tree3,"rock1": rock1,"rock2": rock2,"water1":water1,
                "water2":water2,"water3":water3,"sign1":sign1,"sign2":sign2,
                "water4":water4,"water5":water5,"rock3":rock3
                }
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

        walker_sprite = {"Citizen" : citizen, "Prefet" : prefet}

        return walker_sprite

    def load_buildings_images(self):
        default = load_image("image/Buildings/Housng1a_00001.png")

        return {"default" : default}
    
    def update(self):
        self.camera.update()
        #Update de la position des walkers
        for e in self.entities: e.update()


    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.surface_cells, (self.camera.vect.x, self.camera.vect.y))
       
       # DRAW CELLS
        for cell_x in range(self.nbr_cell_y):
            for cell_y in range(self.nbr_cell_y):
                render_pos =  self.map[cell_x][cell_y].render_pos
                if self.map[cell_x][cell_y].road == None:
                    image = self.map[cell_x][cell_y].sprite
                    self.screen.blit(self.image[image],
                                    (render_pos[0] + self.surface_cells.get_width()/2 + self.camera.vect.x,
                                    render_pos[1] - (self.image[image].get_height() - cell_size) + self.camera.vect.y))
                # DRAW ROADS
                else :
                    image = self.map[cell_x][cell_y].road.sprite
                    self.screen.blit(self.image_route[image],
                                    (render_pos[0] + self.surface_cells.get_width()/2 + self.camera.vect.x,
                                    render_pos[1] - (self.image_route[image].get_height() - cell_size) + self.camera.vect.y))
                    
        # DRAW WALKERS
        for e in self.entities:
            render_pos =  self.map[e.case.x][e.case.y].render_pos
            self.screen.blit(self.image_walkers[e.type][e.action][e.direction][int(e.index_sprite)], 
                                        (render_pos[0] + self.surface_cells.get_width()/2 + self.camera.vect.x,
                                         render_pos[1] - (self.image_walkers[e.type][e.action][e.direction][int(e.index_sprite)].get_height() - cell_size) + self.camera.vect.y))
        
        # DRAW BUILDINGS
        for b in self.buildings:
            render_pos =  self.map[b.case.x][b.case.y].render_pos
            self.screen.blit(self.image_buildings["default"], 
                                        (render_pos[0] + self.surface_cells.get_width()/2 + self.camera.vect.x,
                                         render_pos[1] - (self.image_buildings["default"].get_height() - cell_size) + self.camera.vect.y))
                                         
        self.menu_map.draw_menu(self.screen)

        top_menu_axis_x = 0
        while (top_menu_axis_x < self.width):
            
            self.screen.blit(pnl_1.img_scaled,(top_menu_axis_x,0))
            top_menu_axis_x+=pnl_1.dim[0]
            self.screen.blit(pnl_2.img_scaled,(top_menu_axis_x,0))
            top_menu_axis_x+=pnl_2.dim[0]
            self.screen.blit(pnl_3.img_scaled,(top_menu_axis_x,0))
            top_menu_axis_x+=pnl_3.dim[0]
            self.screen.blit(pnl_4.img_scaled,(top_menu_axis_x,0))
            top_menu_axis_x+=pnl_4.dim[0]
            self.screen.blit(pnl_5.img_scaled,(top_menu_axis_x,0))
            top_menu_axis_x+=pnl_5.dim[0]
            self.screen.blit(pnl_6.img_scaled,(top_menu_axis_x,0))
            top_menu_axis_x+=pnl_6.dim[0]
            self.screen.blit(pnl_7.img_scaled,(top_menu_axis_x,0))
            top_menu_axis_x+=pnl_7.dim[0]
            self.screen.blit(pnl_8.img_scaled,(top_menu_axis_x,0))
            top_menu_axis_x+=pnl_8.dim[0]
         
         
            self.screen.blit(bloc_top_menu.img_scaled,(480,0))
            self.screen.blit(bloc_top_menu.img_scaled,(480+ bloc_top_menu.dim[0]+24,0))
            self.screen.blit(bloc_top_menu.img_scaled,(480+(2*bloc_top_menu.dim[0])+120,0))        

        if state_control_panel=="reduced":
            
            self.screen.blit(small_gap_menu.img_scaled, (self.width-small_gap_menu.dim[0], 24))
            self.screen.blit(deco_bas_small_menu.img_scaled, (self.width-42, 24+450))
            
            display_control_panel_button.update()
            display_control_panel_button.change_pos(self.width-display_control_panel_button.dim[0]-5,28)
            display_control_panel_button.draw(self.screen)

            build_housing_button.update()
            build_housing_button.change_pos(self.width-build_housing_button.dim[0]-1,24+32)
            build_housing_button.draw(self.screen)

            clear_land_button.update()
            clear_land_button.change_pos(self.width-clear_land_button.dim[0]-1,24+67)
            clear_land_button.draw(self.screen)

            build_roads_button.update()
            build_roads_button.change_pos(self.width-build_roads_button.dim[0]-1,24+102)
            build_roads_button.draw(self.screen)
            

            water_related_structures.update()
            water_related_structures.change_pos(self.width-water_related_structures.dim[0]-1,24+137)
            water_related_structures.draw(self.screen)
           
            health_related_structures.update()
            health_related_structures.change_pos(self.width-health_related_structures.dim[0]-1,24+172)
            health_related_structures.draw(self.screen)
           
            religious_structures.update()
            religious_structures.change_pos(self.width-religious_structures.dim[0]-1,24+207)
            religious_structures.draw(self.screen)
            
            education_structures.update()
            education_structures.change_pos(self.width-education_structures.dim[0]-1,24+242)
            education_structures.draw(self.screen)
            
            entertainment_structures.update()
            entertainment_structures.change_pos(self.width-entertainment_structures.dim[0]-1,24+277)
            entertainment_structures.draw(self.screen)
            
            administration_or_government_structures.update()
            administration_or_government_structures.change_pos(self.width-administration_or_government_structures.dim[0]-1,24+312)
            administration_or_government_structures.draw(self.screen)
            
            engineering_structures.update()
            engineering_structures.change_pos(self.width-engineering_structures.dim[0]-1,24+347)
            engineering_structures.draw(self.screen)
            
            security_structures.update()
            security_structures.change_pos(self.width-security_structures.dim[0]-1,24+382)
            security_structures.draw(self.screen)
            
            industrial_structures.update()
            industrial_structures.change_pos(self.width-industrial_structures.dim[0]-1,24+417)
            industrial_structures.draw(self.screen)
        
                    
        if state_control_panel=="full":

            self.screen.blit(big_gap_menu.img_scaled,(self.width-big_gap_menu.dim[0],24))
            self.screen.blit(big_gap_menu.img_scaled,(self.width-big_gap_menu.dim[0],24+big_gap_menu.dim[1])) #usefull to have a white line cover all of the right menu, could be replaced by a white rectangle maybe
            
            overlays_button.update()
            overlays_button.draw(self.screen)

            hide_control_panel_button.update()
            hide_control_panel_button.draw(self.screen)
            
            advisors_button.update()
            advisors_button.draw(self.screen)

            empire_map_button.update()
            empire_map_button.draw(self.screen)

            assignement_button.update()
            assignement_button.draw(self.screen)
            
            compass_button.update()
            compass_button.draw(self.screen)

            arrow_rotate_counterclockwise.update()
            arrow_rotate_counterclockwise.draw(self.screen)
           
            arrow_rotate_clockwise.update()
            arrow_rotate_clockwise.draw(self.screen)

            self.screen.blit(deco_milieu_menu_default.img_scaled,(self.width-deco_milieu_menu_default.dim[0]-7,239))

            build_housing_button.update()
            build_housing_button.change_pos(self.width-149,301)
            build_housing_button.draw(self.screen)

            clear_land_button.update()
            clear_land_button.change_pos(self.width-99,301)
            clear_land_button.draw(self.screen)

            build_roads_button.update()
            build_roads_button.change_pos(self.width-49,301)
            build_roads_button.draw(self.screen)

            water_related_structures.update()
            water_related_structures.change_pos(self.width-149,337)
            water_related_structures.draw(self.screen)

            health_related_structures.update()
            health_related_structures.change_pos(self.width-99,337)
            health_related_structures.draw(self.screen)

            religious_structures.update()
            religious_structures.change_pos(self.width-49,337)
            religious_structures.draw(self.screen)
            
            education_structures.update()
            education_structures.change_pos(self.width-149,373)
            education_structures.draw(self.screen)

            entertainment_structures.update()
            entertainment_structures.change_pos(self.width-99,373)
            entertainment_structures.draw(self.screen)
            
            administration_or_government_structures.update()
            administration_or_government_structures.change_pos(self.width-49,373)
            administration_or_government_structures.draw(self.screen)
           
            engineering_structures.update()
            engineering_structures.change_pos(self.width-149,409)
            engineering_structures.draw(self.screen)
            
            security_structures.update()
            security_structures.change_pos(self.width-99,409)
            security_structures.draw(self.screen)
            
            industrial_structures.update()
            industrial_structures.change_pos(self.width-49,409)
            industrial_structures.draw(self.screen)

            undo_button.update()
            undo_button.draw(self.screen)
            
            message_view_button.update()
            message_view_button.draw(self.screen)
            
            see_recent_troubles_button.update()
            see_recent_troubles_button.draw(self.screen)

            x=self.width-pnl_485.dim[0]-1
            y=24+big_gap_menu.dim[1]
            self.screen.blit(pnl_485.img_scaled,(x,y))

            x-=pnl_485.dim[0]
            self.screen.blit(pnl_482.img_scaled,(x,y))
            x-=pnl_482.dim[0]
            self.screen.blit(pnl_481.img_scaled,(x,y))
            x-=pnl_481.dim[0]
            self.screen.blit(pnl_480.img_scaled,(x,y))
            x-=pnl_480.dim[0]                
            self.screen.blit(pnl_484.img_scaled,(x,y))
            x-=pnl_484.dim[0]                
            self.screen.blit(pnl_483.img_scaled,(x,y))
            x-=pnl_483.dim[0]            
            self.screen.blit(pnl_482.img_scaled,(x,y))
            x-=pnl_482.dim[0]
            self.screen.blit(pnl_481.img_scaled,(x,y))
            x-=pnl_481.dim[0]
            self.screen.blit(pnl_480.img_scaled,(x,y))  
            x-=pnl_480.dim[0]
            self.screen.blit(pnl_479.img_scaled,(x,y))  #Fin 1ère ligne
            y+=pnl_479.dim[1]
            
            tmp_y=y #490
            tmp_x=x #1119
            
            for i in range(0,11):
                self.screen.blit(pnl_486.img_scaled,(x,y))
                y+=pnl_486.dim[1] 
            self.screen.blit(pnl_521.img_scaled,(x,y))      #Fin 1ère colonne - version simplifiée (1 seul pnl)

            x+=pnl_521.dim[0]            
            for i in range(0,8):
                self.screen.blit(pnl_525.img_scaled,(x,y))
                x+=pnl_525.dim[0]            #Fin dernière ligne - version simplifiée (1 seul pnl)
            
            y=tmp_y #490                                                        
            x=tmp_x+pnl_521.dim[0]
            for j in range(0,8):                                           #"bloc" milieu sans les bords"  - version simplifiée (1 seul pnl)
                for i in range(0,11):
                    self.screen.blit(pnl_488.img_scaled,(x,y))
                    y+=pnl_488.dim[1] 
                x+=pnl_488.dim[0]   
                y=tmp_y                      
            
            

            x=tmp_x+pnl_521.dim[0]*9
            for i in range(0,11):                                            #Fin dernière colonne - version simplifiée (1 seul pnl)
                self.screen.blit(pnl_520.img_scaled,(x,y))
                y+=pnl_520.dim[1] 
            self.screen.blit(pnl_527.img_scaled,(x,y))
            y+=pnl_527.dim[1]           


            self.screen.blit(deco_bas_full_menu.img_scaled,(tmp_x,682))

        #Display message of the button if mouse on it
        overlays_button.show_tip(self.screen)
        hide_control_panel_button.show_tip(self.screen)
        display_control_panel_button.show_tip(self.screen)
        advisors_button.show_tip(self.screen)
        empire_map_button.show_tip(self.screen)
        assignement_button.show_tip(self.screen)
        compass_button.show_tip(self.screen)
        arrow_rotate_counterclockwise.show_tip(self.screen)
        arrow_rotate_clockwise.show_tip(self.screen)
        build_housing_button.show_tip(self.screen)
        clear_land_button.show_tip(self.screen)
        build_roads_button.show_tip(self.screen)
        water_related_structures.show_tip(self.screen)
        health_related_structures.show_tip(self.screen)
        religious_structures.show_tip(self.screen)
        education_structures.show_tip(self.screen)
        entertainment_structures.show_tip(self.screen)
        administration_or_government_structures.show_tip(self.screen)
        engineering_structures.show_tip(self.screen)
        security_structures.show_tip(self.screen)
        industrial_structures.show_tip(self.screen)
        undo_button.show_tip(self.screen)
        message_view_button.show_tip(self.screen)
        see_recent_troubles_button.show_tip(self.screen)
        
        pygame.display.flip()
    
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

def load_image(path):
    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(image, (image.get_width() / 2, image.get_height() / 2))

def create_liste_sprites_walker(type, action, nb_frame):
    direction = {1 : "UpRight", 2 : "DownRight", 3 : "DownLeft", 4 : "UpLeft"}
    return {j : list(load_image(f"image/Walkers/{type}/{action}/{direction[j]}/{type}{action}{direction[j]}Frame{i}.png") for i in range(1, nb_frame+1)) for j in range(1, 5)}