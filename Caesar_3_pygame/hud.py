import pygame as pg
from txt import add_text


class Hud:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.hud_colour = (0, 155, 93, 175)


        # building hud
        self.build_surface = pg.Surface((width * 0.15, height * 0.25), pg.SRCALPHA)
        self.build_rect = self.build_surface.get_rect(topleft=(self.width * 0.84, self.height * 0.74))
        self.build_surface.fill(self.hud_colour)

        # select hud
        self.select_surface = pg.Surface((width * 0.3, height * 0.2), pg.SRCALPHA)
        self.select_rect = self.select_surface.get_rect(topleft=(self.width * 0.35, self.height * 0.79))
        self.select_surface.fill(self.hud_colour)

        self.images = self.load_images()
        self.tiles = self.create_build_hud()

        self.selected_tile = None
        self.examined_tile = None

    def create_build_hud(self):

        render_pos = [self.width * 0.84 + 10, self.height * 0.74 + 10]
        object_width = self.build_surface.get_width() // 5

        tiles = []

        for image_name, image in self.images.items():

            pos = render_pos.copy()
            image_tmp = image.copy()
            image_scale = self.scale_image(image_tmp, w=object_width)
            rect = image_scale.get_rect(topleft=pos)

            tiles.append(
                {
                    "name": image_name,
                    "icon": image_scale,
                    "image": self.images[image_name],
                    "rect": rect
                }
            )

            render_pos[0] += image_scale.get_width() + 10

        return tiles

    def update(self):

        mouse_pos = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed()

        if mouse_action[2]:
            self.selected_tile = None

        for tile in self.tiles:
            if tile["rect"].collidepoint(mouse_pos):
                if mouse_action[0]:
                    self.selected_tile = tile

    def draw(self, screen):


        # build hud
        screen.blit(self.build_surface, (self.width * 0.84, self.height * 0.74))
        # select hud
        if self.examined_tile is not None:
            w, h = self.select_rect.width, self.select_rect.height
            screen.blit(self.select_surface, (self.width * 0.35, self.height * 0.79))
            img = self.images[self.examined_tile["object"]].copy()
            img_scale = self.scale_image(img, h=h * 0.9)
            screen.blit(img_scale, (self.width * 0.35 + 10, self.height * 0.79 + 10))
            add_text(screen, self.examined_tile["object"], 40, (255, 255, 255), self.select_rect.center)

        for tile in self.tiles:
            if(tile["name"]!="tree1" and tile["name"]!="tree2" and tile["name"]!="tree3" and tile["name"]!="rock1" and
            tile["name"]!="rock2" and tile["name"]!="water1" and tile["name"]!="water2" and tile["name"]!="water3" and
            tile["name"]!="path3" and tile["name"]!="path2") :
                screen.blit(tile["icon"], tile["rect"].topleft)



    def load_images(self):

        # read images
        building1 = pg.image.load("C3/C3/Housng1a_00033.png")
        building2 = pg.image.load("C3/C3/Housng1a_00027.png")
        building1 = pg.transform.scale(building1, (building1.get_width() / 2, building1.get_height() / 2))
        building2 = pg.transform.scale(building2, (building2.get_width() / 2, building2.get_height() / 2))
        path1 = pg.image.load("C3/C3/Land2a_00095.png").convert_alpha()
        path1 = pg.transform.scale(path1, (path1.get_width() / 2, path1.get_height() / 2))
        tree1 = pg.image.load("C3/C3/Land1a_00059.png").convert_alpha()
        tree1 = pg.transform.scale(tree1, (tree1.get_width() / 2, tree1.get_height() / 2))
        tree2 = pg.image.load("C3/C3/Land1a_00061.png").convert_alpha()
        tree2 = pg.transform.scale(tree2, (tree2.get_width() / 2, tree2.get_height() / 2))
        tree3 = pg.image.load("C3/C3/Land1a_00039.png").convert_alpha()
        tree3 = pg.transform.scale(tree3, (tree3.get_width() / 2, tree3.get_height() / 2))
        rock1 = pg.image.load("C3/C3/Land1a_00292.png").convert_alpha()
        rock1 = pg.transform.scale(rock1, (rock1.get_width() / 2, rock1.get_height() / 2))
        rock3 = pg.image.load("C3/C3/Land1a_00223.png").convert_alpha()
        rock3 = pg.transform.scale(rock3, (rock3.get_width() / 2, rock3.get_height() / 2))
        path2 = pg.image.load("C3/C3/land3a_00089.png").convert_alpha()
        path2 = pg.transform.scale(path2, (path2.get_width() / 2, path2.get_height() / 2))
        path3 = pg.image.load("C3/C3/land3a_00087.png").convert_alpha()
        path3 = pg.transform.scale(path3, (path3.get_width() / 2, path3.get_height() / 2))
        water1 = pg.image.load("C3/C3/Land1a_00122.png").convert_alpha()
        water1 = pg.transform.scale(water1, (water1.get_width() / 2, water1.get_height() / 2))
        water2 = pg.image.load("C3/C3/Land1a_00132.png").convert_alpha()
        water2 = pg.transform.scale(water2, (water2.get_width() / 2, water2.get_height() / 2))
        water3 = pg.image.load("C3/C3/Land1a_00141.png").convert_alpha()
        water3 = pg.transform.scale(water3, (water3.get_width() / 2, water3.get_height() / 2))
        water4 = pg.image.load("C3/C3/Land1a_00146.png").convert_alpha()
        water4 = pg.transform.scale(water4, (water4.get_width() / 2, water4.get_height() / 2))
        water5 = pg.image.load("C3/C3/Land1a_00154.png").convert_alpha()
        water5 = pg.transform.scale(water5, (water5.get_width() / 2, water5.get_height() / 2))

        images = {
            "building1": building1,
            "building2": building2,"path1": path1,
            "tree1": tree1,"tree2": tree2,"tree3": tree3,
            "rock1": rock1,"water1": water1,"water2": water2,
            "water3": water3,"path2": path2,"path3": path3,
            "water4": water4,"water5": water5,"rock3": rock3,


        }

        return images

    def scale_image(self, image, w=None, h=None):

        if (w == None) and (h == None):
            pass
        elif h == None:
            scale = w / image.get_width()
            h = scale * image.get_height()
            image = pg.transform.scale(image, (int(w), int(h)))
        elif w == None:
            scale = h / image.get_height()
            w = scale * image.get_width()
            image = pg.transform.scale(image, (int(w), int(h)))
        else:
            image = pg.transform.scale(image, (int(w), int(h)))

        return image



