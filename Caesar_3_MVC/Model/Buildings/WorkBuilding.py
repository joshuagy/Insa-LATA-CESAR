from Model.Buildings.Building import *
from Model.Walker import *
from Model.Case import *

class WorkBuilding(Building):
    def __init__(self, case, plateau, size, desc, active=0, walker = None):
        super().__init__( case, plateau, size, desc)
        self.active = active
        self.case.setFeature(desc)
        self.walker = walker
        self.timer = 0

    def setActive(self,NewActive):
        self.active = NewActive

    def getActive(self):
        return self.active

    def delete(self):
        self.case.setStructure(None)
        self.case.setFeature("")
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

    def __init__(self, case, plateau, size, desc, active, walker = None):
        super().__init__( case, plateau, size, desc, active, walker)
        self.plateau.treasury = self.plateau.treasury - PREFECTURE_COST

    """def activatePrefecture(aPrefecture,lePlateau) :
        aPrefecture.setActive(True)
        myPrefect=Prefet(aPrefecture.case,lePlateau, "Pompus Prefectus")
        aPrefecture.setWalker(myPrefect)
        #Reste à afficher le drapeau ROUGE"""
    
    def spawnWalker(self):
        self.walker = Prefet(self.case,self.plateau, self, "Prefectus")
    
    
class EnginnerPost(WorkBuilding) :

    def __init__(self, case, plateau, size, desc, active, walker = None):
        super().__init__( case, plateau, size, desc, active, walker)
        self.plateau.treasury = self.plateau.treasury - ENGINEERPOST_COST

    """def activateEngineerPost(anEngineerPost,lePlateau) :
        anEngineerPost.setActive(True)
        myEngineer=Engineer(anEngineerPost.case,lePlateau,"Emerius")
        anEngineerPost.setWalker(myEngineer)
        #Reste à afficher le drapeau BLEU"""
    
    def spawnWalker(self):
        self.walker = Engineer(self.case,self.plateau, self, "UnIngenieur")

