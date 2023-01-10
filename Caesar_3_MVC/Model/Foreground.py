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
    elif effect == 'defaultClearLand':
      if id_image in list_of_undestructible: effectedImage.fill((150, 0, 0))
      else: effectedImage.fill((0, 200, 0))
      originalImage.blit(effectedImage, (0, 0), special_flags = pygame.BLEND_RGBA_MULT)
    elif effect== 'previewHouse':
      mask = pygame.mask.from_surface(originalImage)
      effectedImage = mask.to_surface()
      effectedImage.set_colorkey((0, 0, 0))
      effectedImage.set_alpha(100)
      originalImage.blit(effectedImage, (0, 0))
    elif effect == 'defaultBuildHouse':
      mask = pygame.mask.from_surface(originalImage)
      effectedImage = mask.to_surface()
      effectedImage.set_colorkey((0, 0, 0))
      effectedImage.set_alpha(65)
      originalImage.blit(effectedImage, (0, 0))
    elif effect == 'activeBuildRoads':
      mask = pygame.mask.from_surface(originalImage)
      effectedImage = mask.to_surface()
      effectedImage.set_colorkey((0, 0, 0))
      effectedImage.set_alpha(80)
      originalImage.blit(effectedImage, (0, 0))
    elif effect == 'default':
      mask = pygame.mask.from_surface(originalImage)
      effectedImage = mask.to_surface()
      effectedImage.set_colorkey((0, 0, 0))
      effectedImage.set_alpha(65)
      originalImage.blit(effectedImage, (0, 0))
    return originalImage
    
  def render(self):
    pass