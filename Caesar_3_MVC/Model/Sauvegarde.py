import pickle
import os

class Sauvegarde() :
    def __init__(self, actualGame) -> None:   

        #Sauvegarde des données de la cité 
        self.attractiveness = actualGame.attractiveness
        self.treasury = actualGame.treasury
        self.population = actualGame.population

        #Sauvegarde de la map
        self.map = []
        for cell_x in range(actualGame.nbr_cell_x):
            self.map.append([])
            for cell_y in range(actualGame.nbr_cell_y):
                case_ = actualGame.map[cell_x][cell_y]
                newdict = {"x" : case_.x, "y" : case_.y, "sprite" : case_.sprite, "feature" : case_.feature}
                if case_.road:
                    newdict |= {"road" : 1}
                else:
                    newdict |= {"road" : 0}
                self.map[cell_x].append(newdict)
        
        #Sauvegarde des structures
        self.structures = []
        for s in actualGame.structures :
            if s.desc != "WheatPlot":
                newdict = {"type" : s.desc, "x" : s.case.x, "y" : s.case.y}
                if newdict["type"] != "HousingSpot":
                    newdict |= {"size" : s.size, "fireRisk" : s.fireRisk, "collapseRisk" : s.collapseRisk}
                    if newdict["type"] == "BurningBuilding":
                        newdict |= {"timeBurning" : s.timeBurning}
                    elif newdict["type"] == "SmallTent" or newdict["type"] == "LargeTent":
                        newdict |= {"entertainLvl" : s.entertainLvl, "nbHab" : s.nbHab, "nbHabMax" : s.nbHabMax,
                                    "religiousAccess" : s.religiousAccess}
                    elif newdict["type"] == "SmallTent2" or newdict["type"] == "LargeTent2":
                        newdict|= {"case1_x" : s.secCases[0].x, "case1_y" : s.secCases[0].y,
                                    "case2_x" : s.secCases[1].x, "case2_y" : s.secCases[1].y,
                                    "case3_x" : s.secCases[2].x, "case3_y" : s.secCases[2].y,
                                    "nbHab" : s.nbHab}      
                    elif newdict["type"] == "Prefecture" or newdict["type"] == "EngineerPost":
                        newdict |= {"active" : s.active}
                else:
                    newdict |= {"nb_immigrant" : s.nb_immigrant}
                self.structures.append(newdict)
        #self.structures.append(s)
        
        #Sauvegarde des entités
        self.entities = []
        for e in actualGame.entities :
            if e.type != "Chariot":
                newdict = {"type" : e.type, "x" : e.case.x, "y" : e.case.y, "name" : e.name, "ttw" : e.ttw, "action" : e.action, "direction" : e.direction, "path" : e.path}
                if newdict["type"] == "Prefet" or newdict["type"] == "Engineer":
                    newdict |= {"rest" : e.rest, "workplace_x" : e.workplace.case.x, "workplace_y" : e.workplace.case.y}
                    if newdict["type"] == "Prefet":
                        if e.target:
                            newdict |= {"target_x" : e.target.case.x, "target_y" : e.target.case.y}
                        else :
                            newdict |= {"target_x" : 0, "target_y" : 0}
                elif newdict["type"] == "Immigrant":
                    newdict |= {"target_x" : e.target.x, "target_y" : e.target.y}

                self.entities.append(newdict)
            #self.entities.append(e)
                

def save_object(obj : Sauvegarde, filename : str):
    """Save an object in a file
    Return Success if saving works
    Return Fail if saving failed"""
    full_path = os.path.join("Model\\Save_Folder", filename)
    try:
        with open(full_path, "wb+") as f:
            pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
            return "Success"
    except Exception as ex:
        print("Error when saving")
        print("     -->Error during pickling object :", ex)
        return "Fail"

def load_object(filename:str):
    """
    Load an object from a file
    Return the object if it can be loaded
    Return "error" if the object cannot be loaded
    """
    full_path = os.path.join("Model\\Save_Folder", filename)
    try:
        with open(full_path, "rb") as f:
            return pickle.load(f)
    except Exception as ex:
        print("Error when loading")
        print("Error during unpickling object :", ex)
        return "error" 