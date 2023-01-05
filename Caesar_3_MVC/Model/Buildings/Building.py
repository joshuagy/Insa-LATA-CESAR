from types import NoneType

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
