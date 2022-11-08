class Case():
    def __init__(self, x, y, sprite):
        self.x = x
        self.y = y
        self.sprite = None

class Route(Case):
    def __init__(self, x, y, sprite, connected):
        # connected = [0,0,0,1]: N, E, S, O
        super().__init__(x, y, sprite)
        self.sprite = "path1"
    
