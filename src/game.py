import os
import sys
import loader
import menu
import util
import json
import random
import math

from colorama import Fore, Back, Style

FOOD_UNITS_PER_SURVIVOR = 0.5
DRNK_UNITS_PER_SURVIVOR = 0.75
WATER_PER_COLLECTOR = 20

gameState = {
    "refugeName": "New Refuge",
    "numSurvivors": 15,
    "numAssigned": 6,
    "foodUnits": 75,
    "waterUnits": 75,

    "isRaining": 0,
    "rainCollectors": 4,

    "numThirsty": 0,
    "numVerThirsty": 0,
    "numExtThirsty": 0,

    "details": {
        "Soldiers": 4,
        "Scavengers": 0,
        "Entertainers": 0,
        "Researchers": 0,
        "Chefs": 2,
    },

    "missions": [],
    
    "season": 1,
    "day": 3,
    "year": 2045,
}

seasons = ["Spring", "Summer", "Autumn", "Winter"]

def newGame():
    global gameState
    util.clear() 

    with open(loader.ASSET_DIR + "default.json", "r") as f:
        gameState = json.loads(f.read())

    with open(loader.ASSET_DIR + "newgame-splash.txt", "r") as f:
        print(f.read())

    print(f"Welcome to {Style.BRIGHT + Fore.GREEN}SURVIVOR{Style.RESET_ALL}!") 
    print()
    print("---- 02 Autumn, 2045 ----")
    print(f"Following the recent outbreak of a zombie-like plague, you were tasked with overseeing a refugee camp. Several months later, there is still no sign of aid. With winter rapidly approaching, and supplies diminishing at an alarming rate, you take initiative and decide that you are finished waiting.")
    print()

    nameChosen = False
    while not nameChosen:
        gameState["refugeName"] = input("What shall you name this refuge? ")

        confirm = input("Are you sure? You will not be able to change this later! [y/N] ")
        if confirm.lower() != "y": continue

        nameChosen = True

    print()
    print(f"---- 03 Autumn, 2045 ----")
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

    loadMenu = menu.Menu([(f, None) for f in files] + [("Return to Main Menu", None)])
    filename = loadMenu.menuSelect()
    
    if filename == "Return to Main Menu": return

    with open(loader.SAVE_DIR + filename, "r") as f:
        gameState = json.loads(f.read())

    gameMenu()

def printGameHeader():
    global gameState

    daysOfFood = int(gameState['foodUnits'] / (FOOD_UNITS_PER_SURVIVOR * gameState['numSurvivors']))
    daysOfWater = int(gameState['waterUnits'] / (DRNK_UNITS_PER_SURVIVOR * gameState['numSurvivors']))
    date = f"{str(gameState['day']).rjust(2, '0')} {seasons[gameState['season']]}, {gameState['year']}"

    statusBar = f"{gameState['numSurvivors']} residents ({gameState['numSurvivors'] - gameState['numAssigned']} unassigned) | ~{daysOfFood} days of food | ~{daysOfWater} days of water"
    print(f"---- {Fore.BLUE + Style.BRIGHT}{date}{Style.RESET_ALL} ------ {Fore.GREEN + Style.BRIGHT}{gameState['refugeName']}{Style.RESET_ALL} ---------------------------")
    print(statusBar)
    print(f"-----" + "-"*len(date) + "--------" + "-"*len(gameState['refugeName']) + "-"*28)

def saveGame():
    gameName = input("Give your save a name: ")

    with open(loader.SAVE_DIR + gameName + '.json', "w") as f:
        f.write( json.dumps(gameState) )

def labourMenu():
    global gameState

    while True:
        util.clear()
        printGameHeader()
        print()

        print("=== Labour Management Menu ===")
        print("Select a labour to assign residents to. Residents will automatically carry out any relevant tasks.")
        print()
        management = menu.Menu([(f"{l} ({n} assigned)", None) for l,n in gameState['details'].items()]
                               + [("Back", None)])

        res = management.menuSelect()

        if res == "Back": return
        res = res.split(" ")[0]
        print(f"{Fore.YELLOW + Style.BRIGHT}", end="")

        maxAssignment = gameState['numSurvivors'] - gameState['numAssigned'] + gameState['details'][res]
        done = False

        while not done:
            inp = input(f"Assign how many people? (Max {maxAssignment}) ")
            try: int(inp)
            except: 
                print(f"Please enter an integer between 0 and {maxAssignment}")
                continue

            if int(inp) < 0 or int(inp) > maxAssignment:
                print(f"Please enter an integer between 0 and {maxAssignment}")
                continue

            gameState['numAssigned'] -= gameState['details'][res]
            gameState['numAssigned'] += int(inp)
            gameState['details'][res] = int(inp)
            done = True

def killAmount(n):
    global gameState
    if n == 0: return
    prop = n / gameState['numSurvivors']

    gameState['numSurvivors'] -= n

    for l, v in gameState['details'].items():
        gameState['details'][l] -= math.floor(v * prop)
        gameState['numAssigned'] -= math.floor(v * prop)

def advanceDay():
    global gameState
    util.clear()

    gameState['day'] += 1
    if gameState['day'] == 29:
        gameState['season'] += 1
        gameState['day'] = 1

        print(f"{Fore.GREEN + Style.BRIGHT}It is now {seasons[gameState['season']]}{Style.RESET_ALL}")

    if gameState['season'] == 4:
        gameState['season'] = 0
        gameState['year'] += 1


    gameState['foodUnits'] -= FOOD_UNITS_PER_SURVIVOR * gameState['numSurvivors']
    gameState['waterUnits'] -= DRNK_UNITS_PER_SURVIVOR * gameState['numSurvivors']

    if gameState['isRaining']:
        waterCollected = WATER_PER_COLLECTOR * gameState["rainCollectors"]
        print(f'{Fore.BLUE + Style.BRIGHT}Your rain collectors have collected {waterCollected} units of water.{Style.RESET_ALL}')
        gameState['waterUnits'] += waterCollected

    if gameState['foodUnits'] < 0: gameState['foodUnits'] = 0
    if gameState['waterUnits'] < 0: gameState['waterUnits'] = 0

    if gameState['waterUnits'] < DRNK_UNITS_PER_SURVIVOR * gameState['numSurvivors']:
        if gameState['numExtThirsty'] != 0:
            print(f"{Fore.RED + Style.BRIGHT}{int(gameState['numExtThirsty'] + 0.5)} residents have died of thirst.{Style.RESET_ALL}")

        killAmount(int(gameState['numExtThirsty'] + 0.5))
        gameState['numExtThirsty'] = gameState['numVerThirsty']
        gameState['numVerThirsty'] = gameState['numThirsty']

        defficiency = DRNK_UNITS_PER_SURVIVOR * gameState['numSurvivors'] - gameState['waterUnits']
        survivorsNotGettingDrink = defficiency / DRNK_UNITS_PER_SURVIVOR

        gameState['numThirsty'] = survivorsNotGettingDrink - gameState['numExtThirsty'] - gameState['numVerThirsty']
        print(f"{Fore.YELLOW}You do not have enough water. ({int(gameState['numThirsty'] + 0.5)} thirsty, {int(gameState['numVerThirsty'] + 0.5)} very thirsty, {int(gameState['numExtThirsty'] + 0.5)} extremely thirsty){Style.RESET_ALL}")
    else:
        gameState['numThirsty'] = 0
        gameState['numVerThirsty'] = 0
        gameState['numExtThirsty'] = 0

    if gameState['foodUnits'] < FOOD_UNITS_PER_SURVIVOR * gameState['numSurvivors']:
        if gameState['numExtHungry'] != 0:
            print(f"{Fore.RED + Style.BRIGHT}{int(gameState['numExtHungry'] + 0.5)} residents have died of hunger.{Style.RESET_ALL}")

        killAmount(int(gameState['numExtHungry'] + 0.5))
        gameState['numExtHungry'] = gameState['numExtVerHungry']
        gameState['numExtVerHungry'] = gameState['numVerHungry']
        gameState['numVerHungry'] = gameState['numPreHungry']
        gameState['numPreHungry'] = gameState['numHungry']

        defficiency = FOOD_UNITS_PER_SURVIVOR * gameState['numSurvivors'] - gameState['foodUnits']
        survivorsNotGettingFood = defficiency / FOOD_UNITS_PER_SURVIVOR

        gameState['numHungry'] = survivorsNotGettingFood - gameState['numExtHungry'] - gameState['numExtVerHungry'] - gameState['numVerHungry'] - gameState['numPreHungry']
        print(f"{Fore.YELLOW}You do not have enough food. ({int(gameState['numHungry'] +gameState['numPreHungry']+ 0.5)} hungry, {int(gameState['numVerHungry']+gameState['numExtVerHungry'] + 0.5)} very hungry, {int(gameState['numExtHungry'] + 0.5)} extremely hungry){Style.RESET_ALL}")
    else:
        gameState['numHungry'] = 0
        gameState['numPreHungry'] = 0
        gameState['numVerHungry'] = 0
        gameState['numExtVerHungry'] = 0
        gameState['numExtHungry'] = 0

    if gameState['numSurvivors'] == 0:
        print('==== GAME OVER ====')
        print(f'Despite your best efforts, the members of your refuge have all passed away. As you leave the graveyard you have created, you finally give yourself to the ravenous horde calling your name. And thus, the story of {gameState["refugeName"]} has ended.')
        print()
        input("[Press ENTER to continue] ")
        exit(0)

    rainfallList = []
    if gameState['season'] == 0: rainfallList = [1, 0, 0, 0, 0, 0, 0]
    if gameState['season'] == 1: rainfallList = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    if gameState['season'] == 2: rainfallList = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    if gameState['season'] == 3: rainfallList = [1, 0, 0, 0, 0]

    gameState['isRaining'] = random.choice(rainfallList)
    if gameState['isRaining']: print(f"{Fore.BLUE + Style.BRIGHT}It has started to rain.{Style.RESET_ALL}")

    print(f"{Fore.YELLOW + Style.BRIGHT}A new day has dawned.{Style.RESET_ALL}")
    input("[Press ENTER to continue] ")

def gameMenu():
    global gameState

    while True:
        util.clear()
        printGameHeader()
        print()

        gameMenu = menu.Menu([
            ("Manage Labour", labourMenu),
            ("Next Day", advanceDay),
            ("Save Game", saveGame),
            ("Main Menu", None),
        ])

        if gameMenu.menuSelect() == "Main Menu": return
