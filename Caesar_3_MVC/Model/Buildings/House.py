import pygame
from Model.Buildings.Building import Building
from Model.Plateau import Plateau
from Model.Case import Case

class House(Building):

    cityHousesList = []
    nbHabTotal = 0

    def __init__(self, position, case, entertainLvl, nbHabMax, nbHab, size=(1,1), desc="Small Tent", connectedToRoad=0, fireRisk=0, collapseRisk=0, religiousAccess =0, status=False):
        super().__init__(position, case, size, desc, connectedToRoad, status, fireRisk, collapseRisk)
        self.entertainLvl = 0
        self.nbHab = 1
        self.nbHabMax = 5
        self.religiousAccess
        
    def getDesc(self):
        return self.desc

    def get_entertainLvl(self):
        return self.entertainLvl
    
    def set_entertainLvl(self, newEntertainLvl):
        self.entertainLvl = newEntertainLvl

    def get_nbHab(self):
        return self.nbHab
    
    def set_nbHab(self, newnbHab):
        self.nbHab = newnbHab

    def get_nbHabmax(self):
        return self.nbHabmax
    
    def set_nbHabmax(self, newnbHabmax):
        self.nbHabmax = newnbHabmax

    def buildAHouse(aHousingSpot):
        newHouse = House(aHousingSpot.case,0,10,1,(1,1),"Small Tent",1,0,0,0,True)
        aHousingSpot.case.setFeature("Small Tent")
        House.cityHousesList.append(newHouse)
        HousingSpot.cityHousingSpots.remove(aHousingSpot)
        aHousingSpot.delete()


    def removeAHouse(aHouse) :
        laCase = aHouse.case
        laCase.setSprite("Land1a_00001.png")
        #laCase.setIsAvailable(True)
        laCase.setFeature("")
        House.cityHousesList.remove(aHouse)

"""
    def igniteAHouse(aHouse) :
        aHouse.set_nbHab(0)
        aHouse.set_desc("Burning" + aHouse.get_desc)
        # Gérer les sprites d'incendie
        return

    def burnDownAHouse(aHouse) :
        House.removeAHouse(aHouse)
        aHouse.case.setSprite("RuinSprite")


    def house_upgrade(house) :
        if house.desc=="Small Tent" and house.size is (1,1):
            house.desc="Large Tent"
            house.case.setSprite("LargeTentSprite1*1")
            house.set_nbHabmax(house,7)
        if house.desc=="Small Tent" and house.size is (2,2):
            house.desc="Large Tent"
            house.case.setSprite("LargeTentSprite2*2")
            house.set_nbHabmax(house,28)
        if house.desc=="Large Tent" and house.size is (2,2):
            house.desc="Small Shack"
            house.case.setSprite("SmallShack2*2")
            house.set_nbHabmax(house,36)
        if house.desc=="Small Shack" :
            house.desc="Large Shack"
            house.case.setSprite("LargeShackSprite2*2")
            house.set_nbHabmax(house,44)    


    def checkForUpgrades(cityHouses): # Manque critères : Desirability, waterSuppply, religiousAccess
        for i in cityHouses : 
            if cityHouses[i].desc=="Small Tent" and cityHouses[i].case.waterSupply>0 :
                cityHouses.house_upgrade(cityHouses[i])
            if cityHouses[i].desc=="Large Tent" and cityHouses[i].case.desIn>0 :
                cityHouses.house_upgrade(cityHouses[i])
            if cityHouses[i].desc=="Small Shack" and cityHouses[i].religiousAccess>0 :
                cityHouses.house_upgrade(cityHouses[i])

"""


class HousingSpot() :

    cityHousingSpots = []

    def __init__(self, case, plateau, connectedToRoad, desc="HousingSpot") :
        self.case = case
        self.case.building=self
        self.connectedToRoad = connectedToRoad
        self.desc = desc
        self.plateau=plateau
        plateau.buildings.append(self)
        

    def isConnectedToRoad(self):
        return self.connectedToRoad
    
    def getSprite(self):
        return self.sprite

    def setCase(self, newCase):
        self.case=newCase

    def getCase(self):
        return self.case

    def delete(self) :
        self.case.setBuilding(None)
        self.case.setFeature("")
        HousingSpot.cityHousingSpots.remove(self)
        self.plateau.buildings.remove(self)
        del self


    def placeAHousingSpot(laCase, lePlateau):
        if not(laCase.building==None) :
                return 0
        for x in range (laCase.x-2,laCase.x+2,1) :
            for y in range (laCase.y-2,laCase.y+2,1) :
                if lePlateau.map[x][y].getConnectedToRoad() > 0 :
                    
                    laCase.setFeature("HousingSpot")
                    newHousingSpot = HousingSpot(laCase,lePlateau,laCase.connectedToRoad)
                    HousingSpot.cityHousingSpots.append(newHousingSpot)
                



            

        
        

