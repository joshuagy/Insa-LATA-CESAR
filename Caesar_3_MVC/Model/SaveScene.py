import pygame
from Model.Menu import *

class SaveScene:
    def __init__(self, model, screen, font, soundMixer):
      self.screen = screen
      self.font = font
      self.soundMixer = soundMixer

      self.model = model
      
      self.surface = pygame.Surface((400, 400))
      self.surface.fill((255, 255, 255))

      self.pos = (self.screen.get_width()/2 - self.surface.get_width()/2, self.screen.get_height()/2 - self.surface.get_height()/2)
      self.posX = self.pos[0]
      self.posY = self.pos[1]
      
      self.okButton = pygame.image.load("./image/UI/quit/okButton.png")
      self.okButtonPos = ((self.surface.get_width()/2) - 2*self.okButton.get_width(), (self.surface.get_height() - self.okButton.get_height())-10)
      self.okButtonRect = pygame.Rect(self.okButtonPos,  self.okButton.get_size())

      self.cancelButton = pygame.image.load("./image/UI/quit/cancelButton.png")
      self.cancelButtonPos = ((self.surface.get_width()/2) + self.cancelButton.get_width(), (self.surface.get_height() - self.cancelButton.get_height())-10)
      self.cancelButtonRect = pygame.Rect(self.cancelButtonPos, self.cancelButton.get_size())

      self.userInput = ""
      self.inputRect = pygame.Rect((10, 40), (self.surface.get_width() - 20, 32))
      self.inputRectBorder = pygame.Rect((5, 35), (self.surface.get_width() - 10, 42))

      self.textError = ""

    def getMousePosRelative(self, event):
      return (event.pos[0] - self.posX, event.pos[1] - self.posY)

    def handleMouseInput(self, event) -> Event:
      pos = self.getMousePosRelative(event)
      if self.okButtonRect.collidepoint(pos):
        self.soundMixer.playEffect("clickEffect")
        self.model.actualGame.save_game(self.userInput)
        print('saved!')
        return StateChangeEvent(STATE_PLAY)
      elif self.cancelButtonRect.collidepoint(pos):
        self.soundMixer.playEffect("clickEffect")
        return StateChangeEvent(STATE_PLAY)
      else:
        return TickEvent()

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
        if len(self.userInput) < 20:
          self.userInput += event.unicode
        else:
          self.textError = "Text too long !"
      return TickEvent()

    def render(self):
      self.surface.fill((255, 255, 255))
      f = pygame.font.Font(None, 20)
      self.surface.blit(f.render("Save Name: ", True, (0, 0, 0)), (10, 10))

      pygame.draw.rect(self.surface, (0, 0, 0), self.inputRectBorder, 2, 5)
      pygame.draw.rect(self.surface, (250, 240, 250), self.inputRect)
      self.surface.blit(self.font.render(self.userInput, True, (0, 0, 0)), (10, 40))

      self.surface.blit(f.render(self.textError, True, (255, 0, 0)), (10, 82))

      self.surface.blit(self.okButton, self.okButtonPos)
      self.surface.blit(self.cancelButton, self.cancelButtonPos)

      self.screen.blit(self.surface, self.pos)