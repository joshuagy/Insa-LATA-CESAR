class Case():
    def __init__(self, x, y, rectangle_cell, isometric_cell, render_pos, isAvailable, connectedToRoad, feature=None, sprite=None):
        self.x = x
        self.y = y
        self.rectangle_cell = rectangle_cell
        self.isometric_cell = isometric_cell
        self.render_pos = render_pos
        self.isAvailable = isAvailable
        self.sprite = sprite
        self.feature = feature


    def getRelative(case, dx, dy, plateau):
        if 0 < plateau.listeCase[30*(case.y+dy)+(case.y*dy)] < 1600 :
            return plateau.listeCase[30*(case.y+dy)+(case.y*dy)]
       
                






class Route(Case):
    def __init__(self, x, y, rectangle_cell, isometric_cell, render_pos, sprite):
        # connected = [0,0,0,1]: N, E, S, O
        super().__init__(x, y, rectangle_cell, isometric_cell, render_pos, sprite)
        self.sprite = "path1"
