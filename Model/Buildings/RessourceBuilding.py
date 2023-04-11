from Model.Buildings.Building import *
from Model.Buildings.Building import DamagedBuilding
from Model.Buildings.Building import BurningBuilding
from Model.Walker import *
from Model.Case import *
from Model.Buildings.Building import Building
from Model.Buildings.House import House
import random

class WheatFarm(Building) :
    def __init__(self, case, plateau, size, desc, property = 1, storedQuant = 0, growingQuant = 0):
        super().__init__(case, plateau, size, desc, property=property)
        self.connectedToRoad = self.case.connectedToRoad
        self.storedQuant=storedQuant
        self.storedQuantMax = 100
        self.growingQuant = growingQuant
        self.growingQuantMax = 100
        self.growingTimer = 0
        self.productivity = 0
        self.nbEmpl = 0
        self.plateau.treasury[self.property-1] = self.plateau.treasury[self.property-1] - WHEATFARM_COST
        self.case.render_pos = [self.case.render_pos[0]-35, self.case.render_pos[1]+5]
        self.plots = []
        self.secCases = [self.plateau.map[self.case.x][self.case.y-1],self.plateau.map[self.case.x-1][self.case.y],self.plateau.map[self.case.x-1][self.case.y-1]]
        for sc in self.secCases :
            sc.setStructure(self)
        #Création des parcelles de blé et ajout dans la liste :
        self.plots.append(WheatPlot(self.plateau.map[self.case.x-1][self.case.y+1],self.plateau,(1,1),"WheatPlot",self))
        self.plots.append(WheatPlot(self.plateau.map[self.case.x][self.case.y+1],self.plateau,(1,1),"WheatPlot",self))
        self.plots.append(WheatPlot(self.plateau.map[self.case.x+1][self.case.y+1],self.plateau,(1,1),"WheatPlot",self))
        self.plots.append(WheatPlot(self.plateau.map[self.case.x+1][self.case.y],self.plateau,(1,1),"WheatPlot",self))
        self.plots.append(WheatPlot(self.plateau.map[self.case.x+1][self.case.y-1],self.plateau,(1,1),"WheatPlot",self))
        self.allCases = [self.case]
        for sc in self.secCases : self.allCases.append(sc)
        for p in self.plots : self.allCases.append(p.case)

        self.walker = None



       
    def update(self, currentSpeedFactor) :
        if self.growingQuant<self.growingQuantMax:
            self.growingTimer += 1
        for ac in self.allCases :
            if ac.connectedToRoad > 0:
                
                #Récolte le blé si les champs sont pleins :
                if self.growingQuant>=self.growingQuantMax and not self.walker:
                    cartpusher = CartPusher(ac, self.plateau, self, property = self.property)
                    if self.plateau.multiplayer :
                        self.plateau.multiplayer.send(f"WA.3.{cartpusher.case.x}.{cartpusher.case.y}.{self.case.x}.{self.case.y}.{cartpusher.property}.{cartpusher.id}")
                    self.storedQuant=self.storedQuant+10
                    self.growingQuant=0
                    for p in self.plots :
                        p.level = 0
                #Fait augmnter la quantité de blé qui pousse :
                if self.growingTimer > (500 / currentSpeedFactor):
                    self.growingQuant+=1
                    self.growingTimer = 0

                #Set the sprites of the plots
                elif self.growingQuant > 4 :
                    for p in self.plots :   #Remet toutes les parcelles à 0 pour refaire le calcul
                        p.level = 0
                        rep = 0             #Répartition qui parcours les parcelles en donnant 5 blé à chaque jusqu'à épuisement
                        i=0                                             
                    while rep < self.growingQuant :
                        if self.plots[i].level < 4 :
                            self.plots[i].level = self.plots[i].level+1
                            i=i+1 if i<4 else 0
                            rep = rep+5
                return
        self.plateau.roadWarning = True

    def ignite(self):
        self.delete()
        for oc in self.secCases :
            BurningBuilding(oc, self.plateau,"BurningBuilding")
        for oc in self.plots :
               BurningBuilding(oc.case, self.plateau,"BurningBuilding")
        BurningBuilding(self.case,self.plateau,"BurningBuilding")

    def collapse(self):
        self.delete()
        for oc in self.secCases :
            DamagedBuilding(oc, self.plateau,"Ruins")
        for oc in self.plots :
               DamagedBuilding(oc.case, self.plateau,"Ruins")
        DamagedBuilding(self.case,self.plateau,"Ruins")

        

    def delete(self) :
        self.case.render_pos = [self.case.render_pos[0]+35, self.case.render_pos[1]-5]
        self.case.setStructure(None)
        self.plateau.structures.remove(self)
        if self.walker:
            self.walker.delete()
        for sc in self.secCases :
            sc.setStructure(None)
        for p in self.plots :
            p.deleteFromFarm()
        del self 
            

class WheatPlot(Building) :
    def __init__(self, case, plateau, size, desc, myFarm):
        super().__init__(case, plateau, size, desc)
        self.level = 0
        self.myFarm = myFarm

    def delete(self) :
        self.myFarm.delete()
    
    def deleteFromFarm(self) :
        self.case.setStructure(None)
        self.plateau.structures.remove(self)
        del self


class Market(Building) :
    def __init__(self, case, plateau, size, desc, property = 1, storedWheat = 0):
        super().__init__(case, plateau, size, desc, property=property)
        self.storedWheat = storedWheat
        self.storedWheatMax = 800
        self.plateau.treasury[self.property-1] = self.plateau.treasury[self.property-1] - MARKET_COST
        self.case.render_pos = [self.case.render_pos[0], self.case.render_pos[1]+20]
        self.secCases = [self.plateau.map[self.case.x][self.case.y-1],self.plateau.map[self.case.x+1][self.case.y],self.plateau.map[self.case.x+1][self.case.y-1]]
        self.transporter = None
        self.giver = None
        for sc in self.secCases :
            sc.setStructure(self)

    def update(self, currentSpeedFactor) :
        for ac in self.secCases :
            if ac.connectedToRoad > 0 or self.case.connectedToRoad > 0:
                if self.storedWheat >= 100 and not self.giver:
                    self.storedWheat -= 100
                    markettrader = MarketTrader(ac, self.plateau, self, 2, 100, property = self.property)
                    if self.plateau.multiplayer :
                        self.plateau.multiplayer.send(f"WA.4.{markettrader.case.x}.{markettrader.case.y}.{self.case.x}.{self.case.y}.{markettrader.mode}.{markettrader.wheat}.{markettrader.property}.{markettrader.id}")
                if self.storedWheat <= self.storedWheatMax and not self.transporter:
                    MarketTrader(ac, self.plateau, self, 1, 0, property = self.property)
                    if self.plateau.multiplayer :
                        self.plateau.multiplayer.send(f"WA.4.{markettrader.case.x}.{markettrader.case.y}.{self.case.x}.{self.case.y}.{markettrader.mode}.{markettrader.wheat}.{markettrader.property}.{markettrader.id}")
                return      
        self.plateau.roadWarning = True      
        
    def ignite(self):
        self.delete()
        for oc in self.secCases :
               BurningBuilding(oc, self.plateau,"BurningBuilding")
        BurningBuilding(self.case,self.plateau,"BurningBuilding")

    def collapse(self):
        self.delete()
        for oc in self.secCases :
            DamagedBuilding(oc, self.plateau,"Ruins")
        DamagedBuilding(self.case,self.plateau,"Ruins")

    def delete(self) :
        self.case.render_pos = [self.case.render_pos[0], self.case.render_pos[1]-20]
        self.case.setStructure(None)
        self.plateau.structures.remove(self)
        if self.transporter:
            self.transporter.delete()
        if self.giver:
            self.giver.delete()
        for sc in self.secCases :
            sc.setStructure(None)
        del self 


class Granary(Building) :
    def __init__(self, case, plateau, size, desc, property = 1, storedWheat = 0):
        super().__init__(case, plateau, size, desc, property=property)
        self.storedWheat = storedWheat
        self.storedWheatMax = 2900
        self.levelB = 0
        self.levelV = 0
        self.plateau.treasury[self.property-1] = self.plateau.treasury[self.property-1] - GRANARY_COST
        self.secCases = []
        for sc in self.secCases :
            sc.setStructure(self)
        for xar in range(self.case.x, self.case.x-3, -1) :
            for yar in range(self.case.y, self.case.y-3, -1) :
                if self.plateau.map[xar][yar] != self.case :
                    self.secCases.append(self.plateau.map[xar][yar])


        for sc in self.secCases :
            sc.setStructure(self)


    def update(self, currentSpeedFactor) :
            for ac in self.secCases :
                if ac.connectedToRoad > 0 or self.case.connectedToRoad > 0 :
                    return
            self.plateau.roadWarning = True

        
    def ignite(self):
        self.delete()
        for oc in self.secCases :
               BurningBuilding(oc, self.plateau,"BurningBuilding")
        BurningBuilding(self.case,self.plateau,"BurningBuilding")

    def collapse(self):
        self.delete()
        for oc in self.secCases :
            DamagedBuilding(oc, self.plateau,"Ruins")
        DamagedBuilding(self.case,self.plateau,"Ruins")

    def delete(self) :
        self.case.setStructure(None)
        self.plateau.structures.remove(self)
        for sc in self.secCases :
            sc.setStructure(None)
        del self 

