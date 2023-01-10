import sys

import pygame




class Pausemenu:


    def __init__(self, width, height,screen) :

        self.screen=screen
        self.width = width
        self.height = height

        self.Pause = pygame.image.load("image/UI/pause/Pause.png")
        self.Continue = pygame.image.load("image/UI/pause/Continue.png")

        self.Replay = pygame.image.load("image/UI/pause/Replay.png")
        self.Savegame = pygame.image.load("image/UI/pause/Savegame.png")
        self.Exit=  pygame.image.load("image/UI/pause/Exit.png")
        self.Continue_rect, self.Exit_rect,self.Replay_rect, self.Savegame_rect, self.Pause_rect = self.Continue.get_rect(), self.Exit.get_rect(),self.Replay.get_rect(),self.Savegame.get_rect(), self.Pause.get_rect()

        self.Pause_rect.x, self.Pause_rect.y = self.width / 2 - 100, self.height / 2 - 250
        self.Continue_rect.x, self.Continue_rect.y = self.width / 2 - 100, self.height / 2 - 150
        self.Replay_rect.x,self.Replay_rect.y = self.width / 2 - 100, self.height / 2 - 100
        self.Savegame_rect.x, self.Savegame_rect.y = self.width / 2 - 100, self.height / 2 - 50
        self.Exit_rect.x, self.Exit_rect.y = self.width / 2 - 100, self.height / 2
        self.pause=False






    def draw_pause_menu(self):
        if self.pause:

            self.screen.blit(self.Pause, self.Pause_rect)
            self.screen.blit(self.Continue, self.Continue_rect)
            self.screen.blit(self.Replay, self.Replay_rect)
            self.screen.blit(self.Savegame, self.Savegame_rect)
            self.screen.blit(self.Exit, self.Exit_rect)
    def exit(self):
        pygame.quit()
        sys.exit()