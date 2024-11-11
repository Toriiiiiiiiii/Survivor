import loader
import menu
import game
import util

def mainmenu():
    util.clear()

    with open(loader.ASSET_DIR + "title-splash.txt", "r") as f:
        print(f.read())

    mainMenu = menu.Menu([
        ("New Game", game.newGame),
        ("Quit", quit)
    ])

    mainMenu.menuSelect()


if __name__ == "__main__":
    mainmenu()