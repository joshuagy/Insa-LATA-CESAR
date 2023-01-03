import pygame
import random
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

"""
TO DO LIST
- Déplacement fluide
- Dab (important)
- Spawn à un bâtiment
- Différentes actions
- Sous classes
"""

ttwmax = 30

class Walker:
    def __init__(self, case, plateau, name = "Plebius Prepus"):
        """
        case : La case de départ sur laquelle est le Walker
        plateau : Le plateau sur lequel est le Walker
        name : Le nom du Walker

        Attributs :
        case_de_départ : La case de spawn du walker
        type : string qui contient le nom de la sous classe
        index_sprite : Permet d'animer le walker
        direction : Permet de connaître la direction dans laquelle il va
        ttw : Durée de la marche aléatoire avant de devoir rentrer au point de départ
        move_timer : stock les tick d'horloge
        """

        self.case = case
        self.case_de_départ = case
        self.plateau = plateau
        self.name = name
        self.type = str(type(self))[21:-2]
        self.action = 1
        
        self.plateau.entities.append(self)  #On ajoute le walker à la liste des entitées présentes sur le plateau

        self.index_sprite = 0
        
        self.direction = 1 # | 1 : North | 2 : East | 3 : South | 4 : West |
        self.ttw = ttwmax

        self.move_timer = pygame.time.get_ticks()


    def delete(self) :
        self.plateau.entities.remove(self)
        del self

    
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
        self.case = self.plateau.map[new_tile[0]][new_tile[1]]


class Citizen(Walker):
    def __init__(self, case, plateau, name="Plebius Prepus"):
        super().__init__(case, plateau, name)
    
    def update(self):
        """
        Mise à jour de la prochaine action du walker
        """
        now = pygame.time.get_ticks()
        self.index_sprite += 0.5
        if(self.index_sprite >= len(self.plateau.image_walkers[self.type][self.action][self.direction])):
            self.index_sprite = 0

        """if now - self.move_timer > 500:
            if self.ttw > 0:
                new_pos = self.random_path()

                self.ttw -= 1
                if self.ttw == 0:
                    self.create_path(self.case_de_départ)
            else :
                new_pos = self.path[self.path_index]
                # Mise à jour de la position sur le plateau
                self.path_index += 1
                # On retourne en mode aléatoire si la destination a été atteint
                if self.path_index >= len(self.path) - 1:
                    self.ttw = ttwmax
            self.change_tile(new_pos)
            self.move_timer = now"""

class Prefet(Walker):
    def __init__(self, case, plateau, name="Plebius Prepus"):
        super().__init__(case, plateau, name)
    
    def update(self):
        """
        Mise à jour de la prochaine action du walker
        """
        now = pygame.time.get_ticks()
        self.index_sprite += 0.5
        if(self.index_sprite >= len(self.plateau.image_walkers[self.type][self.action][self.direction])):
            self.index_sprite = 0

        if now - self.move_timer > 500:
            if self.ttw > 0:
                new_pos = self.random_path()

                self.ttw -= 1
                if self.ttw == 0:
                    self.create_path(self.case_de_départ)
            else :
                new_pos = self.path[self.path_index]
                # Mise à jour de la position sur le plateau
                self.path_index += 1
                # On retourne en mode aléatoire si la destination a été atteint
                if self.path_index >= len(self.path) - 1:
                    self.ttw = ttwmax
            self.change_tile(new_pos)
            self.move_timer = now