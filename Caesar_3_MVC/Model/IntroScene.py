import pygame
from EventManager.allEvent import *
from Model.constants import *

class IntroScene:
  def __init__(self, screen):
    self.screen = screen
    self.image = pygame.image.load("./image/UI/intro/introScene_background.png").convert_alpha()
    self.surface = pygame.transform.scale(self.image, self.screen.get_size())

    self.quitScene = QuitScene(self.screen, self.surface.copy())
    self.isQuitState = False

    self.defaultFeedback  = StateChangeEvent(STATE_MENU)
  
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

  def render(self):
    if self.isQuitState:
      self.quitScene.render()
    else: self.screen.blit(self.surface, (0,0))
  
class QuitScene:
  def __init__(self, screen, background_surface):
    self.screen = screen
    self.surface = background_surface
    self.image = pygame.image.load("./image/UI/quit/quitScene_background.png").convert_alpha()
    self.posX = (self.screen.get_width()/2) - (self.image.get_width()/2)
    self.posY = (self.screen.get_height()/2) - (self.image.get_height()/2)

    self.initializeItems()

    self.surface.blit(self.image, (self.posX, self.posY))

  def initializeItems(self) -> None:
    self.okButton = pygame.image.load("./image/UI/quit/okButton.png").convert_alpha()
    okButtonPos = ((self.image.get_width()/2) - 2*self.okButton.get_width(), 100)
    self.okButtonRect = pygame.Rect(okButtonPos,  self.okButton.get_size())

    self.cancelButton = pygame.image.load("./image/UI/quit/cancelButton.png").convert_alpha()
    cancelButtonPos = ((self.image.get_width()/2) + self.cancelButton.get_width(), 100)
    self.cancelButtonRect = pygame.Rect(cancelButtonPos,  self.cancelButton.get_size())

    self.image.blit(self.okButton, okButtonPos)
    self.image.blit(self.cancelButton, cancelButtonPos)

  def handleMouseInput(self, event) -> Event:
    mousePosRelative = (event.pos[0] - self.posX, event.pos[1] - self.posY)
    if self.okButtonRect.collidepoint(mousePosRelative): return 1
    elif  self.cancelButtonRect.collidepoint(mousePosRelative): return 2
    else: return 0
      
  def render(self):
    self.screen.blit(self.surface, (0, 0))
  