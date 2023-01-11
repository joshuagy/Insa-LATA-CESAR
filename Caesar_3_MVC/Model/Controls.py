from Model.control_panel import *

class Controls:
  def __init__(self, screen, font, currentSpeed, buttonsFunctions):
    self.screen = screen
    self.font = font
    self.currentSpeed = currentSpeed

    self.currentState = 'default'

    # buttons' functions
    self.increaseSpeed = buttonsFunctions['increaseSpeed']
    self.decreaseSpeed = buttonsFunctions['decreaseSpeed']

    self.screenWidth, self.screenHeight = self.screen.get_size()

    self.originX = self.screenWidth-big_gap_menu.dim[0]
    self.originY = 24

    self.hiddenButton = []

    self.staticSurface = self.generateStaticSurface()
    self.staticSurfacePos = (self.screenWidth-big_gap_menu.dim[0], 24)
    self.listOfButtons = self.generateListOfButtons()

    self.currentSpeedRender()

  def getCurrentState(self):
    return self.currentState

  def setCurrentState(self, newState):
    print(newState)
    self.currentState = newState
  
  def generateStaticSurface(self) -> pygame.Surface:
    staticSurface = pygame.Surface((big_gap_menu.img_scaled.get_width(), self.screenHeight - 24))

    staticSurface.blit(big_gap_menu.img_scaled, (self.screenWidth-big_gap_menu.dim[0] - self.originX, 24 - self.originY))
    staticSurface.blit(deco_milieu_menu_default.img_scaled, (self.screenWidth-deco_milieu_menu_default.dim[0]-7 - self.originX, 239 - self.originY))

    x=self.screenWidth-pnl_485.dim[0]-1 - self.originX
    y=24+big_gap_menu.dim[1] - self.originY

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

    for _ in range(0,11):
      staticSurface.blit(pnl_486.img_scaled,(x,y))
      y+=pnl_486.dim[1] 
    staticSurface.blit(pnl_521.img_scaled,(x,y))      #Fin 1ère colonne - version simplifiée (1 seul pnl)

    x+=pnl_521.dim[0]            
    for _ in range(0,8):
      staticSurface.blit(pnl_525.img_scaled,(x,y))
      x+=pnl_525.dim[0]            #Fin dernière ligne - version simplifiée (1 seul pnl)
        
    y=tmp_y #490                                                        
    x=tmp_x+pnl_521.dim[0]
    for _ in range(0,8):                                           #"bloc" milieu sans les bords"  - version simplifiée (1 seul pnl)
        for _ in range(0,11):
            staticSurface.blit(pnl_488.img_scaled,(x,y))
            y+=pnl_488.dim[1] 
        x+=pnl_488.dim[0]   
        y=tmp_y

    x=tmp_x+pnl_521.dim[0]*9
    for _ in range(0,11):                                            #Fin dernière colonne - version simplifiée (1 seul pnl)
      staticSurface.blit(pnl_520.img_scaled,(x,y))
      y+=pnl_520.dim[1] 
    staticSurface.blit(pnl_527.img_scaled,(x,y))
    y+=pnl_527.dim[1]           

    staticSurface.blit(deco_bas_full_menu.img_scaled,(tmp_x, 682 - self.originY))
  
    return staticSurface

  def generateListOfButtons(self):
    listOfButtons = []

    self.hide_control_panel_button = ButtonCtrlPnl(self, display_reduced_ctrl_panel,"Hide the Control Panel to see a wider playing area", 0, 0,"image/C3/paneling_00097.png","image/C3/paneling_00098.png","image/C3/paneling_00099.png")
    self.hide_control_panel_button.change_pos(self.screenWidth-self.hide_control_panel_button.dim[0]-4 - self.originX, 24+5 - self.originY)
    listOfButtons.append(self.hide_control_panel_button)

    self.overlays_button = ButtonCtrlPnl(self, self.display_overlay_selection,"Select a city overlay report", 0, 0,"image/UI/menu/menu_overlay_button.png","image/UI/menu/menu_overlay_button_clicked.png","image/UI/menu/menu_overlay_button_clicked.png")
    self.overlays_button.change_pos(self.screenWidth-self.overlays_button.dim[0]-self.hide_control_panel_button.dim[0]-10 - self.originX, 27 - self.originY)
    listOfButtons.append(self.overlays_button)
    
    # self.fire_overlay = ButtonCtrlPnl(self, not_implemented_func,"Show the risk of the structure to catch fire", 0, 0,"image/UI/menu/menu_fire_button.png","image/UI/menu/menu_fire_button_clicked.png","image/UI/menu/menu_fire_button_clicked.png")
    # self.fire_overlay.change_pos(self.screenWidth-self.fire_overlay.dim[0]-self.hide_control_panel_button.dim[0]-150 ,27 )
    # self.fire_overlay.hide = True
    # self.hiddenButton.append(self.fire_overlay)
    
    # self.damage_overlay = ButtonCtrlPnl(self, not_implemented_func,"Show the risk of the structure to collapse", 0, 0,"image/UI/menu/menu_damage_button.png","image/UI/menu/menu_damage_button_clicked.png","image/UI/menu/menu_damage_button_clicked.png")
    # self.damage_overlay.change_pos(self.screenWidth-self.damage_overlay.dim[0]-self.hide_control_panel_button.dim[0]-150 ,52 )
    # self.damage_overlay.hide = True
    # self.hiddenButton.append(self.damage_overlay)
    
    # self.entertainment_overlay = ButtonCtrlPnl(self, not_implemented_func,"Show the level of entertainment of each case", 0, 0,"image/UI/menu/menu_entertainment_button.png","image/UI/menu/menu_entertainment_button_clicked.png","image/UI/menu/menu_entertainment_button_clicked.png")
    # self.entertainment_overlay.change_pos(self.screenWidth-self.entertainment_overlay.dim[0]-self.hide_control_panel_button.dim[0]-150 ,77 )
    # self.entertainment_overlay.hide = True
    # self.hiddenButton.append(self.entertainment_overlay)
    
    # self.water_overlay = ButtonCtrlPnl(self, not_implemented_func,"Show the water level of each case", 0, 0,"image/UI/menu/menu_water_button.png","image/UI/menu/menu_water_button_clicked.png","image/UI/menu/menu_water_button_clicked.png")
    # self.water_overlay.change_pos(self.screenWidth-self.water_overlay.dim[0]-self.hide_control_panel_button.dim[0]-150 ,102 )
    # self.water_overlay.hide = True
    # self.hiddenButton.append(self.water_overlay)
    
    self.advisors_button = ButtonCtrlPnl(self, not_implemented_func, "Visit your advisors", self.screenWidth - 155 - self.originX, 179 - self.originY,"image/C3/paneling_00079.png","image/C3/paneling_00080.png","image/C3/paneling_00081.png")

    listOfButtons.append(self.advisors_button)

    self.empire_map_button = ButtonCtrlPnl(self, not_implemented_func, "Go to the map of the Empire", self.screenWidth - 78 - self.originX ,179 - self.originY, "image/C3/paneling_00082.png","image/C3/paneling_00083.png","image/C3/paneling_00084.png")
    listOfButtons.append(self.empire_map_button)

    self.assignement_button = ButtonCtrlPnl(self, not_implemented_func, "Review your assignement",self.screenWidth-155-self.originX,208-self.originY, "image/C3/paneling_00085.png","image/C3/paneling_00086.png","image/C3/paneling_00087.png")
    listOfButtons.append(self.assignement_button)

    self.compass_button = ButtonCtrlPnl(self, not_implemented_func, "Re_orient your view to Due North", self.screenWidth-116-self.originX,208-self.originY,"image/C3/paneling_00088.png","image/C3/paneling_00089.png","image/C3/paneling_00090.png")
    listOfButtons.append(self.compass_button)
    
    self.arrow_rotate_counterclockwise = ButtonCtrlPnl(self, not_implemented_func, "Rotate the map counterclockwise", self.screenWidth-78-self.originX,208-self.originY,"image/C3/paneling_00091.png","image/C3/paneling_00092.png","image/C3/paneling_00093.png")
    listOfButtons.append(self.arrow_rotate_counterclockwise)

    self.arrow_rotate_clockwise = ButtonCtrlPnl(self, not_implemented_func, "Rotate the map clockwise", self.screenWidth-39-self.originX,208-self.originY,"image/C3/paneling_00094.png","image/C3/paneling_00095.png","image/C3/paneling_00096.png")
    listOfButtons.append(self.arrow_rotate_clockwise)
    
    self.clear_land_button = ButtonCtrlPnl(self, clear_land, "Clear land", self.screenWidth-99 - self.originX, 301 - self.originY, "image/C3/paneling_00131.png", "image/C3/paneling_00132.png","image/C3/paneling_00133.png", state='clearLand')
    listOfButtons.append(self.clear_land_button)

    self.build_roads_button = ButtonCtrlPnl(self, build_roads, "Build roads", self.screenWidth - 49 - self.originX ,301 - self.originY,"image/C3/paneling_00135.png","image/C3/paneling_00136.png","image/C3/paneling_00137.png", state='buildRoads')
    listOfButtons.append(self.build_roads_button)
    
    self.build_housing_button = ButtonCtrlPnl(self, build_housing, "Build housing", self.screenWidth-149 - self.originX, 301 - self.originY,"image/C3/paneling_00123.png","image/C3/paneling_00124.png","image/C3/paneling_00125.png", state='buildHousing')
    listOfButtons.append(self.build_housing_button)

    self.water_related_structures = ButtonCtrlPnl(self, build_water_related_structures, "Water related structure", self.screenWidth - 149 - self.originX, 337 - self.originY,"image/C3/paneling_00127.png","image/C3/paneling_00128.png","image/C3/paneling_00129.png", state='buildWaterRelatedStructures')
    listOfButtons.append(self.water_related_structures)

    self.health_related_structures= ButtonCtrlPnl(self, not_implemented_func,  "Health related structures", self.screenWidth-99-self.originX,337-self.originY, "image/C3/paneling_00163.png", "image/C3/paneling_00164.png", "image/C3/paneling_00165.png","image/C3/paneling_00166.png")
    listOfButtons.append(self.health_related_structures)

    self.religious_structures = ButtonCtrlPnl(self, not_implemented_func, "Religious Structures", 0, 0,"image/C3/paneling_00151.png","image/C3/paneling_00152.png","image/C3/paneling_00153.png","image/C3/paneling_00154.png")
    self.religious_structures.change_pos(self.screenWidth - 49 - self.originX, 337 - self.originY)
    listOfButtons.append(self.religious_structures)

    self.education_structures = ButtonCtrlPnl(self, not_implemented_func, "Education Structures", 0, 0,"image/C3/paneling_00147.png","image/C3/paneling_00148.png","image/C3/paneling_00149.png","image/C3/paneling_00150.png")
    self.education_structures.change_pos(self.screenWidth - 149 - self.originX, 377 - self.originY)
    listOfButtons.append(self.education_structures)

    self.entertainment_structures= ButtonCtrlPnl(self, not_implemented_func, "Entertainment_structures", self.screenWidth-99-self.originX,373-self.originY,"image/C3/paneling_00143.png","image/C3/paneling_00144.png","image/C3/paneling_00145.png","image/C3/paneling_00146.png")      
    listOfButtons.append(self.entertainment_structures)

    self.administration_or_government_structures = ButtonCtrlPnl(self, not_implemented_func, "Administration or Government Structures", self.screenWidth-49-self.originX,373-self.originY,"image/C3/paneling_00139.png","image/C3/paneling_00140.png","image/C3/paneling_00141.png")
    listOfButtons.append(self.administration_or_government_structures)

    self.engineering_structures = ButtonCtrlPnl(self, build_engineer_post, "Engineering function", self.screenWidth - 149 - self.originX,409 - self.originY,"image/C3/paneling_00167.png","image/C3/paneling_00168.png","image/C3/paneling_00169.png", state='buildEngineerPost')
    listOfButtons.append(self.engineering_structures)

    self.security_structures = ButtonCtrlPnl(self, build_prefecture, "Security Structures", self.screenWidth - 99 - self.originX, 409 - self.originY, "image/C3/paneling_00159.png","image/C3/paneling_00160.png","image/C3/paneling_00161.png", state='securityStructures')
    listOfButtons.append(self.security_structures)

    self.industrial_structures = ButtonCtrlPnl(self, not_implemented_func, "Industrial Structures", self.screenWidth-49-self.originX,409-self.originY,"image/C3/paneling_00155.png","image/C3/paneling_00156.png","image/C3/paneling_00157.png")
    listOfButtons.append(self.industrial_structures)
    
    self.undo_button = ButtonCtrlPnl(self, not_implemented_func, "Undo", self.screenWidth-149-self.originX, 445-self.originY,"image/C3/paneling_00171.png","image/C3/paneling_00172.png","image/C3/paneling_00173.png","image/C3/paneling_00174.png")
    listOfButtons.append(self.undo_button)
    
    self.message_view_button = ButtonCtrlPnl(self, not_implemented_func, "Message View", self.screenWidth-99-self.originX,445-self.originY,"image/C3/paneling_00115.png","image/C3/paneling_00116.png","image/C3/paneling_00117.png","image/C3/paneling_00118.png")
    listOfButtons.append(self.message_view_button)

    self.see_recent_troubles_button = ButtonCtrlPnl(self, not_implemented_func, "See recent troubles", self.screenWidth-49-self.originX,445-self.originY,"image/C3/paneling_00119.png","image/C3/paneling_00120.png","image/C3/paneling_00121.png","image/C3/paneling_00122.png")
    listOfButtons.append(self.see_recent_troubles_button)

    self.variable_speed_up = ButtonWithImmediatEffect(self, self.increaseSpeed, "Game speed up", self.screenWidth - 149 - self.originX, 490 - self.originY, "image/UI/menu/variable_speed/paneling_00247.png","image/UI/menu/variable_speed/paneling_00248.png","image/UI/menu/variable_speed/paneling_00249.png")
    listOfButtons.append(self.variable_speed_up)

    self.variable_speed_down = ButtonWithImmediatEffect(self, self.decreaseSpeed, "Game speed down", self.screenWidth + self.variable_speed_up.dim[0] - 145 - self.originX, 490 - self.originY, "image/UI/menu/variable_speed/paneling_00251.png","image/UI/menu/variable_speed/paneling_00252.png","image/UI/menu/variable_speed/paneling_00253.png")
    listOfButtons.append(self.variable_speed_down)

    return listOfButtons

  def update(self, currentSpeed) -> None:
    """ Updates controls.

    Args:
        currentSpeed (int): currentSpeed

    Returns:
        None
    """
    # Updates all buttons
    for button in self.listOfButtons:
      button.update()
    # for button2 in self.hiddenButton:
    #   button2.update()


    # Updates l'affichage de la vitesse actuelle du jeu
    if currentSpeed != self.currentSpeed:
      self.currentSpeed = currentSpeed
      self.currentSpeedRender()

  def currentSpeedRender(self) -> None:
    """Blits currentSpeed actualisé sur staticSurface.

    Returns:
        None
    """
    textSurface = self.font.render(f"{str(self.currentSpeed)}%", 0, (255, 255, 255), (0, 0, 0))
    self.staticSurface.blit(textSurface, (self.screenWidth - 50 - self.originX, 490 - self.originY))

  def render(self):
    self.screen.blit(self.staticSurface, self.staticSurfacePos)
    for button in self.listOfButtons:
      button.draw(self.staticSurface)
      button.show_tip(self.screen)
    for button2 in self.hiddenButton:
      button2.draw(self.screen)
      button2.show_tip(self.screen)
  
  def display_overlay_selection(self):
    """ This function is going to show the differrent ooverlay that we can select"""
    # Not working for the moment
    # liste_overlay = ["image/UI/menu/menu_overlay_button.png", "image/UI/menu/menu_fire_overlay.png"]
    # liste_text = ["Select a city overlay report", "Show the risk of the structure to catch fire"]
    # for i, overlay in enumerate(liste_text):
    #   if self.overlays_button.text == overlay:
    #     if i != len(liste_text):
    #       self.overlays_button.change_image(liste_overlay[i])
    #       self.overlays_button.text = liste_text[i]
    #       return None
    #     else:
    #       self.overlays_button.change_image(liste_overlay[0])
    #       self.overlays_button.text = liste_text[0]
    #       return None
    pass