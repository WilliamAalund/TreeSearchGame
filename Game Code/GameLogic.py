from MatchClasses import *
from MonteCarlo import MonteCarloTreeSearch

def test_game(random_ai = False):
    player_team = Team("Player")
    ai_team = Team("Enemy")
    player_team.add_member(Monster(477, 50))
    player_team.add_member(Monster(498, 50))
    player_team.add_member(Monster(501, 50))
    ai_team.add_member(Monster(495, 50))
    ai_team.add_member(Monster(498, 50))
    ai_team.add_member(Monster(501, 50))

    match_result = match(player_team, ai_team, random_ai=random_ai)
    if match_result:
        print("Player won")

def test_game_2(random_ai = False):
    player_team = Team("Player")
    ai_team = Team("Enemy")
    player_team.add_member(Monster(508, 50))
    player_team.add_member(Monster(508, 50))
    player_team.add_member(Monster(508, 50))

    ai_team.add_member(Monster(506, 50))
    ai_team.add_member(Monster(506, 50))
    ai_team.add_member(Monster(506, 50))
    match_result = match(player_team, ai_team, random_ai=random_ai)
    if match_result:
        print("Player won")

def test_game_3(random_ai = False):
    player_team = Team("Player")
    ai_team = Team("Enemy")
    player_team.add_member(Monster(501, 50))
    ai_team.add_member(Monster(498, 50))
    ai_team.add_member(Monster(495, 50))
    match_result = match(player_team, ai_team, random_ai=random_ai)
    if match_result:
        print("Player won")

def test_game_4(random_ai = False):
    player_team = Team("Player")
    ai_team = Team("Enemy")
    player_team.add_member(Monster(501, 50))
    player_team.add_member(Monster(498, 50))
    player_team.add_member(Monster(495, 50))
    ai_team.add_member(Monster(501, 50))
    ai_team.add_member(Monster(498, 50))
    ai_team.add_member(Monster(495, 50))
    match_result = match(player_team, ai_team, random_ai=random_ai)
    if match_result:
        print("Player won")

def test_game_5(random_ai = False):
    # Match between two teams of 1 of the same pokemon
    player_team = Team("Player")
    ai_team = Team("Enemy")
    player_team.add_member(Monster(501, 50))
    ai_team.add_member(Monster(501, 50))
    match_result = match(player_team, ai_team, random_ai=random_ai)
    if match_result:
        print("Player won")
    

def match(player_team: Team, ai_team: Team, random_ai = False): # Runs a match between two teams. Returns 1 if player won, 0 if AI won
    player_team.active_member_index = 0
    ai_team.active_member_index = 0
    while player_team.has_non_fainted_members() and ai_team.has_non_fainted_members(): # Match loop
        if player_team.get_active_member().fainted: # Make player choose a valid new active member
            player_choice = switch_menu(team_members=player_team.get_list_of_member_names_to_switch_to(),valid_switch_indices=player_team.get_list_of_valid_switch_indices(), Back=False) # FIXME: Implement player choice
            switch_after_fainting(player_team, player_choice - 4)
        if ai_team.get_active_member().fainted: # Make AI choose a valid new active member
            current_game_state = GameState(player_team, ai_team)
            if random_ai == True:
                ai_choice = rng.choice(ai_team.get_list_of_valid_switch_indices()) + 4
            else:
                ai_choice = MonteCarloTreeSearch(current_game_state,random_policy=False).get_best_move()
            switch_after_fainting(ai_team, ai_choice - 4)
        print("You: " + str(player_team.get_member(player_team.active_member_index).name) +(" )" if player_team.get_member(player_team.active_member_index).status else "")+ str(player_team.get_member(player_team.active_member_index).status if player_team.get_member(player_team.active_member_index).status else "") + (") " if player_team.get_member(player_team.active_member_index).status else " ") + str(player_team.get_member(player_team.active_member_index).get_stat(HP)) + "/" + str(player_team.get_active_member().get_stat(MAX_HP)) + " | Opponent: " + str(ai_team.get_member(ai_team.active_member_index).name) + " "+ str(ai_team.get_member(ai_team.active_member_index).get_stat(HP)) + "/" + str(ai_team.get_active_member().get_stat(MAX_HP)))
        uinp = battle_menu_input(player_team.get_member(player_team.active_member_index).get_list_of_moves(), player_team.get_list_of_member_names_to_switch_to(), player_team.get_list_of_valid_switch_indices())
        if uinp == 10: # FIXME: Implement player losing by running away
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
            else: # TODO: Implement MTCS for AI
                current_game_state = GameState(player_team, ai_team)
                print("AI is thinking...")
                ai_choice = MonteCarloTreeSearch(current_game_state,random_policy=False).get_best_move()
            turn(player_team, uinp, ai_team, ai_choice)
    # Match over
    if player_team.has_non_fainted_members():
        return 1
    else:
        print("AI wins")
        return 0
    
test_game_5(random_ai=False)   