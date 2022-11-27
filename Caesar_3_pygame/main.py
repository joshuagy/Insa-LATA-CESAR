import pygame

from game import Game



def main():


    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    game = Game(screen, clock)

    while True:
        game.run()

if __name__ == "__main__":
    main()