import pygame
import os
from EventManager.allEvent import *
from Model.constants import *

class Menu:
  def __init__(self, screen, soundMixer):
    self.screen = screen
    self.image = pygame.image.load("./image/UI/menu/menu_background.png").convert_alpha()
    self.surface = pygame.transform.scale(self.image, self.screen.get_size())
    self.items = []

    self.soundMixer = soundMixer

    self.initializeItems()

    self.quitScene = None
    self.isQuitState = False

    self.loadScene = None
    self.isLoadState = False

    self.joinIPScene = None
    self.isJoinIPState = False

    self.defaultFeedback = TickEvent() # do nothing

    # default mouse position
    self.currentMousePos = (0, 0)

    self.logo = pygame.image.load("./image/UI/menu/logoMenu.png").convert_alpha()
    self.surface.blit(self.logo, (self.surface.get_width()/2 - self.logo.get_width()/2, 200))

  def initializeItems(self):
    startButton = MenuButton(self.surface, "./image/UI/menu/menu_start_button.png", 0, StateChangeEvent(STATE_PLAY))
    loadSaveButton = MenuButton(self.surface, "./image/UI/menu/menu_load_save_button.png", 1, LoadEvent())
    joinLocalNetworkButton = MenuButton(self.surface, "./image/UI/menu/join_local_network.png", 2, LoadEvent())
    joinIPAddressButton = MenuButton(self.surface, "./image/UI/menu/join_by_IP.png", 3, JoinIPEvent())
    exitButton = MenuButton(self.surface, "./image/UI/menu/menu_exit_button.png", 4, QuitEvent())
    
    self.items.append(startButton)
    self.items.append(loadSaveButton)
    self.items.append(joinLocalNetworkButton)
    self.items.append(joinIPAddressButton)
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
      if isinstance(loadSceneFeedBack, TickEvent):
        self.isLoadState = False
        self.soundMixer.playEffect('clickEffect')
        return loadSceneFeedBack
      elif isinstance(loadSceneFeedBack, LoadSave):
          self.soundMixer.playEffect('clickEffect')
          self.isLoadState = False
          return loadSceneFeedBack
      elif self.isJoinIPState:
        self.isLoadState = False
        self.soundMixer.playEffect('clickEffect')

    elif self.isJoinIPState:
      joinIPSceneFeedBack = self.joinIPScene.handleMouseInput(event)
      if isinstance(joinIPSceneFeedBack, TickEvent):
        self.isJoinIPState = False
        self.soundMixer.playEffect('clickEffect')
        return joinIPSceneFeedBack
      else:
       return TickEvent()
    else:
      for item in self.items:
        if item.rect.collidepoint(event.pos):
          if isinstance(item.feedback, QuitEvent):
            self.soundMixer.playEffect('clickEffect')
            self.quitScene = QuitScene(self.screen, self.surface.copy(), self.soundMixer)
            self.isQuitState = True
            return TickEvent()
          elif isinstance(item.feedback, LoadEvent):
            self.soundMixer.playEffect('clickEffect')
            self.loadScene = LoadScene(self.screen, self.surface.copy(), self.soundMixer)
            self.isLoadState = True
            return TickEvent()
          elif isinstance(item.feedback, JoinIPEvent):
            self.soundMixer.playEffect('clickEffect')
            self.joinIPScene = JoinIPScene(self.screen, self.surface.copy(), self.soundMixer)
            self.isJoinIPState = True
            return TickEvent()
          else:
            self.soundMixer.playEffect('clickEffect')
            return item.feedback

    return self.defaultFeedback

  def handleHoverEvent(self, mousePos):
    self.currentMousePos = mousePos

  def render(self):
    if self.isQuitState:
      self.quitScene.render(self.currentMousePos)
    elif self.isLoadState:
      self.loadScene.render()
    elif self.isJoinIPState:
      self.joinIPScene.render()
    else: 
      self.renderItems()
      self.screen.blit(self.surface, (0, 0))


class LoadScene:
  def __init__(self, screen, background_surface, soundMixer):
    self.screen = screen
    self.surface = background_surface
    self.soundMixer = soundMixer

    self.image = pygame.image.load("./image/UI/menu/loadInterface.png").convert_alpha()
    self.defaultSurface = pygame.transform.scale(self.image, (400, 400))

    self.surface = self.defaultSurface.copy()

    self.posX = (self.screen.get_width()/2) - (self.surface.get_width()/2)
    self.posY = (self.screen.get_height()/2) - (self.surface.get_height()/2)

    self.font = pygame.font.SysFont(None, 24)

    self.saveFileNames = [f for f in os.listdir("./Model/Save_Folder") if os.path.isfile(os.path.join("./Model/Save_Folder", f))]
    if ".DS_Store" in self.saveFileNames:
      self.saveFileNames.remove(".DS_Store")
    self.saveFileNames.remove("DefaultMap.pickle")
    
    if len(self.saveFileNames) == 0:
      self.currentSaveLoaded = "No save file found"
    else:
      self.currentSaveLoaded = self.saveFileNames[0]

    self.saveItems = []

    self.getSaveItems()

    self.feedback = LoadSave("DefaultMap.pickle")

    self.okButton = pygame.image.load("./image/UI/quit/okButton.png")
    self.okButtonPos = ((self.surface.get_width()/2) + self.okButton.get_width(), (self.surface.get_height() - self.okButton.get_height())-20)
    self.okButtonRect = pygame.Rect(self.okButtonPos,  self.okButton.get_size())

    self.cancelButton = pygame.image.load("./image/UI/quit/cancelButton.png")
    self.cancelButtonPos = ((self.surface.get_width()/2) + 3*self.cancelButton.get_width(), (self.surface.get_height() - self.cancelButton.get_height())-20)
    self.cancelButtonRect = pygame.Rect(self.cancelButtonPos, self.cancelButton.get_size())
 
  def currentSaveSelectedSurface(self):
    currentSaveSelected = pygame.Surface((380, 30)).convert_alpha()
    currentSaveSelectedPos = (self.surface.get_width()/2 - currentSaveSelected.get_width()/2 + 20, 60)
    currentSaveSelectedText = self.font.render(self.currentSaveLoaded, 0, (0, 0, 0))
    currentSaveSelectedTextPos = (currentSaveSelectedPos[0]+5, currentSaveSelected.get_height()/2 - currentSaveSelectedText.get_height()/2)
    return (currentSaveSelectedText, currentSaveSelectedPos)
  
  def saveSelectorSurface(self):
    saveSelector = pygame.Surface((380, 200))
    saveSelectorPos = (self.surface.get_width()/2 - saveSelector.get_width()/2, 70)
    return (saveSelector, saveSelectorPos)

  def getSaveItems(self): 
    for idx, saveName in enumerate(self.saveFileNames):
      item = ItemLoadScene(saveName, idx, self.font)
      self.saveItems.append(item)
    if len(self.saveItems) > 0:
      self.saveItems[0].selected = True

  def getMousePosRelative(self, event):
    return (event.pos[0] - self.posX, event.pos[1] - self.posY)
    
  def handleMouseInput(self, event) -> Event:
    mousePosRelative = self.getMousePosRelative(event)
    for item in self.saveItems:
      if item.textRect.collidepoint(mousePosRelative):
        item.selected = True
        self.currentSaveLoaded = item.saveName
        self.soundMixer.playEffect('clickEffect')
        for a in self.saveItems:
          if a.saveName != item.saveName:
            a.selected = False
        break
    if self.okButtonRect.collidepoint(mousePosRelative): 
      self.soundMixer.playEffect('clickEffect')
      self.feedback = LoadSave(self.currentSaveLoaded)
      return self.feedback
    elif  self.cancelButtonRect.collidepoint(mousePosRelative):
       self.soundMixer.playEffect('clickEffect')
       return TickEvent()
    else: return 0

  def render(self):
    self.screen.blit(self.defaultSurface, (self.posX, self.posY))
    self.surface = self.defaultSurface.copy()

    a = self.currentSaveSelectedSurface()
    self.surface.blit(a[0], a[1])

    for item in self.saveItems:
      item.render(self.surface)

    self.surface.blit(self.okButton, self.okButtonPos)
    self.surface.blit(self.cancelButton, self.cancelButtonPos)
  
    self.screen.blit(self.surface, (self.posX, self.posY))

class JoinIPScene:
  def __init__(self, screen, background_surface, soundMixer):
    self.screen = screen
    self.surface = background_surface
    self.soundMixer = soundMixer

    self.image = pygame.image.load("./image/UI/menu/joinIPInterface.png").convert_alpha()
    self.defaultSurface = pygame.transform.scale(self.image, (400, 400))

    self.surface = self.defaultSurface.copy()

    self.posX = (self.screen.get_width()/2) - (self.surface.get_width()/2)
    self.posY = (self.screen.get_height()/2) - (self.surface.get_height()/2)

    self.font = pygame.font.SysFont(None, 24)
    self.userInputIP = ""
    self.textErrorIP = ""
    self.userInputPort = ""
    self.textErrorPort = ""

    self.okButton = pygame.image.load("./image/UI/quit/okButton.png")
    self.okButtonPos = ((self.surface.get_width()/2) + self.okButton.get_width(), (self.surface.get_height() - self.okButton.get_height())-20)
    self.okButtonRect = pygame.Rect(self.okButtonPos,  self.okButton.get_size())

    self.cancelButton = pygame.image.load("./image/UI/quit/cancelButton.png")
    self.cancelButtonPos = ((self.surface.get_width()/2) + 3*self.cancelButton.get_width(), (self.surface.get_height() - self.cancelButton.get_height())-20)
    self.cancelButtonRect = pygame.Rect(self.cancelButtonPos, self.cancelButton.get_size())

  def handleKeyboardInput(self, event) -> Event:
    if event.key == pygame.K_BACKSPACE:
      self.userInput = self.userInput[:-1]
      if len(self.userInput) < 20:
        self.textError = ""
      elif event.key == pygame.K_ESCAPE:
        return StateChangeEvent(STATE_PLAY)
      elif event.key == pygame.K_SPACE:
          self.textError = "Invalid caracter !"
      else:
        if len(self.userInput) < 15:
          self.userInput += event.unicode
        else:
          self.textError = "Text too long !"
      return TickEvent()
    
  def getMousePosRelative(self, event):
    return (event.pos[0] - self.posX, event.pos[1] - self.posY)
    
  def handleMouseInput(self, event) -> Event:
    mousePosRelative = self.getMousePosRelative(event)
    if self.okButtonRect.collidepoint(mousePosRelative): 
      self.soundMixer.playEffect('clickEffect')
      self.feedback = TickEvent() # RETOUR DE L'IP ET DU NUM DE PORT
      return self.feedback
    elif  self.cancelButtonRect.collidepoint(mousePosRelative):
       self.soundMixer.playEffect('clickEffect')
       return TickEvent()
    else: return 0

  def render(self):
    self.screen.blit(self.defaultSurface, (self.posX, self.posY))
    self.surface = self.defaultSurface.copy()

    self.surface.blit(self.okButton, self.okButtonPos)
    self.surface.blit(self.cancelButton, self.cancelButtonPos)
  
    self.screen.blit(self.surface, (self.posX, self.posY))

    self.surface.blit(self.font.render(self.userInputIP, True, (0, 0, 0)), (25, 60))
    self.surface.blit(self.font.render(self.userInputPort, True, (0, 0, 0)), (0, 0))
    self.surface.blit(pygame.font.Font(None, 20).render(self.textErrorIP, True, (255, 0, 0)), (10, 85))
    self.surface.blit(pygame.font.Font(None, 20).render(self.textErrorPort, True, (255, 0, 0)), (10, 85))

class ItemLoadScene:
  def __init__(self, saveName, idx, font):
    self.saveName = saveName
    self.font = font
    self.selected = False

    self.text = self.font.render(saveName, 1, (255, 255, 255), (0, 0, 0))
    self.selectedText = self.font.render(saveName, 1, (255, 0, 0), (0, 0, 0))

    self.textRect = self.text.get_rect()

    self.textRect.center = ((self.textRect.width/2) + 20, (self.textRect.height/2) + (100 + 30*idx))

  def render(self, surface_to_blit):
    if self.selected:
      surface_to_blit.blit(self.selectedText, self.textRect)
    else:
      surface_to_blit.blit(self.text, self.textRect)

class QuitScene:
  def __init__(self, screen, background_surface, soundMixer):
    self.screen = screen
    self.surface = background_surface
    self.soundMixer = soundMixer
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
    if self.okButtonRect.collidepoint(mousePosRelative):
      self.soundMixer.playEffect('clickEffect')
      return 1
    elif  self.cancelButtonRect.collidepoint(mousePosRelative): 
      self.soundMixer.playEffect('clickEffect')
      return 2
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

    self.pos = (self.surface_to_blit.get_width()/2 - self.surface.get_width()/2, 400+idx_item*40)
    self.rect = pygame.Rect(self.pos, self.surface.get_size())

    self.feedback = feedback

  def render(self, currentMousePos):
    if self.rect.collidepoint(currentMousePos):
      self.surface_to_blit.blit(self.hoveredSurface, self.pos)
    else: 
      self.surface_to_blit.blit(self.surface, self.pos)