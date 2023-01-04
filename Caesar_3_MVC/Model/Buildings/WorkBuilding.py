from Model.Buildings.Building import *
from Model.Walker import *
from Model.Case import *

class WorkBuilding(Building):
    def __init__(self, case, plateau, size, desc, walker, active =0):
        super().__init__( case, plateau, size, desc)
        self.walker = walker
        self.active = active
        self.case.setFeature(desc)

    def setWalker(self,newWalker):
        self.walker=newWalker

    def getWalker(self):
        return self.walker

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

    def __init__(self, case, plateau, size, desc, walker, active,):
        super().__init__( case, plateau, size, desc, walker, active)

    def activatePrefecture(aPrefecture,lePlateau) :
        aPrefecture.setActive(True)
        myPrefect=Prefet(aPrefecture.case,lePlateau,"Pompus Prefectus")
        aPrefecture.setWalker(myPrefect)
        #Reste à afficher le drapeau ROUGE

class EnginnerPost(WorkBuilding) :

    def __init__(self, case, plateau, size, desc, walker, active,):
        super().__init__( case, plateau, size, desc, walker, active)

    def activateEngineerPost(anEngineerPost,lePlateau) :
        anEngineerPost.setActive(True)
        myEngineer=Engineer(anEngineerPost.case,lePlateau,"Emerius")
        anEngineerPost.setWalker(myEngineer)
        #Reste à afficher le drapeau BLEU
