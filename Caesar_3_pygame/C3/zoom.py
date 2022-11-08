import pygame
from pygameZoom import PygameZoom

class Zoom:
   def __init__(self,screen,width,height):
       self.width=width
       self.height=height
       self.screen=screen
       self.pygameZoom = PygameZoom(self.width, self.height)

   def zom():
       self.pygameZoom.set_background((255, 0, 0))
