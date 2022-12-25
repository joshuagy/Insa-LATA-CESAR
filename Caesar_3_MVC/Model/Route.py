class Route():
    def __init__(self, case, plateau):
        self.case = case
        self.case.road = self

        self.plateau = plateau
        self.draw()

        if self.case.y < self.plateau.nbr_cell_y-1:
            if self.plateau.map[self.case.x][self.case.y+1].road:
                self.plateau.map[self.case.x][self.case.y+1].road.draw()
        if self.case.x < self.plateau.nbr_cell_x-1:
            if self.plateau.map[self.case.x+1][self.case.y].road:
                self.plateau.map[self.case.x+1][self.case.y].road.draw()
        if self.case.y > 0:
            if self.plateau.map[self.case.x][self.case.y-1].road:
                self.plateau.map[self.case.x][self.case.y-1].road.draw()
        if self.case.x > 0:
            if self.plateau.map[self.case.x-1][self.case.y].road:
                self.plateau.map[self.case.x-1][self.case.y].road.draw()

        

    def __del__(self):
        self.case.road = None
        if self.case.y < self.plateau.nbr_cell_y-1:
            if self.plateau.map[self.case.x][self.case.y+1].road:
                self.plateau.map[self.case.x][self.case.y+1].road.draw()
        if self.case.x < self.plateau.nbr_cell_x-1:
            if self.plateau.map[self.case.x+1][self.case.y].road:
                self.plateau.map[self.case.x+1][self.case.y].road.draw()
        if self.case.y > 0:
            if self.plateau.map[self.case.x][self.case.y-1].road:
                self.plateau.map[self.case.x][self.case.y-1].road.draw()
        if self.case.x > 0:
            if self.plateau.map[self.case.x-1][self.case.y].road:
                self.plateau.map[self.case.x-1][self.case.y].road.draw()
    



    def draw(self):
        connected = 0 #0 0 0 0 binaire -> N E S O
        if self.case.y < self.plateau.nbr_cell_y-1:
            if self.plateau.map[self.case.x][self.case.y+1].road:
                connected += 8 # + 1000
        if self.case.x < self.plateau.nbr_cell_x-1:
            if self.plateau.map[self.case.x+1][self.case.y].road:
                connected += 4 # + 0100
        if self.case.y > 0:
            if self.plateau.map[self.case.x][self.case.y-1].road:
                connected += 2 # + 0010
        if self.case.x > 0:
            if self.plateau.map[self.case.x-1][self.case.y].road:
                connected += 1 # + 0001
        self.sprite = connected
