from Model.Buildings.Building import Building
from Model.Walker import *
from Model.Case import *

class WorkBuilding(Building):
    def __init__(self, case, plateau, size, desc, active=0, property = 1, fireRisk = 0, collapseRisk = 0):
        super().__init__( case, plateau, size, desc, property, fireRisk, collapseRisk,)
        self.active = active
        self.case.setFeature(desc)
        self.walker = None
        self.timer = 0

    def setActive(self,NewActive):
        self.active = NewActive

    def getActive(self):
        return self.active

    def delete(self):
        self.case.setStructure(None)
        self.case.setFeature("")
        if self.walker:
            self.walker.delete()
        self.plateau.structures.remove(self)
        del self
    
    def spawnWalker(self):
        pass

    def delay(self):
        if not self.walker:
            if self.timer < 50:
                self.timer += 1
            else:
                self.spawnWalker()
                self.timer = 0

class Prefecture(WorkBuilding) :

    def __init__(self, case, plateau, size, desc, active, property = 1, fireRisk = 0, collapseRisk = 0):
        super().__init__( case, plateau, size, desc, active, property, fireRisk, collapseRisk)
        self.plateau.treasury = self.plateau.treasury - PREFECTURE_COST
    
    def spawnWalker(self):
        Prefet(self.case,self.plateau, self, "Prefectus")
    
    
class EnginnerPost(WorkBuilding) :

    def __init__(self, case, plateau, size, desc, active, property = 1, fireRisk = 0, collapseRisk = 0):
        super().__init__( case, plateau, size, desc, active, property, fireRisk, collapseRisk)
        self.plateau.treasury = self.plateau.treasury - ENGINEERPOST_COST
    
    def spawnWalker(self):
        Engineer(self.case,self.plateau, self, "UnIngenieur")

