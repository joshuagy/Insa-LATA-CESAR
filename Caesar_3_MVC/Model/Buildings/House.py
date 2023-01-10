import pygame
from random import randint
from Model.Buildings.Building import *
from Model.Buildings.Building import BurningBuilding
from Model.Plateau import *
from Model.Case import *
from Model.Walker import Immigrant
from Model.Buildings.Building import DamagedBuilding

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
        self.case.setStructure(None)
        self.case.setFeature("")
        self.plateau.cityHousesList.remove(self)
        self.plateau.structures.remove(self)
        del self

    def udmCheck(self) :
            #Upgrade et Down grade triés par type de maison :
            if (self.desc == "SmallTent" or self.desc =="SmallTent2") and self.case.waterAccess>0 : #Il faudra ajouter plus tard la condition de désirabilité
                self.upgrade()
            if (self.desc == "LargeTent" or self.desc =="LargeTent2") and self.case.waterAccess<1 : #Il faudra ajouter plus tard la condition de désirabilité
                self.downgrade()

            #Merge 4 1*1 en un 2*2 :
            if (self.desc == "SmallTent" or self.desc =="LargeTent") :
                if self.plateau.map[self.case.x][self.case.y-1].structure and self.plateau.map[self.case.x+1][self.case.y].structure and self.plateau.map[self.case.x+1][self.case.y-1].structure :
                    ans = (self.desc == self.plateau.map[self.case.x][self.case.y-1].structure.desc,self.desc == self.plateau.map[self.case.x+1][self.case.y].structure.desc,self.desc == self.plateau.map[self.case.x+1][self.case.y-1].structure.desc)
                    if all(ans) :
                        fornh = self.nbHab
                        self.delete()
                        MergedHouse(self.case,self.plateau,(2,2),self.desc+"2",[self.plateau.map[self.case.x][self.case.y-1].structure,self.plateau.map[self.case.x+1][self.case.y].structure,self.plateau.map[self.case.x+1][self.case.y-1].structure],fornh)


    def upgrade(self) :
        if self.desc=="SmallTent" : 
            self.desc="LargeTent"
            self.set_nbHabmax(20)
        if self.desc=="SmallTent2" : 
            self.desc="LargeTent2"
            self.set_nbHabmax(28)

    def downgrade(self) :
        if self.desc == "LargeTent":
            self.desc = "SmallTent"
            self.set_nbHabmax(5)
        if self.desc=="LargeTent2" : 
            self.desc="SmallTent2"
            self.set_nbHabmax(20)
        #Ramène le nombre d'habitants au maximum de la nouvelle taille
        if self.nbHab > self.nbHabMax :
            self.nbHab = self.nbHabMax

class MergedHouse(House) :
    def __init__(self, case, plateau, size, desc, ohouses, fornh) :
        super().__init__(case, plateau, size, desc)
        self.nbHab = fornh+ohouses[0].nbHab+ohouses[1].nbHab+ohouses[2].nbHab
        self.nbHabMax=self.nbHabMax * 4
        self.case.render_pos=[self.case.render_pos[0], self.case.render_pos[1]+10]
        self.secCases=[]
        for h in ohouses :
            self.secCases.append(h.case)
            h.delete()
        for c in self.secCases :
            c.setStructure(self)

    def ignite(self):
        self.delete()
        for oc in self.secCases :
               BurningBuilding(oc, self.plateau,"BurningBuilding")
        BurningBuilding(self.case,self.plateau,"BurningBuilding")

    def delete(self) :
        self.case.render_pos=[self.case.render_pos[0], self.case.render_pos[1]-10]
        self.case.setStructure(None)
        for oc in self.secCases :
            oc.setStructure(None)
        self.plateau.cityHousesList.remove(self)
        self.plateau.structures.remove(self)
        self.plateau.cityHousesList.remove(self)


        del self     

class HousingSpot() :

    def __init__(self, case, plateau, desc="HousingSpot") :
        self.case = case
        self.case.setStructure(self)
        self.desc = desc
        self.plateau=plateau
        self.plateau.structures.append(self)
        self.plateau.treasury = self.plateau.treasury - HOUSE_COST
        self.case.setFeature("HousingSpot")
        self.plateau.cityHousingSpotsList.append(self)
        self.spawn_timer = pygame.time.get_ticks()
        self.nb_immigrant = 0
        self.immigrant = None

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
        if self.immigrant :
            self.immigrant.chariot.delete()
            self.immigrant.delete()
        del self

    def becomeAHouse(self):
        self.plateau.cityHousingSpotsList.remove(self)
        self.plateau.structures.remove(self)
        House(self.case,self.plateau,(1,1), "SmallTent")
        self.case.setFeature("Small Tent")
        del self
    
    def generateImmigrant(self):
        now = pygame.time.get_ticks()

        if now - self.spawn_timer > 500:
            if randint(0, 10) == 0 and self.nb_immigrant < 1:
                self.immigrant = Immigrant(self.plateau.map[19][38], self.plateau, self.case)
                self.nb_immigrant += 1
            self.spawn_timer = now

"""
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

"""

        
        

