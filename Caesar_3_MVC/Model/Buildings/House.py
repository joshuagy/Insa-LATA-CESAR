import pygame
from Building import Building
from Plateau import Plateau
from Case import Case

class House(Building):

    cityHousesList = []

    def __init__(self, position, case, entertainLvl, nbHabMax, nbHab, size=(1,1), desc="Small Tent", connectedToRoad=0, fireRisk=0, collapseRisk=0, religiousAccess =0, status=False):
        super().__init__(position, case, size, desc, connectedToRoad, status, fireRisk, collapseRisk)
        self.entertainLvl = 0
        self.nbHab = 1
        self.nbHabMax = 5
        self.religiousAccess
        

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
        laCase = aHousingSpot.case
        newHouse = House(laCase.coor, laCase,0,10,1,(1,1),"Small Tent",1,0,0,0,True)
        aHousingSpot.case.setFeature("Small Tent")
        aHousingSpot.case.setSprite("Housng1a_00001.png")
        House.cityHousesList.append(newHouse)
        HousingSpot.cityHousingSpots.remove(aHousingSpot)

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

    def __init__(self, position, case, connectedToRoad) :
        self.position = position
        self.case = case
        self.connectedToRoad = connectedToRoad

    def isConnectedToRoad(self):
        return self.connectedToRoad
    
    def getSprite(self):
        return self.sprite

    def setCase(self, newCase):
        self.case=newCase

    def getCase(self):
        return self.case

    def getPosition(self):
        return self.position

    def placeAHousingSpot(coord, lePlateau):
        listeCase = lePlateau.listeCase
        p=30*coord(1)+coord(0) #Ajouter '-31' si on veut considérer la première ligne/colonne comme ayant l'indice 1.
        if(not(listeCase[p].feature=="") or not(listeCase[p].isConnectedToRoad)):
                return 0
        else :
                listeCase[p].setFeature("HousingSpot")
                listeCase[p].setSprite("Housng1a_00045.png")
                #listeCase[p].setIsAvailable(False)
                newHousingSpot = HousingSpot(coord,listeCase[p],True)
                HousingSpot.cityHousingSpots.append(newHousingSpot)
                
    def removeAHousingSpot(aHousingSpot) :
        laCase = aHousingSpot.case
        laCase.setSprite("Land1a_00001.png")
        #laCase.setIsAvailable(True)
        laCase.setFeature("")
        HousingSpot.cityHousingSpots.remove(aHousingSpot)




            

        
        

