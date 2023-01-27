import os

Case = "Water"

# specify the directory containing the files to be renamed
directory = f".\image\Case\{Case}"


files = os.listdir(directory)

# loop through the files and rename them
i = 0
for file in files:
    # get the current file name and extension
    filename, file_extension = os.path.splitext(file)

    # rename the file
    new_filename = f"{Case}{i}{file_extension}"
    new_dir = f"{directory}"
    os.rename(os.path.join(directory, file), os.path.join(new_dir, new_filename))
    i+=1