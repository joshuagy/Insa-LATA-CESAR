import pygame
import sys
from txt import add_text


class Menu_map:

    def __init__(self,width,height):
        self.height=height
        self.width=width
        self.img_File = pygame.image.load("C3/C3/File.png")
        self.img_Options = pygame.image.load("C3/C3/Options.png")
        self.img_Help = pygame.image.load("C3/C3/Help.png")
        self.img_Advisors = pygame.image.load("C3/C3/Advisors.png")
        self.img_generate= pygame.image.load("C3/C3/Briefing1a_00001.png")
        self.img_File_rect = None
        self.img_Options_rect = None
        self.img_Help_rect = None
        self.img_Advisors_rect = None



    def draw_menu(self,screen):

        img_up=pygame.image.load("C3/C3/paneling_00002.png")
        rect_up=img_up.get_rect()
        i=(self.width)/8
        img_up=pygame.transform.scale(img_up,((self.width)/8,21))
        rect_x=rect_up.x
        rect_y=rect_up.y
        while rect_x<self.width:
            screen.blit(img_up,(rect_x,rect_y))
            rect_x+=i

        img_cercle = pygame.image.load("C3/C3/paneling_00015.png")
        img_cercle = pygame.transform.scale(img_cercle, (150, 19))
        screen.blit(img_cercle,(rect_up.x + 500, rect_up.y + 1))
        screen.blit(img_cercle,(rect_up.x + 700, rect_up.y + 1))
        screen.blit(img_cercle, (rect_up.x + 900, rect_up.y + 1))
        add_text(screen,"Nov 72       BC", 23,(255,255,0),(rect_up.x + 920, rect_up.y + 4))
        add_text(screen,"Pop            ", 23,(255,255,255), (rect_up.x + 520, rect_up.y + 4))
        add_text(screen,"Dn             ", 23,(255,255,255), (rect_up.x + 720, rect_up.y + 4))
        self.img_File=pygame.transform.scale(self.img_File,(62,21))
        self.img_Options = pygame.transform.scale(self.img_Options, (75, 21))
        self.img_Help = pygame.transform.scale(self.img_Help, (62, 21))
        self.img_Advisors = pygame.transform.scale(self.img_Advisors, (75, 21))

        self.img_File_rect=self.img_File.get_rect()
        self.img_Options_rect = self.img_Options.get_rect()
        self.img_Options_rect.x+=62
        self.img_Help_rect = self.img_Help.get_rect()
        self.img_Help_rect.x=self.img_Options_rect.x+74
        self.img_Advisors_rect = self.img_Advisors.get_rect()
        self.img_Advisors_rect.x=self.img_Help_rect.x+62
        screen.blit(self.img_File, self.img_File_rect)
        screen.blit(self.img_Options,self.img_Options_rect)
        screen.blit(self.img_Help,self.img_Help_rect)
        screen.blit(self.img_Advisors, self.img_Advisors_rect)

    def generate_window(self,screen):
        screen.blit(self.img_generate,(100,100))




