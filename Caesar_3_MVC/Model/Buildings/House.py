import pygame
from random import randint
from Model.Buildings.Building import Building
from Model.Plateau import *
from Model.Case import *
from Model.Walker import Immigrant

class House(Building):

    def __init__(self, case, plateau, size, desc):
        super().__init__(case, plateau, size, desc)
        self.entertainLvl = 0
        self.nbHab = 1
        self.nbHabMax = 5
        self.religiousAccess = 0
        self.plateau.cityHousesList.append(self)
    
    def get_desc(self):
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

    def delete(self) :
        #Supprimer les habitants
        self.case.setStructure(None)
        self.case.setFeature("")
        self.plateau.cityHousesList.remove(self)
        self.plateau.structures.remove(self)
        del self


class HousingSpot() :

    def __init__(self, case, plateau, desc="HousingSpot") :
        self.case = case
        self.case.setStructure(self)
        self.desc = desc
        self.plateau=plateau
        self.plateau.structures.append(self)
        self.case.setFeature("HousingSpot")
        self.plateau.cityHousingSpotsList.append(self)
        self.spawn_timer = pygame.time.get_ticks()
        self.nb_immigrant = 0

    def isConnectedToRoad(self):
        return self.connectedToRoad
    
    def getSprite(self):
        return self.sprite

    def setCase(self, newCase):
        self.case=newCase

    def getCase(self):
        return self.case

    def delete(self) :
        self.case.setStructure(None)
        self.case.setFeature("")
        self.plateau.cityHousingSpotsList.remove(self)
        self.plateau.structures.remove(self)
        del self

    def becomeAHouse(self):
        House(self.case,self.plateau, 1, "SmallTent")
        self.case.setFeature("Small Tent")
        self.delete()
    
    def generateImmigrant(self):
        now = pygame.time.get_ticks()

        if now - self.spawn_timer > 500:
            if randint(0, 10) == 0 and self.nb_immigrant < 1:
                Immigrant(self.plateau.map[19][38], self.plateau, self.case)
                self.nb_immigrant += 1
            self.spawn_timer = now

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

        
        

