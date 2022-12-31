from types import NoneType

class Building():
    def __init__(self, position, case, plateau, size, connectedToRoad, fireRisk, collapseRisk, desc = "Default", status=False):
        self.position = position
        self.size = size
        self.desc = desc
        self.connectedToRoad = connectedToRoad
        self.status = status
        self.case = case
        self.case.building = self
        self.plateau = plateau
        self.plateau.buildings.append(self)
    
    def delete(self):
        self.case.building = None
        self.plateau.buildings.remove(self)
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
