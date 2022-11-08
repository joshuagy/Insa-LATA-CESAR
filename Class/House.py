from Building import Building

class House(Building):
    def __init__(self, position, size, desc, connectedToRoad, entertainLvl, riskLevel, riskStatus, status=False , ressources = dict()):
        super().__init__(position, size, desc, connectedToRoad, status , ressources)
        self.entertainLvl = entertainLvl
        self.riskLevel = riskLevel
        self.riskStatus = riskStatus

    def get_entertainLvl(self):
        return self.entertainLvl
    
    def set_entertainLvl(self, newEntertainLvl):
        self.entertainLvl = newEntertainLvl
    
    def get_riskLevel(self):
        return self.riskLevel
    
    def set_riskLevel(self, newRiskLevel):
        self.riskLevel = newRiskLevel
    
    def get_riskStatus(self):
        return self.riskStatus
    
    def set_riskStatus(self, newRiskStatus):
        self.riskStatus = newRiskStatus
    