
import pygame
from Model.constants import *

class Music:
  def __init__(self, state: str = STATE_INTRO_SCENE):
    pygame.mixer.init()
    self.currentState = state

    # load deault song
    pygame.mixer.music.load("assets/Rome4.mp3")

  def loadMusic(self):
    if self.currentState == STATE_PLAY:
      pygame.mixer.music.load("assets/Rome1.mp3")
      self.play()
    elif self.currentState == STATE_MENU:
      pass

  def pause(self):
    pygame.mixer.music.pause()

  def play(self) -> None:
    pygame.mixer.music.play(-1)

  def changeMusic(self, state):
    if self.currentState != state:
      self.currentState = state
      self.loadMusic()
