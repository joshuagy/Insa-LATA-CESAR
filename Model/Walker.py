import random
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

ttwmax = 30

class Walker:
    def __init__(self, case, plateau, name = "Plebius Prepus", ttw = ttwmax, action = 1, direction = 1, path = [], path_index = 0):
        """
        case : La case de départ sur laquelle est le Walker
        plateau : Le plateau sur lequel est le Walker
        name : Le nom du Walker
        ttw : Durée de la marche aléatoire avant de devoir rentrer au point de départ
        action : l'état dans lequel ils sont

        Attributs :
        case_de_depart : La case de spawn du walker
        type : string qui contient le nom de la sous classe
        index_sprite : Permet d'animer le walker
        direction : Permet de connaître la direction dans laquelle il va
        move_timer : stock les tick d'horloge
        """

        self.case = case
        self.case_de_depart = case
        self.plateau = plateau
        self.name = name
        self.type = str(type(self))[21:-2]
        self.set_action(action)
        
        self.plateau.entities.append(self)  #On ajoute le walker à la liste des entitées présentes sur le plateau
        self.plateau.walkers[case.x][case.y].append(self)
        
        self.direction = direction # | 1 : North | 2 : East | 3 : South | 4 : West |
        self.ttw = ttw
        self.path = path
        self.path_index = path_index

        self.move_timer = 0


    def delete(self) :
        self.plateau.entities.remove(self)
        self.plateau.walkers[self.case.x][self.case.y].remove(self)
        del self

    def set_action(self, newAction) :
        self.index_sprite = 0
        self.action = newAction

    
    def random_path(self):
        """
        Retourne aléatoirement la prochaine case du walker.
        Ne peut pas se retourner à 180° sauf s'il est dans un cul de sac
        Ne fonctionne que sur les routes
        """
        possibilities = []

        if self.direction != 1:
            try : 
                if self.plateau.map[self.case.x][self.case.y+1].road :
                    possibilities.append((self.case.x, self.case.y+1))
            except IndexError : pass
        if self.direction != 2:
            if self.case.x > 0 :
                if self.plateau.map[self.case.x-1][self.case.y].road :
                    possibilities.append((self.case.x-1, self.case.y))
            else : pass
        if self.direction != 3:
            if self.case.y > 0 :
                if self.plateau.map[self.case.x][self.case.y-1].road :
                    possibilities.append((self.case.x, self.case.y-1))
            else : pass
        if self.direction != 4:
            try :
                if self.plateau.map[self.case.x+1][self.case.y].road :
                    possibilities.append((self.case.x+1, self.case.y))
            except IndexError : pass



        if len(possibilities) == 0:
            match(self.direction):
                case 1 :
                    if self.plateau.map[self.case.x][self.case.y+1].road == None:
                        self.ttw = 1
                    new_tile = (self.case.x, self.case.y+1)
                case 2 :
                    if self.plateau.map[self.case.x-1][self.case.y].road == None:
                        self.ttw = 1
                    new_tile = (self.case.x-1, self.case.y)
                case 3 :
                    if self.plateau.map[self.case.x][self.case.y-1].road == None:
                        self.ttw = 1
                    new_tile = (self.case.x, self.case.y-1)
                case 4 :
                    if self.plateau.map[self.case.x+1][self.case.y].road == None:
                        self.ttw = 1
                    new_tile = (self.case.x+1, self.case.y)
        else:
            new_tile = possibilities[random.randint(0, len(possibilities)- 1)]
        return new_tile
    
    def create_path(self, case_finale):
        """
        Création d'un chemin entre la case de départ (la case actuelle), la case finale,
        en prenant en compte les collisions.
        """
        x = case_finale.x
        y = case_finale.y
        self.path_index = 0
        #On appelle la fonction Grid de pathfinding en lui passant en paramètre la matrice de collision
        #On pourrait faire pareil avec une matrice de route si nécessaire
        self.grid = Grid(matrix=self.plateau.collision_matrix)

        self.start = self.grid.node(self.case.x, self.case.y)
        self.end = self.grid.node(x, y)
        if self.start == self.end :
            self.path = [(case_finale.x, case_finale.y)]
        else :

            #On empêche les mouvements diagonaux
            finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
            self.path, runs = finder.find_path(self.start, self.end, self.grid)

            if self.path == []:
                print("Error : impossible path")
                self.delete()


            #Permet d'observer facilement la map et le walker
            #print('operations:', runs, 'path length:', len(self.path))
            #print(self.grid.grid_str(path=self.path, start=self.start, end=self.end))        
        

    def change_tile(self, new_tile):
        """
        Changement de case et de direction d'un walker.
        """
        if self.case.x < new_tile[0]:
            self.direction = 2
        elif self.case.x > new_tile[0]:
            self.direction = 4
        elif self.case.y > new_tile[1]:
            self.direction = 1
        elif self.case.y < new_tile[1]:
            self.direction = 3
        self.plateau.walkers[self.case.x][self.case.y].remove(self)
        self.plateau.walkers[new_tile[0]][new_tile[1]].append(self)
        self.case = self.plateau.map[new_tile[0]][new_tile[1]]
    
    def update(self, currentSpeedFactor):
        pass
    
    def animate_sprite(self, currentSpeedFactor):
        self.index_sprite += (0.2 * currentSpeedFactor)
        if(self.index_sprite >= len(self.plateau.image_walkers[self.type][self.action][self.direction])):
            self.index_sprite = 0


class Citizen(Walker):
    def __init__(self, case, plateau, name="Plebius Prepus", ttw = ttwmax, action = 1, direction = 1, path = [], path_index = 0):
        super().__init__(case, plateau, name, ttw, action, direction, path, path_index)
    
    def update(self, currentSpeedFactor):
        """
        Mise à jour de la prochaine action du walker
        """
        self.move_timer += 1
        self.animate_sprite(currentSpeedFactor)

        """if self.move_timer > 500:
            if self.ttw > 0:
                new_pos = self.random_path()

                self.ttw -= 1
                if self.ttw == 0:
                    self.create_path(self.case_de_depart)
            else :
                new_pos = self.path[self.path_index]
                # Mise à jour de la position sur le plateau
                self.path_index += 1
                # On retourne en mode aléatoire si la destination a été atteint
                if self.path_index >= len(self.path) - 1:
                    self.ttw = ttwmax
            self.change_tile(new_pos)
            self.move_timer = 0"""

class Immigrant(Walker):
    def __init__(self, case, plateau, target, name="Plebius Prepus", ttw = ttwmax, action = 1, direction = 1, path = [], path_index = 0):
        super().__init__(case, plateau, name, ttw, action, direction, path, path_index)
        self.target = target
        self.chariot = Chariot(self.plateau.map[self.case.x][self.case.y+1], self.plateau, self)
        self.target.structure.immigrant = self
        self.create_path(target)
    
    def delete(self):
        super().delete()
        if self.target.structure :
            self.target.structure.immigrant = None
        self.chariot.delete()
    
    def update(self, currentSpeedFactor):
        """
        Mise à jour de la prochaine action du walker
        """
        self.move_timer += 1
        self.animate_sprite(currentSpeedFactor)
        if self.move_timer > (50 / currentSpeedFactor):
            new_pos = self.path[self.path_index]
            # Mise à jour de la position sur le plateau
            self.path_index += 1
            if self.path_index >= len(self.path) - 1:
                self.target.structure.becomeAHouse()
                self.delete()
            else :
                self.chariot.change_tile((self.case.x, self.case.y))
                self.change_tile(new_pos)
                self.move_timer = 0

class Chariot(Walker):
    def __init__(self, case, plateau, owner, name=""):
        super().__init__(case, plateau, name)
        self.owner = owner
        self.direction = self.owner.direction

class Engineer(Walker):
    def __init__(self, case, plateau, workplace, name="Plebius Prepus", rest = 0, ttw = ttwmax, action = 1, direction = 1, path = [], path_index = 0):
        super().__init__(case, plateau, name, ttw, action, direction, path, path_index)
        self.workplace = workplace
        self.rest = rest
        self.workplace.walker = self

    def delete(self):
        super().delete()
        self.workplace.walker = None

    def reduceRisk(self):
        x_min = self.case.x - 2
        if x_min < 0 : x_min = 0
        x_max = self.case.x + 3
        if x_max > self.plateau.nbr_cell_x : x_max = self.plateau.nbr_cell_x
        y_min = self.case.y - 2
        if y_min < 0 : y_min = 0
        y_max = self.case.y + 3
        if y_max > self.plateau.nbr_cell_y : y_max = self.plateau.nbr_cell_y

        for i in range(x_min, x_max):
            for j in range(y_min, y_max):
                if self.plateau.map[i][j].getStructure() and self.plateau.map[i][j].structure not in self.plateau.cityHousingSpotsList:
                    self.plateau.map[i][j].structure.set_collapseRisk(0)
    
    def update(self, currentSpeedFactor):
        """
        Mise à jour de la prochaine action du walker
        """
        self.move_timer += 1
        self.animate_sprite(currentSpeedFactor)

        if self.move_timer > (50 / currentSpeedFactor):
            if self.ttw > 0:
                new_pos = self.random_path()

                self.ttw -= 1
                if self.ttw == 0:
                    self.create_path(self.case_de_depart)
            else :
                new_pos = self.path[self.path_index]
                # Mise à jour de la position sur le plateau
                self.path_index += 1
                # On supprime le walker si la destination a été atteint
                if self.path_index >= len(self.path) - 1:
                    self.rest = 1
            self.change_tile(new_pos)
            self.reduceRisk()
            if self.rest:
                self.delete()
            self.move_timer = 0

class Prefet(Walker):
    def __init__(self, case, plateau, workplace, name="Plebius Prepus", rest = 0, ttw = ttwmax, action = 1, direction = 1, target = None, path = [], path_index = 0):
        super().__init__(case, plateau, name, ttw, action, direction, path, path_index)
        self.workplace = workplace
        self.rest = rest
        self.workplace.walker = self
        self.throw_timer = 0
        self.target = target

    
    def delete(self):
        super().delete()
        self.workplace.walker = None

    def reduceRisk(self):
        x_min = self.case.x - 2
        if x_min < 0 : x_min = 0
        x_max = self.case.x + 3
        if x_max > self.plateau.nbr_cell_x : x_max = self.plateau.nbr_cell_x
        y_min = self.case.y - 2
        if y_min < 0 : y_min = 0
        y_max = self.case.y + 3
        if y_max > self.plateau.nbr_cell_y : y_max = self.plateau.nbr_cell_y

        for i in range(x_min, x_max):
            for j in range(y_min, y_max):
                if self.plateau.map[i][j].getStructure() and self.plateau.map[i][j].structure not in self.plateau.cityHousingSpotsList:
                    self.plateau.map[i][j].structure.set_fireRisk(0)

    def update(self, currentSpeedFactor):
        """
        Mise à jour de la prochaine action du walker
        """
        self.move_timer += 1
        self.animate_sprite(currentSpeedFactor)
        if self.move_timer > (50 / currentSpeedFactor):
            match(self.action):
                case 1 : #Ronde
                    #Déplacement
                    if self.ttw > 0:    #Déplacement aléatoire
                        new_pos = self.random_path()

                        self.ttw -= 1
                        if self.ttw == 0:
                            self.create_path(self.case_de_depart)
                    else :              #Retour à la préfecture
                        new_pos = self.path[self.path_index]
                        # Mise à jour de la position sur le plateau
                        self.path_index += 1
                        # On supprime le walker si la destination a été atteint
                        if self.path_index >= len(self.path) - 1:
                            self.rest = 1
                    self.change_tile(new_pos)
                    self.reduceRisk()
                    if self.rest:
                        self.delete()

                    #Check s'il y a un feu
                    if len(self.plateau.burningBuildings) > 0:
                        self.target = random.choice(self.plateau.burningBuildings)
                        self.create_path(self.target.case)
                        self.set_action(2)

                case 2 : #Se dirige vers un feu
                    if self.target in self.plateau.burningBuildings:
                        new_pos = self.path[self.path_index]
                        self.path_index += 1
                        if self.path_index >= len(self.path) - 2:
                            self.set_action(3)
                            self.throw_timer = 0
                        self.change_tile(new_pos)
                        self.reduceRisk()
                    else:
                        self.set_action(1)
                case 3 : #Eteint un feu
                    if self.throw_timer < 3:
                        self.throw_timer += 1
                    else :
                        if self.target in self.plateau.burningBuildings:
                            self.target.off()
                        if len(self.plateau.burningBuildings) > 0:
                            self.target = random.choice(self.plateau.burningBuildings)
                            self.create_path(self.target.case)
                            self.set_action(2)
                        else :
                            self.create_path(self.case_de_depart)
                            self.ttw = 0
                            self.set_action(1)
            self.move_timer = 0
    

class CartPusher(Walker):
    def __init__(self, case, plateau, workplace, name="Plebius Prepus", mode = 0, rest = 0, ttw = ttwmax, action = 1, direction = 1, target = None, path = [], path_index = 0):
        super().__init__(case, plateau, name, ttw, action, direction, path, path_index)
        self.workplace = workplace
        self.rest = rest
        self.workplace.walker = self
        self.mode = mode
        self.cart = Cart(self.plateau.map[self.case.x][self.case.y], self.plateau, self)
        self.findGranary()

    
    def delete(self):
        super().delete()
        self.workplace.walker = None
        self.cart.delete()
    
    def findGranary(self):
        self.path_index = 0
        self.path = []
        self.granary = None
        for s in self.plateau.structures :
            if s.desc == "Granary" and s.storedWheat < s.storedWheatMax:
                x = s.case.x
                y = s.case.y

                grid = Grid(matrix=self.plateau.collision_matrix)

                start = grid.node(self.case.x, self.case.y)
                end = grid.node(x, y)
                if start == end :
                    newPath = [(x, y)]
                else :

                    finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
                    newPath, runs = finder.find_path(start, end, grid)
                if newPath and len(newPath) < len(self.path) or not self.path:
                    self.path = newPath.copy()
                    self.granary = s.case
    
    def update(self, currentSpeedFactor):
        self.move_timer += 1
        if self.mode != 1 and self.granary:
            self.animate_sprite(currentSpeedFactor)
        if self.move_timer > (50 / currentSpeedFactor):
            #Aller vers un grenier
            if self.mode == 0 :
                if self.granary:
                    new_pos = self.path[self.path_index]
                    # Mise à jour de la position sur le plateau
                    self.path_index += 1

                    if self.path_index >= len(self.path) - 3:
                        self.mode = 1
                    self.change_tile((self.cart.case.x, self.cart.case.y))
                    self.cart.change_tile(new_pos)
                else :
                    self.findGranary()

            #Livrer les ressources
            elif self.mode == 1:
                if self.granary.structure  and self.granary.structure.desc == "Granary":
                    if self.granary.structure.storedWheat < self.granary.structure.storedWheatMax:
                        self.granary.structure.storedWheat += 100
                        if self.granary.structure.storedWheat > self.granary.structure.storedWheatMax:
                            self.granary.structure.storedWheat = self.granary.structure.storedWheatMax
                        self.mode = 2
                        self.cart.action = 1
                        self.create_path(self.case_de_depart)
                    else :
                        self.mode = 2
                else :
                    self.mode = 2
            #Rentre à la ferme
            elif self.mode == 2:
                new_pos = self.path[self.path_index]
                # Mise à jour de la position sur le plateau
                self.path_index += 1
                # On supprime le walker si la destination a été atteint
                if self.path_index >= len(self.path) - 1:
                    self.rest = 1
                self.change_tile((self.cart.case.x, self.cart.case.y))
                self.cart.change_tile(new_pos)
                if self.rest:
                    self.delete()
            self.move_timer = 0
                


class Cart(Walker):

    def __init__(self, case, plateau, owner, name=""):
        super().__init__(case, plateau, name)
        self.owner = owner
        self.direction = self.owner.direction
        if self.owner.mode == 0:
            self.action = 2
        else:
            self.action = 1

class MarketTrader(Walker):
    def __init__(self, case, plateau, workplace, mode, wheat, name="Plebius Prepus", rest = 0, ttw = ttwmax, action = 1, direction = 1, path = [], path_index = 0):
        super().__init__(case, plateau, name, ttw, action, direction, path, path_index)
        self.workplace = workplace
        self.rest = rest
        self.wheat = wheat
        self.mode = mode #1 = aller chercher du blé au grenier. #2 = aller distribuer du blé aux maisons
        if self.mode == 1:
            self.findGranary()
            self.workplace.transporter = self
        if self.mode == 2:
            self.workplace.giver = self

    def delete(self):
        super().delete()
        if self.mode == 1:
            self.workplace.transporter = None
        if self.mode == 2:
            self.workplace.giver = None

    def findGranary(self):
        self.path_index = 0
        self.path = []
        self.granary = None
        for s in self.plateau.structures :
            if s.desc == "Granary" and s.storedWheat > 0:
                x = s.case.x
                y = s.case.y

                grid = Grid(matrix=self.plateau.collision_matrix)

                start = grid.node(self.case.x, self.case.y)
                end = grid.node(x, y)
                if start == end :
                    newPath = [(x, y)]
                else :

                    finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
                    newPath, runs = finder.find_path(start, end, grid)
                if len(newPath) > len(self.path):
                    self.path = newPath.copy()
                    self.granary = s.case
    
    def distribFood(self):
        if self.wheat >= 5:
            x_min = self.case.x - 2
            if x_min < 0 : x_min = 0
            x_max = self.case.x + 3
            if x_max > self.plateau.nbr_cell_x : x_max = self.plateau.nbr_cell_x
            y_min = self.case.y - 2
            if y_min < 0 : y_min = 0
            y_max = self.case.y + 3
            if y_max > self.plateau.nbr_cell_y : y_max = self.plateau.nbr_cell_y

            for i in range(x_min, x_max):
                for j in range(y_min, y_max):
                    if self.plateau.map[i][j].getStructure() and self.plateau.map[i][j].structure in self.plateau.cityHousesList:
                        if self.plateau.map[i][j].structure.wheat < self.plateau.map[i][j].structure.wheatMax:
                            self.wheat -= 5
                            self.plateau.map[i][j].structure.wheat += 5
                            if self.plateau.map[i][j].structure.wheat > self.plateau.map[i][j].structure.wheatMax:
                                self.plateau.map[i][j].structure.wheat = self.plateau.map[i][j].structure.wheatMax
    
    def update(self, currentSpeedFactor):
        """
        Mise à jour de la prochaine action du walker
        """
        self.move_timer += 1
        self.animate_sprite(currentSpeedFactor)

        if self.move_timer > (50 / currentSpeedFactor):
            self.move_timer = 0
            if self.ttw > 0:
                match(self.mode):
                    case 1 :
                        if self.granary:
                            new_pos = self.path[self.path_index]

                            self.path_index += 1

                            if self.path_index >= len(self.path) - 3:
                                if self.granary.structure and self.granary.structure.desc == "Granary":
                                    if self.granary.structure.storedWheat >= 100 :
                                        self.wheat += 100
                                        self.granary.structure.storedWheat -= 100
                                    else:
                                        self.wheat = self.granary.structure.storedWheat
                                        self.granary.structure.storedWheat = 0
                                self.ttw = 0
                                self.create_path(self.case_de_depart)
                            self.change_tile(new_pos)
                        else :
                            self.findGranary()
                    case 2 :
                        new_pos = self.random_path()

                        self.ttw -= 1
                        if self.ttw == 0:
                            self.create_path(self.case_de_depart)
                        self.change_tile(new_pos)
                        self.distribFood()
            else :  
                new_pos = self.path[self.path_index]
                self.path_index += 1
                if self.path_index >= len(self.path) - 1:
                    self.rest = 1
                self.change_tile(new_pos)
                self.distribFood()
                if self.rest:
                    self.workplace.storedWheat += self.wheat
                    self.delete()