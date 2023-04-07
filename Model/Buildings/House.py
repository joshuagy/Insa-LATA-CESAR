import pygame
from random import randint
from Model.Buildings.Building import *
from Model.Buildings.Building import BurningBuilding
from Model.Plateau import *
from Model.Case import *
from Model.Walker import Immigrant
from Model.Buildings.Building import DamagedBuilding

class House(Building):

    def __init__(self, case, plateau, size, desc, wheat = 0, entertainLvl = 0, nbHab = 1, nbHabMax = 5, religiousAccess = 0, property = 1, fireRisk = 0, collapseRisk = 0):
        super().__init__(case, plateau, size, desc, property, fireRisk, collapseRisk)
        self.entertainLvl = entertainLvl
        self.wheat = wheat
        self.wheatMax = 10
        self.nbHab = nbHab
        self.nbHabMax = nbHabMax
        self.religiousAccess = religiousAccess
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

    def get_nbHabMax(self):
        return self.nbHabMax
    
    def set_nbHabMax(self, newnbHabmax):
        self.nbHabMax = newnbHabmax

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
            if (self.desc == "LargeTent" or self.desc =="LargeTent2") and (self.case.waterAccess<1 or self.case.getDesirability(self.plateau, self.property) < -12): #Il faudra ajouter plus tard la condition de désirabilité
                self.downgrade()
            if (self.desc == "LargeTent2") and self.wheat>0 and self.case.getDesirability(self.plateau, self.property)>-5 and self.case.waterAccess>0 :
                self.upgrade()
            if (self.desc == "SmallShack") and (self.case.waterAccess<1 or self.case.getDesirability(self.plateau, self.property)<-7 or self.wheat<1) :
                self.downgrade()
            if (self.desc == "SmallShack") and self.case.religiousAccess>0 and self.case.waterAccess>0 and self.wheat>0 and self.case.getDesirability(self.plateau, self.property)>0 :
                self.upgrade()
            if self.desc == "LargeShack" and (self.case.religiousAccess<1 or self.case.waterAccess<1 or self.wheat==0 or self.case.getDesirability(self.plateau, self.property)<-2) :
                self.downgrade()


            #Augmentation du nombre d'habitant en fonction du blé disponible
            if self.wheat >4 and self.nbHab < self.nbHabMax:
                self.wheat = self.wheat-3
                self.nbHab = self.nbHab +1

            #Merge 4 1*1 en un 2*2 :
            if (self.desc == "SmallTent" or self.desc =="LargeTent") :
                if self.plateau.map[self.case.x][self.case.y-1].structure and self.plateau.map[self.case.x+1][self.case.y].structure and self.plateau.map[self.case.x+1][self.case.y-1].structure :
                    ans = (self.desc == self.plateau.map[self.case.x][self.case.y-1].structure.desc,self.desc == self.plateau.map[self.case.x+1][self.case.y].structure.desc,self.desc == self.plateau.map[self.case.x+1][self.case.y-1].structure.desc)
                    if all(ans) :
                        houses = [self,self.plateau.map[self.case.x][self.case.y-1].structure,self.plateau.map[self.case.x+1][self.case.y].structure,self.plateau.map[self.case.x+1][self.case.y-1].structure]
                        nbHab = houses[0].nbHab+houses[1].nbHab+houses[2].nbHab+houses[3].nbHab
                        secCases=[]
                        for h in houses[1:] :
                            secCases.append(h.case)
                        for h in houses :
                            h.delete()
                        MergedHouse(self.case,self.plateau,(2,2),self.desc+"2",self.wheat,nbHab, secCases)


    def upgrade(self) :
        if self.desc=="SmallTent" : 
            self.desc="LargeTent"
            self.set_nbHabMax(7)
        if self.desc=="SmallTent2" : 
            self.desc="LargeTent2"
            self.set_nbHabMax(28)
        if self.desc=="LargeTent2" : 
            self.desc="SmallShack"
            self.set_nbHabMax(36)
        if self.desc == "SmallShack" :
            self.desc = "LargeShack"
            self.set_nbHabMax(44)
        self.wheatMax = self.nbHabMax + 10

    def downgrade(self) :
        if self.desc == "LargeTent":
            self.desc = "SmallTent"
            self.set_nbHabMax(5)
            if self.nbHab>self.nbHabMax : 
                self.nbHab=self.nbHabMax
        if self.desc=="LargeTent2" : 
            self.desc="SmallTent2"
            self.set_nbHabMax(20)
            if self.nbHab>self.nbHabMax : 
                self.nbHab=self.nbHabMax
        if self.desc =="SmallShack" :
            self.desc = "LargeTent2"
            self.set_nbHabMax(28)
            if self.nbHab>self.nbHabMax : 
                self.nbHab=self.nbHabMax
        if self.desc == "LargeShack" :
            self.desc = "SmallShack"
            self.set_nbHabMax(36)
            if self.nbHab>self.nbHabMax : 
                self.nbHab=self.nbHabMax
        self.wheatMax = self.nbHabMax + 10
        if self.wheat > self.wheatMax :
            self.wheat = self.wheatMax

        #Ramène le nombre d'habitants au maximum de la nouvelle taille
        if self.nbHab > self.nbHabMax :
            self.nbHab = self.nbHabMax

    def foodConsumption(plateau) :
        for h in plateau.structures :
            if isinstance(h,House) :
                if h.wheat > h.nbHab :
                    h.wheat = h.wheat-h.nbHab
                else :
                    h.nbHab = h.nbHab - (h.nbHab-h.wheat)
                    if h.nbHab==0 : h.nbHab = 1 

        

class MergedHouse(House) :
    def __init__(self, case, plateau, size, desc, wheat, nbHab, secCases, property = 1, fireRisk = 0, collapseRisk = 0) :
        super().__init__(case, plateau, size, desc, fireRisk=fireRisk, collapseRisk=collapseRisk, property=property)
        self.nbHab = nbHab
        self.wheat = wheat
        self.nbHabMax=self.nbHabMax * 4
        self.case.render_pos=[self.case.render_pos[0], self.case.render_pos[1]+10]
        self.secCases=secCases
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
        del self     

class HousingSpot() :

    def __init__(self, case, plateau, desc="HousingSpot", property = 1, nb_immigrant = 0) :
        self.case = case
        self.case.setStructure(self)
        self.desc = desc
        self.plateau=plateau
        self.plateau.structures.append(self)
        self.plateau.treasury = self.plateau.treasury - HOUSE_COST
        self.case.setFeature("HousingSpot")
        self.plateau.cityHousingSpotsList.append(self)
        self.spawn_timer = pygame.time.get_ticks()
        self.nb_immigrant = nb_immigrant
        self.immigrant = None
        self.property = property

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
            self.immigrant.delete()
        del self

    def becomeAHouse(self):
        self.plateau.cityHousingSpotsList.remove(self)
        self.plateau.structures.remove(self)
        House(self.case,self.plateau,(1,1), "SmallTent", property = self.property)
        self.case.setFeature("Small Tent")
        del self
    
    def generateImmigrant(self, currentSpeedFactor):
        if self.property == self.plateau.property :
            now = pygame.time.get_ticks()

            if now - self.spawn_timer > (500 / currentSpeedFactor):
                if randint(0, 10) == 0 and self.nb_immigrant < 1:
                    Immigrant(self.plateau.map[19][38], self.plateau, self.case)
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

        
        

