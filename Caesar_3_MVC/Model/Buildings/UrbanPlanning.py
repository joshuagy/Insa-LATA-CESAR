from Model.Plateau import *
from Model.Buildings.House import *

class Well:

    listWell = []

    def __init__(self, case, plateau, desc) :
        self.desc=desc
        self.case=case
        self.case.setStructure(self)
        self.plateau=plateau
        self.plateau.structures.append(self)
        self.plateau.treasury = self.plateau.treasury - WELL_COST
        Well.listWell.append(self)
        for xi in range (self.case.x-2,self.case.x+2,1) :
            for yi in range (self.case.y-2,self.case.y+2,1) :
                if 0<=xi<self.plateau.nbr_cell_x and 0<=yi<self.plateau.nbr_cell_y: 
                    if self.plateau.map[xi][yi].waterAccess==0 :
                        self.plateau.map[xi][yi].waterAccess=1

    def delete(self):
        self.case.setStructure(None)
        self.case.setFeature("")
        self.plateau.structures.remove(self)
        Well.listWell.remove(self)
        for xi in range (self.case.x-2,self.case.x+2,1) :
            for yi in range (self.case.y-2,self.case.y+2,1) :
                if 0<=xi<self.plateau.nbr_cell_x and 0<=yi<self.plateau.nbr_cell_y:
                    self.plateau.map[xi][yi].waterAccess=0
                    for cw in Well.listWell :
                        if abs(cw.case.x-xi)<=2 and abs(cw.case.y-yi)<=2 :
                            self.plateau.map[xi][yi].waterAccess=1


        del self
        
