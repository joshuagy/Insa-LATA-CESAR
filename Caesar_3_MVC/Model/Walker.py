import pygame as pg
import random
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

#à connecter à la variable de constants.py
cell_size = 30

class Walker:
    def __init__(self, case, plateau, name = "Plebius"):
        """
        case : La case de départ sur laquelle est le Walker
        plateau : Le plateau sur lequel est le Walker
        name : Le nom du Walker

        Attributs :
        image : Le sprite du Walker
        move_timer : 
        """

        #self.pos = (pos_x, pos_y)
        self.case = case
        self.plateau = plateau
        self.name = name
        
        self.plateau.entities.append(self)  #On ajoute le walker à la liste des entitées présentes sur le plateau
        
        image = pg.image.load("image/Walkers/Citizen/HD/Citizen01_00001.png").convert_alpha()
        self.image = pg.transform.scale(image, (image.get_width() / 2, image.get_height() / 2))

        # pathfinding
        self.plateau.walkers[case.x][case.y] = self
        self.move_timer = pg.time.get_ticks()

        self.create_path()
    
    def create_path(self):
        """
        Création d'un chemin entre la case de départ (la case actuelle), la case finale,
        en prenant en compte les collisions.
        """
        searching_for_path = True
        #Ici on cherche une case de destination de manière aléatoire
        while searching_for_path:
            x = random.randint(0, self.plateau.nbr_cell_x - 1)
            y = random.randint(0, self.plateau.nbr_cell_y - 1)
            dest_case = self.plateau.map[x][y]

            #Si la destination est valide
            if True: #Quand il y aura les collisions : if not dest_tile["collision"]:

                #On appelle la fonction Grid de pathfinding en lui passant en paramètre la matrice de collision
                #On pourrait faire pareil avec une matrice de route si nécessaire
                self.grid = Grid(matrix=self.plateau.collision_matrix)

                self.start = self.grid.node(self.case.x, self.case.y)
                self.end = self.grid.node(x, y)

                #On empêche les mouvements diagonaux
                finder = AStarFinder(diagonal_movement=DiagonalMovement.never)

                self.path_index = 0
                self.path, runs = finder.find_path(self.start, self.end, self.grid)
                searching_for_path = False

    def change_tile(self, new_tile):
        """
        Changement de case d'un walker. On actualise le tableau présent dans le plateau, et la case du walker
        """
        self.plateau.walkers[self.case.x][self.case.y] = None
        self.plateau.walkers[new_tile[0]][new_tile[1]] = self
        self.case = self.plateau.map[new_tile[0]][new_tile[1]]

    
    def update(self):
        """
        Mise à jour de la position du walker 
        """
        now = pg.time.get_ticks()

        if now - self.move_timer > 1000:
            new_pos = self.path[self.path_index]
            # Mise à jour de la position sur le plateau
            self.change_tile(new_pos)
            self.path_index += 1
            self.move_timer = now       # Note : on pourrait jouer sur le move_timer pour savoir quand un walker doit rentre chez lui?


            # On recréé un path si le dernier a été atteint
            if self.path_index == len(self.path) - 1:
                self.create_path()
