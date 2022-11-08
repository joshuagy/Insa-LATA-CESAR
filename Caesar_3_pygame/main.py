import pygame
from game import Game

# set the pygame window name
pygame.display.set_caption("INSA'lata Cesare")

 # set image as icon for the window
pygame.display.set_icon(pygame.image.load("C3/augustus_IDI_ICON1-0.png"))

def main():


    pygame.init() 
    pygame.mixer.init() # For sound
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    game = Game(screen, clock)

    while True:
        game.run()

if __name__ == "__main__":
    main()