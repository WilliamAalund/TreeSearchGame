game_on_calculator = False
force_game_in_terminal = True # Will force the game to run in terminal even if on calculator

def get_platform():
    global game_on_calculator
    try:
        import ti_system
        print("Running on TI calculator")
        game_on_calculator = True
    except:
        print("Not running on TI calculator")
        game_on_calculator = False
    print("\n")

def using_calculator_menus():
    return game_on_calculator and not force_game_in_terminal

def title_screen():
    if using_calculator_menus():
        print("Welcome to Pokemini!")
        generic_input()
    else:
        uinp = generic_input("Welcome to Pokemini!")
        if uinp == 0:
            print("Player requested to continue")
            return 0
        elif uinp == 1:
            print("Ending game")
            return 1

def generic_input(input_message = "Enter input { ", action_1 = "continue", action_2 = "quit", action_3 = "", action_4 = "", action_5 = "", action_6 = "", action_7 = ""):
    if using_calculator_menus():
        return input()
    else: # Case where not on calculator, or force_game_in_terminal is True
        action_1_available = action_1 != ""
        action_2_available = action_2 != ""
        action_3_available = action_3 != ""
        action_4_available = action_4 != ""
        action_5_available = action_5 != ""
        action_6_available = action_6 != ""
        action_7_available = action_7 != ""
        print(input_message + " { ", end="")
        if action_1 != "":
            print("z: " + action_1, end="")
        if action_2 != "":
            print(", x: " + action_2, end="")
        if action_3 != "":
            print(", c: " + action_3, end="")
        if action_4 != "":
            print(", v: " + action_4, end="")
        if action_5 != "":
            print(", b: " + action_5, end="")
        if action_6 != "":
            print(", n: " + action_6, end="")
        if action_7 != "":
            print(", m: " + action_7, end="")
        print(" }: ", end="")
        uinp = ""
        while uinp not in ["z", "x", "c", "v", "b", "n", "m"]:
            uinp = input()
            if uinp not in ["z", "x", "c", "v", "b", "n", "m"]:
                print("Invalid input. Please try again.")
        if uinp == "z" and action_1_available:
            return 0
        elif uinp == "x" and action_2_available:
            return 1
        elif uinp == "c" and action_3_available:
            return 2
        elif uinp == "v" and action_4_available:
            return 3
        elif uinp == "b" and action_5_available:
            return 4
        elif uinp == "n" and action_6_available:
            return 5
        elif uinp == "m" and action_7_available:
            return 6


def battle_menu_input(active_member_moves, team_members):
    if using_calculator_menus():
        return input()
    else: # Case where not on calculator, or force_game_in_terminal is True
        uinp = -1
        in_menu = True
        while in_menu:
            minp = generic_input("What will you do?", "Attack", "Pokemon", "Run")
            if minp == 0: # Attack
                attack_input = -1
                input_message = "Choose a move."
                if len(active_member_moves) == 4:
                    attack_input = generic_input(input_message, active_member_moves[0], active_member_moves[1], active_member_moves[2], active_member_moves[3], "Back")
                elif len(active_member_moves) == 3:
                    attack_input = generic_input(input_message, active_member_moves[0], active_member_moves[1], active_member_moves[2], "Back")
                elif len(active_member_moves) == 2:
                    attack_input = generic_input(input_message, active_member_moves[0], active_member_moves[1], "Back")
                elif len(active_member_moves) == 1:
                    attack_input = generic_input(input_message, active_member_moves[0], "Back")
                else:
                    print("Error: No moves available")
                if attack_input in range(len(active_member_moves)): # Attack chosen
                    uinp = int(attack_input)
                    in_menu = False
            elif minp == 1: # Pokemon
                switch_input = -1
                input_message = "Choose a Pokemon."
                if len(team_members) == 6:
                    switch_input = generic_input(input_message, team_members[0], team_members[1], team_members[2], team_members[3], team_members[4], team_members[5], "Back")
                elif len(team_members) == 5:
                    switch_input = generic_input(input_message, team_members[0], team_members[1], team_members[2], team_members[3], team_members[4], "Back")
                elif len(team_members) == 4:
                    switch_input = generic_input(input_message, team_members[0], team_members[1], team_members[2], team_members[3], "Back")
                elif len(team_members) == 3:
                    switch_input = generic_input(input_message, team_members[0], team_members[1], team_members[2], "Back")
                elif len(team_members) == 2:
                    switch_input = generic_input(input_message, team_members[0], team_members[1], "Back")
                elif len(team_members) == 1:
                    switch_input = generic_input(input_message, team_members[0], "Back")
                else:
                    print("You have no other Pokemon to switch to.")
                if switch_input in range(len(team_members)):
                    uinp = int(switch_input) + 4
                    in_menu = False
                # List team, then list options about team
            elif minp == 2: # Run
                uinp = 10
                in_menu = False
        return uinp

#battle_menu_input(["Tackle", "Growl", "Tail Whip", "Scratch"], ["Bulbasaur", "Charmander", "Squirtle"])