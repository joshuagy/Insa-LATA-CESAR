import pygame  as pg
import pygame.transform
from PIL import Image

class MiniMap:
    scale = 0.18

    def __init__(self, width, height,nbr_cell_x,nbr_cell_y) :


        self.width = width
        self.height = height

        self.mini_screen_width = MiniMap.scale * width
        self.mini_screen_height = MiniMap.scale* height

        self.longueur, self.largeur = (nbr_cell_x,nbr_cell_y)
        self.image = Image.new('RGB', (self.longueur, self.largeur))


    def draw_position(self, screen, camera,create_map):

        # #Tentative échouée d'afficher le rectangle jaune là où est la map
        # self.mini_screen_rect = pg.Rect(self.width-img.get_size()[0]-17,
        #                         - camera.vect[1] * MiniMap.scale+75,
        #                         self.mini_screen_width/12, self.mini_screen_height/10)
        # if(not (
        #     #right x limit
        #     (self.width-img.get_size()[0]-17)>self.width-26
        #     #left x limit
        #     or ((self.width-img.get_size()[0]-17)<self.width-26-img.get_size()[0]
        #     #bottom y limit
        #     or( - camera.vect[1] * MiniMap.scale+75)<60+img.get_size()[1] )
        #     #top y limit
        #     or ( - camera.vect[1] * MiniMap.scale+75)>60 ) 
        #     ):
        #     pg.draw.rect(screen, (255, 255, 0), self.mini_screen_rect, 1)
        
        #Du coup là ça affiche le rectangle jaune là ou était la map quand elle était pas aux bonnes coordonnées, donc ça devrait continuer de fonctionner sur certains écrans
        self.draw_mini_map(screen)

        self.mini_screen_rect = pg.Rect(- camera.vect[0] * MiniMap.scale+self.width*0.94,
                                        - camera.vect[1] * MiniMap.scale+0.08*self.height,
                                        self.mini_screen_width/12, self.mini_screen_height/10)
        if(not ((- camera.vect[0] * MiniMap.scale+self.width*0.94)>self.width*0.98 or ((- camera.vect[0] * MiniMap.scale+self.width*0.94)<self.width*0.92or( - camera.vect[1] * MiniMap.scale+0.08*self.height)<self.height*0.05 ) or ( - camera.vect[1] * MiniMap.scale+0.08*self.height)>self.height*0.147 ) ):
            pg.draw.rect(screen, (255, 255, 0), self.mini_screen_rect, 1)

    def draw_mini_map(self, screen) -> None:
        img=pygame.image.load("mini_map.png").convert_alpha()
        img = pygame.transform.smoothscale(img,(75,75))
        img = pygame.transform.rotate(img, -45).convert_alpha()


        screen.blit(img,(self.width*0.93,self.height*0.058))

    def update_mini_map(self, create_map):
        self.image = Image.new('RGB', (self.longueur, self.largeur))

        for cell_x in range(self.longueur):
            for cell_y in range(self.largeur):
                if not create_map[cell_x][cell_y].road and not create_map[cell_x][cell_y].structure:
                    id_image = create_map[cell_x][cell_y].sprite
                    if id_image == 'land':
                        rouge, vert, bleu = (34, 177, 76)
                        self.image.putpixel((cell_x, cell_y), (rouge, vert, bleu))
                    elif id_image == "tree":
                        rouge, vert, bleu = (128, 255, 0)
                        self.image.putpixel((cell_x, cell_y), (rouge, vert, bleu))
                    elif id_image == "rock":
                        rouge, vert, bleu = (127, 127, 127)
                        self.image.putpixel((cell_x, cell_y), (rouge, vert, bleu))
                    elif id_image == "water":
                        rouge, vert, bleu = (63, 72, 204)
                        self.image.putpixel((cell_x, cell_y), (rouge, vert, bleu))
                    elif id_image == "sign":
                        rouge, vert, bleu = (127, 127, 127)
                        self.image.putpixel((cell_x, cell_y), (rouge, vert, bleu))

                # DRAW ROADS
                elif create_map[cell_x][cell_y].road:
                    rouge, vert, bleu = (0, 0, 0)
                    self.image.putpixel((cell_x, cell_y), (rouge, vert, bleu))



                # DRAW STRUCTURES
                else:
                        rouge, vert, bleu = (255, 255, 0)
                        self.image.putpixel((cell_x, cell_y), (rouge, vert, bleu))

        self.image.save("mini_map.png")

    def cartesian_to_isometric(self, x, y):
         return x - y,(x + y)/2
