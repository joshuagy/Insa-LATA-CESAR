from Model.Buildings.Building import *
from Model.Walker import *
from Model.Case import *

class WorkBuilding(Building):
    def __init__(self, case, plateau, size, desc, walker, active = 0, connectedToRoad=0, fireRisk=0, collapseRisk=0, status=False):
        super().__init__( case, plateau, size, desc, connectedToRoad, fireRisk, collapseRisk, status)
        self.walker = walker
        self.active = active

    def setWalker(self,newWalker):
        self.walker=newWalker

    def getWalker(self):
        return self.walker

    def setActive(self,NewActive):
        self.active = NewActive

    def getActive(self):
        return self.active

    def buildAWorkBuilding(laCase,lePlateau, wbsize,desc,wbwalker,wbSprite):
            if not(laCase.building==None) :
                return 0
            for x in range (laCase.x-2,laCase.x+2,1) :
                for y in range (laCase.y-2,laCase.y+2,1) :
                    if lePlateau.map[x][y].getConnectedToRoad() > 0 :
                        newWorkbuilding = WorkBuilding(laCase,lePlateau,wbsize,desc,wbwalker,0,laCase.connectedToRoad,0,0,True)
                        laCase.setFeature(desc)
                        #laCase.setSprite(wbSprite)
                        return newWorkbuilding

class Prefecture(WorkBuilding) :

    cityPrefectures = []

    def __init__(self, case, size, desc, walker, active, connectedToRoad=0, fireRisk=0, collapseRisk=0, status=False):
        super().__init__( case, size, desc, connectedToRoad, walker, active, status, fireRisk, collapseRisk)

     
    def buildAPrefecture(laCase, lePlateau) :
        myRecruiter = Prefet(laCase,lePlateau,"Recrutus")
        newPrefecture = WorkBuilding.buildAWorkBuilding(laCase,lePlateau,(1,1),"Prefecture",myRecruiter,"Security_00001.png")
        Prefecture.cityPrefectures.append(newPrefecture)
    

    def activatePrefecture(aPrefecture,lePlateau) :
        aPrefecture.setActive(True)
        myPrefect=Prefet(aPrefecture.case,lePlateau,"Pompus Prefectus")
        aPrefecture.setWalker(myPrefect)
        #Case.getRelative(aPrefecture.case,0,1,lePlateau).addSprite("Security_00002.png")
        

