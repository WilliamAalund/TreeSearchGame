from MatchClasses import *
from MonteCarlo import MonteCarloTreeSearch
from PlayerClass import Player


trainer_level = 50

def infinite_game():
    player_lost = False
    player_wins = 0
    player_team = Team("Player")
    player_team.add_member(Monster(SERPERIOR, trainer_level))
    player_team.add_member(Monster(EMBOAR, trainer_level))
    player_team.add_member(Monster(SAMUROTT, trainer_level))
    while not player_lost:
        enemy_team = generate_enemy_team(member_count=3)
        match_result = match(player_team, enemy_team)
        if match_result == 0:
            player_lost = True
            print("Player lost")
        else:
            print("\033[33mPlayer won")
            player_wins += 1
            print("Player wins: " + str(player_wins),"\033[0m")
        player_team.fully_heal_team()
        
def generate_enemy_team(member_count = 3):
    enemy_team = Team("Enemy")
    num_team_members = member_count
    if num_team_members == 1:
        print("Invalid member count: setting to one")
    for i in range(num_team_members):
        enemy_team.add_member(Monster(rng.randint(494,620), trainer_level))
    return enemy_team

def match(player_team: Team, ai_team: Team, random_ai = False,random_ai_policy=False, verbose_MTCS=False): # Runs a match between two teams. Returns 1 if player won, 0 if AI won
    
    player_team.active_member_index = 0
    ai_team.active_member_index = 0
    while player_team.has_non_fainted_members() and ai_team.has_non_fainted_members(): # Match loop
        if player_team.get_active_member().fainted: # Make player choose a valid new active member
            print(player_team)
            player_choice = gm.switch_menu(team_members=player_team.get_list_of_member_names_to_switch_to(),valid_switch_indices=player_team.get_list_of_valid_switch_indices(), Back=False) # FIXME: Implement player choice
            switch_after_fainting(player_team, player_choice - 4)
        if ai_team.get_active_member().fainted: # Make AI choose a valid new active member
            current_game_state = GameState(player_team, ai_team)
            # If the ai only has one valid switch, then make it choose that without using MCTS
            if len(ai_team.get_list_of_valid_switch_indices()) == 1:
                ai_choice = ai_team.get_list_of_valid_switch_indices()[0] + 4
            elif random_ai == True:
                ai_choice = rng.choice(ai_team.get_list_of_valid_switch_indices()) + 4
            else:
                ai_choice = MonteCarloTreeSearch(current_game_state,random_policy=random_ai_policy).get_best_move()
            switch_after_fainting(ai_team, ai_choice - 4)
        print("-----------------------------------------")   
        gm.battle_scene(player_team, ai_team)
        uinp = gm.battle_menu_input(player_team.get_member(player_team.active_member_index).get_list_of_moves(), player_team.get_list_of_member_names_to_switch_to(), player_team.get_list_of_valid_switch_indices())
        print("-----------------------------------------")    
        if uinp == 10: # FIXME: Implement player losing by running away
            print("Player ran away!")
            return 0 
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
            else:
                current_game_state = GameState(player_team, ai_team)
                print("AI is thinking...", end="")
                ai_choice = MonteCarloTreeSearch(current_game_state,random_policy=False, verbose=verbose_MTCS).get_best_move()
            turn(player_team, uinp, ai_team, ai_choice)
    # Match over
    if player_team.has_non_fainted_members():
        print(player_team.name + " defeated " + ai_team.name + "!")
        return 1
    else:
        print(ai_team.name + " defeated " + player_team.name + "!")
        return 0

def test_game(random_ai = False):
    # Match between two teams of 2 of the same pokemon
    player_team = Team("Player")
    ai_team = Team("Enemy")
    player_team.add_member(Monster(501, 15))
    ai_team.add_member(Monster(501, 15))
    match_result = match(player_team, ai_team, random_ai=random_ai)
    if match_result:
        print("Player won")

def starter_game(random_ai = False):
    # Match bewteen two teams of 3 pokemon
    player_team = Team("Player")
    ai_team = Team("Enemy")
    player_team.add_member(Monster(SAMUROTT, 15))
    player_team.add_member(Monster(SERPERIOR, 15))
    player_team.add_member(Monster(EMBOAR, 15))
    ai_team.add_member(Monster(SAMUROTT, 15))
    ai_team.add_member(Monster(SERPERIOR, 15))
    ai_team.add_member(Monster(EMBOAR, 15))
    match_result = match(player_team, ai_team, random_ai=random_ai)
    if match_result:
        print("Player won")

def easy_game(random_ai = False):
    # Match between one team of 3 pokemon and one team of one pokemon
    player_team = Team("Player")
    ai_team = Team("Enemy")
    player_team.add_member(Monster(501, 15))
    player_team.add_member(Monster(498, 15))
    player_team.add_member(Monster(495, 15))
    ai_team.add_member(Monster(501, 15))
    match_result = match(player_team, ai_team, random_ai=random_ai)
    
def recoil_game(random_ai = False):
    # Match between two teams with one emboar
    player_team = Team("Player")
    ai_team = Team("Enemy")
    player_team.add_member(Monster(EMBOAR, 15))
    ai_team.add_member(Monster(EMBOAR, 15))
    match_result = match(player_team, ai_team, random_ai=random_ai)

def error_game(random_ai = False):
    # Match between two teams of one snivy
    player_team = Team("Player")
    ai_team = Team("Enemy")
    player_team.add_member(Monster(SNIVY, 15))
    ai_team.add_member(Monster(SNIVY, 15))
    match_result = match(player_team, ai_team, random_ai=random_ai)

def alter_boost_after_attack_game(random_ai = False):
    # Match between two teams of one cobalion with superpower
    player_team = Team("Player")
    ai_team = Team("Enemy")
    player_team.add_member(Monster(COBALION, 15))
    ai_team.add_member(Monster(COBALION, 15))
    match_result = match(player_team, ai_team, random_ai=random_ai)

def alter_boost_after_effect_move_game(random_ai = False):
    # Match between two teams of terrakion with tackle and swords dance
    player_team = Team("Player")
    ai_team = Team("Enemy")
    player_team.add_member(Monster(TERRAKION, 15))
    ai_team.add_member(Monster(TERRAKION, 15))
    match_result = match(player_team, ai_team, random_ai=random_ai)

def heal_after_attack_game(random_ai = False):
    # Match between two teams of one serperior with gigadrain
    player_team = Team("Player")
    ai_team = Team("Enemy")
    player_team.add_member(Monster(SERPERIOR, 15))
    ai_team.add_member(Monster(SERPERIOR, 15))
    match_result = match(player_team, ai_team, random_ai=random_ai)

def multi_hit_attack_game(random_ai = False):
    # Match between two teams of one swadloon with Pin Missile
    player_team = Team("Player")
    ai_team = Team("Enemy")
    player_team.add_member(Monster(SWADLOON, 15))
    ai_team.add_member(Monster(SWADLOON, 15))
    match_result = match(player_team, ai_team, random_ai=random_ai)

def bug_game(random_ai = False, verbose_MTCS=False): # FIXED: Bug where AI taking recoil and fainting would not cause a node to be terminal
    # Match between player team of Serperior, Samurott, and Emboar, and an Audino
    player_team = Team("Player")
    ai_team = Team("Enemy")
    player_team.add_member(Monster(SERPERIOR, 50))
    player_team.add_member(Monster(SAMUROTT, 50))
    player_team.add_member(Monster(EMBOAR, 50))
    ai_team.add_member(Monster(AUDINO, 50))
    match_result = match(player_team, ai_team, random_ai=random_ai, verbose_MTCS=verbose_MTCS)


def behavior_game(random_ai = False):
    # Match between a superior against a drillbur and a seismitoad
    player_team = Team("Player")
    ai_team = Team("Enemy")
    player_team.add_member(Monster(SERPERIOR, 15))
    ai_team.add_member(Monster(DRILBUR, 15))
    ai_team.add_member(Monster(SEISMITOAD, 15))
    match_result = match(player_team, ai_team, random_ai=random_ai)

infinite_game()