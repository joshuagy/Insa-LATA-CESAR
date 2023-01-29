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

    self.overlayGrid = None
    self.initOverlayGrid()
    self.overlayName = None

    self.originalImageActiveBuildHouse = pygame.image.load('image/Buildings/Housng1a_00045.png').convert_alpha()
    self.originalImageActiveBuildHouse = pygame.transform.scale(self.originalImageActiveBuildHouse, (self.originalImageActiveBuildHouse.get_width() / 2, self.originalImageActiveBuildHouse.get_height() / 2))

    self.originalImageActiveEngineerPost = pygame.image.load('image/Buildings/transport_00056.png').convert_alpha()
    self.originalImageActiveEngineerPost = pygame.transform.scale(self.originalImageActiveEngineerPost, (self.originalImageActiveEngineerPost.get_width() / 2, self.originalImageActiveEngineerPost.get_height() / 2))

    self.originalImageActiveSecurityStructures = pygame.image.load('image/Buildings/Security_00001.png').convert_alpha()
    self.originalImageActiveSecurityStructures = pygame.transform.scale(self.originalImageActiveSecurityStructures, (self.originalImageActiveSecurityStructures.get_width() / 2, self.originalImageActiveSecurityStructures.get_height() / 2))

    self.originalImageActiveAA = pygame.image.load('image/Buildings/Utilitya_00001.png').convert_alpha()
    self.originalImageActiveAA = pygame.transform.scale(self.originalImageActiveAA, (self.originalImageActiveAA.get_width() / 2, self.originalImageActiveAA.get_height() / 2))


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
      print(id_image, " active clear land")
      originalImage.blit(effectedImage, (0, 0), special_flags = pygame.BLEND_RGBA_MULT)
    elif effect == 'activeBuildHouse':
      originalImage = self.originalImageActiveBuildHouse.copy()
      mask = pygame.mask.from_surface(originalImage)
      effectedImage = mask.to_surface()
      effectedImage.set_colorkey((0, 0, 0))
      effectedImage.set_alpha(120)
      originalImage.blit(effectedImage, (0, 0))
    elif effect == 'activeBuildRoads':
      effectedImage.fill((0, 0, 100))
      originalImage.blit(effectedImage, (0, 0), special_flags = pygame.BLEND_RGBA_MULT)
    elif effect == 'wrong':
      effectedImage.fill((200, 0, 0))
      originalImage.blit(effectedImage, (0, 0), special_flags = pygame.BLEND_RGBA_MULT)
    elif effect == 'activeEngineerPost':
      originalImage = self.originalImageActiveEngineerPost.copy()
      mask = pygame.mask.from_surface(originalImage)
      effectedImage = mask.to_surface()
      effectedImage.set_colorkey((0, 0, 0))
      effectedImage.set_alpha(120)
      originalImage.blit(effectedImage, (0, 0))
    elif effect == 'activeSecurityStructures':
      originalImage = self.originalImageActiveSecurityStructures.copy()
      mask = pygame.mask.from_surface(originalImage)
      effectedImage = mask.to_surface()
      effectedImage.set_colorkey((0, 0, 0))
      effectedImage.set_alpha(120)
      originalImage.blit(effectedImage, (0, 0))
    elif effect == "activeAA":
      originalImage = self.originalImageActiveAA.copy()
      mask = pygame.mask.from_surface(originalImage)
      effectedImage = mask.to_surface()
      effectedImage.set_colorkey((0, 0, 0))
      effectedImage.set_alpha(120)
      originalImage.blit(effectedImage, (0, 0))
    elif effect == 'default':
      mask = pygame.mask.from_surface(originalImage)
      effectedImage = mask.to_surface()
      effectedImage.set_colorkey((0, 0, 0))
      effectedImage.set_alpha(65)
      originalImage.blit(effectedImage, (0, 0))
    return originalImage

  def initOverlayGrid(self):
    self.overlayGrid = [[None for _ in range(self.nbr_cell_x)] for _ in range(self.nbr_cell_y)]
  
  def setOverlayName(self, name):
    self.overlayName = name
  
  def getOverlayName(self):
    return self.overlayName

  def addOverlayInfo(self, x, y, level):
    self.overlayGrid[x][y] = level
  
  def getOverlayInfo(self, x, y):
    return self.overlayGrid[x][y]

  def putRed(self, originalImage):
      effectedImage = pygame.Surface(originalImage.get_size()).convert_alpha()
      effectedImage.fill((200, 0, 0))
      originalImage.blit(effectedImage, (0, 0), special_flags = pygame.BLEND_RGBA_MULT)
      return originalImage

  def putGreenYellow(self, originalImage):
      effectedImage = pygame.Surface(originalImage.get_size()).convert_alpha()
      effectedImage.fill((130, 185, 46))
      originalImage.blit(effectedImage, (0, 0), special_flags = pygame.BLEND_RGBA_MULT)
      return originalImage

  def putYellow(self, originalImage):
        effectedImage = pygame.Surface(originalImage.get_size()).convert_alpha()
        effectedImage.fill((255, 255, 0))
        originalImage.blit(effectedImage, (0, 0), special_flags = pygame.BLEND_RGBA_MULT)
        return originalImage

  def putYellowOrange(self, originalImage):
        effectedImage = pygame.Surface(originalImage.get_size()).convert_alpha()
        effectedImage.fill((255, 183, 0))
        originalImage.blit(effectedImage, (0, 0), special_flags = pygame.BLEND_RGBA_MULT)
        return originalImage

  def putOrange(self, originalImage):
        effectedImage = pygame.Surface(originalImage.get_size()).convert_alpha()
        effectedImage.fill((255, 130, 0))
        originalImage.blit(effectedImage, (0, 0), special_flags = pygame.BLEND_RGBA_MULT)
        return originalImage
  
  def putOrangeRed(self, originalImage):
      effectedImage = pygame.Surface(originalImage.get_size()).convert_alpha()
      effectedImage.fill((255, 94, 0))
      originalImage.blit(effectedImage, (0, 0), special_flags = pygame.BLEND_RGBA_MULT)
      return originalImage

  def putGreen(self, originalImage):
    effectedImage = pygame.Surface(originalImage.get_size()).convert_alpha()
    effectedImage.fill((0, 200, 0))
    originalImage.blit(effectedImage, (0, 0), special_flags = pygame.BLEND_RGBA_MULT)
    return originalImage

  def render(self):
    pass