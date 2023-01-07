import pygame
from EventManager.allEvent import *
from Model.constants import *

class IntroScene:
  def __init__(self, screen):
    self.screen = screen
    self.image = pygame.image.load("./image/UI/intro/introScene_title.png").convert_alpha()
    self.surface = pygame.Surface(self.screen.get_size())

    self.imagePos = (self.surface.get_width()/2 - self.image.get_width()/2, self.surface.get_height()/2 - self.image.get_height()/2)
    
    self.surface.fill((0, 0, 0))

    self.surface.blit(self.image, self.imagePos)

    self.font = pygame.font.Font("./assets/caesar.ttf", 20)

    self.textSurface = self.font.render("Click To Start", True, (255, 255, 255), (0, 0, 0))
    self.textSurfacePos = (self.surface.get_width()/2 - self.textSurface.get_width()/2, self.surface.get_height()/2 + self.image.get_height()/2 + 25)
    self.surface.blit(self.textSurface, self.textSurfacePos)

    self.quitScene = QuitScene(self.screen, self.surface.copy())
    self.isQuitState = False

    self.defaultFeedback  = StateChangeEvent(STATE_MENU)

    self.currentMousePos = (0, 0)

  def handleMouseInput(self, event) -> Event:
    if self.isQuitState:
      quitSceneFeedBack = self.quitScene.handleMouseInput(event)
      print(quitSceneFeedBack)
      match quitSceneFeedBack:
        case 1:
          return ExitEvent()
        case 2:
          self.isQuitState = False
          return TickEvent()
        case _:
          return TickEvent()
    return self.defaultFeedback
    
  def handleKeyboardInput(self, event) -> None:
    if event.key == pygame.K_ESCAPE:
      self.isQuitState = True

  def handleHoverEvent(self, mousePos):
    self.currentMousePos = mousePos

  def render(self):
    if self.isQuitState:
      self.quitScene.render(self.currentMousePos)
    else: 
      self.screen.blit(self.surface, (0, 0))
  
class QuitScene:
  def __init__(self, screen, background_surface):
    self.screen = screen
    self.surface = background_surface
    self.image = pygame.image.load("./image/UI/quit/quitScene_background.png").convert_alpha()
    self.posX = (self.screen.get_width()/2) - (self.image.get_width()/2)
    self.posY = (self.screen.get_height()/2) - (self.image.get_height()/2)

    self.initializeItems()

  def initializeItems(self) -> None:
    self.okButton = pygame.image.load("./image/UI/quit/okButton.png").convert_alpha()
    self.okButtonHovered = pygame.image.load("./image/UI/quit/okButton_hovered.png").convert_alpha()
    self.okButtonPos = ((self.image.get_width()/2) - 2*self.okButton.get_width(), 100)
    self.okButtonRect = pygame.Rect(self.okButtonPos,  self.okButton.get_size())

    self.cancelButton = pygame.image.load("./image/UI/quit/cancelButton.png").convert_alpha()
    self.cancelButtonHovered = pygame.image.load("./image/UI/quit/cancelButton_hovered.png").convert_alpha()
    self.cancelButtonPos = ((self.image.get_width()/2) + self.cancelButton.get_width(), 100)
    self.cancelButtonRect = pygame.Rect(self.cancelButtonPos,  self.cancelButton.get_size())
    
  def getMousePosRelative(self, pos):
    return (pos[0] - self.posX, pos[1] - self.posY)

  def handleMouseInput(self, event) -> Event:
    mousePosRelative = self.getMousePosRelative(event.pos)
    if self.okButtonRect.collidepoint(mousePosRelative): return 1
    elif  self.cancelButtonRect.collidepoint(mousePosRelative): return 2
    else: return 0

  def render(self, currentMousePos):
    mousePosRelative = self.getMousePosRelative(currentMousePos)
    if self.okButtonRect.collidepoint(mousePosRelative):
       self.image.blit(self.okButtonHovered, self.okButtonPos)
    else:
        self.image.blit(self.okButton, self.okButtonPos)
  
    if self.cancelButtonRect.collidepoint(mousePosRelative):
      self.image.blit(self.cancelButtonHovered, self.cancelButtonPos)
    else: 
      self.image.blit(self.cancelButton, self.cancelButtonPos)

    self.surface.blit(self.image, (self.posX, self.posY))
    self.screen.blit(self.surface, (0, 0))