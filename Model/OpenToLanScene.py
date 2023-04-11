import pygame
from Model.Menu import *
from ip import *
from Model.Multiplayer import *

class OpenToLanScene:
    def __init__(self, model, screen, font, soundMixer):
        self.screen = screen
        self.font = font
        self.soundMixer = soundMixer

        self.ip_local = get_ip()

        self.model = model
        self.image = pygame.image.load("./image/UI/menu/saveInterface.png").convert_alpha()
        self.defaultSurface = pygame.transform.scale(self.image, (400, 400))
        self.surface = self.defaultSurface.copy()

        self.pos = (self.screen.get_width()/2 - self.surface.get_width()/2, self.screen.get_height()/2 - self.surface.get_height()/2)
        self.posX = self.pos[0]
        self.posY = self.pos[1]

        self.okButton = pygame.image.load("./image/UI/quit/okButton.png")
        self.okButtonPos = ((self.surface.get_width()/2) + self.okButton.get_width(), 100)
        self.okButtonRect = pygame.Rect(self.okButtonPos,  self.okButton.get_size())

        self.cancelButton = pygame.image.load("./image/UI/quit/cancelButton.png")
        self.cancelButtonPos = ((self.surface.get_width()/2) + 3*self.cancelButton.get_width(), 100)
        self.cancelButtonRect = pygame.Rect(self.cancelButtonPos, self.cancelButton.get_size())

        self.userInput = "8888"
        
    def getMousePosRelative(self, event):
        return (event.pos[0] - self.posX, event.pos[1] - self.posY)
    
    def handleMouseInput(self, event) -> Event:
        pos = self.getMousePosRelative(event)
        if self.okButtonRect.collidepoint(pos):
            self.soundMixer.playEffect("clickEffect")
            self.model.actualGame.multiplayer = Multiplayer(self.model.actualGame, None, "127.0.0.1", 8888, int(self.userInput), 0)
            return StateChangeEvent(STATE_PLAY)
        elif self.cancelButtonRect.collidepoint(pos):
            self.soundMixer.playEffect("clickEffect")
            return StateChangeEvent(STATE_PLAY)
        else:
            return TickEvent()

    def handleKeyboardInput(self, event) -> Event:
        if event.key == pygame.K_BACKSPACE:
            self.userInput = self.userInput[:-1]
        elif event.key == pygame.K_ESCAPE:
            return StateChangeEvent(STATE_PLAY)
        else:
            if len(self.userInput) < 4:
                self.userInput += event.unicode
        return TickEvent()
    
    def render(self):
        self.screen.blit(self.defaultSurface, (self.posX, self.posY))
        self.surface = self.defaultSurface.copy()
        f = pygame.font.Font(None, 25)
        self.surface.blit(f.render(f"Votre IP locale : {self.ip_local}", True, (0, 0, 0)), (25, 25))
        self.surface.blit(self.font.render(self.userInput, True, (0, 0, 0)), (25, 60))

        self.surface.blit(self.okButton, self.okButtonPos)
        self.surface.blit(self.cancelButton, self.cancelButtonPos)

        self.screen.blit(self.surface, self.pos)