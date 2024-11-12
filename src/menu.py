from colorama import Fore, Style

class Menu:
    def __init__(self, entries: list) -> None:
        self.entries = entries

    def menuSelect(self) -> str:
        nDigits = len( str(len(self.entries) - 1) )
        for index, entry in enumerate(self.entries):
            print(f" {str(index + 1).rjust(nDigits)} | {entry[0]}")

        print()
        option = ""
        validChoice = False

        while not validChoice:
            print(f"{Fore.YELLOW + Style.BRIGHT}", end="")
            option = input("> ")
            print(f"{Style.RESET_ALL}", end="")

            try: int(option)
            except:
                print(f"Please enter a number within the range 1 - {len(self.entries)}")
                continue

            if int(option) not in range(1, len(self.entries) + 1):
                print(f"Please enter a number within the range 1 - {len(self.entries)}")
                continue

            validChoice = True

        entry = self.entries[ int(option) - 1]
        callback = entry[1]
        if not callback: return entry[0]

        callback()
        return entry[0]
