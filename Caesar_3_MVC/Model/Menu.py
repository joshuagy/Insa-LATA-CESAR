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

    self.quitScene = QuitScene(self.screen, self.surface.copy(), self.soundMixer)
    self.isQuitState = False

    self.loadScene = LoadScene(self.screen, self.surface.copy(), self.soundMixer)
    self.isLoadState = False

    self.defaultFeedback = TickEvent() # do nothing

    # default mouse position
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
      if isinstance(loadSceneFeedBack, TickEvent):
        self.isLoadState = False
        self.soundMixer.playEffect('clickEffect')
        return loadSceneFeedBack
      elif isinstance(loadSceneFeedBack, LoadSave):
          self.soundMixer.playEffect('clickEffect')
          self.isLoadState = False
          return loadSceneFeedBack
      else:
       return TickEvent()
    else:
      for item in self.items:
        if item.rect.collidepoint(event.pos):
          if isinstance(item.feedback, QuitEvent):
            self.soundMixer.playEffect('clickEffect')
            self.isQuitState = True
            return TickEvent()
          elif isinstance(item.feedback, LoadEvent):
            self.soundMixer.playEffect('clickEffect')
            self.isLoadState = True
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
    else: 
      self.renderItems()
      self.screen.blit(self.surface, (0, 0))


class LoadScene:
  def __init__(self, screen, background_surface, soundMixer):
    self.screen = screen
    self.surface = background_surface
    self.soundMixer = soundMixer
    self.surface = pygame.Surface((400, 400))
    self.surface.fill((0, 0, 0))
    self.posX = (self.screen.get_width()/2) - (self.surface.get_width()/2)
    self.posY = (self.screen.get_height()/2) - (self.surface.get_height()/2)

    self.font = pygame.font.SysFont(None, 24)

    self.saveFileNames = [f for f in os.listdir("./Model/Save_Folder") if os.path.isfile(os.path.join("./Model/Save_Folder", f))]
    self.saveFileNames.remove("save_to_load.pickle")
    self.saveFileNames.remove("DefaultMap.pickle")
    
    if len(self.saveFileNames) == 0:
      self.currentSaveLoaded = "No save file found"
    else:
      self.currentSaveLoaded = self.saveFileNames[0]

    self.saveItems = []

    self.getSaveItems()

    self.feedback = LoadSave("DefaultMap.pickle")

    self.okButton = pygame.image.load("./image/UI/quit/okButton.png")
    okButtonPos = ((self.surface.get_width()/2) - 2*self.okButton.get_width(), (self.surface.get_height() - self.okButton.get_height())-10)
    self.okButtonRect = pygame.Rect(okButtonPos,  self.okButton.get_size())

    self.cancelButton = pygame.image.load("./image/UI/quit/cancelButton.png")
    cancelButtonPos = ((self.surface.get_width()/2) + self.cancelButton.get_width(), (self.surface.get_height() - self.cancelButton.get_height())-10)
    self.cancelButtonRect = pygame.Rect(cancelButtonPos, self.cancelButton.get_size())

    self.surface.blit(self.okButton, okButtonPos)
    self.surface.blit(self.cancelButton, cancelButtonPos)
  
  def currentSaveSelectedSurface(self):
    currentSaveSelected = pygame.Surface((380, 30))
    currentSaveSelected.fill((255, 255, 255))
    currentSaveSelectedPos = (self.surface.get_width()/2 - currentSaveSelected.get_width()/2, 10)
    currentSaveSelectedText = self.font.render(self.currentSaveLoaded, 0, (0, 0, 0))
    currentSaveSelectedTextPos = (currentSaveSelectedPos[0]+5, currentSaveSelected.get_height()/2 - currentSaveSelectedText.get_height()/2)
    currentSaveSelected.blit(currentSaveSelectedText, currentSaveSelectedTextPos)
    return (currentSaveSelected, currentSaveSelectedPos)
  
  def saveSelectorSurface(self):
    saveSelector = pygame.Surface((380, 200))
    saveSelector.fill((255, 255, 255))
    saveSelectorPos = (self.surface.get_width()/2 - saveSelector.get_width()/2, 50)
    return (saveSelector, saveSelectorPos)

  def getSaveItems(self): 
    for idx, saveName in enumerate(self.saveFileNames):
      item = ItemLoadScene(saveName, idx, self.font)
      self.saveItems.append(item)

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
      # with open("./Model/Save_Folder/save_to_load.pickle", "w") as f, open("./Model/Save_Folder/"+self.currentSaveLoaded, "r") as f2:
      #   print("copy de ", self.currentSaveLoaded, " vers save_to_load.pickle")
      #   shutil.copyfile("./Model/Save_Folder/"+self.currentSaveLoaded, "./Model/Save_Folder/save_to_load.pickle")
      self.feedback = LoadSave(self.currentSaveLoaded)
      return self.feedback
    elif  self.cancelButtonRect.collidepoint(mousePosRelative):
       self.soundMixer.playEffect('clickEffect')
       return TickEvent()
    else: return 0

  def render(self):
    a = self.currentSaveSelectedSurface()
    self.surface.blit(a[0], a[1])

    b = self.saveSelectorSurface()
    self.surface.blit(b[0], b[1])
    
    for item in self.saveItems:
      item.render(self.surface)

    self.screen.blit(self.surface, (self.posX, self.posY))

class ItemLoadScene:
  def __init__(self, saveName, idx, font):
    self.saveName = saveName
    self.font = font
    self.selected = False

    self.text = self.font.render(saveName, 1, (255, 255, 255), (0, 0, 0))
    self.selectedText = self.font.render(saveName, 1, (255, 0, 0), (0, 0, 0))

    self.textRect = self.text.get_rect()

    self.textRect.center = ((self.textRect.width/2) + 20, (self.textRect.height/2) + (55 + 30*idx))

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

    self.pos = (self.surface_to_blit.get_width()/2 - self.surface.get_width()/2, 300+idx_item*40)
    self.rect = pygame.Rect(self.pos, self.surface.get_size())

    self.feedback = feedback

  def render(self, currentMousePos):
    if self.rect.collidepoint(currentMousePos):
      self.surface_to_blit.blit(self.hoveredSurface, self.pos)
    else: 
      self.surface_to_blit.blit(self.surface, self.pos)