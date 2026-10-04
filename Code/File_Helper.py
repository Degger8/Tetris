import os
import csv

current_dir = os.path.dirname(__file__)
directory_path_file = current_dir + "/../Resources/Highscores.csv"
highscores = 3

def start():
    global directory_path_file, highscores

    in_highscores = read()
    if highscores > len(in_highscores):
        add = highscores - len(in_highscores)
        print(add)
        if add < 3:
            with open(directory_path_file, "a") as file:
                file.write("".join([",0"] * add))
        else:
            with open(directory_path_file, "a") as file:
                file.write(",".join(["0"] * add))

def read():
    global directory_path_file

    numbers_all = []
    with open(directory_path_file, "r") as file:
        data = csv.reader(file)
        for i in data:
            txt = ",".join(i)
            numbers = txt.split(",")
            for k in range(len(numbers)):
                numbers_all.append(numbers[k])
    return numbers_all

def write_replace(file_content):
    global directory_path_file, highscores

    with open(directory_path_file, "w") as file:
        for i in range(highscores):
            file.write(str(file_content[i]))
            if i + 1 < highscores:
                file.write(",")

def set_score(score):
    global directory_path_file

    start()
    file_content = read()

    index = -1
    for i in range(len(file_content)):
        found = False
        if int(file_content[i]) < score:
            found = True
        
        if found:
            index = i
            break

    if index >= 0:
        i = index
        former_content = file_content.copy()
        while i < len(file_content):
            if i + 1 < highscores:
                file_content[i + 1] = former_content[i]
            
            i = i + 1

        file_content[index] = score
        write_replace(file_content)

set_score(0)