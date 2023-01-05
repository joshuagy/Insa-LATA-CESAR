from Model.Buildings.Building import *
from Model.Walker import *
from Model.Case import *

class WorkBuilding(Building):
    def __init__(self, case, plateau, size, desc, fireRisk, collapseRisk, active=0):
        super().__init__( case, plateau, size, desc, fireRisk, collapseRisk)
        self.active = active
        self.case.setFeature(desc)

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

class Prefecture(WorkBuilding) :

    def __init__(self, case, plateau, size, desc, active, fireRisk=0, collapseRisk=0):
        super().__init__( case, plateau, size, desc, active, collapseRisk)
        self.walker = Prefet(self.case,self.plateau,"Prefectus")

    def activatePrefecture(aPrefecture,lePlateau) :
        aPrefecture.setActive(True)
        myPrefect=Prefet(aPrefecture.case,lePlateau,"Pompus Prefectus")
        aPrefecture.setWalker(myPrefect)
        #Reste à afficher le drapeau ROUGE
    
    def collapse(self):
        self.delete()
        DamagedBuilding(self.case,self.plateau,"Ruins")
        

class EnginnerPost(WorkBuilding) :

    def __init__(self, case, plateau, size, desc, active, fireRisk=0, collapseRisk=0):
        super().__init__( case, plateau, size, desc, active, fireRisk, collapseRisk)
        self.walker = Engineer(self.case,self.plateau,"UnIngenieur")

    def activateEngineerPost(anEngineerPost,lePlateau) :
        anEngineerPost.setActive(True)
        myEngineer=Engineer(anEngineerPost.case,lePlateau,"Emerius")
        anEngineerPost.setWalker(myEngineer)
        #Reste à afficher le drapeau BLEU

    def ignite(self):
        self.delete()
        DamagedBuilding(self.case,self.plateau,"BurningBuilding")