from Model.Buildings.Building import *
from Model.Buildings.Building import DamagedBuilding
from Model.Buildings.Building import BurningBuilding
from Model.Walker import *
from Model.Case import *
from Model.Buildings.Building import Building

class WheatFarm(Building) :
    def __init__(self, case, plateau, size, desc):
        super().__init__(case, plateau, size, desc)
        self.connectedToRoad = self.case.connectedToRoad
        self.storedQuant=0
        self.storedQuantMax = 100
        self.growingQuant = 0
        self.growingQuantMax = 100
        self.productivity = 0
        self.nbEmpl = 0
        self.case.render_pos = [self.case.render_pos[0], self.case.render_pos[1]+15]
        self.plots = []
        self.secCases = [self.plateau.map[self.case.x][self.case.y-1],self.plateau.map[self.case.x+1][self.case.y],self.plateau.map[self.case.x+1][self.case.y-1]]
        for sc in self.secCases :
            sc.setStructure(self)
        #Création des parcelles de blé et ajout dans la liste :
        self.plots.append(WheatPlot(self.plateau.map[self.case.x][self.case.y+1],self.plateau,(1,1),"WheatPlot",self))
        self.plots.append(WheatPlot(self.plateau.map[self.case.x+1][self.case.y+1],self.plateau,(1,1),"WheatPlot",self))
        self.plots.append(WheatPlot(self.plateau.map[self.case.x+2][self.case.y+1],self.plateau,(1,1),"WheatPlot",self))
        self.plots.append(WheatPlot(self.plateau.map[self.case.x+2][self.case.y],self.plateau,(1,1),"WheatPlot",self))
        self.plots.append(WheatPlot(self.plateau.map[self.case.x+2][self.case.y-1],self.plateau,(1,1),"WheatPlot",self))
    
    def update(self) : 

        #Affiche un message et annule toute mise à jour si le bâtiment n'est pas connecté à la route :

        #Récolte le blé si les champs sont pleins :
        if self.growingQuant>=100 :
            self.storedQuant=self.storedQuant+10
            self.growingQuant=0
            for p in self.plots :
                p.level = 0
            return
        
        #Fait augmnter la quantité de blé qui pousse si la ferme est productive :
        #Je vais me renseigner pour le fonctionnement

        #Set the sprites of the plots
        if self.growingQuant > 4 :
            for p in self.plots :   #Remet toutes les parcelles à 0 pour refaire le calcul
                p.level = 0
            rep = 0                 #Répartition qui parcours les parcelles en donnant 5 blé à chaque jusqu'à épuisement 
            i = 0
            while rep < self.growingQuant :
                if self.plots[i].level < 4 :
                    self.plots[i].level = self.plots[i].level+1
                    i=i+1 if i<4 else 0
                    rep = rep+5

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
        self.case.render_pos = [self.case.render_pos[0], self.case.render_pos[1]-15]
        self.case.setStructure(None)
        self.plateau.structures.remove(self)
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
    def __init__(self, case, plateau, size, desc):
        super().__init__(case, plateau, size, desc)
        self.storedWheat = 0
        self.secCases = [self.plateau.map[self.case.x][self.case.y-1],self.plateau.map[self.case.x+1][self.case.y],self.plateau.map[self.case.x+1][self.case.y-1]]
        for sc in self.secCases :
            sc.setStructure(self)

    def delete(self) :
        self.case.render_pos = [self.case.render_pos[0], self.case.render_pos[1]]
        self.case.setStructure(None)
        self.plateau.structures.remove(self)
        for sc in self.secCases :
            sc.setStructure(None)
        del self 

