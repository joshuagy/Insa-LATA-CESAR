import pygame
import random
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

#à connecter à la variable de constants.py
cell_size = 30

"""
TO DO LIST
- Directions
- Déplacement fluide
- Dab (important)
- Déplacement aléatoire
- TTW
- Spawn à un bâtiment

WIP :
- Animation
"""


class Walker:
    def __init__(self, case, plateau, name = "Plebius Prepus"):
        """
        case : La case de départ sur laquelle est le Walker
        plateau : Le plateau sur lequel est le Walker
        name : Le nom du Walker

        Attributs :
        sprites : Le sprite du Walker
        move_timer : 
        """

        #self.pos = (pos_x, pos_y)
        self.case = case
        self.plateau = plateau
        self.name = name
        
        self.plateau.entities.append(self)  #On ajoute le walker à la liste des entitées présentes sur le plateau
        
        self.sprites = self.load_sprites()
        self.index_sprite = 0

        # pathfinding
        self.move_timer = pygame.time.get_ticks()

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
            if not dest_case.collision:

                #On appelle la fonction Grid de pathfinding en lui passant en paramètre la matrice de collision
                #On pourrait faire pareil avec une matrice de route si nécessaire
                self.grid = Grid(matrix=self.plateau.collision_matrix)

                self.start = self.grid.node(self.case.x, self.case.y)
                self.end = self.grid.node(x, y)

                #On empêche les mouvements diagonaux
                finder = AStarFinder(diagonal_movement=DiagonalMovement.never)

                self.path_index = 0
                self.path, runs = finder.find_path(self.start, self.end, self.grid)
                if self.path :
                    searching_for_path = False

                    #Permet d'observer facilement la map et le walker
                    #print('operations:', runs, 'path length:', len(self.path))
                    #print(self.grid.grid_str(path=self.path, start=self.start, end=self.end))
        

    def change_tile(self, new_tile):
        """
        Changement de case d'un walker.
        """
        self.case = self.plateau.map[new_tile[0]][new_tile[1]]

    
    def update(self):
        """
        Mise à jour de la position du walker 
        """
        now = pygame.time.get_ticks()
        self.index_sprite += 0.5
        if(self.index_sprite >= len(self.sprites)):
            self.index_sprite = 0

        if now - self.move_timer > 1000:
            try : new_pos = self.path[self.path_index]
            except IndexError:
                print(f"IndexError : Path : {self.path}, index : {self.path_index}")
                self.create_path()
                return
            # Mise à jour de la position sur le plateau
            self.change_tile(new_pos)
            self.path_index += 1
            self.move_timer = now       # Note : on pourrait jouer sur le move_timer pour savoir quand un walker doit rentre chez lui?


            # On recréé un path si le dernier a été atteint
            if self.path_index == len(self.path) - 1:
                self.create_path()
    

    def load_sprites(self):
        
        sprites = []

        #HD
        sprites.append(pygame.image.load("image/Walkers/Citizen/HD/Citizen01_00001.png").convert_alpha())
        sprites.append(pygame.image.load("image/Walkers/Citizen/HD/Citizen01_00009.png").convert_alpha())
        sprites.append(pygame.image.load("image/Walkers/Citizen/HD/Citizen01_00017.png").convert_alpha())
        sprites.append(pygame.image.load("image/Walkers/Citizen/HD/Citizen01_00025.png").convert_alpha())
        sprites.append(pygame.image.load("image/Walkers/Citizen/HD/Citizen01_00033.png").convert_alpha())
        sprites.append(pygame.image.load("image/Walkers/Citizen/HD/Citizen01_00041.png").convert_alpha())
        sprites.append(pygame.image.load("image/Walkers/Citizen/HD/Citizen01_00049.png").convert_alpha())
        sprites.append(pygame.image.load("image/Walkers/Citizen/HD/Citizen01_00057.png").convert_alpha())
        sprites.append(pygame.image.load("image/Walkers/Citizen/HD/Citizen01_00065.png").convert_alpha())
        sprites.append(pygame.image.load("image/Walkers/Citizen/HD/Citizen01_00073.png").convert_alpha())
        sprites.append(pygame.image.load("image/Walkers/Citizen/HD/Citizen01_00081.png").convert_alpha())
        sprites.append(pygame.image.load("image/Walkers/Citizen/HD/Citizen01_00089.png").convert_alpha())


        for i in range(12):
            sprites[i] = pygame.transform.scale(sprites[i], (sprites[i].get_width() / 2, sprites[i].get_height() / 2))
        
        return sprites