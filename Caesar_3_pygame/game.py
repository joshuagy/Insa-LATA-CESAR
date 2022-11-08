from turtle import width
import pygame
import sys

import pygame.draw 
from map import *
from txt import add_text
from camera import Camera
from menu_map import Menu_map

from control_panel import sprite


cell_size1=cell_size
class Game:

    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()
        self.map = Map(40, 40, self.width, self.height)
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
                        self.zoomed=True
                        x,y=pygame.mouse.get_pos()
                        self.camera.vect=pygame.Vector2(self.camera.vect.x-x-200, self.camera.vect.y-y)
                        self.camera.get_cell_size(60)
                        self.map.zoom(2,self.zoomed)
                        cell_size1=60
                        self.zoomed=False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    if cell_size1==60:
                        self.zoomed=True
                        self.camera.vect = pygame.Vector2(-700,-100)
                        cell_size1=30
                        self.camera.get_cell_size(30)
                        self.map.zoom(0.5,self.zoomed)
                        self.zoomed=False



    def update(self):
        self.camera.update()

    def zoom(self):
        if self.zoomed:
            g1 


    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.map.surface_cells, (self.camera.vect.x, self.camera.vect.y))
       
        for cell_x in range(self.map.nbr_cell_y):
            for cell_y in range(self.map.nbr_cell_y):
                render_pos =  self.map.create_map[cell_x][cell_y]["render_pos"]
                image = self.map.create_map[cell_x][cell_y]["image"]
                if image != "":

                    self.screen.blit(self.map.image[image],
                                    (render_pos[0] + self.map.surface_cells.get_width()/2 + self.camera.vect.x,
                                     render_pos[1] - (self.map.image[image].get_height() - cell_size1) + self.camera.vect.y))

        self.menu_map.draw_menu(self.screen)

        
      
        top_menu_axis_x = 0
        while (top_menu_axis_x < self.width):
            self.screen.blit(pygame.image.load("C3/paneling_00001.png"),(top_menu_axis_x,0))
            top_menu_axis_x+=sprite._get_size_of_("C3/paneling_00001.png","width")
            self.screen.blit(pygame.image.load("C3/paneling_00002.png"),(top_menu_axis_x,0))
            top_menu_axis_x+=sprite._get_size_of_("C3/paneling_00002.png","width")
            self.screen.blit(pygame.image.load("C3/paneling_00003.png"),(top_menu_axis_x,0))
            top_menu_axis_x+=sprite._get_size_of_("C3/paneling_00003.png","width")
            self.screen.blit(pygame.image.load("C3/paneling_00004.png"),(top_menu_axis_x,0))
            top_menu_axis_x+=sprite._get_size_of_("C3/paneling_00004.png","width")
            self.screen.blit(pygame.image.load("C3/paneling_00005.png"),(top_menu_axis_x,0))
            top_menu_axis_x+=sprite._get_size_of_("C3/paneling_00005.png","width")
            self.screen.blit(pygame.image.load("C3/paneling_00006.png"),(top_menu_axis_x,0))
            top_menu_axis_x+=sprite._get_size_of_("C3/paneling_00006.png","width")
            self.screen.blit(pygame.image.load("C3/paneling_00007.png"),(top_menu_axis_x,0))
            top_menu_axis_x+=sprite._get_size_of_("C3/paneling_00007.png","width")
            self.screen.blit(pygame.image.load("C3/paneling_00008.png"),(top_menu_axis_x,0))
            top_menu_axis_x+=sprite._get_size_of_("C3/paneling_00008.png","width")
         
            bloc_top_menu=("C3/paneling_00015.png")
            self.screen.blit(pygame.image.load(bloc_top_menu),(480,0))
            self.screen.blit(pygame.image.load(bloc_top_menu),(480+sprite._get_size_of_(bloc_top_menu,"width")+24,0))
            self.screen.blit(pygame.image.load(bloc_top_menu),(480+(2*sprite._get_size_of_(bloc_top_menu,"width"))+120,0))
       
        #fps
        add_text(
            self.screen,
            'FPS={}'.format(round(self.clock.get_fps())),
            25,
            (0, 0, 0),
            (0.5, 0.5)
        )
        if sprite.state_control_panel=="full":

            self.screen.blit(pygame.image.load(sprite.big_gap_menu),(self.width-sprite._get_size_of_(sprite.big_gap_menu,"width"),24))
            self.screen.blit(pygame.image.load(sprite.big_gap_menu),(self.width-sprite._get_size_of_(sprite.big_gap_menu,"width"),24+sprite._get_size_of_(sprite.big_gap_menu,"height"))) #usefull to have a white line cover all of the right menu, could be replaced by a white rectangle maybe
            
            self.screen.blit(pygame.image.load(sprite.overlays_button),(self.width-sprite._get_size_of_(sprite.overlays_button,"width")-sprite._get_size_of_(sprite.hide_control_panel_button,"width")-10,27))
            self.screen.blit(pygame.image.load(sprite.hide_control_panel_button),(self.width-sprite._get_size_of_(sprite.hide_control_panel_button,"width")-4,24+5))
            
            self.screen.blit(pygame.image.load(sprite.advisors),(self.width-155,179))
            self.screen.blit(pygame.image.load(sprite.empire_map),(self.width-78,179))

            self.screen.blit(pygame.image.load(sprite.assignement_scroll),(self.width-155,208))
            self.screen.blit(pygame.image.load(sprite.compass),(self.width-116,208))
            self.screen.blit(pygame.image.load(sprite.arrow_rotate_counterclockwise),(self.width-78,208))
            self.screen.blit(pygame.image.load(sprite.arrow_rotate_clockwise),(self.width-39,208))

            self.screen.blit(pygame.image.load(sprite.deco_milieu_menu_default),(self.width-sprite._get_size_of_(sprite.deco_milieu_menu_default,"width")-7,239))

            self.screen.blit(pygame.image.load(sprite.build_housing),(self.width-149,301))
            self.screen.blit(pygame.image.load(sprite.clear_land),(self.width-99,301))
            self.screen.blit(pygame.image.load(sprite.build_roads),(self.width-49,301))
            self.screen.blit(pygame.image.load(sprite.water_related_structures),(self.width-149,337))
            self.screen.blit(pygame.image.load(sprite.health_related_structures),(self.width-99,337))
            self.screen.blit(pygame.image.load(sprite.religious_structures),(self.width-49,337))
            self.screen.blit(pygame.image.load(sprite.education_structures),(self.width-149,373))
            self.screen.blit(pygame.image.load(sprite.entertainment_structures),(self.width-99,373))
            self.screen.blit(pygame.image.load(sprite.administration_or_government_structures),(self.width-49,373))
            self.screen.blit(pygame.image.load(sprite.engineering_structures),(self.width-149,409))
            self.screen.blit(pygame.image.load(sprite.security_structures),(self.width-99,409))
            self.screen.blit(pygame.image.load(sprite.industrial_structures),(self.width-49,409))
            self.screen.blit(pygame.image.load(sprite.undo_button),(self.width-149,445))
            self.screen.blit(pygame.image.load(sprite.message_view_button),(self.width-99,445))
            self.screen.blit(pygame.image.load(sprite.see_recent_troubles_button),(self.width-49,445))

           
            #Partie sous control panel  (largeur = 10 panels et hauteur = 13 panels)
            x=self.width-sprite._get_size_of_("C3/paneling_00485.png","width")-1
            y=24+sprite._get_size_of_(sprite.big_gap_menu,"height")
            self.screen.blit(pygame.image.load("C3/paneling_00485.png"),(x,y))
            x-=sprite._get_size_of_("C3/paneling_00485.png","width")
            self.screen.blit(pygame.image.load("C3/paneling_00482.png"),(x,y))
            x-=sprite._get_size_of_("C3/paneling_00482.png","width")
            self.screen.blit(pygame.image.load("C3/paneling_00481.png"),(x,y))
            x-=sprite._get_size_of_("C3/paneling_00481.png","width")
            self.screen.blit(pygame.image.load("C3/paneling_00480.png"),(x,y))
            x-=sprite._get_size_of_("C3/paneling_00480.png","width")                
            self.screen.blit(pygame.image.load("C3/paneling_00484.png"),(x,y))
            x-=sprite._get_size_of_("C3/paneling_00484.png","width")                
            self.screen.blit(pygame.image.load("C3/paneling_00483.png"),(x,y))
            x-=sprite._get_size_of_("C3/paneling_00483.png","width")            
            self.screen.blit(pygame.image.load("C3/paneling_00482.png"),(x,y))
            x-=sprite._get_size_of_("C3/paneling_00482.png","width")
            self.screen.blit(pygame.image.load("C3/paneling_00481.png"),(x,y))
            x-=sprite._get_size_of_("C3/paneling_00481.png","width")
            self.screen.blit(pygame.image.load("C3/paneling_00480.png"),(x,y))  
            x-=sprite._get_size_of_("C3/paneling_00480.png","width")
            self.screen.blit(pygame.image.load("C3/paneling_00479.png"),(x,y))  #Fin 1ère ligne
            y+=sprite._get_size_of_("C3/paneling_00479.png","height")
            
            tmp_y=y #490
            tmp_x=x #1119
            
            for i in range(0,11):
                self.screen.blit(pygame.image.load("C3/paneling_00486.png"),(x,y))
                y+=sprite._get_size_of_("C3/paneling_00486.png","height") 
            self.screen.blit(pygame.image.load("C3/paneling_00521.png"),(x,y))      #Fin 1ère colonne - version simplifiée (1 seul panel)

            x+=sprite._get_size_of_("C3/paneling_00521.png","width")            
            for i in range(0,8):
                self.screen.blit(pygame.image.load("C3/paneling_00525.png"),(x,y))
                x+=sprite._get_size_of_("C3/paneling_00525.png","width")            #Fin dernière ligne - version simplifiée (1 seul panel)
            
            y=tmp_y #490                                                        
            x=tmp_x+sprite._get_size_of_("C3/paneling_00521.png","width")
            for j in range(0,8):                                           #"bloc" milieu sans les bords"  - version simplifiée (1 seul panel)
                for i in range(0,11):
                    self.screen.blit(pygame.image.load("C3/paneling_00488.png"),(x,y))
                    y+=sprite._get_size_of_("C3/paneling_00488.png","height") 
                x+=sprite._get_size_of_("C3/paneling_00488.png","width")   
                y=tmp_y                      

            x=tmp_x+sprite._get_size_of_("C3/paneling_00521.png","width")*9
            for i in range(0,11):                                            #Fin dernière colonne - version simplifiée (1 seul panel)
                self.screen.blit(pygame.image.load("C3/paneling_00520.png"),(x,y))
                y+=sprite._get_size_of_("C3/paneling_00520.png","height") 
            self.screen.blit(pygame.image.load("C3/paneling_00527.png"),(x,y))
            y+=sprite._get_size_of_("C3/paneling_00527.png","height")           






            self.screen.blit(pygame.image.load(sprite.deco_bas_full_menu),(1119,682))
           
        
        elif sprite.state_control_panel=="reduced":
            self.screen.blit(pygame.image.load(sprite.small_gap_menu), (self.width-sprite._get_size_of_(sprite.small_gap_menu,"width"), 24))
            self.screen.blit(pygame.image.load(sprite.deco_bas_small_menu), (self.width-42, 24+450))

            ##clickable buttons (not clickable yet)

            self.screen.blit(pygame.image.load(sprite.display_control_panel_button), (self.width-sprite._get_size_of_(sprite.display_control_panel_button,"width")-5, 24+4))
            self.screen.blit(pygame.image.load(sprite.build_housing),(self.width-sprite._get_size_of_(sprite.build_housing,"width")-1,24+32))
            self.screen.blit(pygame.image.load(sprite.clear_land),(self.width-sprite._get_size_of_(sprite.clear_land,"width")-1,24+67))
            self.screen.blit(pygame.image.load(sprite.build_roads),(self.width-sprite._get_size_of_(sprite.build_roads,"width")-1,24+102))
            self.screen.blit(pygame.image.load(sprite.water_related_structures),(self.width-sprite._get_size_of_(sprite.water_related_structures,"width")-1,24+137))
            self.screen.blit(pygame.image.load(sprite.health_related_structures),(self.width-sprite._get_size_of_(sprite.health_related_structures,"width")-1,24+172))
            self.screen.blit(pygame.image.load(sprite.religious_structures),(self.width-sprite._get_size_of_(sprite.religious_structures,"width")-1,24+207))
            self.screen.blit(pygame.image.load(sprite.education_structures),(self.width-sprite._get_size_of_(sprite.education_structures,"width")-1,24+242))
            self.screen.blit(pygame.image.load(sprite.entertainment_structures),(self.width-sprite._get_size_of_(sprite.entertainment_structures,"width")-1,24+277))
            self.screen.blit(pygame.image.load(sprite.administration_or_government_structures),(self.width-sprite._get_size_of_(sprite.administration_or_government_structures,"width")-1,24+312))
            self.screen.blit(pygame.image.load(sprite.engineering_structures),(self.width-sprite._get_size_of_(sprite.engineering_structures,"width")-1,24+347))
            self.screen.blit(pygame.image.load(sprite.security_structures),(self.width-sprite._get_size_of_(sprite.security_structures,"width")-1,24+382))
            self.screen.blit(pygame.image.load(sprite.industrial_structures),(self.width-sprite._get_size_of_(sprite.industrial_structures,"width")-1,24+417))
       
        pygame.display.flip()