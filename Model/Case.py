from Model.constants import *

class Case():
    def __init__(self, x, y, rectangle_cell, isometric_cell, render_pos, connectedToRoad=0, feature=None, sprite=None, indexSprite = -1, road = None, structure = None):
        self.x = x
        self.y = y
        self.rectangle_cell = rectangle_cell
        self.isometric_cell = isometric_cell
        self.render_pos = render_pos
        self.setSprite(sprite, indexSprite)
        self.feature = feature
        self.road = road
        self.structure = structure
        self.connectedToRoad = connectedToRoad
        self.waterAccess = 0
        self.religiousAccess = 0
        self.influenceDifIndex = 0
    
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
    def getInfluenceDifIndex(self) :
        return self.influenceDifIndex
    def setSprite(self, newSprite, indexSprite):
        self.sprite = newSprite
        self.indexSprite = int(indexSprite)
        if (self.sprite in list_of_undestructible ):
            self.collision = 1
        else:
            self.collision = 0 

    def getDesirability(self, plateau, player) :
        alreadyCheckedBuilding = []
        desTotal = 0
        for ray in range(1,6) :
            for xi in range(self.x-ray, self.x+ray) :
                for yi in range(self.y-ray,self.y+ray) :
                    if 0<xi<plateau.nbr_cell_x and 0<yi<plateau.nbr_cell_y :
                        if plateau.map[xi][yi] is not self :
                            if plateau.map[xi][yi].structure :
                                if plateau.map[xi][yi].structure.property == player :
                                    if plateau.map[xi][yi].structure not in alreadyCheckedBuilding :
                                        if plateau.map[xi][yi].structure.desc in desirabilityDict :
                                            desTotal = desTotal + desirabilityDict[plateau.map[xi][yi].structure.desc][ray-1]
                                            alreadyCheckedBuilding.append(plateau.map[xi][yi].structure)
        return desTotal

    def setPlayerInfluence(self, plateau, player) :
        myInf = self.getDesirability(plateau, player)
        challInf = max(self.getDesirability(plateau,i) for i in range(1,5) if i != player)
        dif = myInf - challInf
        if dif >= 3 : u= 0
        elif dif >= 2 : u= 1
        elif dif >= 1 : u= 2
        elif dif == 0 : u= -1
        elif dif >= -1 : u= 3
        elif dif >= -2 : u= 4
        elif dif < -2 : u= 5
        self.influenceDifIndex = u

