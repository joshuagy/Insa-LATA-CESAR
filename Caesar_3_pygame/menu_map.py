import pygame
from txt import add_text


class Menu_map:

    def __init__(self,width,height):
        self.height=height
        self.width=width


    def draw_menu(self,screen):

        img_up=pygame.image.load("C3/C3/paneling_00235.png")
        rect_up=img_up.get_rect()
        img_up=pygame.transform.scale(img_up,(self.width,20))
        screen.blit(img_up,rect_up)
        add_text(screen, "pour zoomer:2", 30, (0, 0, 0), (rect_up.x + 5, rect_up.y + 1))
        add_text(screen, "pour dezoomer:1", 30, (0, 0, 0), (rect_up.x + 200, rect_up.y + 1))
