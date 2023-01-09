import pygame
from EventManager.allEvent import *
from Model.constants import *

class Menu:
  def __init__(self, screen):
    self.screen = screen
    self.image = pygame.image.load("./image/UI/menu/menu_background.png").convert_alpha()
    self.surface = pygame.transform.scale(self.image, self.screen.get_size())
    self.items = []
    self.initializeItems()

    self.quitScene = QuitScene(self.screen, self.surface.copy())
    self.isQuitState = False

    self.loadScene = LoadScene(self.screen, self.surface.copy())
    self.isLoadState = False

    self.defaultFeedback = TickEvent() # do nothing

    self.currentMousePos = (0, 0)

  def initializeItems(self):
    startButton = MenuButton(self.surface, "./image/UI/menu/menu_start_button.png", 0, StateChangeEvent(STATE_PLAY))
    loadSaveButton = MenuButton(self.surface, "./image/UI/menu/menu_load_save_button.png", 1, LoadEvent())
    exitButton = MenuButton(self.surface, "./image/UI/menu/menu_exit_button.png", 2, QuitEvent())
    
    self.items.append(startButton)
    self.items.append(loadSaveButton)
    self.items.append(exitButton)

  def renderItems(self) -> None:
    for item in self.items:
      item.render(self.currentMousePos)

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
    elif self.isLoadState:
      loadSceneFeedBack = self.loadScene.handleMouseInput(event)
      match loadSceneFeedBack:
        case 1:
          self.isLoadState = False
          return TickEvent()
        case 2:
          self.isLoadState = False
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
          elif isinstance(item.feedback, LoadEvent):
            self.isLoadState = True
            return TickEvent()
          else:
            return item.feedback

    return self.defaultFeedback

  def handleHoverEvent(self, mousePos):
    self.currentMousePos = mousePos

  def render(self):
    if self.isQuitState:
      self.quitScene.render(self.currentMousePos)
    elif self.isLoadState:
      self.loadScene.render()
    else: 
      self.renderItems()
      self.screen.blit(self.surface, (0, 0))


class LoadScene:
  def __init__(self, screen, background_surface):
    self.screen = screen
    self.surface = background_surface
    self.image = pygame.Surface((400, 400))
    self.image.fill((0, 0, 0))
    self.posX = (self.screen.get_width()/2) - (self.image.get_width()/2)
    self.posY = (self.screen.get_height()/2) - (self.image.get_height()/2)

    self.currentSaveLoaded = "save1"
    self.font = pygame.font.SysFont(None, 24)

    self.SaveSelector = None
    self.initializeItems()

    self.surface.blit(self.image, (self.posX, self.posY))
  
  def initializeItems(self) -> None:
    # Item 1
    currentSaveLoaded = pygame.Surface((380, 30))
    currentSaveLoaded.fill((255, 255, 255))
    currentSaveLoadedPos = (self.image.get_width()/2 - currentSaveLoaded.get_width()/2, 10)
    
    currentSaveLoadedText = self.font.render(self.currentSaveLoaded, 0, (0, 0, 0))
    currentSaveLoadedTextPos = (currentSaveLoadedPos[0]+5, currentSaveLoaded.get_height()/2 - currentSaveLoadedText.get_height()/2)
    currentSaveLoaded.blit(currentSaveLoadedText, currentSaveLoadedTextPos)

    # Item 4 
    self.saveSelector = self.getCurrentSaveSelector()  

    # Item 2
    self.okButton = pygame.image.load("./image/UI/quit/okButton.png")
    okButtonPos = ((self.image.get_width()/2) - 2*self.okButton.get_width(), (self.image.get_height() - self.okButton.get_height())-10)
    self.okButtonRect = pygame.Rect(okButtonPos,  self.okButton.get_size())

    # Item 3
    self.cancelButton = pygame.image.load("./image/UI/quit/cancelButton.png")
    cancelButtonPos = ((self.image.get_width()/2) + self.cancelButton.get_width(), (self.image.get_height() - self.cancelButton.get_height())-10)
    self.cancelButtonRect = pygame.Rect(cancelButtonPos, self.cancelButton.get_size())

    # Blit all items
    self.image.blit(self.okButton, okButtonPos)
    self.image.blit(self.cancelButton, cancelButtonPos)
    self.image.blit(currentSaveLoaded, currentSaveLoadedPos)
    self.image.blit(self.saveSelector[0], self.saveSelector[1])

  def getCurrentSaveSelector(self): 
    currrentSaveSelector = pygame.Surface((380, 200))
    currrentSaveSelector.fill((255, 255, 255))
    currrentSaveSelectorPos = (self.image.get_width()/2 - currrentSaveSelector.get_width()/2, 50)

    for idx, saveName in enumerate(["save1", "save2", "save3"]):
      item = pygame.Surface((300, 20))
      item.fill((0, 0, 0))
      itemPos = (5, 5 + 30*idx)

      itemText = self.font.render(saveName, 1, (255, 255, 255))
      itemTextPos = (itemPos[0]+5, currrentSaveSelector.get_height()/2 - itemText.get_height()/2)
      item.blit(itemText, itemTextPos)

      currrentSaveSelector.blit(item, itemPos)

    return (currrentSaveSelector, currrentSaveSelectorPos)

  def getMousePosRelative(self, event):
    return (event.pos[0] - self.posX, event.pos[1] - self.posY)
    
  def handleMouseInput(self, event) -> Event:
    mousePosRelative = self.getMousePosRelative(event)
    if self.okButtonRect.collidepoint(mousePosRelative): return 1
    elif  self.cancelButtonRect.collidepoint(mousePosRelative): return 2
    else: return 0

  def render(self):
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

class MenuButton:
  def __init__(self, surface_to_blit, image, idx_item, feedback: Event):
    self.surface_to_blit = surface_to_blit
    self.image = pygame.image.load(image).convert_alpha()
    self.surface = pygame.transform.scale(self.image, (274, 26))

    self.hoveredSurface = self.surface.copy()
    filter = pygame.Surface(self.surface.get_size()).convert_alpha()
    filter.fill((180, 180, 180))
    self.hoveredSurface.blit(filter, (0,0), special_flags = pygame.BLEND_RGBA_MULT)

    self.pos = (self.surface_to_blit.get_width()/2 - self.surface.get_width()/2, 300+idx_item*40)
    self.rect = pygame.Rect(self.pos, self.surface.get_size())

    self.feedback = feedback

  def render(self, currentMousePos):
    if self.rect.collidepoint(currentMousePos):
      self.surface_to_blit.blit(self.hoveredSurface, self.pos)
    else: 
      self.surface_to_blit.blit(self.surface, self.pos)