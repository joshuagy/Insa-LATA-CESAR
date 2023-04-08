from Model.control_panel import *
from ip import *

class TopBar:
  def __init__(self, screen, treasury, population, date):
    self.screen = screen
    self.screenWidth, self.screenHeight = self.screen.get_size()
    self.staticSurface = self.generateStaticSurface()

    self.treasury = treasury
    self.population = population
    self.date = "Jan 340 BC"
    
    self.IP = get_ip()
    print("Ceci est un print to see when am i called")
    print(self.IP)
    #display_surface = pygame.display.set_mode((400, 400))
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('TextnjlnkjnkjnkjnTest', True, (0, 255, 0), (0, 0, 128))
    textRect = text.get_rect()
    self.screen.fill((255, 255, 255))
    self.screen.blit(text, textRect)
   
    
    

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

    self.File = pygame.image.load("image/Menutop/File.png")
    self.File = pygame.transform.scale(self.File, 
                                       (self.File.get_width() * 0.9, self.File.get_height() * 0.7))
    
    self.Options = pygame.image.load("image/Menutop/Options.png")
    self.Options = pygame.transform.scale(self.Options,
                                          (self.Options.get_width() * 0.9, self.Options.get_height() * 0.7))
    
    self.Help = pygame.image.load("image/Menutop/Help.png")
    self.Help = pygame.transform.scale(self.Help, 
                                       (self.Help.get_width() * 0.9, self.Help.get_height() * 0.7))
    
    self.Advisors = pygame.image.load("image/Menutop/Advisors.png")
    self.Advisors = pygame.transform.scale(self.Advisors,
                                           (self.Advisors.get_width() * 0.9, self.Advisors.get_height() * 0.7))
    
    self.OpenToLan = pygame.image.load("image/Menutop/OpenToLan.png")
    self.OpenToLan = pygame.transform.scale(self.OpenToLan, 
                                       (self.OpenToLan.get_width() * 0.9, self.OpenToLan.get_height() * 0.7))

    self.File_rect = self.File.get_rect()
    self.Options_rect = self.Options.get_rect()
    self.Options_rect.x = self.File_rect.x + self.File_rect.width
    self.Help_rect = self.Help.get_rect()
    self.Help_rect.x = self.Options_rect.x + self.Options_rect.width
    self.Advisors_rect = self.Advisors.get_rect()
    self.Advisors_rect.x = self.Help_rect.x + self.Help_rect.width
    self.OpenToLan_rect = self.OpenToLan.get_rect()
    self.OpenToLan_rect.x = self.dateBlocPos[0] + 350

    self.File_menu_Rm = pygame.image.load("image/Menutop/Rm.png")
    self.File_menu_Sg = pygame.image.load("image/Menutop/Sg.png")
    self.File_menu_Eg = pygame.image.load("image/Menutop/Eg.png")
    self.File_menu_Rm = pygame.transform.scale(self.File_menu_Rm,
                                               (self.File.get_width() * 1.5, self.File.get_height() * 1.5))
    self.File_menu_Sg = pygame.transform.scale(self.File_menu_Sg,
                                               (self.File.get_width() * 1.5, self.File.get_height() * 1.5))
    self.File_menu_Eg = pygame.transform.scale(self.File_menu_Eg,
                                               (self.File.get_width() * 1.5, self.File.get_height() * 1.5))

    self.File_menu_Rm_rect = self.File_menu_Rm.get_rect()
    self.File_menu_Rm_rect.y += self.File.get_height()
    self.File_menu_Rm_rect.x -= 0.1
    self.File_menu_Sg_rect = self.File_menu_Sg.get_rect()
    self.File_menu_Sg_rect.y = self.File_menu_Rm_rect.y + self.File_menu_Rm.get_height()
    self.File_menu_Eg_rect = self.File_menu_Eg.get_rect()
    self.File_menu_Eg_rect.y = self.File_menu_Sg_rect.y + self.File_menu_Sg.get_height()

    self.File_bol = False

    self.staticSurface.blit(self.Options, self.Options_rect)
    self.staticSurface.blit(self.Help, self.Help_rect)
    self.staticSurface.blit(self.Advisors, self.Advisors_rect)
    self.staticSurface.blit(self.File, self.File_rect)
    self.staticSurface.blit(self.OpenToLan, self.OpenToLan_rect)
    

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
