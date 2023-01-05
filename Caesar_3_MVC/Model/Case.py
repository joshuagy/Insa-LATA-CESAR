from Model.constants import *

class Case():
    def __init__(self, x, y, rectangle_cell, isometric_cell, render_pos, connectedToRoad=0, feature=None, sprite=None, road = None, structure = None):
        self.x = x
        self.y = y
        self.rectangle_cell = rectangle_cell
        self.isometric_cell = isometric_cell
        self.render_pos = render_pos
        self.sprite = sprite
        if (self.sprite in list_of_undestructible ):
            self.collision = 1
        else:
            self.collision = 0 
        self.feature = feature
        self.road = road
        self.structure = structure
        self.connectedToRoad = connectedToRoad
        self.waterAccess = 0

    def setFeature(self,newFeature):
        self.feature=newFeature
    def getFeature(self):
        return self.feature
    def setStructure(self,newStruct):
        self.structure=newStruct
    def getStructure(self):
        return self.structure
    def getConnectedToRoad(self):
        return self.connectedToRoad
    def changeConnectedToRoad(self, number):
        self.connectedToRoad=self.connectedToRoad+number


    def getRelative(case, dx, dy, plateau):
        if 0 < plateau.listeCase[30*(case.y+dy)+(case.y*dy)] < 1600 :
            return plateau.listeCase[30*(case.y+dy)+(case.y*dy)]