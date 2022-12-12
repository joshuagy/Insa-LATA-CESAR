import pygame
from Building import Building

class House(Building):
    def __init__(self, position, entertainLvl, nbHabMax, nbHab, size=(1,1), desc="Small Tent", connectedToRoad=0, fireRisk=0, collapseRisk=0, status=False):
        super().__init__(position, size, desc, connectedToRoad, status, fireRisk, collapseRisk, sprite="Housng1a_00001.png")
        self.entertainLvl = 0
        self.nbHab = 1
        self.nbHabMax = 5

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

    def setSprite(self, newSprite):
        self.sprite=newSprite
    
    def getSprite(self):
        return self.sprite


class HousingSpot :
    def __init__(self, sprite, position, case, connectedToRoad) :
        self.position = position
        self.case = case
        self.connectedToRoad = connectedToRoad
        self.sprite= "Housng1a_00045.png"

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

    def placeAHousingSpot(coord):
        for i in list :
            if(list(i).coor==coord):
                if(not(list(i).isAvailable) or not(list(i).isConnectedToRoad)):
                    return
        list(i).setFeature("HousingSpot")
        HousingSpot.__init__(HousingSpot,"Housng1a_00045.png",coord,list(i),1)
        
        




#class Ruin ?

def house_upgrade(house) :
    if house.desc=="Small Tent" and house.size is (1,1):
        house.desc="Large Tent"
        #Changer Sprite
        house.set_nbHabmax(house,7)
    if house.desc=="Small Tent" and house.size is (2,2):
        house.desc="Large Tent"
        #Changer Sprite
        house.set_nbHabmax(house,28)
    if house.desc=="Large Tent" and house.size is (2,2):
        house.desc="Small Shack"
        #Changer Sprite
        house.set_nbHabmax(house,36)
    if house.desc=="Small Shack" and house.size is (2,2):
        house.desc="Large Shack"
        #Changer Sprite
        house.set_nbHabmax(house,44)

#def house_merge(house) :
#    if house.size is (1,1) :
#        pos = get_position(house)
#    If 4 1*1 tents form a square, they merge in a 2*2 tent, change nbHabMax and sprite
# 


def house_checkForUpgrades(cityHouses):
    for i in cityHouses : 
        if cityHouses(i).desc=="Small Tent" and cityHouses(i).waterSupply>0 :
            house_upgrade(cityHouses(i))
        if cityHouses(i).desc=="Large Tent" and cityHouses(i).desIn>0 :
            house_upgrade(cityHouses(i))
        if cityHouses(i).desc=="Small Shack" and cityHouses(i).religiousAccess>0 :
            house_upgrade(cityHouses(i))
