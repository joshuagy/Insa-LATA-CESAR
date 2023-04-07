from types import NoneType
from Model.constants import *
from random import *
from Model.Buildings.House import *

class Building():
    def __init__(self, case, plateau, size, desc, property = 1, fireRisk = 0, collapseRisk = 0):
        self.size = size
        self.desc = desc
        self.connectedToRoad = 0
        self.case = case
        self.case.setStructure(self)
        self.plateau = plateau
        self.plateau.structures.append(self)
        self.fireRisk = fireRisk
        self.collapseRisk= collapseRisk
        self.riskTimer = 0
        self.cost = 0
        self.property = property
    
    def delete(self):
        self.case.setStructure(None)
        self.plateau.structures.remove(self)
        del self

    def get_position(self):
        return self.position
    
    def set_position(self, newPos):
        self.position = newPos

    def get_size(self):
        return self.size
    
    def set_size(self, newsize):
        self.size = newsize

    def get_desc(self):
        return self.desc

    def set_desc(self, newDesc):
        self.desc = newDesc

    def get_connectedToRoad(self):
        return self.connectedToRoad

    def set_connectedToRoad(self, newConnectedToRoad):
        self.connectedToRoad = newConnectedToRoad

    def set_status(self):
        return self.status
    
    def get_status(self, newStatus):
        self.status = newStatus

    def get_fireRisk(self):
        return self.fireRisk

    def set_fireRisk(self, newFireRisk):
        self.fireRisk=newFireRisk
    
    def get_collapseRisk(self):
        return self.collapseRisk
    
    def set_collapseRisk(self, newcollapseRisk):
        self.collapseRisk = newcollapseRisk

    def setCase(self, newCase):
        self.case = newCase

    def getCase(self):
        return self.case

    def riskCheck(self, currentSpeedFactor) :
        if self.property == self.plateau.property :
            self.riskTimer += 1
            if self.riskTimer > (500 / currentSpeedFactor):
                #CollapseRisk :
                if self.desc in list_of_brittle_structures :
                    if randint(0, 200) == 0:
                        self.set_collapseRisk(self.get_collapseRisk()+1)
                        if(self.get_collapseRisk() > 6):
                            self.collapse()
                #FireRisk :
                if self.desc in list_of_flammable_structures :
                    if randint(0, 150) == 0:
                        self.set_fireRisk(self.get_fireRisk()+1)
                        if(self.get_fireRisk() > 6):
                            self.ignite()
                
                self.riskTimer = 0

    def collapse(self):
        self.delete()
        DamagedBuilding(self.case,self.plateau,"Ruins")

    def ignite(self):
        self.delete()
        BurningBuilding(self.case,self.plateau,"BurningBuilding")

class DamagedBuilding(Building) :
    def __init__(self, case, plateau, desc, size = (1,1), property=1, fireRisk = 0, collapseRisk = 0):
        self.case=case
        self.size = size
        self.plateau = plateau
        self.desc = desc
        self.plateau.structures.append(self)
        self.case.setStructure(self)
        self.fireRisk = fireRisk 
        self.collapseRisk = collapseRisk
        self.riskTimer = 0
        self.property = property

    def delete(self):
        self.plateau.structures.remove(self)
        self.case.setStructure(None)
        del self


class BurningBuilding(Building) :
    def __init__(self, case, plateau, desc, size = (1,1), property = 1, fireRisk = 0, collapseRisk = 0, timeBurning = 0):
        self.property = property
        self.case=case
        self.timeBurning=timeBurning
        self.plateau = plateau
        self.desc = desc
        self.size = size
        self.plateau.structures.append(self)
        self.case.setStructure(self)
        self.plateau.burningBuildings[self.property].append(self)
        self.fireRisk = fireRisk 
        self.collapseRisk = collapseRisk
        self.index_sprite = 0
        self.riskTimer = 0
    
    def delete(self):
        self.plateau.structures.remove(self)
        self.case.setStructure(None)
        self.plateau.burningBuildings[self.property].remove(self)
        del self
    
    def off(self):
        self.delete()
        DamagedBuilding(self.case,self.plateau,"BurnedRuins", property=self.property)

    def update(self, currentSpeedFactor):
        self.index_sprite += (0.1 * currentSpeedFactor)
        if(self.index_sprite >= len(self.plateau.image_structures["BurningBuilding"])):
            self.index_sprite = 0
        # Chance qu'un incendie s'éteigne de lui-même (Pour l'instant 0,5% par tick après 1000 ticks)
        if self.timeBurning < 1000 :
            self.timeBurning = self.timeBurning+1
        else :
            val = randint(0,1000)
            if val<=5 :
                self.off()
                
