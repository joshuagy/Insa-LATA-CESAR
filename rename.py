import os

Walker = "MarketTrader"
Action = "Walk"

# specify the directory containing the files to be renamed
directory = f".\image\Walkers\{Walker}\{Action}"

# get a list of all files in the directory
files = os.listdir(directory)
os.mkdir(os.path.join(directory, "UpRight"))
os.mkdir(os.path.join(directory, "Right"))
os.mkdir(os.path.join(directory, "DownRight"))
os.mkdir(os.path.join(directory, "Down"))
os.mkdir(os.path.join(directory, "DownLeft"))
os.mkdir(os.path.join(directory, "Left"))
os.mkdir(os.path.join(directory, "UpLeft"))
os.mkdir(os.path.join(directory, "Up"))
# loop through the files and rename them
i = 1
j = 1
for file in files:
    # get the current file name and extension
    filename, file_extension = os.path.splitext(file)

    match(i):

        case 1 : direction = "UpRight"
        case 2 : direction = "Right"
        case 3 : direction = "DownRight"
        case 4 : direction = "Down"
        case 5 : direction = "DownLeft"
        case 6 : direction = "Left"
        case 7 : direction = "UpLeft"
        case 8 : direction = "Up"
    # rename the file
    new_filename = f"{Walker}{Action}{direction}Frame{j}{file_extension}"
    new_dir = f"{directory}\{direction}"
    os.rename(os.path.join(directory, file), os.path.join(new_dir, new_filename))
    i+=1
    if i == 9 :
        j += 1
        i = 1


def water(x, y) :
        index = 0
        if x < self.model.actualGame.nbr_cell_x-1 and y < self.model.actualGame.nbr_cell_y-1:
            if self.model.actualGame.map[x+1][y+1].sprite == "water":
                index += 128 # + 10000000
        if x < self.model.actualGame.nbr_cell_x-1 and y > 0:
            if self.model.actualGame.map[x+1][y-1].sprite == "water":
                index += 64 # + 01000000
        if x > 0 and y < self.model.actualGame.nbr_cell_y-1:
            if self.model.actualGame.map[x-1][y+1].sprite == "water":
                index += 32 # + 00100000
        if x > 0 and y > 0:
            if self.model.actualGame.map[x-1][y-1].sprite == "water":
                index += 16 # + 00010000
        if y < self.model.actualGame.nbr_cell_y-1:
            if self.model.actualGame.map[x][y+1].sprite == "water":
                index += 8 # + 00001000
        if x < self.model.actualGame.nbr_cell_x-1:
            if self.model.actualGame.map[x+1][y].sprite == "water":
                index += 4 # + 00000100
        if y > 0:
            if self.model.actualGame.map[x][y-1].sprite == "water":
                index += 2 # + 00000010
        if x > 0:
            if self.model.actualGame.map[x-1][y].sprite == "water":
                index += 1 # + 00000001
        table_correspondance = {0 : 0}
        index = table_correspondance.get(key=index, default=0)
        self.model.actualGame.map[x][y].indexSprite = table_correspondance[index]