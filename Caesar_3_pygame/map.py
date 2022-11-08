import pygame
import random
from zoom import Zoom



cell_size = 30
counter=1

class Map:

    def __init__(self, nbr_cell_x, nbr_cell_y, width, height):
        self.nbr_cell_x = nbr_cell_x
        self.nbr_cell_y = nbr_cell_y
        self.width = width
        self.height = height
        self.surface_cells = pygame.Surface((nbr_cell_x * cell_size * 2, nbr_cell_y * cell_size  + 2 * cell_size )).convert_alpha()
        self.image = self.load_images()
        self.create_map = self.default_map()
        self.zoom__=Zoom(self.image)







    def default_map(self):

        map = []

        for cell_x in range(self.nbr_cell_x):
            map.append([])
            for cell_y in range(self.nbr_cell_y):
                cells_to_map = self.cells_to_map(cell_x, cell_y)
                map[cell_x].append(cells_to_map)
                render_pos = cells_to_map["render_pos"]
                self.surface_cells.blit(self.image["land2"], (render_pos[0] + self.surface_cells.get_width()/2, render_pos[1]))


        return map

    def cells_to_map(self, cell_x, cell_y):

        rectangle_cell = [
            (cell_x * cell_size , cell_y * cell_size ),
            (cell_x * cell_size  + cell_size , cell_y * cell_size ),
            (cell_x * cell_size  + cell_size , cell_y * cell_size  + cell_size ),
            (cell_x * cell_size , cell_y * cell_size  + cell_size )
        ]

        isometric_cell = [self.cartesian_to_isometric(x, y) for x, y in rectangle_cell]

        return {
            "grid": [cell_x, cell_y],
            "rectangle_cell": rectangle_cell,
            "isometric_cell": isometric_cell,
            "render_pos": [min([x for x, y in isometric_cell]), min([y for x, y in isometric_cell])],
            "image": self.choose_image()
            }



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
                image = "path1"
            elif (counter == 721):
                image = "path3"
            elif (counter == 760):
                image = "path2"
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

    def load_images(self):


        land1 = pygame.image.load("C3/C3/Land1a_00116.png").convert_alpha()
        land1 = pygame.transform.scale(land1,(land1.get_width()/2,land1.get_height()/2))
        land2 = pygame.image.load("C3/C3/Land1a_00265.png").convert_alpha()
        land2 = pygame.transform.scale(land2, (land2.get_width() / 2, land2.get_height() / 2))



        tree1 = pygame.image.load("C3/C3/Land1a_00059.png").convert_alpha()
        tree1 = pygame.transform.scale(tree1,(tree1.get_width()/2,tree1.get_height()/2))
        tree2 = pygame.image.load("C3/C3/Land1a_00061.png").convert_alpha()
        tree2 = pygame.transform.scale(tree2, (tree2.get_width() / 2, tree2.get_height() / 2))
        tree3 = pygame.image.load("C3/C3/Land1a_00039.png").convert_alpha()
        tree3 = pygame.transform.scale(tree3, (tree3.get_width() / 2, tree3.get_height() / 2))



        rock1 = pygame.image.load("C3/C3/Land1a_00292.png").convert_alpha()
        rock1 = pygame.transform.scale(rock1, (rock1.get_width() / 2, rock1.get_height() / 2))
        rock2 = pygame.image.load("C3/C3/land3a_00084.png").convert_alpha()
        rock2 = pygame.transform.scale(rock2, (rock2.get_width() / 2, rock2.get_height() / 2))
        rock3 = pygame.image.load("C3/C3/Land1a_00223.png").convert_alpha()
        rock3 = pygame.transform.scale(rock3, (rock3.get_width() / 2, rock3.get_height() / 2))



        path1 = pygame.image.load("C3/C3/Land2a_00095.png").convert_alpha()
        path1 = pygame.transform.scale(path1, (path1.get_width() / 2, path1.get_height() / 2))
        path2 = pygame.image.load("C3/C3/land3a_00089.png").convert_alpha()
        path2 = pygame.transform.scale(path2, (path2.get_width() / 2, path2.get_height() / 2))
        path3 = pygame.image.load("C3/C3/land3a_00087.png").convert_alpha()
        path3 = pygame.transform.scale(path3, (path3.get_width() / 2, path3.get_height() / 2))


        water1 = pygame.image.load("C3/C3/Land1a_00122.png").convert_alpha()
        water1 = pygame.transform.scale(water1, (water1.get_width() / 2, water1.get_height() / 2))
        water2 = pygame.image.load("C3/C3/Land1a_00132.png").convert_alpha()
        water2 = pygame.transform.scale(water2, (water2.get_width() / 2, water2.get_height() / 2))
        water3 = pygame.image.load("C3/C3/Land1a_00141.png").convert_alpha()
        water3 = pygame.transform.scale(water3, (water3.get_width() / 2, water3.get_height() / 2))
        water4=pygame.image.load("C3/C3/Land1a_00146.png").convert_alpha()
        water4 = pygame.transform.scale(water4, (water4.get_width() / 2, water4.get_height() / 2))
        water5 = pygame.image.load("C3/C3/Land1a_00154.png").convert_alpha()
        water5 = pygame.transform.scale(water5, (water5.get_width() / 2, water5.get_height() / 2))






        return {"land1": land1,"land2": land2, "tree1": tree1,"tree2": tree2,
                "tree3": tree3,"rock1": rock1,"rock2": rock2,"water1":water1,
                "water2":water2,"water3":water3,"path1":path1,"path2":path2,
                "path3":path3,"water4":water4,"water5":water5,"rock3":rock3
                }