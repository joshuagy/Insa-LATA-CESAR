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
            #Formule de base mêlant ancienneté du bâtiment et hasard. Pourra être modifiée si besoin
            safeTime = 1000          # Nombre de ticks pendant lequel le bâtiment est 100% safe
            criticalTime = 50000    # Nombre de ticks après lequels le bâtiment s'écroule forcément
            randC = randint(safeTime,criticalTime)
            if randC+self.get_collapseRisk() >= safeTime+criticalTime :
                self.collapse()
            else :
                self.set_collapseRisk(self.get_collapseRisk()+1)
        #FireRisk :
        if self.desc in list_of_flammable_structures :
            #Formule de base mêlant ancienneté du bâtiment et hasard. Pourra être modifiée si besoin
            safeTime = 1000          # Nombre de ticks pendant lequel le bâtiment est 100% safe
            criticalTime = 50000    # Nombre de ticks après lesquels le bâtiment s'écroule forcément
            randF = randint(safeTime,criticalTime)
            if randF+self.get_fireRisk() >= safeTime+criticalTime :
                self.ignite()
            else :
                self.set_fireRisk(self.get_fireRisk()+1)
            # Chance qu'un incendie s'éteigne de lui-même (Pour l'instant 0,5% par tick après 1000 ticks)
        if self.desc == "BurningBuilding" :
            if self.timeBurning < 1000 :
                self.timeBurning = self.timeBurning+1
            else :
                val = randint(0,1000)
                if val<=5 :
                    self.desc="BurnedRuins"

    def collapse(self):
        self.delete()
        DamagedBuilding(self.case,self.plateau,"Ruins")

    def ignite(self):
        self.delete()
        DamagedBuilding(self.case,self.plateau,"BurningBuilding")

class DamagedBuilding :
    def __init__(self, case, plateau, desc):
        self.case=case
        self.timeBurning=0
        self.plateau = plateau
        self.desc = desc
        self.plateau.structures.append(self)
        self.case.setStructure(self)

    def delete(self):
        self.plateau.structures.remove(self)
        self.case.setStructure(None)
        del self
