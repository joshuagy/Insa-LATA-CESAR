import pygame
from EventManager.allEvent import *
from Model import model

class Menu:
  def __init__(self, screen):
    self.screen = screen
    self.image = pygame.image.load("./image/UI/menu/menu_background.png")
    self.surface = pygame.transform.scale(self.image, self.screen.get_size())
    self.items = []
    self.initialize_items()
  
  def initialize_items(self):
    startButton = TextButton("Start Game", (300, 50), StateChangeEvent(model.STATE_PLAY))
    exitButton = TextButton("Exit", (300, 50), ExitEvent())
    
    self.items.append(startButton)
    self.items.append(exitButton)

  def handleInput(self, pos) -> Event:
    for item in self.items:
      if item.rect.collidepoint(pos):
        return item.feedback
      
  def render(self):
    for idx, item in enumerate(self.items):
      item.render(self.surface, (100, 100 + (idx*200)))

    self.screen.blit(self.surface, (0,0))
  
class Button:
  def __init__(self, size, feedback: Event):
    self.size = size
    self.surface = pygame.Surface(self.size)
    self.surface.fill((0,0,0))

    self.feedback = feedback
    self.rect = None
    
  def render(self, surface_to_blit, pos):
    self.rect = pygame.Rect(pos, self.size)
    surface_to_blit.blit(self.surface, pos)

class TextButton(Button):
  def __init__(self, text, size, feedback: Event):
    super().__init__(size, feedback)
    self.font = self.font = pygame.font.Font(None, 30)
    self.text = self.font.render(text, 0, (255, 255, 255))
    self.surface.blit(self.text, (0,0))

class ImageButton(Button):
  def __init__(self, image, size, feedback: Event):
    super().__init__(size, feedback)
