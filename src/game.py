import os
import sys
import loader
import menu
import util
import json

from colorama import Fore, Back, Style

FOOD_UNITS_PER_SURVIVOR = 0.5
DRNK_UNITS_PER_SURVIVOR = 0.75

gameState = {
    "refugeName": "New Refuge",
    "numSurvivors": 50,
    "foodUnits": 500,
    "waterUnits": 500,
    
    "season": 1,
    "day": 3,
    "year": 2045,
}

seasons = ["Spring", "Summer", "Autumn", "Winter"]
gameRunning = True

def newGame():
    global gameState
    util.clear() 

    with open(loader.ASSET_DIR + "default.json", "r") as f:
        gameState = json.loads(f.read())

    with open(loader.ASSET_DIR + "newgame-splash.txt", "r") as f:
        print(f.read())

    print(f"Welcome to {Style.BRIGHT + Fore.GREEN}SURVIVOR{Style.RESET_ALL}!") 
    print()
    print("2nd Autumn, 2045")
    print(f"Following the recent outbreak of a zombie-like plague, you were tasked with overseeing a refugee camp. Several months later, there is still no sign of aid. With winter rapidly approaching, and supplies diminishing at an alarming rate, you take initiative and decide that you are finished waiting.")
    print()

    nameChosen = False
    while not nameChosen:
        gameState["refugeName"] = input("What shall you name this refuge? ")

        confirm = input("Are you sure? You will not be able to change this later! [y/N] ")
        if confirm.lower() != "y": continue

        nameChosen = True

    print()
    print(f"3rd Autumn, 2045")
    print(f"In this morning's weekly briefing, you declared to the residents of {Style.BRIGHT + Fore.GREEN}{gameState['refugeName'].upper()}{Style.RESET_ALL} that you were appointing yourself as leader of the camp. While most people accepted this, some were not so eager. Several people attempted to flee, however they were quickly dispatched by the growing hordes outside the gate.")
    print()
    input("[Press ENTER to continue]")

    gameMenu()

def loadGame():
    global gameState
    util.clear()

    with open(loader.ASSET_DIR + "loadgame-splash.txt", "r") as f:
        print(f.read())

    print()

    files = [f for f in os.listdir(loader.SAVE_DIR) if os.path.isfile(os.path.join(loader.SAVE_DIR, f))]

    for index, f in enumerate(files):
        print(f"{index + 1} | {f}")


    option = ""
    validChoice = False

    while not validChoice:
        option = input("> ")

        try: int(option)
        except:
            print(f"Please enter a number within the range 1 - {len(files)}")
            continue

        if int(option) not in range(1, len(files) + 1):
            print(f"Please enter a number within the range 1 - {len(files)}")
            continue

        validChoice = True

    with open(loader.SAVE_DIR + files[int(option) - 1], "r") as f:
        gameState = json.loads(f.read())

    gameMenu()

def printGameHeader():
    global gameState

    print(f"---- {str(gameState['day']).rjust(2, '0')} {seasons[gameState['season']]}, {gameState['year']} ----")
    print(f"Survivors: {gameState['numSurvivors']}")
    print(f"Food:      ~{int(gameState['foodUnits'] / (FOOD_UNITS_PER_SURVIVOR * gameState['numSurvivors']))} Days remaining.")
    print(f"Water:     ~{int(gameState['foodUnits'] / (DRNK_UNITS_PER_SURVIVOR * gameState['numSurvivors']))} Days remaining.")

def saveGame():
    gameName = input("Give your save a name: ")

    with open(loader.SAVE_DIR + gameName + '.json', "w") as f:
        f.write( json.dumps(gameState) )

def mainMenu():
    global gameRunning

    gameRunning = False

def gameMenu():
    global gameState
    global gameRunning
    while gameRunning:
        util.clear()
        printGameHeader()
        print()

        gameMenu = menu.Menu([
            ("Save Game", saveGame),
            ("Main Menu", mainMenu),
        ])

        gameMenu.menuSelect()

    gameRunning = True
