from Model.control_panel import *

class TopBar:
  def __init__(self, screen, treasury, population, date):
    self.screen = screen
    self.screenWidth, self.screenHeight = self.screen.get_size()
    self.staticSurface = self.generateStaticSurface()

    self.treasury = treasury
    self.population = population
    self.date = "Jan 340 BC"

    self.treasuryBloc = bloc_top_menu.img_scaled.copy()
    self.treasuryBlocPos = (480, 0)
    self.treasuryBloc.blit(TextRender("Dn",(25,20)).img_scaled,(490 - self.treasuryBlocPos[0], 2.5))
    self.treasuryBlocWithDynamicText = self.treasuryBloc.copy()
    self.treasuryBlocWithDynamicText.blit(TextRender(str(self.treasury), (60-self.get_snss_treasury(), 20)).img_scaled, (520 - self.treasuryBlocPos[0], 2.5))

    self.populationBloc = bloc_top_menu.img_scaled.copy()
    self.populationBlocPos = (480+ bloc_top_menu.dim[0]+24,0)
    self.populationBloc.blit(TextRender("Pop",(30,20)).img_scaled,(637 - self.populationBlocPos[0], 2.5))
    self.populationBlocWithDynamicText = self.populationBloc.copy()
    self.populationBlocWithDynamicText.blit(TextRender(str(self.population), (60-self.get_snss_population(), 20)).img_scaled, (680 - self.populationBlocPos[0], 2.5))

    self.dateBloc = bloc_top_menu.img_scaled.copy()
    self.dateBlocPos = (840, 0)
    self.dateBlocWithDynamicText = self.dateBloc.copy()
    self.dateBlocWithDynamicText.blit(TextRender(date.visualDate, (100, 20),(255,255,0)).img_scaled, (850 - self.dateBlocPos[0], 2.5))

  def generateStaticSurface(self):
    staticSurface = pygame.Surface((self.screenWidth, int(pnl_4.dim[1])+1))
    top_menu_axis_x = 0
    while (top_menu_axis_x < self.screenWidth):        
        staticSurface.blit(pnl_1.img_scaled,(top_menu_axis_x,0))
        top_menu_axis_x+=pnl_1.dim[0]
        staticSurface.blit(pnl_2.img_scaled,(top_menu_axis_x,0))
        top_menu_axis_x+=pnl_2.dim[0]
        staticSurface.blit(pnl_3.img_scaled,(top_menu_axis_x,0))
        top_menu_axis_x+=pnl_3.dim[0]
        staticSurface.blit(pnl_4.img_scaled,(top_menu_axis_x,0))
        top_menu_axis_x+=pnl_4.dim[0]
        staticSurface.blit(pnl_5.img_scaled,(top_menu_axis_x,0))
        top_menu_axis_x+=pnl_5.dim[0]
        staticSurface.blit(pnl_6.img_scaled,(top_menu_axis_x,0))
        top_menu_axis_x+=pnl_6.dim[0]
        staticSurface.blit(pnl_7.img_scaled,(top_menu_axis_x,0))
        top_menu_axis_x+=pnl_7.dim[0]
        staticSurface.blit(pnl_8.img_scaled,(top_menu_axis_x,0))
        top_menu_axis_x+=pnl_8.dim[0]         
      
        staticSurface.blit(bloc_top_menu.img_scaled,(480+(2*bloc_top_menu.dim[0])+120,0)) 

    return staticSurface
      
  def get_snss_treasury(self):
    return 15 if 99 < abs(self.treasury) < 1000 else 30 if 9<abs(self.treasury)<100 else 68 if abs(self.treasury)<10 else 0  #Smaller number -> smaller size
 
  def get_snss_population(self):
    return 15 if 99 < abs(self.population) < 1000 else 30 if 9<abs(self.population)<100 else 40 if abs(self.population)<10 else 0  #Smaller number -> smaller size

  def update(self, treasury, population, date):
    if self.treasury != treasury:
      self.treasury = treasury
      self.treasuryBlocWithDynamicText = self.treasuryBloc.copy()
      self.treasuryBlocWithDynamicText.blit(TextRender(str(self.treasury), (60-self.get_snss_treasury(), 20)).img_scaled, (520 - self.treasuryBlocPos[0], 2.5))

    if self.population != population:
      self.population = population   
      self.populationBlocWithDynamicText = self.populationBloc.copy()
      self.populationBlocWithDynamicText.blit(TextRender(str(self.population), (60-self.get_snss_population(), 20)).img_scaled, (680 - self.populationBlocPos[0], 2.5))

    if self.date != date.visualDate :
      self.date = date.visualDate
      self.dateBlocWithDynamicText = self.dateBloc.copy()
      self.dateBlocWithDynamicText.blit(TextRender(date.visualDate, (100, 20),(255,255,0)).img_scaled, (850 - self.dateBlocPos[0], 2.5))


  def render(self):
    self.staticSurface.blit(self.treasuryBlocWithDynamicText, self.treasuryBlocPos)
    self.staticSurface.blit(self.populationBlocWithDynamicText, self.populationBlocPos)
    self.staticSurface.blit(self.dateBlocWithDynamicText, self.dateBlocPos)
    self.screen.blit(self.staticSurface, (0, 0))