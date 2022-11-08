from turtle import width
import pygame
import sys

import pygame.draw 
from map import *
from txt import add_text
from camera import Camera
from menu_map import Menu_map

from control_panel import *



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
            self.screen.blit(display_control_panel_button.img_scaled, (self.width-display_control_panel_button.dim[0]-5, 24+4))
            self.screen.blit(build_housing.img_scaled,(self.width-build_housing.dim[0]-1,24+32))
            self.screen.blit(clear_land.img_scaled,(self.width-clear_land.dim[0]-1,24+67))
            self.screen.blit(build_roads.img_scaled,(self.width-build_roads.dim[0]-1,24+102))
            self.screen.blit(water_related_structures.img_scaled,(self.width-water_related_structures.dim[0]-1,24+137))
            self.screen.blit(health_related_structures.img_scaled,(self.width-health_related_structures.dim[0]-1,24+172))
            self.screen.blit(religious_structures.img_scaled,(self.width-religious_structures.dim[0]-1,24+207))
            self.screen.blit(education_structures.img_scaled,(self.width-education_structures.dim[0]-1,24+242))
            self.screen.blit(entertainment_structures.img_scaled,(self.width-entertainment_structures.dim[0]-1,24+277))
            self.screen.blit(administration_or_government_structures.img_scaled,(self.width-administration_or_government_structures.dim[0]-1,24+312))
            self.screen.blit(engineering_structures.img_scaled,(self.width-engineering_structures.dim[0]-1,24+347))
            self.screen.blit(security_structures.img_scaled,(self.width-security_structures.dim[0]-1,24+382))
            self.screen.blit(industrial_structures.img_scaled,(self.width-industrial_structures.dim[0]-1,24+417))
        
        if state_control_panel=="full":

            self.screen.blit(big_gap_menu.img_scaled,(self.width-big_gap_menu.dim[0],24))
            self.screen.blit(big_gap_menu.img_scaled,(self.width-big_gap_menu.dim[0],24+big_gap_menu.dim[1])) #usefull to have a white line cover all of the right menu, could be replaced by a white rectangle maybe
            
            self.screen.blit(overlays_button.img_scaled,(self.width-overlays_button.dim[0]-hide_control_panel_button.dim[0]-10,27))
            self.screen.blit(hide_control_panel_button.img_scaled,(self.width-hide_control_panel_button.dim[0]-4,24+5))
            
            self.screen.blit(advisors.img_scaled,(self.width-155,179))
            self.screen.blit(empire_map.img_scaled,(self.width-78,179))

            self.screen.blit(assignement_scroll.img_scaled,(self.width-155,208))
            self.screen.blit(compass.img_scaled,(self.width-116,208))
            self.screen.blit(arrow_rotate_counterclockwise.img_scaled,(self.width-78,208))
            self.screen.blit(arrow_rotate_clockwise.img_scaled,(self.width-39,208))

            self.screen.blit(deco_milieu_menu_default.img_scaled,(self.width-deco_milieu_menu_default.dim[0]-7,239))

            self.screen.blit(build_housing.img_scaled,(self.width-149,301))
            self.screen.blit(clear_land.img_scaled,(self.width-99,301))
            self.screen.blit(build_roads.img_scaled,(self.width-49,301))
            self.screen.blit(water_related_structures.img_scaled,(self.width-149,337))
            self.screen.blit(health_related_structures.img_scaled,(self.width-99,337))
            self.screen.blit(religious_structures.img_scaled,(self.width-49,337))
            self.screen.blit(education_structures.img_scaled,(self.width-149,373))
            self.screen.blit(entertainment_structures.img_scaled,(self.width-99,373))
            self.screen.blit(administration_or_government_structures.img_scaled,(self.width-49,373))
            self.screen.blit(engineering_structures.img_scaled,(self.width-149,409))
            self.screen.blit(security_structures.img_scaled,(self.width-99,409))
            self.screen.blit(industrial_structures.img_scaled,(self.width-49,409))
            self.screen.blit(undo_button.img_scaled,(self.width-149,445))
            self.screen.blit(message_view_button.img_scaled,(self.width-99,445))
            self.screen.blit(see_recent_troubles_button.img_scaled,(self.width-49,445))

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






            self.screen.blit(deco_bas_full_menu.img_scaled,(1119,682))

        pygame.display.flip()