class Case():
    def __init__(self, x, y, rectangle_cell, isometric_cell, render_pos, sprite=None):
        self.x = x
        self.y = y
        self.rectangle_cell = rectangle_cell
        self.isometric_cell = isometric_cell
        self.render_pos = render_pos
        self.sprite = sprite

class Route(Case):
    def __init__(self, x, y, rectangle_cell, isometric_cell, render_pos, sprite):
        # connected = [0,0,0,1]: N, E, S, O
        super().__init__(x, y, rectangle_cell, isometric_cell, render_pos, sprite)
        self.sprite = "path1"
