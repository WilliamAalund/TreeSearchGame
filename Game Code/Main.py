import GameMenus as gm
import GameLogic as gl

def main():
    if not gm.force_game_in_terminal:
        gm.get_platform()
    uinp = gm.title_screen()
    if uinp == 1:
        print("Starting tutorial")
    if uinp == 2:
        return
    elif uinp == 0:
        print("Starting game. Good luck!")
        gl.campaign_game()
        

main() # Run the game