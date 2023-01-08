from Model.control_panel import *

class Controls:
  def __init__(self, screen):
    self.screen = screen
    self.screenWidth, self.screenHeight = self.screen.get_size()
    self.staticSurface = self.generateStaticSurface()
    self.staticSurfacePos = (self.screenWidth-big_gap_menu.dim[0], 24)
    self.listOfButtons = self.generateListOfButtons()

  def generateStaticSurface(self) -> pygame.Surface:
    originX = self.screenWidth-big_gap_menu.dim[0];
    originY = 24

    staticSurface = pygame.Surface((big_gap_menu.img_scaled.get_width(), self.screenHeight - 24))

    staticSurface.blit(big_gap_menu.img_scaled, (self.screenWidth-big_gap_menu.dim[0] - originX, 24 - originY))

    staticSurface.blit(deco_milieu_menu_default.img_scaled, (self.screenWidth-deco_milieu_menu_default.dim[0]-7 - originX, 239 - originY))

    x=self.screenWidth-pnl_485.dim[0]-1 - originX
    y=24+big_gap_menu.dim[1] - originY

    staticSurface.blit(pnl_485.img_scaled, (x, y))

    x-=pnl_485.dim[0]
    staticSurface.blit(pnl_482.img_scaled,(x,y))
    x-=pnl_482.dim[0]
    staticSurface.blit(pnl_481.img_scaled,(x,y))
    x-=pnl_481.dim[0]
    staticSurface.blit(pnl_480.img_scaled,(x,y))
    x-=pnl_480.dim[0]                
    staticSurface.blit(pnl_484.img_scaled,(x,y))
    x-=pnl_484.dim[0]                
    staticSurface.blit(pnl_483.img_scaled,(x,y))
    x-=pnl_483.dim[0]            
    staticSurface.blit(pnl_482.img_scaled,(x,y))
    x-=pnl_482.dim[0]
    staticSurface.blit(pnl_481.img_scaled,(x,y))
    x-=pnl_481.dim[0]
    staticSurface.blit(pnl_480.img_scaled,(x,y))  
    x-=pnl_480.dim[0]
    staticSurface.blit(pnl_479.img_scaled,(x,y))  #Fin 1ère ligne
    y+=pnl_479.dim[1]
    
    tmp_y=y #490
    tmp_x=x #1119

    for i in range(0,11):
      staticSurface.blit(pnl_486.img_scaled,(x,y))
      y+=pnl_486.dim[1] 
    staticSurface.blit(pnl_521.img_scaled,(x,y))      #Fin 1ère colonne - version simplifiée (1 seul pnl)

    x+=pnl_521.dim[0]            
    for i in range(0,8):
      staticSurface.blit(pnl_525.img_scaled,(x,y))
      x+=pnl_525.dim[0]            #Fin dernière ligne - version simplifiée (1 seul pnl)
        
    y=tmp_y #490                                                        
    x=tmp_x+pnl_521.dim[0]
    for j in range(0,8):                                           #"bloc" milieu sans les bords"  - version simplifiée (1 seul pnl)
        for i in range(0,11):
            staticSurface.blit(pnl_488.img_scaled,(x,y))
            y+=pnl_488.dim[1] 
        x+=pnl_488.dim[0]   
        y=tmp_y

    x=tmp_x+pnl_521.dim[0]*9
    for i in range(0,11):                                            #Fin dernière colonne - version simplifiée (1 seul pnl)
      staticSurface.blit(pnl_520.img_scaled,(x,y))
      y+=pnl_520.dim[1] 
    staticSurface.blit(pnl_527.img_scaled,(x,y))
    y+=pnl_527.dim[1]           


    staticSurface.blit(deco_bas_full_menu.img_scaled,(tmp_x, 682 - originY))
  
    return staticSurface

  def generateListOfButtons(self):
    originX = self.screenWidth-big_gap_menu.dim[0];
    originY = 24

    listOfButtons = []
    # list_of_buttons.append(overlays_button)
    # list_of_buttons.append(hide_control_panel_button)
    
    # list_of_buttons.append(advisors_button)
    # list_of_buttons.append(empire_map_button)
    # list_of_buttons.append(assignement_button)
    # list_of_buttons.append(compass_button)
    # list_of_buttons.append(arrow_rotate_counterclockwise)
    # list_of_buttons.append(arrow_rotate_clockwise)
    
    self.clear_land_button = ButtonCtrlPnl(self, clear_land,"Clear land", self.screenWidth-99 - originX, 301 - originY, "image/C3/paneling_00131.png", "image/C3/paneling_00132.png","image/C3/paneling_00133.png")
    listOfButtons.append(self.clear_land_button)

    self.build_roads_button = ButtonCtrlPnl(self, build_roads,"Build roads", self.screenWidth - 49 - originX ,301 - originY,"image/C3/paneling_00135.png","image/C3/paneling_00136.png","image/C3/paneling_00137.png")
    listOfButtons.append(self.build_roads_button)
   
    
    self.build_housing_button = ButtonCtrlPnl(self, build_housing, "Build housing", self.screenWidth-149 - originX, 301 - originY,"image/C3/paneling_00123.png","image/C3/paneling_00124.png","image/C3/paneling_00125.png")
    listOfButtons.append(self.build_housing_button)

    self.water_related_structures = ButtonCtrlPnl(self, build_water_related_structures, "Water related structure", self.screenWidth - 149 - originX, 337 - originY,"image/C3/paneling_00127.png","image/C3/paneling_00128.png","image/C3/paneling_00129.png")
    listOfButtons.append(self.water_related_structures)

    # list_of_buttons.append(health_related_structures)
    # list_of_buttons.append(religious_structures)
    # list_of_buttons.append(education_structures)
    # list_of_buttons.append(entertainment_structures)
    # list_of_buttons.append(administration_or_government_structures)

    self.engineering_structures = ButtonCtrlPnl(self, build_engineer_post, "Engineering function", self.screenWidth - 149 - originX,409 - originY,"image/C3/paneling_00167.png","image/C3/paneling_00168.png","image/C3/paneling_00169.png")
    listOfButtons.append(self.engineering_structures)

    self.security_structures = ButtonCtrlPnl(self, build_prefecture,"Security Structures", self.screenWidth - 99 - originX,409 - originY,"image/C3/paneling_00159.png","image/C3/paneling_00160.png","image/C3/paneling_00161.png")
    listOfButtons.append(self.security_structures)

    # list_of_buttons.append(industrial_structures)
    # list_of_buttons.append(undo_button)
    # list_of_buttons.append(message_view_button)
    # list_of_buttons.append(see_recent_troubles_button)

    return listOfButtons

  def update(self):
    for button in self.listOfButtons:
      button.update()

  def render(self):  
    self.screen.blit(self.staticSurface, self.staticSurfacePos)
    for button in self.listOfButtons:
      button.draw(self.staticSurface)
   