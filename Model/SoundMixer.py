import pygame

class SoundMixer:
  def __init__(self):
    self.buildEffect = pygame.mixer.Sound("assets/soundEffects/buildEffect.wav")
    self.clickEffect = pygame.mixer.Sound("assets/soundEffects/clickEffect.wav")

  def playEffect(self, effect):
    if effect ==  'buildEffect':
      self.buildEffect.play()
    elif effect ==  'clickEffect':
      self.clickEffect.play()
    else:
      pass
