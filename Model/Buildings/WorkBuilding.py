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
        self.plateau.treasury[self.property-1] = self.plateau.treasury[self.property-1] - PREFECTURE_COST
    
    def spawnWalker(self):
        prefet = Prefet(self.case,self.plateau, self, "Prefectus", property = self.property)
        if self.plateau.multiplayer :
            self.plateau.multiplayer.send(f"WA.2.{prefet.case.x}.{prefet.case.y}.{self.case.x}.{self.case.y}.{prefet.property}.{prefet.id}")
    
    
class EnginnerPost(WorkBuilding) :

    def __init__(self, case, plateau, size, desc, active, property = 1, fireRisk = 0, collapseRisk = 0):
        super().__init__( case, plateau, size, desc, active, property, fireRisk, collapseRisk)
        self.plateau.treasury[self.property-1] = self.plateau.treasury[self.property-1] - ENGINEERPOST_COST
    
    def spawnWalker(self):
        engineer = Engineer(self.case,self.plateau, self, "UnIngenieur", property = self.property)
        if self.plateau.multiplayer :
            self.plateau.multiplayer.send(f"WA.1.{engineer.case.x}.{engineer.case.y}.{self.case.x}.{self.case.y}.{engineer.property}.{engineer.id}")

