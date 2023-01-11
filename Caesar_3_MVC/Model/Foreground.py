import pygame
from Model.control_panel import *

class Foreground:
  def __init__(self, screen, nbr_cell_x, nbr_cell_y):
    self.screen = screen
    self.nbr_cell_x = nbr_cell_x
    self.nbr_cell_y = nbr_cell_y
    self.screenWidth, self.screenHeight = self.screen.get_size()

    self.foregroundGrid = None
    self.initForegroundGrid()

    self.originalImageActiveBuildHouse = pygame.image.load('image/Buildings/Housng1a_00045.png').convert_alpha()
    self.originalImageActiveBuildHouse = pygame.transform.scale(self.originalImageActiveBuildHouse, (self.originalImageActiveBuildHouse.get_width() / 2, self.originalImageActiveBuildHouse.get_height() / 2))

  def initForegroundGrid(self):
    self.foregroundGrid = [[None for _ in range(self.nbr_cell_x)] for _ in range(self.nbr_cell_y)]
  
  def addEffect(self, x, y, effect):
    self.foregroundGrid[x][y] = effect
  
  def hasEffect(self, x, y):
    return self.foregroundGrid[x][y] != None

  def getEffect(self, x, y):
    return self.foregroundGrid[x][y]

  def getEffectedImage(self, id_image, originalImage, x, y):
    effect = self.getEffect(x, y)
    effectedImage = pygame.Surface(originalImage.get_size()).convert_alpha()
    if effect == 'activeClearLand':
      effectedImage.fill((200, 0, 0))
      originalImage.blit(effectedImage, (0, 0), special_flags = pygame.BLEND_RGBA_MULT)
    elif effect == 'activeBuildHouse':
      originalImage = self.originalImageActiveBuildHouse.copy()
      mask = pygame.mask.from_surface(originalImage)
      effectedImage = mask.to_surface()
      effectedImage.set_colorkey((0, 0, 0))
      effectedImage.set_alpha(40)
      originalImage.blit(effectedImage, (0, 0))
    elif effect == 'activeBuildRoads':
      effectedImage.fill((0, 0, 100))
      originalImage.blit(effectedImage, (0, 0), special_flags = pygame.BLEND_RGBA_MULT)
    elif effect == 'wrong':
      effectedImage.fill((200, 0, 0))
      originalImage.blit(effectedImage, (0, 0), special_flags = pygame.BLEND_RGBA_MULT)
    elif effect == 'default':
      mask = pygame.mask.from_surface(originalImage)
      effectedImage = mask.to_surface()
      effectedImage.set_colorkey((0, 0, 0))
      effectedImage.set_alpha(65)
      originalImage.blit(effectedImage, (0, 0))
    return originalImage
    
  def render(self):
    pass