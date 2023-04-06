from Model.constants import *
from Model.Buildings.House import *
from Model.Buildings.WorkBuilding import *

class Route():
    def __init__(self, case, plateau, property = 1):
        self.case = case
        self.case.road = self
        self.plateau = plateau
        self.plateau.treasury = self.plateau.treasury - ROAD_COST
        self.property = property

        #Informe les cases adjacentes qu'elles sont maintenant connectées à la route :
        self.case.changeConnectedToRoad(1)
        if self.case.x != 0 :
            self.plateau.map[self.case.x-1][self.case.y].changeConnectedToRoad(1)
        if self.case.x != self.plateau.nbr_cell_x-1 :
            self.plateau.map[self.case.x+1][self.case.y].changeConnectedToRoad(1)
        if self.case.y != self.plateau.nbr_cell_y-1 :
            self.plateau.map[self.case.x][self.case.y+1].changeConnectedToRoad(1)
        if self.case.y != 0 :
            self.plateau.map[self.case.x][self.case.y-1].changeConnectedToRoad(1)  
        

    
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

        

    def delete(self):
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
        # Informe toutes les cases adjacentes qu'elles ne sont plus connectées à la route 
            # (Sauf bien sûr si elles sont connectées à une autre route)
        self.case.changeConnectedToRoad(-1)
        if self.case.x != 0 :
            self.plateau.map[self.case.x-1][self.case.y].changeConnectedToRoad(-1)
        if self.case.x != self.plateau.nbr_cell_x-1 :
            self.plateau.map[self.case.x+1][self.case.y].changeConnectedToRoad(-1)
        if self.case.y != self.plateau.nbr_cell_y-1 :
            self.plateau.map[self.case.x][self.case.y+1].changeConnectedToRoad(-1)
        if self.case.y != 0 :
            self.plateau.map[self.case.x][self.case.y-1].changeConnectedToRoad(-1)
        #Supprime les maisons, housing spots et désactive les workbuildings
        for xcb in range (self.case.x-1,self.case.x+2,1) :
            for ycb in range (self.case.y-1,self.case.y+2,1) :
                if 0<=xcb<self.plateau.nbr_cell_x and 0<=ycb<self.plateau.nbr_cell_y:
                    if self.plateau.map[xcb][ycb].structure :
                        if isinstance(self.plateau.map[xcb][ycb].structure, HousingSpot) or isinstance(self.plateau.map[xcb][ycb].structure,House):
                            self.plateau.map[xcb][ycb].structure.delete
                        return   
        del self
    



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
