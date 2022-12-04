import pygame

# === CONSTANTS === (UPPER_CASE names)

SCREEN_WIDTH  = 600
SCREEN_HEIGHT = 400

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# === CLASSES === (CamelCase names)

class Button():

    def __init__(self,text ,x=0, y=0, image_normal=None, image_hovered=None, image_clicked=None, image_locked=None):
        """Create a button. Set the images to their path or to None if you don't want to have a hovered and clicked version of your button."""

        self.text = text
        self.textsurface = pygame.font.SysFont('default_font', 20).render(self.text, False,BLACK, WHITE)

        self.image_normal =  pygame.image.load(image_normal)

        if(image_hovered!=None):
            self.image_hovered_exists = True
            self.image_hovered = pygame.image.load(image_hovered)
        else:
            self.image_hovered_exists = False
            
        if(image_clicked!=None):
            self.image_clicked_exists = True
            self.image_clicked = pygame.image.load(image_clicked)
        else:
            self.image_clicked_exists = False

        if(image_locked!=None):
            self.unlocked=False
            self.image_locked_exists = True
            self.image_locked = pygame.image.load(image_locked)
        else:
            self.image_locked_exists = False
            self.unlocked=True
               
        self.image = self.image_normal
        self.rect = self.image.get_rect()

        # you can't use it before `blit` 
        self.rect.topleft = (x, y)

        self.hovered = False
        self.clicked = False

    def update(self):

        if self.unlocked==True:
            if self.image_clicked_exists and self.clicked:
                self.image = self.image_clicked
            elif self.image_hovered_exists and self.hovered:
                self.image = self.image_hovered
            else:
                self.image = self.image_normal
        else:
             self.image = self.image_locked

    def showTip(self, display):
        if self.hovered:
            mouse_pos = pygame.mouse.get_pos()
            display.blit(self.textsurface, (mouse_pos[0]-100, mouse_pos[1]+20))
          
        
    def draw(self, surface):

        surface.blit(self.image, self.rect)

    def handle_event(self, event):

        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
            
            
            if self.hovered:
                print('Hovered')
                                                             
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #We consider that the button is in the clicked state until we click again
            if self.hovered:
                if self.clicked:
                    self.clicked = False
                else:
                    self.clicked = True
                    print('Clicked')
            else:
                self.clicked = False
                
                   
  
# === MAIN === (lower_case names)

def main():

    # --- init ---

    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
 
    clock = pygame.time.Clock()
    is_running = False

      
    # --- objects ---
      
    btn1 = Button("Hide the Control Panel",200, 50,"paneling_00097.png","paneling_00098.png","paneling_00099.png")
    btn2 = Button("World",200, 150,"paneling_00097.png","paneling_00098.png","paneling_00099.png","paneling_00100.png")
    

    # --- mainloop --- 

    is_running = True

    while is_running:

        # --- events ---

        for event in pygame.event.get():

            # --- global events ---

            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    is_running = False

            # --- objects events ---

            btn1.handle_event(event)
            btn2.handle_event(event)
            

        # --- updates ---

        btn1.update()
        btn2.update()
        
       

        # --- draws ---

        screen.fill(BLACK)

        btn1.draw(screen)
        btn1.showTip(screen)
        btn2.draw(screen)
        btn2.showTip(screen)
        
        
        pygame.display.update()

        # --- FPS ---

        clock.tick(25)

    # --- the end ---

    pygame.quit()


#----------------------------------------------------------------------

if __name__ == '__main__':

    main()
