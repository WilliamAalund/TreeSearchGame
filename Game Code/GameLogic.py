from MatchClasses import *
from MonteCarlo import MonteCarloTreeSearch
from PlayerClass import Player

def exclusive_total():
    return genie_exclusive + forest_exclusive_1 + forest_exclusive_2 + town_exclusive + mountain_exclusive + fossil_exclusive + rugged_exclusive

gym_level = 7
trainer_level = 4
wild_level = 3
num_badges = 0
environment = 'Pasture'
visited_biomes = ['Pasture'] # A bit hacky, but makes sure trainers can at least have access to pasture pokemon
genie_exclusive = rng.randint(BLACK_EXCLUSIVE,WHITE_EXCLUSIVE)
forest_exclusive_1 = rng.randint(BLACK_EXCLUSIVE,WHITE_EXCLUSIVE)
forest_exclusive_2 = rng.randint(BLACK_EXCLUSIVE,WHITE_EXCLUSIVE)
town_exclusive = rng.randint(BLACK_EXCLUSIVE,WHITE_EXCLUSIVE)
mountain_exclusive = rng.randint(BLACK_EXCLUSIVE,WHITE_EXCLUSIVE)
fossil_exclusive = rng.randint(BLACK_EXCLUSIVE,WHITE_EXCLUSIVE)
rugged_exclusive = rng.randint(BLACK_EXCLUSIVE,WHITE_EXCLUSIVE)
legendary_exclusive = None
if exclusive_total() < 4:
    legendary_exclusive = BLACK_EXCLUSIVE
elif exclusive_total() > 4:
    legendary_exclusive = WHITE_EXCLUSIVE
else:
    legendary_exclusive = rng.randint(BLACK_EXCLUSIVE,WHITE_EXCLUSIVE)

def update_level_caps():
    global gym_level
    global trainer_level
    global wild_level
    if num_badges == 1:
        gym_level = 10
        trainer_level = 7
        wild_level = 6
    elif num_badges == 2:
        gym_level = 15
        trainer_level = 10
        wild_level = 9
    elif num_badges == 3:
        gym_level = 20
        trainer_level = 16
        wild_level = 12
    elif num_badges == 4:
        gym_level = 24
        trainer_level = 23
        wild_level = 15
    elif num_badges == 5:
        gym_level = 29
        trainer_level = 25
        wild_level = 20
    elif num_badges == 6:
        gym_level = 33
        trainer_level = 30
        wild_level = 25
    elif num_badges == 7:
        gym_level = 37
        trainer_level = 35
        wild_level = 30
    elif num_badges == 8:
        gym_level = 41
        trainer_level = 40
        wild_level = 35

def roll_current_environment():
    if num_badges == 0:
        return 'Pasture'
    elif num_badges <= 2:
        return rng.choice(COMMON_ENVIRONMENTS)
    elif num_badges <= 4:
        return rng.choice(UNCOMMON_ENVIRONMENTS)
    elif num_badges <= 6:
        return rng.choice(RARE_ENVIRONMENTS)
    elif num_badges <= 8:
        return rng.choice(RARE_ENVIRONMENTS + ELEMENTAL_ENVIRONMENTS)

def generate_wild_team(wild_streak = 0, environment = 'Pasture'):
    team = Team("Wild")
    if environment == 'Pasture':
        roster = PASTURE_COMMON_1
        if wild_streak > 0:
            roster += PASTURE_UNCOMMON_1
        if wild_streak > 1:
            roster += PASTURE_RARE_1
    elif environment == 'Forest':
        roster = FOREST_COMMON_1
        if wild_streak > 0:
            roster += FOREST_UNCOMMON_1 + [FOREST_EXCLUSIVES_1[forest_exclusive_1]] + [FOREST_EXCLUSIVES_2[forest_exclusive_2]]
        if wild_streak > 1:
            roster += FOREST_RARE_1
    elif environment == 'Urban':
        roster = TOWN_COMMON_1
        if wild_streak > 0:
            roster += TOWN_UNCOMMON_1 + [TOWN_EXCLUSIVES[town_exclusive]]
        if wild_streak > 1:
            roster += TOWN_RARE_1
    elif environment == 'Desert':
        roster = DESERT_COMMON_1
        if wild_streak > 0:
            roster += DESERT_UNCOMMON_1
        if wild_streak > 1:
            roster += DESERT_RARE_1
    elif environment == 'Cave':
        roster = CAVE_COMMON_1
        if wild_streak > 0:
            roster += CAVE_UNCOMMON_1 + [FOSSIL_EXCLUSIVES[fossil_exclusive]]
        if wild_streak > 1:
            roster += CAVE_RARE_1
    elif environment == 'Charge Cave':
        roster = CHARGE_CAVE_COMMON_1
        if wild_streak > 0:
            roster += CHARGE_CAVE_UNCOMMON_1
        if wild_streak > 1:
            roster += CHARGE_CAVE_RARE_1
    elif environment == 'Mountain':
        roster = MOUNTAIN_COMMON_1
        if wild_streak > 0:
            roster += MOUNTAIN_UNCOMMON_1 + [MOUNTAIN_EXCLUSIVES[mountain_exclusive]]
        if wild_streak > 1:
            roster += MOUNTAIN_RARE_1
    elif environment == 'Ocean':
        roster = OCEAN_COMMON_1
        if wild_streak > 0:
            roster += OCEAN_UNCOMMON_1 + [FOSSIL_EXCLUSIVES[fossil_exclusive]]
        if wild_streak > 1:
            roster += OCEAN_RARE_1
    elif environment == 'Rugged':
        roster = RUGGED_COMMON_1
        if wild_streak > 0:
            roster += [RUGGED_EXCLUSIVES[rugged_exclusive]]
        if wild_streak > 1:
            roster += RUGGED_RARE_1
    elif environment == 'Heat':
        roster = HEAT_COMMON_1
        if wild_streak > 0:
            roster += HEAT_UNCOMMON_1
        if wild_streak > 1:
            roster += HEAT_RARE_1
    elif environment == 'Wet':
        roster = WET_COMMON_1
        if wild_streak > 0:
            roster += WET_UNCOMMON_1
        if wild_streak > 1:
            roster += WET_RARE_1
    elif environment == 'Lush':
        roster = LUSH_COMMON_1
        if wild_streak > 0:
            roster += LUSH_UNCOMMON_1
        if wild_streak > 1:
            roster += LUSH_RARE_1
    elif environment == 'Energized':
        roster = ENERGISED_COMMON_1
        if wild_streak > 0:
            roster += ENERGISED_UNCOMMON_1
        if wild_streak > 1:
            roster += ENERGISED_RARE_1
    pick = rng.choice(roster)
    team.add_member(Monster(pick,wild_level))
    return team

def generate_trainer_team(visited_environments, num_badges): # Trainers will gain more pokemon as the player gets badges. Trainers can only have pokemon that the player has had a chance to encounter
    trainer_team = Team("Opponent")
    potential_roster = []
    for visited_environment in visited_environments:
        if visited_environment == 'Pasture':
            potential_roster = potential_roster + PASTURE_COMMON_1
        elif visited_environment == 'Forest':
            potential_roster = potential_roster + FOREST_COMMON_1
        elif visited_environment == 'Town':
            potential_roster = potential_roster + TOWN_COMMON_1
        elif visited_environment == 'Desert':
            potential_roster = potential_roster + DESERT_COMMON_1
        elif visited_environment == 'Cave':
            potential_roster = potential_roster + CAVE_COMMON_1
        elif visited_environment == 'Charge Cave':
            potential_roster = potential_roster + CHARGE_CAVE_COMMON_1
        elif visited_environment == 'Mountain':
            potential_roster = potential_roster + MOUNTAIN_COMMON_1
        elif visited_environment == 'Ocean':
            potential_roster = potential_roster + OCEAN_COMMON_1
        elif visited_environment == 'Rugged':
            potential_roster = potential_roster + RUGGED_COMMON_1
        elif visited_environment == 'Heat':
            potential_roster = potential_roster + HEAT_COMMON_1
        elif visited_environment == 'Wet':
            potential_roster = potential_roster + WET_COMMON_1
        elif visited_environment == 'Lush':
            potential_roster = potential_roster + LUSH_COMMON_1
        elif visited_environment == 'Energized':
            potential_roster = potential_roster + ENERGISED_COMMON_1
        elif visited_environment == 'Ruins':
            potential_roster = potential_roster + RUINS_COMMON_1
        else:
            print("Error in generate_trainer_team: Invalid environment, defaulting to pasture.")
            potential_roster = potential_roster + PASTURE_COMMON_1
        if MINCCINO in potential_roster:
            print("Minccino in potential roster")

    def add_members_to_trainer_team(members_to_add: int):
        # Helper function, adds monsters to the trainer team, and removed the added monster id from potential_roster
        for member in range(members_to_add):
            pick = rng.choice(potential_roster)
            trainer_team.add_member(Monster(pick,trainer_level))
            potential_roster.remove(pick)
        
    if num_badges <= 1:
        add_members_to_trainer_team(1)
    elif num_badges <= 4:
        add_members_to_trainer_team(2)
    elif num_badges <= 6:
        add_members_to_trainer_team(3)
    elif num_badges <= 8:
        add_members_to_trainer_team(4)
    else:
        print("Error: Invalid number of badges")
    return trainer_team

def generate_gym_team(badges = 0):
    gym_team = Team("Gym Leader")
    if badges == 0:
        gym_team.add_member(Monster(PATRAT,gym_level))
        gym_team.add_member(Monster(LILLIPUP,gym_level))
    elif badges == 1:
        gym_team.add_member(Monster(PURRLOIN,gym_level))
        gym_team.add_member(Monster(MUNNA,gym_level))
    elif badges == 2:
        slot_1 = rng.choice([PANSAGE,PANSEAR,PANPOUR])
        slot_2 = rng.choice([TIMBURR,LILLIPUP])
        slot_3 = rng.choice([PIDOVE, WOOBAT])
        gym_team.add_member(Monster(slot_1,gym_level))
        gym_team.add_member(Monster(slot_2,gym_level))
        gym_team.add_member(Monster(slot_3,gym_level))
    elif badges == 3:
        gym_team.add_member(Monster(SANDILE,gym_level))
        gym_team.add_member(Monster(DARUMAKA,gym_level))
        gym_team.add_member(Monster(MARACTUS,gym_level))
    elif badges == 4:
        gym_team.add_member(Monster(EMOLGA,gym_level))
        gym_team.add_member(Monster(EXCADRILL,gym_level))
        gym_team.add_member(Monster(ALOMOMOLA,gym_level))
        gym_team.add_member(Monster(ARCHEN,gym_level))
    elif badges == 5:
        gym_team.add_member(Monster(ZEBSTRIKA,gym_level))
        gym_team.add_member(Monster(COFAGRIGUS,gym_level))
        gym_team.add_member(Monster(GOTHORITA,gym_level))
        gym_team.add_member(Monster(GARBODOR,gym_level))
    elif badges == 6:
        gym_team.add_member(Monster(JELLICENT,gym_level))
        gym_team.add_member(Monster(VANILLUXE,gym_level))
        gym_team.add_member(Monster(CRUSTLE,gym_level))
        gym_team.add_member(Monster(LEAVANNY,gym_level))
        gym_team.add_member(Monster(SCOLIPEDE,gym_level))
    elif badges == 7:
        gym_team.add_member(Monster(EELEKTROSS,gym_level))
        gym_team.add_member(Monster(CHANDELURE,gym_level))
        gym_team.add_member(Monster(HAXORUS,gym_level))
        gym_team.add_member(Monster(BRAVIARY,gym_level))
        gym_team.add_member(Monster(COBALION,gym_level))
    elif badges == 8:
        if legendary_exclusive == BLACK_EXCLUSIVE:
            gym_team.add_member(Monster(ZEKROM,gym_level))
        else:
            gym_team.add_member(Monster(RESHIRAM,gym_level))
        gym_team.add_member(Monster(MIENSHAO,gym_level))
        gym_team.add_member(Monster(BISHARP,gym_level))
        gym_team.add_member(Monster(BEARTIC,gym_level))
        gym_team.add_member(Monster(REUNICLUS,gym_level))
        gym_team.add_member(Monster(MANDIBUZZ,gym_level))
    return gym_team

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

def wild_encounter(player: Player, wild_level: int, wild_streak: int):
    wild_team = generate_wild_team(environment=environment, wild_streak=wild_streak)
    wild_pokemon_name = wild_team.get_active_member().name
    print("Player encountered a wild \033[33m" + wild_pokemon_name + "\033[0m!")
    match_result = match(player.get_team(), wild_team, random_ai=True,wild_encounter=True)
    if match_result == 2: # Player caught the wild monster
        player.get_team().add_member(wild_team.pop_member(wild_team.active_member_index))
    elif match_result == 1: # Player defeated the wild monster
        player.add_experience(3)
        return 1
    else: # Player lost to the wild monster
        return 0

def trainer_encounter(player: Player, trainer_level: int):
    trainer_team = generate_trainer_team(visited_biomes, num_badges)
    print
    match_result = match(player.get_team(), trainer_team, random_ai=False)
    if match_result == 1: # Player defeated the trainer
        player.add_experience(4)
        return 1
    else: # Player lost to the trainer
        return 0

def gym_encounter(player: Player, gym_level: int, gym_badges: int):
    gym_team = generate_gym_team(gym_badges)
    match_result = match(player.get_team(), gym_team, random_ai=False)
    if match_result == 1: # Player defeated the gym leader
        player.level_up(1)
        return 1
    else: # Player lost to the gym leader
        return 0

def campaign_game():
    # The real game
    player = Player()
    global num_badges
    global environment
    while num_badges < 8:
        travel_distance = 7
        wild_streak = 0
        while travel_distance > 0:
            print("\nDistance to gym: " + str(travel_distance), end=" | ")
            print("Current location: " + environment, end=" | ")
            if wild_streak > 0:
                print("Wild streak: " + str(wild_streak))
            else:
                print("")
            response = gm.generic_input("Where will you head to?", "Fight", "Explore", "Town", "Pokemon", "Quit")
            if response == 0:
                print("Decided to fight a trainer")
                wild_streak = 0
                fight_result = trainer_encounter(player, trainer_level)
                if fight_result == 0:
                    print("Player lost... you rushed to the pokemon center to heal your team.")
                    player.heal_team()
                travel_distance -= 1
            elif response == 1:
                print("Decided to explore the area.")
                travel_distance -= 1
                explore_result = wild_encounter(player, wild_level, wild_streak)
                if explore_result != 0:
                    wild_streak += 1
                if explore_result == 0:
                    print("Player lost... you rushed to the pokemon center to heal your team.")
                    player.heal_team()
            elif response == 2:
                print("Decided to head into town. \033[32mParty is fully healed.\033[0m")
                TOWNSFOLK_TALK_ABOUT_LEGENDARY = 0
                TOWNSFOLK_TALK_ABOUT_EXCLUSIVES = 1
                TOWNSFOLK_TALK_ABOUT_GYM = 2
                TOWNSFOLK_TALK_ABOUT_GOSSIP = 3
                travel_distance -= 1   
                wild_streak = 0
                player.heal_team() 
            elif response == 3:
                print("Decided to check out your pokemon.")
                player.view_team()
            elif response == 4:
                print("Decided to quit")
                return
            else:
                print("Error: Invalid response")
        print("Player arrived at the gym. \033[32mYou healed your team before the battle.\033[0m")
        player.heal_team()
        gym_result = gym_encounter(player, gym_level, num_badges)
        if gym_result == 0:
            print("Player lost")
            return
        elif gym_result == 1:
            print("\33[33mPlayer obtained a badge!\033[0m")
            num_badges += 1
            environment = roll_current_environment()
            global visited_biomes
            if environment not in visited_biomes:
                visited_biomes.append(environment)
            update_level_caps()
            print("\033[32mParty is fully healed.\033[0m")
            player.heal_team()

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

def match(player_team: Team, ai_team: Team, random_ai = False,random_ai_policy=False, verbose_MTCS=False, wild_encounter = False, player_bag = None): # Runs a match between two teams. Returns 1 if player won, 0 if AI won
    player_team.active_member_index = player_team.get_leading_member_index()
    ai_team.active_member_index = ai_team.get_leading_member_index()
    catch_attempts = 0
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
        if wild_encounter:
            print("-- \033[32mWILD BATTLE\033[0m --------------------------")
        else:
            print("-- \033[33mTRAINER BATTLE\033[0m -----------------------")
        in_menu = True
        while in_menu:
            gm.battle_scene(player_team, ai_team)
            if wild_encounter:
                uinp = gm.battle_menu_input(player_team.get_member(player_team.active_member_index).get_list_of_moves(), player_team.get_list_of_members_to_switch_to(), player_team.get_list_of_valid_switch_indices(), wild_encounter=True)
            else:
                uinp = gm.battle_menu_input(player_team.get_member(player_team.active_member_index).get_list_of_moves(), player_team.get_list_of_members_to_switch_to(), player_team.get_list_of_valid_switch_indices())
            if uinp == 10 and not wild_encounter: # Player can only run away from wild encounters
                # Color text red
                print("\033[31mNo! There's no running away from a trainer battle!\033[0m")
            else:
                in_menu = False
        print("-----------------------------------------")    
        if uinp == 11 and wild_encounter == True: # throw pokeball 
            print("Player used a pokeball on the wild " + ai_team.get_active_member().name + "!")
            base_catch_rate = (800 - ai_team.get_active_member().get_base_stat_total()) / 1000
            #print("Base catch rate: " + str(base_catch_rate))
            hp_catch_rate = (1 -(ai_team.get_active_member().get_stat(HP) / ai_team.get_active_member().get_stat(MAX_HP))) * 0.4
            #print("HP catch rate: " + str(hp_catch_rate))
            attempt_amount_catch_rate = catch_attempts / 100
            #print("Attempt amount catch rate: " + str(attempt_amount_catch_rate))
            total_catch_rate = base_catch_rate + hp_catch_rate + attempt_amount_catch_rate
            if total_catch_rate > 1:
                total_catch_rate = 1
            #print("Total catch rate: " + str(total_catch_rate))
            catch_roll = rng.randint(0,100)
            if catch_roll < total_catch_rate * 100:
                print("\33[32mPlayer caught the wild " + ai_team.get_active_member().name + "!\033[0m")
                print("-----------------------------------------")  
                return 2
            else:
                print("The wild " + ai_team.get_active_member().name + " broke free!")
                catch_attempts += 1
        if uinp == 10: # FIXME: Implement player not losing by running away
            print("Player ran away!")
            return 0
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
        print("-----------------------------------------")
        return 1
    else:
        print(ai_team.name + " defeated " + player_team.name + "!\n")
        print("-----------------------------------------")
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

def burn_game(random_ai = False):
    # Match between one lampent and one throh
    player_team = Team("Player")
    ai_team = Team("Enemy")
    player_team.add_member(Monster(LAMPENT, 15))
    ai_team.add_member(Monster(THROH, 15))
    match_result = match(player_team, ai_team, random_ai=random_ai)

def confusion_game(random_ai = False):
    # Match between a frillish and a blitzle
    player_team = Team("Player")
    ai_team = Team("Enemy")
    player_team.add_member(Monster(FRILLISH, 50))
    ai_team.add_member(Monster(BLITZLE, 5))
    match_result = match(player_team, ai_team, random_ai=random_ai)

def asleep_game(random_ai = False):
    # Match between an amoonguss and a frillish
    player_team = Team("Player")
    ai_team = Team("Enemy")
    player_team.add_member(Monster(AMOONGUSS, 50))
    ai_team.add_member(Monster(FRILLISH, 5))
    match_result = match(player_team, ai_team, random_ai=random_ai)

def level_one_game(random_ai = False):
    # Match between level 5 oshawott, lillipup and patrat versus a level 4 patrat and purrloin
    player_team = Team("Player")
    ai_team = Team("Enemy")
    player_team.add_member(Monster(OSHAWOTT, 5))
    player_team.add_member(Monster(LILLIPUP, 5))
    ai_team.add_member(Monster(PATRAT, 4))
    ai_team.add_member(Monster(PURRLOIN, 4))
    match_result = match(player_team, ai_team, random_ai=random_ai)

def level_two_game(random_ai = False):
    # Match between level 20 dewott, herdier and watchog vs level 19 blitzle, and tranquill
    player_team = Team("Player")
    ai_team = Team("Enemy")
    player_team.add_member(Monster(DEWOTT, 20))
    player_team.add_member(Monster(HERDIER, 20))
    player_team.add_member(Monster(WATCHOG, 20))
    ai_team.add_member(Monster(BLITZLE, 19))
    ai_team.add_member(Monster(TRANQUILL, 19))
    match_result = match(player_team, ai_team, random_ai=random_ai)

def final_batle(random_ai = False):
    # Match between two teams of six pokemon at level 70: player team is samurott, chandelure, haxorus, braviary, cobalion and reshiram. AI team is emboar, hydreigon, seismitoad, zoroark, virizion and zekrom
    player_team = Team("Player")
    ai_team = Team("Enemy")
    player_team.add_member(Monster(SAMUROTT, 70))
    player_team.add_member(Monster(CHANDELURE, 70))
    player_team.add_member(Monster(HAXORUS, 70))
    player_team.add_member(Monster(BRAVIARY, 70))
    player_team.add_member(Monster(COBALION, 70))
    player_team.add_member(Monster(RESHIRAM, 70))
    ai_team.add_member(Monster(EMBOAR, 70))
    ai_team.add_member(Monster(HYDREIGON, 70))
    ai_team.add_member(Monster(SEISMITOAD, 70))
    ai_team.add_member(Monster(ZOROARK, 70))
    ai_team.add_member(Monster(VIRIZION, 70))
    ai_team.add_member(Monster(ZEKROM, 70))
    match_result = match(player_team, ai_team, random_ai=random_ai)

def test_case_generate_trainer(n = 15):
    # Test case for generating a trainer team
    possible_environments = []
    current_badges = 0
    for place in ENVIRONMENTS:
        possible_environments.append(place)
        print("Trainer team for " + place + ":")
        for i in range(n):
            trainer_team = generate_trainer_team(possible_environments, current_badges)
            print(trainer_team.small_str())
        current_badges = min(current_badges + 1, 8)


if __name__ == "__main__":
    # For testing
    print("Running test cases...")
    test_case_generate_trainer()