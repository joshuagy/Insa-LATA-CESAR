# Constant file

cell_size = 30

# Scale to redimension the sprites
SCL = 1/2 

#Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# State machine constants for the StateMachine class below
STATE_INTRO_SCENE = 1
STATE_MENU = 2
STATE_HELP = 3
STATE_QUIT = 4
STATE_PLAY = 5
STATE_SAVE_SCENE = 6


# ARGENT :
START_TREASURY = 5000 # Argent au début du jeu
# Coût des différentes structures :
PREFECTURE_COST = 50
ENGINEERPOST_COST = 70
HOUSE_COST = 10
DESTRUCTION_COST = 2
WELL_COST = 10
ROAD_COST = 4
MARKET_COST = 20
GRANARY_COST = 100
WHEATFARM_COST = 50
TEMPLE_COST = 100
SENATE_COST = 500


list_of_collision = ["tree", "water", "rock", "sign"]
list_of_undestructible = ["water", "rock", "sign"]
list_of_flammable_structures = ["EngineerPost", "SmallTent", "LargeTent", "SmallTent2", "LargeTent2", "WheatFarm", "Market", "Granary"]
list_of_brittle_structures = ["Prefecture", "WheatFarm", "Market", "Granary"]

#DESIRABILITY
#Housing :
smalltentd = [-3,-2,-1,0,0,0]
largetentd = [-3,-2,-1,0,0,0]
smallshackd = [-2,-1,0,0,0,0]
largeshackd = [-2, -1, 0,0,0]
#Security :
prefectured = [-2,-1,0,0,0]
#Administrative :
senated = [8,8,7,7,6,6]
#Religion :
templed = [4,4,3,3,2,2]
#Water :
welld =[-1,0,0,0,0]
#Engineering :
enginpostd = [0,0,0,0,0]



desirabilityDict = {"SmallTent" : smalltentd, "LargeTent" : largetentd, "SmallShack" : smallshackd, "Senate" : senated,
"LargeShack" : largeshackd, "Prefecture" : prefectured, "SmallTemple" : templed, "Well" : welld, "EngineerPost" : enginpostd,
}