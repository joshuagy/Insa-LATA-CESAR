from types import NoneType
from Model.constants import *
from random import *

class Building():
    def __init__(self, case, plateau, size, desc):
        self.size = size
        self.desc = desc
        self.connectedToRoad = 0
        self.case = case
        self.case.setStructure(self)
        self.plateau = plateau
        self.plateau.structures.append(self)
        self.fireRisk = 0
        self.collapseRisk= 0
        self.cost = 0
    
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

    def riskCheck(self) :
        #CollapseRisk :
        if self.desc in list_of_brittle_structures :
            if randint(0, 200) == 0:
                self.set_collapseRisk(self.get_collapseRisk()+1)
                if(self.get_collapseRisk() > 6):
                    self.collapse()
        #FireRisk :
        if self.desc in list_of_flammable_structures :
            if randint(0, 200) == 0:
                self.set_fireRisk(self.get_fireRisk()+1)
                if(self.get_fireRisk() > 6):
                    self.ignite()
                    for e in self.plateau.prefets : e.newFire()

    def collapse(self):
        self.delete()
        DamagedBuilding(self.case,self.plateau,"Ruins")

    def ignite(self):
        self.delete()
        BurningBuilding(self.case,self.plateau,"BurningBuilding")

class DamagedBuilding(Building) :
    def __init__(self, case, plateau, desc):
        self.case=case
        self.plateau = plateau
        self.desc = desc
        self.plateau.structures.append(self)
        self.case.setStructure(self)

    def delete(self):
        self.plateau.structures.remove(self)
        self.case.setStructure(None)
        del self


class BurningBuilding(Building) :
    def __init__(self, case, plateau, desc):
        self.case=case
        self.timeBurning=0
        self.plateau = plateau
        self.desc = desc
        self.plateau.structures.append(self)
        self.case.setStructure(self)
        self.plateau.burningBuildings.append(self)
        self.index_sprite = 0
    
    def delete(self):
        self.plateau.structures.remove(self)
        self.case.setStructure(None)
        self.plateau.burningBuildings.remove(self)
        del self
    
    def off(self):
        self.delete()
        DamagedBuilding(self.case,self.plateau,"BurnedRuins")

    def update(self):
        self.index_sprite += 0.5
        if(self.index_sprite >= len(self.plateau.image_structures["BurningBuilding"])):
            self.index_sprite = 0
        # Chance qu'un incendie s'éteigne de lui-même (Pour l'instant 0,5% par tick après 1000 ticks)
        if self.timeBurning < 1000 :
            self.timeBurning = self.timeBurning+1
        else :
            val = randint(0,1000)
            if val<=5 :
                self.off()