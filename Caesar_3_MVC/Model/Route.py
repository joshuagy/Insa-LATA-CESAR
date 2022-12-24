class Route():
    def __init__(self, case, plateau):
        # connected = [0,0,0,1]: N, E, S, O
        self.case = case
        self.case.road = self

        self.plateau = plateau
        self.sprite = self.draw()

    def __del__(self):
        self.case.road = None
    
    def draw(self):
        return "path1"