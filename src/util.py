import os
import time
import sys

def slowprint(text: str, interval = 0.075, end="\n") -> None:
    punctuation = "!,.?"
    for ch in text:
        print(ch, end="")
        sys.stdout.flush()

        time.sleep(interval * (2 if ch in punctuation else 1))

    print(end=end)

def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def goto(x, y):
    print("\033[%d;%dH" % (y, x))
