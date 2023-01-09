import pygame

class Foreground:
  def __init__(self, screen, nbr_cell_x, nbr_cell_y):
    self.screen = screen
    self.nbr_cell_x = nbr_cell_x
    self.nbr_cell_y = nbr_cell_y
    self.screenWidth, self.screenHeight = self.screen.get_size()

    self.foregroundGrid = None
    self.initForegroundGrid()

  def initForegroundGrid(self):
    self.foregroundGrid = [[None for _ in range(self.nbr_cell_x)] for _ in range(self.nbr_cell_y)]
  
  def addEffect(self, x, y, effect):
    self.foregroundGrid[x][y] = effect
  
  def hasEffect(self, x, y):
    return self.foregroundGrid[x][y] != None

  def getEffect(self, x, y):
    return self.foregroundGrid[x][y]

  def getEffectedImage(self, originalImage, x, y):
    effectedImage = pygame.Surface(originalImage.get_size()).convert_alpha()
    if self.getEffect(x, y) == 'red':
      effectedImage.fill((200, 0, 0))
    elif self.getEffect(x, y) == 'default':
      effectedImage.fill((150, 150, 150))
    originalImage.blit(effectedImage, (0, 0), special_flags = pygame.BLEND_RGBA_MULT)
    return originalImage
    
  def render(self):
    pass