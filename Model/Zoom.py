import pygame



class Zoom:
    def __init__(self,image):
        self.image=image
    def set_zoom(self,X__):

        self.image["land1"]=pygame.transform.scale(self.image["land1"],(self.image["land1"].get_width()*X__,self.image["land1"].get_height()*X__))
        self.image["tree1"] = pygame.transform.scale(self.image["tree1"],(self.image["tree1"].get_width()*X__, self.image["tree1"].get_height()*X__))
        self.image["rock1"] = pygame.transform.scale(self.image["rock1"], (self.image["rock1"].get_width()*X__, self.image["rock1"].get_height()*X__))
        self.image["land2"] = pygame.transform.scale(self.image["land2"], (self.image["land2"].get_width() * X__, self.image["land2"].get_height() * X__))
        self.image["tree2"] = pygame.transform.scale(self.image["tree2"], (self.image["tree2"].get_width() * X__, self.image["tree2"].get_height() * X__))
        self.image["rock2"] = pygame.transform.scale(self.image["rock2"], (self.image["rock2"].get_width() * X__, self.image["rock2"].get_height() * X__))
        self.image["tree3"] = pygame.transform.scale(self.image["tree3"], (self.image["tree3"].get_width() * X__, self.image["tree3"].get_height() * X__))
        self.image["water1"] = pygame.transform.scale(self.image["water1"], (self.image["water1"].get_width() * X__, self.image["water1"].get_height() * X__))
        self.image["sign1"] = pygame.transform.scale(self.image["sign1"], (self.image["sign1"].get_width() * X__, self.image["sign1"].get_height() * X__))
        self.image["water2"] = pygame.transform.scale(self.image["water2"], (self.image["water2"].get_width() * X__, self.image["water2"].get_height() * X__))
        self.image["sign2"] = pygame.transform.scale(self.image["sign2"], (self.image["sign2"].get_width() * X__, self.image["sign2"].get_height() * X__))
        self.image["water3"] = pygame.transform.scale(self.image["water3"], (self.image["water3"].get_width() * X__, self.image["water3"].get_height() * X__))
        self.image["water4"] = pygame.transform.scale(self.image["water4"], (self.image["water4"].get_width() * X__, self.image["water4"].get_height() * X__))
        self.image["water5"] = pygame.transform.scale(self.image["water5"], (self.image["water5"].get_width() * X__, self.image["water5"].get_height() * X__))
        self.image["rock3"] = pygame.transform.scale(self.image["rock3"], (self.image["rock3"].get_width() * X__, self.image["rock3"].get_height() * X__))