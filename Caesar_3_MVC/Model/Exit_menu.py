import pygame

pause=False


class Exitmenu:


    def __init__(self, width, height,screen) :

        self.screen=screen
        self.width = width
        self.height = height

        self.Pause = pygame.image.load("image/UI/menu/Pause.png")
        self.Continue = pygame.image.load("image/UI/menu/Continue.png")

        self.Replay = pygame.image.load("image/UI/menu/Replay.png")
        self.Savegame = pygame.image.load("image/UI/menu/Savegame.png")
        self.Exit=  pygame.image.load("image/UI/menu/Exit.png")
        self.Continue_rect, self.Exit_rect,self.Replay_rect, self.Savegame_rect, self.Pause_rect = self.Continue.get_rect(), self.Exit.get_rect(),self.Replay.get_rect(),self.Savegame.get_rect(), self.Pause.get_rect()

        self.Pause_rect.x, self.Pause_rect.y = self.width / 2 - 100, self.height / 2 - 250
        self.Continue_rect.x, self.Continue_rect.y = self.width / 2 - 100, self.height / 2 - 150
        self.Replay_rect.x,self.Replay_rect.y = self.width / 2 - 100, self.height / 2 - 100
        self.Savegame_rect.x, self.Savegame_rect.y = self.width / 2 - 100, self.height / 2 - 50
        self.Exit_rect.x, self.Exit_rect.y = self.width / 2 - 100, self.height / 2



    def choosen(self,bol):
        global pause
        pause = bol

    def draw_exit_menu(self):
        if pause:

            self.screen.blit(self.Pause, self.Pause_rect)
            self.screen.blit(self.Continue, self.Continue_rect)
            self.screen.blit(self.Replay, self.Replay_rect)
            self.screen.blit(self.Savegame, self.Savegame_rect)
            self.screen.blit(self.Exit, self.Exit_rect)


