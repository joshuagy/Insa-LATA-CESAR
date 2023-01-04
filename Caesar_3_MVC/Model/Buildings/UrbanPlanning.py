from Model.Plateau import *
from Model.Buildings.House import *

class Well:
    def __init__(self, case, plateau, desc) :
        self.desc=desc
        self.case=case
        self.case.setStructure(self)
        self.plateau=plateau
        self.plateau.structures.append(self)
        for xi in range (self.case.x-2,self.case.x+2,1) :
            for yi in range (self.case.y-2,self.case.y+2,1) :
                if self.plateau.map[xi][yi].waterAccess==0 :
                    self.plateau.map[xi][yi].waterAccess==1

    def delete(self):
        self.case.setStructure(None)
        self.case.setFeature("")
        self.plateau.structures.remove(self)
        del self
        
