from Model.constants import list_of_collision

class Case():
    def __init__(self, x, y, rectangle_cell, isometric_cell, render_pos, connectedToRoad=0, feature=None, sprite=None, road = None, building = None):
        self.x = x
        self.y = y
        self.rectangle_cell = rectangle_cell
        self.isometric_cell = isometric_cell
        self.render_pos = render_pos
        self.sprite = sprite
        if (self.sprite in list_of_collision ):
            self.collision = 1
        else:
            self.collision = 0 
        self.feature = feature
        self.road = road
        self.building = building

    def setFeature(self,newFeature):
        self.feature=newFeature
    def getFeature(self):
        return self.feature


    def getRelative(case, dx, dy, plateau):
        if 0 < plateau.listeCase[30*(case.y+dy)+(case.y*dy)] < 1600 :
            return plateau.listeCase[30*(case.y+dy)+(case.y*dy)]