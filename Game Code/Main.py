from MonteCarlo import MonteCarloTreeSearch
from GameMenus import *
from MatchClasses import *   

def main():
    print("Program start")
    if not force_game_in_terminal:
        get_platform()
    uinp = title_screen()
    if uinp == 1:
        return
    elif uinp == 0:
        print("Starting game")
        

main() # Run the game