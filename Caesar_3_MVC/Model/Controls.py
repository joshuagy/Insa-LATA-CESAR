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
    originX = self.screenWidth-big_gap_menu.dim[0]
    originY = 24

    listOfButtons = []

    self.hide_control_panel_button = ButtonCtrlPnl(self, display_reduced_ctrl_panel,"Hide the Control Panel to see a wider playing area", 0, 0,"image/C3/paneling_00097.png","image/C3/paneling_00098.png","image/C3/paneling_00099.png")
    self.hide_control_panel_button.change_pos(self.screenWidth-self.hide_control_panel_button.dim[0]-4 - originX, 24+5 - originY)
    listOfButtons.append(self.hide_control_panel_button)

    self.overlays_button = ButtonCtrlPnl(self, not_implemented_func,"Select a city overlay report", 0, 0,"image/C3/paneling_00234.png","image/C3/paneling_00235.png","image/C3/paneling_00236.png")
    self.overlays_button.change_pos(self.screenWidth-self.overlays_button.dim[0]-self.hide_control_panel_button.dim[0]-10 - originX, 27 - originY)
    listOfButtons.append(self.overlays_button)
    
    self.advisors_button = ButtonCtrlPnl(self, not_implemented_func, "Visit your advisors", self.screenWidth - 155 - originX, 179 - originY,"image/C3/paneling_00079.png","image/C3/paneling_00080.png","image/C3/paneling_00081.png")
    listOfButtons.append(self.advisors_button)

    self.empire_map_button = ButtonCtrlPnl(self, not_implemented_func,"Go to the map of the Empire", self.screenWidth - 78 - originX ,179 - originY, "image/C3/paneling_00082.png","image/C3/paneling_00083.png","image/C3/paneling_00084.png")
    listOfButtons.append(self.empire_map_button)

    self.assignement_button = ButtonCtrlPnl(self, not_implemented_func,"Review your assignement",self.screenWidth-155-originX,208-originY, "image/C3/paneling_00085.png","image/C3/paneling_00086.png","image/C3/paneling_00087.png")
    listOfButtons.append(self.assignement_button)

    self.compass_button = ButtonCtrlPnl(self, not_implemented_func,"Re_orient your view to Due North", self.screenWidth-116-originX,208-originY,"image/C3/paneling_00088.png","image/C3/paneling_00089.png","image/C3/paneling_00090.png")
    listOfButtons.append(self.compass_button)
    
    self.arrow_rotate_counterclockwise = ButtonCtrlPnl(self, not_implemented_func,"Rotate the map counterclockwise", self.screenWidth-78-originX,208-originY,"image/C3/paneling_00091.png","image/C3/paneling_00092.png","image/C3/paneling_00093.png")
    listOfButtons.append(self.arrow_rotate_counterclockwise)

    self.arrow_rotate_clockwise = ButtonCtrlPnl(self, not_implemented_func,"Rotate the map clockwise", self.screenWidth-39-originX,208-originY,"image/C3/paneling_00094.png","image/C3/paneling_00095.png","image/C3/paneling_00096.png")
    listOfButtons.append(self.arrow_rotate_clockwise)
    
    self.clear_land_button = ButtonCtrlPnl(self, clear_land,"Clear land", self.screenWidth-99 - originX, 301 - originY, "image/C3/paneling_00131.png", "image/C3/paneling_00132.png","image/C3/paneling_00133.png")
    listOfButtons.append(self.clear_land_button)

    self.build_roads_button = ButtonCtrlPnl(self, build_roads,"Build roads", self.screenWidth - 49 - originX ,301 - originY,"image/C3/paneling_00135.png","image/C3/paneling_00136.png","image/C3/paneling_00137.png")
    listOfButtons.append(self.build_roads_button)
    
    self.build_housing_button = ButtonCtrlPnl(self, build_housing, "Build housing", self.screenWidth-149 - originX, 301 - originY,"image/C3/paneling_00123.png","image/C3/paneling_00124.png","image/C3/paneling_00125.png")
    listOfButtons.append(self.build_housing_button)

    self.water_related_structures = ButtonCtrlPnl(self, build_water_related_structures, "Water related structure", self.screenWidth - 149 - originX, 337 - originY,"image/C3/paneling_00127.png","image/C3/paneling_00128.png","image/C3/paneling_00129.png")
    listOfButtons.append(self.water_related_structures)

    self.health_related_structures= ButtonCtrlPnl(self, not_implemented_func, "Health related structures", self.screenWidth-99-originX,337-originY, "image/C3/paneling_00163.png", "image/C3/paneling_00164.png", "image/C3/paneling_00165.png","image/C3/paneling_00166.png")
    listOfButtons.append(self.health_related_structures)

    # list_of_buttons.append(religious_structures)
    # list_of_buttons.append(education_structures)
    # list_of_buttons.append(entertainment_structures)
    # list_of_buttons.append(administration_or_government_structures)

    self.engineering_structures = ButtonCtrlPnl(self, build_engineer_post, "Engineering function", self.screenWidth - 149 - originX,409 - originY,"image/C3/paneling_00167.png","image/C3/paneling_00168.png","image/C3/paneling_00169.png")
    listOfButtons.append(self.engineering_structures)

    self.security_structures = ButtonCtrlPnl(self, build_prefecture,"Security Structures", self.screenWidth - 99 - originX,409 - originY,"image/C3/paneling_00159.png","image/C3/paneling_00160.png","image/C3/paneling_00161.png")
    listOfButtons.append(self.security_structures)

    self.industrial_structures = ButtonCtrlPnl(self, not_implemented_func,"Industrial Structures", self.screenWidth-49-originY,409-originY,"image/C3/paneling_00155.png","image/C3/paneling_00156.png","image/C3/paneling_00157.png","image/C3/paneling_00158.png")
    listOfButtons.append(self.industrial_structures)
    
    self.undo_button = ButtonCtrlPnl(self, not_implemented_func,"Undo", self.screenWidth-149-originX, 445-originY,"image/C3/paneling_00171.png","image/C3/paneling_00172.png","image/C3/paneling_00173.png","image/C3/paneling_00174.png")
    listOfButtons.append(self.undo_button)
    
    self.message_view_button = ButtonCtrlPnl(self, not_implemented_func,"Message View", self.screenWidth-99-originX,445-originY,"image/C3/paneling_00115.png","image/C3/paneling_00116.png","image/C3/paneling_00117.png","image/C3/paneling_00118.png")
    listOfButtons.append(self.message_view_button)

    self.see_recent_troubles_button = ButtonCtrlPnl(self, not_implemented_func,"See recent troubles", self.screenWidth-49-originY,445-originY,"image/C3/paneling_00119.png","image/C3/paneling_00120.png","image/C3/paneling_00121.png","image/C3/paneling_00122.png")
    listOfButtons.append(self.see_recent_troubles_button)

    return listOfButtons

  def update(self):
    for button in self.listOfButtons:
      button.update()

  def render(self):  
    self.screen.blit(self.staticSurface, self.staticSurfacePos)
    for button in self.listOfButtons:
      button.draw(self.staticSurface)
      button.show_tip(self.screen)