import pygame

class Camera:

    def __init__(self, width, height):

        self.width = width
        self.height = height
        self.cell_size=30

        self.vect = pygame.Vector2(-100, -100)
        self.dx = 0
        self.dy = 0
        self.speed = 25

    def get_cell_size(self,cell_size):
        self.cell_size=cell_size

    def update(self):
        mouse_pos = pygame.mouse.get_pos()

        # x movement
        if mouse_pos[0] > self.width * 0.999:
            self.dx = -self.speed
        elif mouse_pos[0] < self.width * 0.02:
            self.dx = self.speed
        else:
            self.dx = 0

        if mouse_pos[1] > self.height * 0.98:
            self.dy = -self.speed
        elif mouse_pos[1] < self.height * 0.02:
            self.dy = self.speed
        else:
            self.dy = 0

        #Left
        if not (self.vect.x> 0.1*self.width ) and self.dx>0:
            self.vect.x += self.dx
        #Top
        if not (self.vect.y>0.1*self.height ) and self.dy>0:
            self.vect.y += self.dy
            
        #These ones need to be adapted if we change the map size,
        #otherwise we either don't see the whole map or there is too much black background
        #Right
        #if not (self.vect.x<-0.999*self.width) and self.dx <0:     
        if not (self.vect.x<-self.width*2) and self.dx <0:
            self.vect.x += self.dx
        #Bottom
        #if not (self.vect.y<-0.6*self.height) and self.dy <0:
        if not (self.vect.y<-self.height*1.5) and self.dy <0:
            self.vect.y += self.dy