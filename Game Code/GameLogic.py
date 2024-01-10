from GameClasses import *
from MonteCarlo import MonteCarloTreeSearch

def test_game():
    player_team = Team("Player")
    ai_team = Team()
    player_team.add_member(Monster2(2, 50))
    ai_team.add_member(Monster2(1, 50))

    match_result = match(player_team, ai_team)
    if match_result:
        print("Player won")

def match(player_team: Team, ai_team: Team, random_ai = False): # Runs a match between two teams. Returns 1 if player won, 0 if AI won
    player_team.active_member_index = 0
    ai_team.active_member_index = 0
    while player_team.has_non_fainted_members() and ai_team.has_non_fainted_members(): # Match loop
        
        print(str(player_team.get_member(player_team.active_member_index).name) + ": " + str(player_team.get_member(player_team.active_member_index).get_stat(HP)) + " | " + str(ai_team.get_member(ai_team.active_member_index).name) + ": "+ str(ai_team.get_member(ai_team.active_member_index).get_stat(HP)))
        uinp = battle_menu_input(player_team.get_member(player_team.active_member_index).get_list_of_moves(), player_team.get_list_of_member_names_to_switch_to())
        if uinp == 10:
            break
        else:
            if random_ai == True:
                list_of_ai_choices = []
                ai_moves = ai_team.get_member(ai_team.active_member_index).get_number_of_moves()
                ai_switches = ai_team.get_list_of_valid_switch_indices()
                for i in range(ai_moves):
                    list_of_ai_choices.append(i)
                for i in ai_switches:
                    list_of_ai_choices.append(i + 4)
                ai_choice = rng.choice(list_of_ai_choices)
            else: # TODO: Implemente MTCS for AI
                current_game_state = GameState(player_team, ai_team)
                ai_choice = MonteCarloTreeSearch(current_game_state).get_best_move()
            turn(player_team, uinp, ai_team, ai_choice)
    # Match over
    if player_team.has_non_fainted_members():
        return 1
    else:
        print("AI wins")
        return 0
    
test_game()