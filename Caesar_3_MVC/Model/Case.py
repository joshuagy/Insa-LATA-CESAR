from Model.constants import *

class Case():
    def __init__(self, x, y, rectangle_cell, isometric_cell, render_pos, connectedToRoad=0, feature=None, sprite=None, road = None, structure = None):
        self.x = x
        self.y = y
        self.rectangle_cell = rectangle_cell
        self.isometric_cell = isometric_cell
        self.render_pos = render_pos
        self.setSprite(sprite)
        self.feature = feature
        self.road = road
        self.structure = structure
        self.connectedToRoad = connectedToRoad
        self.waterAccess = 0
        self.religiousAccess = 0
    
    def delete(self):
        del self

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
    def setSprite(self, newSprite):
        self.sprite = newSprite
        if (self.sprite in list_of_undestructible ):
            self.collision = 1
        else:
            self.collision = 0 
