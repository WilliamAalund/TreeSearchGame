from MatchClasses import *
from MonteCarlo import MonteCarloTreeSearch
from PlayerClass import Player

def exclusive_total():
    return genie_exclusive + forest_exclusive_1 + forest_exclusive_2 + town_exclusive + mountain_exclusive + fossil_exclusive + rugged_exclusive

trainer_level = 4
player_level = 5
wild_level = 5
genie_exclusive = rng.randint(0,1)
forest_exclusive_1 = rng.randint(0,1)
forest_exclusive_2 = rng.randint(0,1)
town_exclusive = rng.randint(0,1)
mountain_exclusive = rng.randint(0,1)
fossil_exclusive = rng.randint(0,1)
rugged_exclusive = rng.randint(0,1)
legendary_exclusive = None
if exclusive_total() < 4:
    legendary_exclusive = 0
elif exclusive_total() > 4:
    legendary_exclusive = 1
else:
    legendary_exclusive = rng.randint(0,1)

def player_starter_selection():
    pass

def generate_wild_team():
    pass

def generate_trainer_team():
    pass

def generate_map():
    pass

def explore_location():
    pass

# Pasture: contains pasture monsters
# Forest: contains forest monsters
# Road: contains town monsters
# Town: contains a pokemon center
# City: contains city monsters, and a pokemon center
# Mountain: contains mountain monsters
# Desert: contains desert monsters, and fossils
# Cave: contains cave monsters
# Gym: Contains a gym leader/powerful trainer

def campaign_game():
    # The real game
    player_starter_selection()
    generate_map()
    pass


def infinite_game():
    player_lost = False
    player_wins = 0
    player_team = Team("Player")
    player_team.add_member(Monster(SERPERIOR, trainer_level))
    player_team.add_member(Monster(EMBOAR, trainer_level))
    player_team.add_member(Monster(SAMUROTT, trainer_level))
    player_team.add_member(Monster(RESHIRAM,trainer_level))
    while not player_lost:
        enemy_team = generate_enemy_team()
        match_result = match(player_team, enemy_team)
        if match_result == 0:
            player_lost = True
            print("Player lost")
        else:
            print("\033[33mPlayer won")
            player_wins += 1
            print("Player wins: " + str(player_wins),"\033[0m")
        player_team.fully_heal_team()
        
def generate_enemy_team(member_count = 4):
    enemy_team = Team("Enemy")
    num_team_members = member_count
    if num_team_members == 1:
        print("Invalid member count: setting to one")
    for i in range(num_team_members):
        enemy_team.add_member(Monster(rng.randint(494,649), trainer_level))
    return enemy_team

def match(player_team: Team, ai_team: Team, random_ai = False,random_ai_policy=False, verbose_MTCS=False): # Runs a match between two teams. Returns 1 if player won, 0 if AI won
    
    player_team.active_member_index = 0
    ai_team.active_member_index = 0
    while player_team.has_non_fainted_members() and ai_team.has_non_fainted_members(): # Match loop
        if player_team.get_active_member().fainted: # Make player choose a valid new active member
            print(player_team)
            player_choice = gm.switch_menu(team_members=player_team.get_list_of_members_to_switch_to(),valid_switch_indices=player_team.get_list_of_valid_switch_indices(), Back=False) # FIXME: Implement player choice
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
        uinp = gm.battle_menu_input(player_team.get_member(player_team.active_member_index).get_list_of_moves(), player_team.get_list_of_members_to_switch_to(), player_team.get_list_of_valid_switch_indices())
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

def gear_shift_game(random_ai=False):
    # Match between a klinklang and a serperior
    player_team = Team("Player")
    ai_team = Team("Enemy")
    player_team.add_member(Monster(KLINKLANG, 15))
    ai_team.add_member(Monster(KLINKLANG, 15))
    match_result = match(player_team, ai_team, random_ai=random_ai)

def switch_menu_game(random_ai=False):
    # Match between a team of three starters, and a lillipup
    player_team = Team("Player")
    ai_team = Team("Enemy")
    player_team.add_member(Monster(SAMUROTT, 15))
    player_team.add_member(Monster(LILLIPUP, 15))
    ai_team.add_member(Monster(LILLIPUP, 2))
    match_result = match(player_team, ai_team, random_ai=random_ai)

def super_fang_game(random_ai = False):
    # Match between two watchogs
    player_team = Team("Player")
    ai_team = Team("Enemy")
    player_team.add_member(Monster(WATCHOG, 15))
    player_team.add_member(Monster(WATCHOG, 15))
    ai_team.add_member(Monster(WATCHOG, 15))
    match_result = match(player_team, ai_team, random_ai=random_ai)

def paralysis_game(random_ai = False):
    # Match between two emolga
    player_team = Team("Player")
    ai_team = Team("Enemy")
    player_team.add_member(Monster(EMOLGA, 15))
    player_team.add_member(Monster(EMOLGA, 15))
    ai_team.add_member(Monster(EMOLGA, 15))
    match_result = match(player_team, ai_team, random_ai=random_ai)

#paralysis_game(random_ai = False)
#super_fang_game(random_ai = False)
infinite_game()