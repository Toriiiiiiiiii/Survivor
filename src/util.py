import os

def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def goto(x, y):
    print("\033[%d;%dH" % (y, x))
