import json
import random
import matplotlib.pyplot as plt
from datetime import datetime

foxes = 20    #DEFAULT POPULATION
rabbits = 60  #DEFAULT POPULATION
bornraterabbit = 7       # 1 to 7  EASY
bornratefox =     10      # 1 to 10 HARDER
dayage = 25     #DEFAULT LIFE EXPECTANCY IN DAYS

DAYS = 0
timeMultiplier = 100 #STANDART

def addFox():
    global rabbits
    global foxes
    if random.randint(0, bornratefox) == 1 and rabbits > 0:
        foxes += 1
        rabbits -= 1

def addRabbit():
    global rabbits
    if random.randint(0, bornraterabbit) == 1:
        rabbits += 1

def updateeco():
    global DAYS
    DAYS += 1
    addRabbit()
    addFox()
    update_birthdays()
    replace_dead_animals()

def printeco():
    print("\rBUNNYS: "+str(rabbits)+ "      FOXES: "+str(foxes)+"      DAY: "+str(DAYS)+"   |  ", end="   ")

def update_birthdays():
    with open("data.json", "r") as file:
        data = json.load(file)
    
    data["birthdays"] = {k: data["birthdays"][k] + 1 for k in data["birthdays"]}
    
    with open("data.json", "w") as file:
        json.dump(data, file)

def replace_dead_animals():
    global foxes, rabbits
    with open("data.json", "r") as file:
        data = json.load(file)
    
    for animal in list(data["birthdays"]):
        if data["birthdays"][animal] > dayage:
            if animal == "foxes":
                if foxes > 0:
                    foxes -= 1
                    data["birthdays"][animal] = 0
                else:
                    data["birthdays"][animal] = -1
            elif animal == "rabbits":
                if rabbits > 0:
                    rabbits -= 1
                    data["birthdays"][animal] = 0
                else:
                    data["birthdays"][animal] = -1
        if data["birthdays"][animal] == -1:
            if animal == "foxes":
                rabbits += 10
                foxes = max(0, foxes - 20)  
            elif animal == "rabbits":
                foxes += 10
                rabbits = max(0, rabbits - 20)  
    
    with open("data.json", "w") as file:
        json.dump(data, file)




def livegraph():
    fig, ax = plt.subplots()
    x, y1, y2 = [], [], []
    
    while True:
        printeco()
        updateeco()
        x.append(DAYS)
        y1.append(rabbits)
        y2.append(foxes)
        
        ax.clear()
        ax.plot(x, y1, label="Rabbits")
        ax.plot(x, y2, label="Foxes")
        ax.set_xlabel("Days")
        ax.set_ylabel("Population")
        ax.set_title("Ecosystem Simulation")
        ax.legend()
        
        plt.pause(1 / timeMultiplier)

if __name__ == "__main__":
    data = {"birthdays": {"rabbits": 0, "foxes": 0}}
    with open("data.json", "w") as file:
        json.dump(data, file)

    printeco()
    livegraph()
