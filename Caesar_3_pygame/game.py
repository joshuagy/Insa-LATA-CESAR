import pygame
import sys
from hud import Hud

import pygame.draw
from map import *

from camera import Camera
from menu_up_map import Menu_map



cell_size1=cell_size
class Game:

    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.entities = []
        self.width, self.height = self.screen.get_size()
        self.hud = Hud(self.width, self.height)
        self.map = Map(self.hud,self.entities,40, 40, self.width, self.height)
        self.camera = Camera(self.width, self.height)

        self.running = True
        self.zoomed=True
        self.menu_map=Menu_map(self.width,self.height)


    def run(self):
        while self.running:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()



    def events(self):
        global cell_size1
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_2:
                    if cell_size1==30:
                        pass
                     #   self.zoomed=True
                     #   x,y=pygame.mouse.get_pos()
                     #   self.camera.vect=pygame.Vector2(self.camera.vect.x-x-200, self.camera.vect.y-y)
                     #   self.camera.get_cell_size(60)
                     #   self.map.zoom(2,self.zoomed)

                     #   cell_size1=60
                     #   self.zoomed=False


                elif event.key == pygame.K_1:
                    pass
                    #if cell_size1==60:
                    #    self.zoomed=True
                    #    self.camera.vect = pygame.Vector2(-700,-100)
                    #    cell_size1=30
                    #    self.camera.get_cell_size(30)
                    #    self.map.zoom(0.5,self.zoomed)
                    #    self.zoomed=False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
                #if self.menu_map.img_File_rect.collidepoint(event.pos):
                 #   self.menu_map.generate_window(self.screen)
                #if self.menu_map.img_Options_rect.collidepoint(event.pos):
                 #   self.menu_map.generate_window(self.screen)
                #if self.menu_map.img_Help_rect.collidepoint(event.pos):
                 #   self.menu_map.generate_window(self.screen)
               # if self.menu_map.img_Advisors_rect.collidepoint(event.pos):
                #    self.menu_map.generate_window(self.screen)





    def update(self):
        self.camera.update()
        self.hud.update()
        self.map.update(self.camera)


    def draw(self):
        self.screen.fill((0, 0, 0))
        self.map.draw(self.screen,self.camera,self.menu_map)
        self.hud.draw(self.screen)
        pygame.display.flip()