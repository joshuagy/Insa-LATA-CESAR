import pygame
from EventManager.allEvent import *
from Model.constants import *

class Menu:
  def __init__(self, screen):
    self.screen = screen
    self.image = pygame.image.load("./image/UI/menu/menu_background.png").convert_alpha()
    self.surface = pygame.transform.scale(self.image, self.screen.get_size())
    self.items = []
    self.initialize_items()

    self.quitScene = QuitScene(self.screen, self.surface.copy())
    self.isQuitState = False

    self.defaultFeedback = TickEvent() # do nothing

  def initialize_items(self):
    startButton = MenuButton(self.surface, "./image/UI/menu/menu_start_button.png", 0, StateChangeEvent(STATE_PLAY))
    loadSaveButton = MenuButton(self.surface, "./image/UI/menu/menu_load_save_button.png", 1, TickEvent)
    exitButton = MenuButton(self.surface, "./image/UI/menu/menu_exit_button.png", 2, QuitEvent())
    
    self.items.append(startButton)
    self.items.append(loadSaveButton)
    self.items.append(exitButton)

  def renderItems(self) -> None:
    for item in self.items:
      item.render()

  def handleMouseInput(self, event) -> Event:
    if self.isQuitState:
      quitSceneFeedBack = self.quitScene.handleMouseInput(event)
      match quitSceneFeedBack:
        case 1:
          return ExitEvent()
        case 2:
          self.isQuitState = False
          return TickEvent()
        case _:
          return TickEvent()
    else:
      for item in self.items:
        if item.rect.collidepoint(event.pos):
          print(item.feedback, isinstance(item.feedback, QuitEvent))
          if isinstance(item.feedback, QuitEvent):
            self.isQuitState = True
            return TickEvent()
          else:
            return item.feedback

    return self.defaultFeedback

  def render(self):
    if self.isQuitState:
      self.quitScene.render()
    else: 
      self.renderItems()
      self.screen.blit(self.surface, (0, 0))
  
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


class MenuButton:
  def __init__(self, surface_to_blit, image, idx_item, feedback: Event):
    self.surface_to_blit = surface_to_blit
    self.image = pygame.image.load(image).convert_alpha()
    self.surface = pygame.transform.scale(self.image, (270, 23))
    self.pos = (self.surface_to_blit.get_width()/2 - self.surface.get_width()/2, 300+idx_item*40)
    self.rect = pygame.Rect(self.pos, self.surface.get_size())

    self.feedback = feedback

  def render(self):
    self.surface_to_blit.blit(self.surface, self.pos)
  