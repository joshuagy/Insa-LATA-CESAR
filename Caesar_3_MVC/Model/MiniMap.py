import pygame  as pg



class MiniMap:
    scale = 0.18

    def __init__(self, width, height,surface_width,surface_height) :


        self.width = width
        self.height = height

        self.mini_screen_width = MiniMap.scale * width
        self.mini_screen_height = MiniMap.scale* height




    def draw_position(self, screen, camera,create_map,nb_cell_x,nbr_cell_y,image):
        self.draw_mini_map(screen,create_map,nb_cell_x,nbr_cell_y,image)

        self.mini_screen_rect = pg.Rect(- camera.vect[0] * MiniMap.scale+self.width*0.87,
                                        - camera.vect[1] * MiniMap.scale+0.05*self.height,
                                        self.mini_screen_width/7, self.mini_screen_height/6)
        if(not ((- camera.vect[0] * MiniMap.scale+self.width*0.86)>self.width*0.98 or ((- camera.vect[0] * MiniMap.scale+self.width*0.86)<self.width*0.85or( - camera.vect[1] * MiniMap.scale+0.05*self.height)<self.height*0.02 ) or ( - camera.vect[1] * MiniMap.scale+0.05*self.height)>self.height*0.14 ) ):
            pg.draw.rect(screen, (255, 255, 0), self.mini_screen_rect, 1)





    def draw_mini_map(self,screen,create_map,nbr_cell_x,nbr_cell_y,image):

        for cell_x in range(nbr_cell_x):
            for cell_y in range(nbr_cell_y):

                object = create_map[cell_x][cell_y].sprite
                rectangle__cell = [
                    (cell_x * 15 / 5, cell_y * 15 / 5),
                    (cell_x * 15 / 5 + 15 / 5, cell_y * 15 / 5),
                    (cell_x * 15 / 5 + 15/4, cell_y * 15 / 5 + 15 / 5),
                    (cell_x * 15 / 5, cell_y * 15 / 5 + 15 / 5)
                ]

                isometric__cell = [self.cartesian_to_isometric(x, y) for x, y in rectangle__cell]

                render__pos = [min([x for x, y in isometric__cell]), min([y for x, y in isometric__cell])]

                screen.blit(pg.transform.scale(image[object],
                                                   (image[object].get_width() * (0.5) / 5,
                                                    image[object].get_height() * (0.5) / 5)),
                            (render__pos[0] + self.width * 0.94,
                             render__pos[1] - (image[object].get_height() / 5**1000- (15 / 5)) + 40))


    def cartesian_to_isometric(self, x, y):
         return x - y,(x + y)/2