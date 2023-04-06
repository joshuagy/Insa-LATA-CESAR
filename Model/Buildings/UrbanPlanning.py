from Model.Plateau import *
from Model.Buildings.House import *
from Model.Buildings.Building import *

class Well(Building):

    listWell = []

    def __init__(self, case, plateau, size, desc, property = 1) :
        self.desc=desc
        self.case=case
        self.size = size
        self.case.setStructure(self)
        self.plateau=plateau
        self.plateau.structures.append(self)
        self.plateau.treasury = self.plateau.treasury - WELL_COST
        self.riskTimer = 0
        self.fireRisk = 0
        self.collapseRisk = 0
        self.property = property
        Well.listWell.append(self)
        for xi in range (self.case.x-2,self.case.x+3,1) :
            for yi in range (self.case.y-2,self.case.y+3,1) :
                if 0<=xi<self.plateau.nbr_cell_x and 0<=yi<self.plateau.nbr_cell_y: 
                    if self.plateau.map[xi][yi].waterAccess==0 :
                        self.plateau.map[xi][yi].waterAccess=1

    def delete(self):
        self.case.setStructure(None)
        self.case.setFeature("")
        self.plateau.structures.remove(self)
        Well.listWell.remove(self)
        for xi in range (self.case.x-2,self.case.x+3,1) :
            for yi in range (self.case.y-2,self.case.y+3,1) :
                if 0<=xi<self.plateau.nbr_cell_x and 0<=yi<self.plateau.nbr_cell_y:
                    self.plateau.map[xi][yi].waterAccess=0
                    for cw in Well.listWell :
                        if abs(cw.case.x-xi)<=2 and abs(cw.case.y-yi)<=2 :
                            self.plateau.map[xi][yi].waterAccess=1
        del self
        
class Senate(Building) :
    def __init__(self, case, plateau, size, desc, property = 1,) :
        super().__init__(case, plateau, size, desc, property=property)
        self.secCases = []
        self.plateau.treasury = self.plateau.treasury - SENATE_COST
        self.case.render_pos = [self.case.render_pos[0], self.case.render_pos[1]+60]
        for xi in range(self.case.x, self.case.x+5, 1) :
            for yi in range(self.case.y, self.case.y-5, -1 ) :
                if self.plateau.map[xi][yi] != self.case :
                    self.secCases.append(self.plateau.map[xi][yi])
                    self.plateau.map[xi][yi].setStructure(self)


    def delete(self) :
        self.case.render_pos = [self.case.render_pos[0], self.case.render_pos[1]-60]
        self.plateau.structures.remove(self)
        self.case.setStructure(None)
        for oc in self.secCases :
            oc.setStructure(None)
        del self
        
class Temple(Building) :

    listTemple = []

    def __init__(self, case, plateau, size, desc, property = 1) :
        super().__init__(case, plateau, size, desc, property=property)
        self.plateau.treasury = self.plateau.treasury - TEMPLE_COST
        self.secCases = []
        self.case.render_pos = [self.case.render_pos[0], self.case.render_pos[1]+20]
        for xi in range(self.case.x, self.case.x+2, 1) :
            for yi in range(self.case.y, self.case.y-2, -1 ) :
                if self.plateau.map[xi][yi] != self.case :
                    self.secCases.append(self.plateau.map[xi][yi])
                    self.plateau.map[xi][yi].setStructure(self)
        Temple.listTemple.append(self)
        for xi in range (self.case.x-10,self.case.x+10,1) :
            for yi in range (self.case.y-10,self.case.y+10,1) :
                if 0<=xi<self.plateau.nbr_cell_x and 0<=yi<self.plateau.nbr_cell_y: 
                    if self.plateau.map[xi][yi].religiousAccess==0 :
                        self.plateau.map[xi][yi].religiousAccess=1


    def delete(self) :
        self.case.render_pos = [self.case.render_pos[0], self.case.render_pos[1]-20]
        self.plateau.structures.remove(self)
        self.case.setStructure(None)
        for oc in self.secCases :
            oc.setStructure(None)
        Temple.listTemple.remove(self)
        for xi in range (self.case.x-10,self.case.x+10,1) :
            for yi in range (self.case.y-10,self.case.y+10,1) :
                if 0<=xi<self.plateau.nbr_cell_x and 0<=yi<self.plateau.nbr_cell_y:
                    self.plateau.map[xi][yi].religiousAccess=0
                    for ct in Temple.listTemple :
                        if abs(ct.case.x-xi)<=10 and abs(ct.case.y-yi)<=10 :
                            self.plateau.map[xi][yi].religiousAccess=0
        del self
        
