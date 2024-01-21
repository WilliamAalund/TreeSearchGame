from MonsterClasses import HP, MAX_HP

 
game_on_calculator = False
force_game_in_terminal = True # Will force the game to run in terminal even if on calculator

def get_platform():
    global game_on_calculator
    try:
        import ti_system # This will produce a warning if not running on a TI calculator
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
        print("Expand your terminal size for a better experience. PLEASE READ THE DOCUMENTATION BEFORE PLAYING!")
        generic_input()
    else:
        print("Expand your terminal size for a better experience. \33[31mPLEASE READ THE DOCUMENTATION BEFORE PLAYING!\33[0m\n")
        uinp = generic_input("Welcome to Pokemini!", "start", "documentation", "quit")
        if uinp == 0:
            return 0
        elif uinp == 1:
            return 1
        elif uinp == 2:
            return 2

def generic_continue():
    if using_calculator_menus():
        print("Press z to continue")
        generic_input()
    else:
        uinp = ''
        while uinp != 'z':
            uinp = input("Press z to continue. { z: continue }: ")

def generic_input(input_message = "Enter input { ", action_1 = "continue", action_2 = "quit", action_3 = "", action_4 = "", action_5 = "", action_6 = "", action_7 = ""):
    if using_calculator_menus():
        return input()
    else: # Case where not on calculator, or force_game_in_terminal is True
        valid_keys = []
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
            valid_keys.append("z")
        if action_2 != "":
            print(", x: " + action_2, end="")
            valid_keys.append("x")
        if action_3 != "":
            print(", c: " + action_3, end="")
            valid_keys.append("c")
        if action_4 != "":
            print(", v: " + action_4, end="")
            valid_keys.append("v")
        if action_5 != "":
            print(", b: " + action_5, end="")
            valid_keys.append("b")
        if action_6 != "":
            print(", n: " + action_6, end="")
            valid_keys.append("n")
        if action_7 != "":
            print(", m: " + action_7, end="")
            valid_keys.append("m")
        print(" }: ", end="")
        uinp = ""
        while uinp not in valid_keys:
            uinp = input()
            if uinp not in valid_keys:
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

def switch_menu(input_message = "Choose a Pokemon.", team_members=[], valid_switch_indices=[], Back = True): # Team members is a list of Monster objects
    uinp = -1
    if Back:
        able_to_back = "Back"
    else:
        able_to_back = ""
    if using_calculator_menus():
        return input()
    else: # Case where not on calculator, or force_game_in_terminal is True
        in_menu = True
        while in_menu:
            switch_input = -1
            input_message = input_message
            if len(valid_switch_indices) == 6:
                switch_input = generic_input(input_message, team_members[0].name, team_members[1].name, team_members[2].name, team_members[3].name, team_members[4].name, team_members[5].name, able_to_back)
            elif len(valid_switch_indices) == 5:
                switch_input = generic_input(input_message, team_members[0].name, team_members[1].name, team_members[2].name, team_members[3].name, team_members[4].name, able_to_back)
            elif len(valid_switch_indices) == 4:
                switch_input = generic_input(input_message, team_members[0].name, team_members[1].name, team_members[2].name, team_members[3].name, able_to_back)
            elif len(valid_switch_indices) == 3:
                switch_input = generic_input(input_message, team_members[0].name, team_members[1].name, team_members[2].name, able_to_back)
            elif len(valid_switch_indices) == 2:
                switch_input = generic_input(input_message, team_members[0].name, team_members[1].name, able_to_back)
            elif len(valid_switch_indices) == 1:
                switch_input = generic_input(input_message, team_members[0].name, able_to_back)
            else:
                print("You have no other Pokemon to switch to.")
                in_menu = False
            if Back: # Back indicates that function is being used in a larger menu
                in_menu = False
            else:
                if switch_input in range(len(valid_switch_indices)):
                    uinp = valid_switch_indices[int(switch_input)] + 4
                    in_menu = False
                    return uinp
        return switch_input

def battle_menu_input(active_member_moves, team_members, valid_switch_indices = [], wild_encounter = False):
    if using_calculator_menus():
        return input()
    else: # Case where not on calculator, or force_game_in_terminal is True
        uinp = -1
        in_menu = True
        while in_menu:
            if wild_encounter:
                minp = generic_input("What will you do?", "Attack", "Pokemon", "Bag", "Run")
            else:
                minp = generic_input("What will you do?", "Attack", "Pokemon", "Run")
            if minp == 0: # Attack
                attack_input = -1
                input_message = "Choose a move." # FIXME: Implement a way to show PP
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
                input_message = "Choose a Pokemon."
                switch_input = switch_menu(input_message, team_members, valid_switch_indices, True)
                if switch_input in range(len(valid_switch_indices)):
                    print(team_members[switch_input])
                    affirm_input = generic_input("Switch to " + team_members[switch_input].name + "?", "Yes", "No")
                    if affirm_input == 0:
                        uinp = valid_switch_indices[int(switch_input)] + 4
                        in_menu = False
                    else:
                        uinp = -1
                # List team, then list options about team
            elif minp == 2: # Run or bag
                if wild_encounter: # Bag
                    uinp = 11
                    in_menu = False
                else: # Run
                    uinp = 10
                    in_menu = False
            elif minp == 3: # Run with wild menu
                uinp = 10
                in_menu = False
        print()
        return uinp

def battle_scene(player_team, ai_team):
    print(player_team.name + ": ", end="")
    print("Lv." + str(player_team.get_member(player_team.active_member_index).level) + " ", end="")
    print(player_team.get_member(player_team.active_member_index).name, end="")
    print(" " + player_team.get_member(player_team.active_member_index).get_status_string() if player_team.get_member(player_team.active_member_index).get_status_string() else "", end="")
    player_percent_health = round((player_team.get_member(player_team.active_member_index).get_stat(HP) / player_team.get_active_member().get_stat(MAX_HP)) * 100, 1)
    if player_percent_health > 50:
        # Color text green
        print("\33[32m HP: " + str(player_team.get_member(player_team.active_member_index).get_stat(HP)) + "/" + str(player_team.get_active_member().get_stat(MAX_HP)), end="")
        print(" (" + str(player_percent_health) + " %)", end="\033[0m")
    elif player_percent_health > 25:
        # Color text yellow
        print("\33[33m HP: " + str(player_team.get_member(player_team.active_member_index).get_stat(HP)) + "/" + str(player_team.get_active_member().get_stat(MAX_HP)), end="")
        print(" (" + str(player_percent_health) + " %)", end="\033[0m")
    else:
        # Color text red
        print("\33[31m HP: " + str(player_team.get_member(player_team.active_member_index).get_stat(HP)) + "/" + str(player_team.get_active_member().get_stat(MAX_HP)), end="")    
        print(" (" + str(player_percent_health) + " %)", end="\033[0m")
    number_of_pokemon = player_team.get_number_of_members_to_switch_to() + 1
    number_of_enemy_pokemon = ai_team.get_number_of_members_to_switch_to() + 1
    if number_of_pokemon > number_of_enemy_pokemon:
        # Text color green
        print(" |\33[32m" + str(number_of_pokemon) + "v" + str(number_of_enemy_pokemon) + "\033[0m| ", end="")
    elif number_of_pokemon < number_of_enemy_pokemon:
        # Text color red
        print(" |\33[31m" + str(number_of_pokemon) + "v" + str(number_of_enemy_pokemon) + "\033[0m| ", end="")
    else:
        # Text color white (default)
        print(" |" + str(number_of_pokemon) + "v" + str(number_of_enemy_pokemon) + "| ", end="")
    print(ai_team.name + ": ", end="")
    print("Lv." + str(ai_team.get_member(ai_team.active_member_index).level) + " ", end="")
    print(ai_team.get_member(ai_team.active_member_index).name, end="")
    print(" " + ai_team.get_member(ai_team.active_member_index).get_status_string() if ai_team.get_member(ai_team.active_member_index).get_status_string() else "", end="")
    ai_hp_percentage = round((ai_team.get_member(ai_team.active_member_index).get_stat(HP) / ai_team.get_active_member().get_stat(MAX_HP)) * 100, 1)
    if ai_hp_percentage > 50:
        print("\33[32m HP: " + str(ai_hp_percentage),"%\033[0m")
    elif ai_hp_percentage > 25:
        print("\33[33m HP: " + str(ai_hp_percentage),"%\033[0m")
    else:
        print("\33[31m HP: " + str(ai_hp_percentage),"%\033[0m")

def starter_menu(name1, name2, name3):
    if using_calculator_menus():
        return input()
    else: # Case where not on calculator, or force_game_in_terminal is True
        starter_choice = generic_input("Choose your starter.", name1, name2, name3)
        return starter_choice


#switch_menu("yyyy",["Charmander", "Squirtle", "Bulbasaur"], [0, 1, 2])
#battle_menu_input(["Tackle", "Scratch", "Growl", "Tail Whip"], ["Charmander", "Squirtle", "Bulbasaur"], [0, 1, 2])