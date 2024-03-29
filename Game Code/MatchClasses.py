import random as rng
import GameMenus as gm
from MoveClasses import Move
from MonsterClasses import * # Monster class, constants, nature dictionary
from TeamClass import Team
import math

# --- CONSTANTS ---
# Battle input constants (10 potential inputs for a player to make per turn)
MOVE_1 = 0
MOVE_2 = 1
MOVE_3 = 2
MOVE_4 = 3
SWITCH_OUT_0 = 4
SWITCH_OUT_1 = 5
SWITCH_OUT_2 = 6
SWITCH_OUT_3 = 7
SWITCH_OUT_4 = 8
SWITCH_OUT_5 = 9
STRUGGLE = 10

CRIT_MULTIPLIER = 1.5
STAB_MULTIPLIER = 1.5
DEFAULT_CRIT_CHANCE = (1 / 24) * 100

# Game Constants
MAX_TEAM_SIZE = 6
TYPE_CHART = {'Normal':{'Normal':1, 'Fire':1, 'Water':1, 'Electric':1, 'Grass':1, 'Ice':1, 'Fighting':1, 'Poison':1, 'Ground':1, 'Flying':1, 'Psychic':1, 'Bug':1, 'Rock':1, 'Ghost':0, 'Dragon':1, 'Dark':1, 'Steel':1, 'Fairy':1, 'Typeless':1},
              'Fire':{'Normal':1, 'Fire':0.5, 'Water':0.5, 'Electric':1, 'Grass':2, 'Ice':2, 'Fighting':1, 'Poison':1, 'Ground':1, 'Flying':1, 'Psychic':1, 'Bug':2, 'Rock':0.5, 'Ghost':1, 'Dragon':0.5, 'Dark':1, 'Steel':2, 'Fairy':0.5, 'Typeless':1},
              'Water':{'Normal':1, 'Fire':2, 'Water':0.5, 'Electric':1, 'Grass':0.5, 'Ice':1, 'Fighting':1, 'Poison':1, 'Ground':2, 'Flying':1, 'Psychic':1, 'Bug':1, 'Rock':2, 'Ghost':1, 'Dragon':0.5, 'Dark':1, 'Steel':1, 'Fairy':1, 'Typeless':1},
              'Electric':{'Normal':1, 'Fire':1, 'Water':2, 'Electric':0.5, 'Grass':0.5, 'Ice':1, 'Fighting':1, 'Poison':1, 'Ground':0, 'Flying':2, 'Psychic':1, 'Bug':1, 'Rock':1, 'Ghost':1, 'Dragon':0.5, 'Dark':1, 'Steel':1, 'Fairy':1, 'Typeless':1},
              'Grass':{'Normal':1, 'Fire':0.5, 'Water':2, 'Electric':1, 'Grass':0.5, 'Ice':1, 'Fighting':1, 'Poison':0.5, 'Ground':2, 'Flying':0.5, 'Psychic':1, 'Bug':0.5, 'Rock':2, 'Ghost':1, 'Dragon':0.5, 'Dark':1, 'Steel':0.5, 'Fairy':1, 'Typeless':1},
              'Ice':{'Normal':1, 'Fire':0.5, 'Water':0.5, 'Electric':1, 'Grass':2, 'Ice':0.5, 'Fighting':1, 'Poison':1, 'Ground':2, 'Flying':2, 'Psychic':1, 'Bug':1, 'Rock':1, 'Ghost':1, 'Dragon':2, 'Dark':1, 'Steel':0.5, 'Fairy':1, 'Typeless':1},
              'Fighting':{'Normal':2, 'Fire':1, 'Water':1, 'Electric':1, 'Grass':1, 'Ice':2, 'Fighting':1, 'Poison':0.5, 'Ground':1, 'Flying':0.5, 'Psychic':0.5, 'Bug':0.5, 'Rock':2, 'Ghost':0, 'Dragon':1, 'Dark':2, 'Steel':2, 'Fairy':0.5, 'Typeless':1},
              'Poison':{'Normal':1, 'Fire':1, 'Water':1, 'Electric':1, 'Grass':2, 'Ice':1, 'Fighting':1, 'Poison':0.5, 'Ground':0.5, 'Flying':1, 'Psychic':1, 'Bug':1, 'Rock':0.5, 'Ghost':0.5, 'Dragon':1, 'Dark':1, 'Steel':0, 'Fairy':2, 'Typeless':1},
              'Ground':{'Normal':1, 'Fire':2, 'Water':1, 'Electric':2, 'Grass':0.5, 'Ice':1, 'Fighting':1, 'Poison':2, 'Ground':1, 'Flying':0, 'Psychic':1, 'Bug':0.5, 'Rock':2, 'Ghost':1, 'Dragon':1, 'Dark':1, 'Steel':2, 'Fairy':1, 'Typeless':1},
              'Flying':{'Normal':1, 'Fire':1, 'Water':1, 'Electric':0.5, 'Grass':2, 'Ice':1, 'Fighting':2, 'Poison':1, 'Ground':1, 'Flying':1, 'Psychic':1, 'Bug':2, 'Rock':0.5, 'Ghost':1, 'Dragon':1, 'Dark':1, 'Steel':0.5, 'Fairy':1, 'Typeless':1},
              'Psychic':{'Normal':1, 'Fire':1, 'Water':1, 'Electric':1, 'Grass':1, 'Ice':1, 'Fighting':2, 'Poison':2, 'Ground':1, 'Flying':1, 'Psychic':0.5, 'Bug':1, 'Rock':1, 'Ghost':1, 'Dragon':1, 'Dark':0, 'Steel':0.5, 'Fairy':1, 'Typeless':1},
              'Bug':{'Normal':1, 'Fire':0.5, 'Water':1, 'Electric':1, 'Grass':2, 'Ice':1, 'Fighting':0.5, 'Poison':0.5, 'Ground':1, 'Flying':0.5, 'Psychic':2, 'Bug':1, 'Rock':1, 'Ghost':0.5, 'Dragon':1, 'Dark':2, 'Steel':0.5, 'Fairy':0.5, 'Typeless':1},
              'Rock':{'Normal':1, 'Fire':2, 'Water':1, 'Electric':1, 'Grass':1, 'Ice':2, 'Fighting':0.5, 'Poison':1, 'Ground':0.5, 'Flying':2, 'Psychic':1, 'Bug':2, 'Rock':1, 'Ghost':1, 'Dragon':1, 'Dark':1, 'Steel':0.5, 'Fairy':1, 'Typeless':1},
              'Ghost':{'Normal':0, 'Fire':1, 'Water':1, 'Electric':1, 'Grass':1, 'Ice':1, 'Fighting':1, 'Poison':1, 'Ground':1, 'Flying':1, 'Psychic':2, 'Bug':1, 'Rock':1, 'Ghost':2, 'Dragon':1, 'Dark':0.5, 'Steel':1, 'Fairy':1, 'Typeless':1},
              'Dragon':{'Normal':1, 'Fire':1, 'Water':1, 'Electric':1, 'Grass':1, 'Ice':1, 'Fighting':1, 'Poison':1, 'Ground':1, 'Flying':1, 'Psychic':1, 'Bug':1, 'Rock':1, 'Ghost':1, 'Dragon':2, 'Dark':1, 'Steel':0.5, 'Fairy':0, 'Typeless':1},
              'Dark':{'Normal':1, 'Fire':1, 'Water':1, 'Electric':1, 'Grass':1, 'Ice':1, 'Fighting':0.5, 'Poison':1, 'Ground':1, 'Flying':1, 'Psychic':2, 'Bug':1, 'Rock':1, 'Ghost':2, 'Dragon':1, 'Dark':0.5, 'Steel':1, 'Fairy':0.5, 'Typeless':1},
              'Steel':{'Normal':1, 'Fire':0.5, 'Water':0.5, 'Electric':0.5, 'Grass':1, 'Ice':2, 'Fighting':1, 'Poison':1, 'Ground':1, 'Flying':1, 'Psychic':1, 'Bug':1, 'Rock':2, 'Ghost':1, 'Dragon':1, 'Dark':1, 'Steel':0.5, 'Fairy':2, 'Typeless':1},
              'Fairy':{'Normal':1, 'Fire':0.5, 'Water':1, 'Electric':1, 'Grass':1, 'Ice':1, 'Fighting':2, 'Poison':0.5, 'Ground':1, 'Flying':1, 'Psychic':1, 'Bug':1, 'Rock':1, 'Ghost':1, 'Dragon':2, 'Dark':2, 'Steel':0.5, 'Fairy':1, 'Typeless':1},
              'Typeless':{'Normal':1, 'Fire':1, 'Water':1, 'Electric':1, 'Grass':1, 'Ice':1, 'Fighting':1, 'Poison':1, 'Ground':1, 'Flying':1, 'Psychic':1, 'Bug':1, 'Rock':1, 'Ghost':1, 'Dragon':1, 'Dark':1, 'Steel':1, 'Fairy':1, 'Typeless':1}}

def quick_damage_calc(attacker_attack, attacker_attack_multiplier, attacker_level, defender_defense, defender_defense_multiplier, base_power, type_multiplier): 
    raw_calc = ((((2*attacker_level / 5 + 2) * base_power * (attacker_attack / defender_defense)) / 50) + 2)
    multiplier_calc = (raw_calc * type_multiplier * attacker_attack_multiplier) / defender_defense_multiplier
    return math.ceil(multiplier_calc)

def damage_calc(user: Monster, target: Monster, move: Move, user_team, target_team, can_crit = True, visualization = True, is_struggle = False, crit_chance = DEFAULT_CRIT_CHANCE):
    crit_mult = CRIT_MULTIPLIER if can_crit and rng.randint(1,100) < crit_chance else 1
    if visualization and crit_mult == CRIT_MULTIPLIER:
        print("Critical hit!", end=" ")

    if is_struggle:
        return math.ceil(((((2*user.level / 5 + 2) * move.base_power * (user.attack / target.defense)) / 50) + 2))

    stab_mult = STAB_MULTIPLIER if move.type in {user.type_1, user.type_2} else 1
    type_mult = get_type_multiplier(move.type, target.type_1, target.type_2)

    if move.category in {'Physical', 'Special'}:
        is_physical = move.category == 'Physical'
        used_attack = user.get_stat_after_status_condition(ATTACK if is_physical else SP_ATTACK)
        used_attack_multiplier = user.get_multiplier_for_stat(ATTACK if is_physical else SP_ATTACK)
        used_defense = target.defense if is_physical else target.special_defense
        used_defense_multiplier = 1 if crit_mult == CRIT_MULTIPLIER and target.get_multiplier_for_stat(DEFENSE if is_physical else SP_DEFENSE) > 0 else target.get_multiplier_for_stat(DEFENSE if is_physical else SP_DEFENSE)
    else:
        if visualization:
            print("damage_calc error: calling damage_calc() on an effect move. Returning 0")
        return 0

    raw_calc = ((((2*user.level / 5 + 2) * move.base_power * (used_attack / used_defense)) / 50) + 2)
    multiplier_calc = (raw_calc * crit_mult * stab_mult * type_mult * used_attack_multiplier) / used_defense_multiplier
    return math.ceil(multiplier_calc)

def get_type_multiplier(move_type, target_type_1, target_type_2 = None):
    type_multiplier = 1
    type_multiplier *= TYPE_CHART[move_type][target_type_1]
    if target_type_2:
        type_multiplier *= TYPE_CHART[move_type][target_type_2]
    return type_multiplier

def get_strongest_move_against(user_team: Team, target_team: Team): # Returns the strongest move against the enemy monster
        # For each move in the monster's moveset, calculate the damage it would do to the enemy monster
        user = user_team.get_active_member()
        target = target_team.get_active_member()
        move_damages = [-1,-1,-1,-1]
        if user.move_1:
            if user.move_1.pp > 0:
                move_1_damage = damage_calc(user, target, user.move_1, user_team, target_team, visualization=False)
                move_damages[0] = move_1_damage
        if user.move_2:
            if user.move_2.pp > 0:
                move_2_damage = damage_calc(user, target, user.move_2, user_team, target_team, visualization=False)
                move_damages[1] = move_2_damage
        if user.move_3:
            if user.move_3.pp > 0:
                move_3_damage = damage_calc(user, target, user.move_3, user_team, target_team, visualization=False)
                move_damages[2] = move_3_damage
        if user.move_4:
            if user.move_4.pp > 0:
                move_4_damage = damage_calc(user, target, user.move_4, user_team, target_team, visualization=False)
                move_damages[3] = move_4_damage
        if max(move_damages) == -1:
            return STRUGGLE
        else:
            return move_damages.index(max(move_damages)) # Return the move that does the most damage

def does_first_team_win_matchup(user_team: Team, target_team: Team):
    # Will quickly simulate a matchup between two monsters. Both monsters will use their strongest move every turn until one faints. Returns True if user_team wins, False if target_team wins
    # Get references to the two monsters
    user = user_team.get_active_member()
    target = target_team.get_active_member()
    # Get strongest move from both monsters
    user_strongest_move = get_strongest_move_against(user_team, target_team)
    target_strongest_move = get_strongest_move_against(target_team, user_team) 
    # Simulate turns until one faints
    user_damage = damage_calc(user, target, user.get_move(user_strongest_move), user_team, target_team,can_crit=False, visualization=False)
    target_damage = damage_calc(target, user, target.get_move(target_strongest_move), target_team, user_team,can_crit=False, visualization=False)
    
    user_speed = user.get_stat(SPEED)
    target_speed = target.get_stat(SPEED)

    user_remaining_hp = user.get_stat(HP)
    target_remaining_hp = target.get_stat(HP)

    while user_remaining_hp > 0 and target_remaining_hp > 0:
        if user_speed > target_speed:
            target_remaining_hp -= user_damage
            if target_remaining_hp > 0:
                user_remaining_hp -= target_damage
        elif target_speed > user_speed:
            user_remaining_hp -= target_damage
            if user_remaining_hp > 0:
                target_remaining_hp -= user_damage
        else:
            if rng.randint(0,1) == 0:
                target_remaining_hp -= user_damage
                if target_remaining_hp > 0:
                    user_remaining_hp -= target_damage
            else:
                user_remaining_hp -= target_damage
                if user_remaining_hp > 0:
                    target_remaining_hp -= user_damage
    # Return True if user_team wins, False if target_team wins
    if target_remaining_hp <= 0 and user_remaining_hp > 0:
        return True
    else:
        return False

class GameState():
    def __init__(self, player_team, ai_team, turn_count = 0, last_move = 0) -> None:
        self.player_team = player_team
        self.player_needs_to_switch = self.player_team.is_active_member_fainted()
        self.ai_team = ai_team
        self.ai_needs_to_switch = self.ai_team.is_active_member_fainted()
        self.ai_has_switched_after_fainting = False
        self.turn_count = turn_count
        self.last_move = last_move
        self.last_turn_summary = None
        self.policy_rating = self.calculate_policy_rating() # Called in MTCS algorithm
    
    def __str__(self) -> str: # Called in MTCS algorithm when debugging
        return f"Player team: {self.player_team}\nAI team: {self.ai_team}\nTurn count: {self.turn_count}\nLast move: {self.last_move}\nLast turn summary: {self.last_turn_summary}\nGame over: {self.state_is_terminal()}\nPolicy rating: {self.policy_rating}\nNumber of AI possible actions: {len(self.get_ai_possible_actions(debug=True))}\n"

    def state_is_terminal(self): # Called in MTCS algorithm
        return self.did_elimination_occur()

    def state_is_victory(self): # Called in MTCS algorithm
        return self.did_ai_win_a_matchup()

    def calculate_policy_rating(self): # Called in MTCS algorithm
        policy_rating = 0
        if self.did_elimination_occur() and self.did_ai_win_a_matchup(): # If the node is a victory for the AI, policy rating is 100
            policy_rating = 100
        elif self.did_elimination_occur() and not self.did_ai_win_a_matchup(): # If the node is a victory for the player, policy rating is -100
            policy_rating = -100
        return policy_rating 
    
    def did_elimination_occur(self):
        if not self.last_turn_summary:
            return False
        for action in self.last_turn_summary:
            # If the action was an opponent switching in after fainting, return true
            if action.target_fainted or action.user_fainted:
                return True
        return False
    
    def did_ai_win_a_matchup(self):
        if not self.last_turn_summary:
            return False
        else:
            for action in self.last_turn_summary:
                if action.was_ai_action and action.target_fainted: 
                    return True 
                elif not action.was_ai_action and action.target_fainted :
                    return False
            return False

    def get_victory_reward(self): # Number that represents magnitude by which the AI won.
        victory_reward = 0
        for action in self.last_turn_summary:
            if not action.was_ai_action and action.was_effect_move: # Invalidate victories where AI won because the player did not attack
                victory_reward = -1
                return victory_reward
        # Reward for victories with more hp left
        victory_reward += 1 * (self.ai_team.get_active_member().get_stat(HP) / self.ai_team.get_active_member().get_stat(MAX_HP))
        victory_reward += 2 * (1 - (self.turn_count / 5))
        return victory_reward
    
    def get_loss_penalty(self):
        loss_penalty = 0
        return loss_penalty

    
    def get_valid_switches_for_team(self, team: Team):
        list_of_ai_choices = []
        valid_switch_indices = team.get_list_of_valid_switch_indices()
        for i in valid_switch_indices:
            append_state = GameState(self.player_team.deep_copy(), self.ai_team.deep_copy(), self.turn_count).advance_game(i + 4) # 
            list_of_ai_choices.append(append_state)
        print("Valid team switch indices: " + str(valid_switch_indices))
        return list_of_ai_choices

    def get_ai_possible_actions(self, debug = False):
        if self.ai_needs_to_switch: # If ai needs to switch, return list of inputs representing every valid switch the AI can perform
            #return self.get_valid_switches_for_team(self.ai_team)
            list_of_ai_choices = []
            valid_switch_indices = self.ai_team.get_list_of_valid_switch_indices()
            if debug:
                print("Valid ai switch indices: " + str(valid_switch_indices))
                if len(valid_switch_indices) == 0:
                    print("WARNING: No valid switches found for AI. ")
                    print("Debug variables: ai_needs_to_switch: " + str(self.ai_needs_to_switch) + " player_needs_to_switch: " + str(self.player_needs_to_switch))
                    print("Turn action summary: ")
                    for action in self.last_turn_summary:
                        print(action)
            for i in valid_switch_indices:
                append_state = GameState(self.player_team.deep_copy(), self.ai_team.deep_copy(), self.turn_count).advance_game(i + 4) # 
                list_of_ai_choices.append(append_state)
            return list_of_ai_choices
        
        elif self.player_needs_to_switch: # Switch Player monster, then return new state in the list
            list_of_ai_choices = []
            valid_switch_indices = self.player_team.get_list_of_valid_switch_indices()
            if debug:
                print("Valid player switch indices: " + str(valid_switch_indices))
                if len(valid_switch_indices) == 0:
                    print("WARNING: No valid switches found for player. ")
            for i in valid_switch_indices:
                append_state = GameState(self.player_team.deep_copy(), self.ai_team.deep_copy(), self.turn_count).advance_game(0, i + 4) # 0, 1, 2, 3, are move choices
                list_of_ai_choices.append(append_state)
            return list_of_ai_choices
        
        else: # If no team needs to switch: return list of inputs representing every valid move and switch the AI can perform
            list_of_ai_choices = []
            if self.turn_count != 0 or self.ai_has_switched_after_fainting:
                ai_switches = []
            else:
                ai_switches = self.ai_team.get_list_of_valid_switch_indices()
                for i in range(len(ai_switches)):
                    ai_switches[i] += 4 # Convert switch indices to switch inputs
            ai_moves_list = self.ai_team.get_member(self.ai_team.active_member_index).get_list_of_valid_move_numbers()
            ai_combination_list = ai_moves_list + ai_switches
            player_moves_list = self.player_team.get_member(self.player_team.active_member_index).get_list_of_valid_move_numbers()
            if debug:
                print("AI moves: " + str(ai_moves_list))
                print("AI switches: " + str(ai_switches))
                print("Player moves: " + str(player_moves_list))
            for i in ai_combination_list: # Get all 2-16 combinations of moves
                for j in player_moves_list:
                    # Check if the move combination is valid (Neither move has 0 pp)
                    append_state = GameState(self.player_team.deep_copy(), self.ai_team.deep_copy(), self.turn_count).advance_game(i, j) # 0, 1, 2, 3, are move choices
                    list_of_ai_choices.append(append_state)
            # FIXME: Implement voluntary switching (switching to a better matchup)
            if len(list_of_ai_choices) == 0:
                print("WARNING: No valid moves found for AI. ")
            return list_of_ai_choices

    
    def advance_game(self, ai_choice, player_choice = 0): # Simulates moving game forward. Will flip switch booleans and if both are False, will run turn
        if self.ai_needs_to_switch and not self.did_elimination_occur(): # If ai needs to switch, change the active monster according to the ai_choice
            self.ai_team.switch_active_member(ai_choice - 4) 
            self.ai_needs_to_switch = False
            self.last_turn_summary = [TurnActionSummary(was_ai_action=True,was_switch_after_faint=True)]
            self.ai_has_switched_after_fainting = True
        elif self.player_needs_to_switch and not self.did_elimination_occur(): # If player needs to switch, change the active monster according to the player_choice
            if player_choice == self.player_team.team_size:
                print("Player choice is out of range")
                print("Debug variables: player_choice: " + str(player_choice) + " ai_choice: " + str(ai_choice))
            switch_after_fainting(self.player_team, player_choice - 4, False)
            self.player_needs_to_switch = False
            self.last_turn_summary = [TurnActionSummary(was_ai_action=False,was_switch_after_faint=True)]
        else: # If no one needs to switch, run turn with inputs according to the ai_choice and player_choice
            visualization = False
            self.last_turn_summary = turn(self.player_team, player_choice, self.ai_team, ai_choice, visualization, rng=False) # Teams passed by reference, will be altered by turn function
            self.update_team_needs_to_switch_booleans() # The line that saved the world
            self.turn_count += 1 # If ran turn, increment turn counter and check if game is over
        self.last_move = ai_choice
        return self

    def does_team_need_to_switch(self):
        self.update_team_needs_to_switch_booleans()
        if self.player_needs_to_switch or self.ai_needs_to_switch:
            return True
        else:
            return False

    def update_team_needs_to_switch_booleans(self):
        if self.player_team.get_member(self.player_team.active_member_index).fainted:
            self.player_needs_to_switch = True
        if self.ai_team.get_member(self.ai_team.active_member_index).fainted:
            self.ai_needs_to_switch = True

def switch_after_fainting(switching_team: Team, switch_index, visualization = True): # Switches the active monster of a team
    if visualization:
        print(switching_team.name, "sent out", switching_team.get_member(switch_index).name + "!")
    switching_team.switch_active_member(switch_index)

def turn(player_team: Team, player_choice, ai_team: Team, ai_choice, visualization = True, rng = True): # Calculates a turn in the game. Used in the GameState class, as well as by the game when a player makes an input
    # visualize controls the visualization property of the TurnAction object, which in turn controls the visualization of the damage_calc function
    action_summaries = []
    action_list = []

    player_active_member = player_team.get_active_member()
    ai_active_member = ai_team.get_active_member()

    if player_choice > MOVE_4 and not player_choice == 10 and not player_choice == 11: # Switch if necessary
        player_turn_action = TurnAction(player_active_member, player_team, player_choice, ai_active_member, ai_team, False, visualization, can_crit = rng)
        player_turn_action.excecute_action()
        player_active_member = player_team.get_active_member() # FIXME: This is a hacky way to update the active member
    
    if ai_choice > MOVE_4 and not ai_choice == 10: # Switch if necessary
        ai_turn_action = TurnAction(ai_active_member, ai_team, ai_choice, player_active_member, player_team, True,visualization, can_crit = rng)
        ai_turn_action.excecute_action()
        ai_active_member = ai_team.get_active_member()

    if not player_choice > MOVE_4:
        player_turn_action = TurnAction(player_active_member, player_team, player_choice, ai_active_member, ai_team, False, visualization, can_crit=rng)
        action_list.append(player_turn_action)
    
    if not ai_choice > MOVE_4:
        ai_turn_action = TurnAction(ai_active_member, ai_team, ai_choice, player_active_member, player_team, True,visualization, can_crit=rng)
        action_list.append(ai_turn_action)


    if action_list: # For each pokemon, if they haven't fainted, deal damage
        action_list.sort(key=lambda x: (-x.get_action_priority()[0], -x.get_action_priority()[1]), reverse=False) # Sort based on speed tier.        
        # Execute moves
        for turn in action_list: # turn action excecuted here
            action_summaries.append(turn.excecute_action())
        if visualization:
            if player_active_member.fainted:
                print("\033[91m" + player_active_member.name + " fainted!" + "\033[0m")  # Red color for player fainting
            elif ai_active_member.fainted:
                print("\033[92m" + ai_active_member.name + " fainted!" + "\033[0m")  # Green color for AI fainting
            print()
    # Apply field effects, status effects, etc.
    return action_summaries
        
    
###################################### TURN ACTION CLASS ######################################
MOVE_EFFECTS = ["None", "Multi_Hit", "High_Crit", "Recoil", "Moderate_Recoil", "Heal_Damage", "Alter_Attack", "Alter_Defense", "Alter_Sp_Attack", "Alter_Sp_Defense", "Alter_Speed", "Alter_Accuracy", "Alter_Evasion", "Recharge", "Halve_HP", "40_Damage", "Set_Sun", "Set_Rain", "Set_Sandstorm", "Heal_Damage", "Sleep", "Freeze_Flinch", "Burn_Flinch", "Synthesis_Heal", "Charge"]
class TurnAction: # Used in turn function to organize actions that need to be taken
    def __init__(self, user: Monster, user_team: Team, uinp, target: Monster, target_team: Team, was_ai_action, visualization = True, can_crit = True) -> None:
        self.was_ai_action = was_ai_action
        self.user: Monster = user
        self.user_team = user_team
        self.uinp = uinp
        self.target = target
        self.target_team = target_team
        self.priority = self.set_priority()
        self.visualization = visualization
        self.turn_action_summary = TurnActionSummary(self.was_ai_action,input_number=uinp)
        self.can_crit = can_crit
        if self.uinp > MOVE_4:
            self.move_used = None
        else:
            self.move_used = self.user.get_move(self.uinp)
    
    def set_priority(self): # TODO
        if self.uinp <= MOVE_4:
            return self.user.get_move(self.uinp).get_priority()
        else:
            return 10 # Switching will always happen before moves (not counting Pursuit if that gets implemented)
    
    def excecute_action(self):
        if self.visualization:
            print()
        if self.uinp <= MOVE_4:
            self.turn_action_summary.record_move_as_attacking_move()
            if not self.user.fainted: # Check if user is fainted  
                # FIXME: Status conditions will need to reset taunt timers
                if self.user.status_condition == SLEEP or self.user.status_condition == FROZEN:
                    status = self.user.status_condition
                    user_woke_up_or_thawed_out = self.user.get_sleep_or_freeze_result()
                    if user_woke_up_or_thawed_out:
                        if self.visualization:
                            if status == SLEEP:
                                print(self.user_team.name + "'s " + self.user.name + " woke up!")
                            elif status == FROZEN:
                                print(self.user_team.name + "'s " + self.user.name + " thawed out!")
                        self.turn_action_summary.record_as_woke_up_or_thawed_out()
                    else:
                        if self.visualization:
                            if status == SLEEP:
                                print(self.user_team.name + "'s " + self.user.name + " is fast asleep.")
                            elif status == FROZEN:
                                print(self.user_team.name + "'s " + self.user.name + " is frozen solid!")
                        self.turn_action_summary.record_as_asleep_or_frozen()
                        if self.user.must_recharge:
                            self.user.set_recharge()
                            self.turn_action_summary.record_user_recharging()
                        return self.turn_action_summary
                if self.user.status_condition == PARALYSIS and self.can_crit:
                    if rng.randint(1,4) == 1:
                        if self.visualization:
                            print(self.user_team.name + "'s " + self.user.name + " is fully paralyzed and can't move!")
                        self.turn_action_summary.record_as_paralyzed()
                        if self.user.must_recharge:
                            self.user.set_recharge()
                            self.turn_action_summary.record_user_recharging()
                        return self.turn_action_summary 
                if self.user.is_confused:
                    user_hits_itself = self.user.get_confusion_result()
                    if user_hits_itself == SNAP_OUT_OF_CONFUSION:
                        if self.visualization:
                            print(self.user_team.name + "'s " + self.user.name + " snapped out of confusion!")
                        self.turn_action_summary.record_as_snapped_out_of_confusion()
                        self.user.is_confused = False
                    elif user_hits_itself == CONFUSED_NO_DAMAGE:
                        if self.visualization:
                            print(self.user_team.name + "'s " + self.user.name + " is confused!")
                    elif user_hits_itself == CONFUSED_DAMAGE:
                        if self.visualization:
                            print(self.user_team.name + "'s " + self.user.name + " is confused!")
                            print(self.user_team.name + "'s " + self.user.name + " hurt itself in confusion!")
                        self.do_confusion_damage()
                        self.turn_action_summary.record_as_confused()
                        return self.turn_action_summary
                if self.user.must_recharge:
                    self.user.set_recharge()
                    if self.visualization:
                        print(self.user_team.name + "'s " + self.user.name + " must recharge!") 
                    self.turn_action_summary.record_user_recharging()
                    return self.turn_action_summary            
                if self.move_used.pp == 0: # FIXME: This is running during the MTCS algorithm, but it shouldn't be
                    if self.visualization:
                        print("But it failed! Move is out of PP:",self.move_used.pp)
                    self.turn_action_summary.record_move_failed()
                    return self.turn_action_summary
                if self.visualization:
                    print(self.user_team.name + "'s " + self.user.name + " used " + self.move_used.name, end="")
                    if self.move_used.targeting == "U":
                        print("!")
                    else:
                        print(" on " + self.target.name + "!")
                
                accuracy_check = self.accuracy_check(self.move_used.accuracy)
                if not accuracy_check:
                    if self.visualization:
                        print("But it missed!")
                    self.turn_action_summary.record_as_missed()
                    self.turn_action_summary.set_damage_dealt(0)
                    return self.turn_action_summary
                effect_chance_check = self.accuracy_check(self.move_used.effect_chance)

                if self.move_used.category == 'Physical' or self.move_used.category == 'Special':
                    if self.move_used.effect == "Halve_HP":
                        damage = max(1,math.floor(self.target.HP / 2))
                        self.do_set_damage(damage)
                        return self.turn_action_summary
                    elif self.move_used.effect == "40_Damage":
                        damage = 40
                        self.do_set_damage(damage)
                        return self.turn_action_summary
                    if self.move_used.effect == "High_Crit":
                        elevated_crit_chance = float(self.move_used.effect_chance)
                        result = self.do_damage(crit_chance=elevated_crit_chance)
                    elif self.move_used.effect == "Multi_Hit": # FIXME: Multi hit moves should respond to rng constraints so MTCS is less random
                        max_hits = int(self.move_used.effect_magnitude)
                        if not self.can_crit:
                            if max_hits != 2:
                                hit_roll = 3
                            else:
                                hit_roll = 2
                        else:
                            hit_roll = rng.randint(2,max_hits)
                        result = 0
                        for i in range(hit_roll):
                            result += self.do_damage()
                        if self.visualization:
                            if hit_roll == 1:
                                print("Hit once!")
                            else:
                                print("Hit " + str(hit_roll) + " times!")
                    else: # None effect move, or move that hasn't been implemented
                        result = self.do_damage()   
                    if result:
                        if self.move_used.effect == "Moderate_Recoil":
                            recoil_result = self.moderate_recoil(result)
                            if self.visualization:
                                print(self.user_team.name + "'s " + self.user.name + " took " + str(recoil_result) + " damage from recoil!")
                        elif self.move_used.effect == "Recoil":
                            recoil_result = self.recoil(result)
                            if self.visualization:
                                print(self.user_team.name + "'s " + self.user.name + " took " + str(recoil_result) + " damage from recoil!")
                        elif self.move_used.effect == "Heal_Damage":
                            heal_percentage = self.move_used.effect_magnitude
                            self.heal_by_amount(result, heal_percentage)
                        elif "Alter" in self.move_used.effect:
                            self.alter_boosts()
                        elif self.move_used.effect == "Recharge":
                            self.user.set_recharge()
                    self.expend_pp()
                else:
                    if self.move_used.effect == "Synthesis_Heal":
                        self.synthesis_heal()
                    elif self.move_used.effect == "Heal_User":
                        heal_percentage = self.move_used.effect_magnitude
                        self.heal_by_percentage(heal_percentage)
                    elif "Alter" in self.move_used.effect: # FIXME: Theres probably a better way to do this
                        self.alter_boosts()            
                        # Special exception for Gear Shift which raises attack by one stage and speed by two stages
                    elif self.move_used.effect == "Shift_Gear":
                        self.shift_gear()
                    elif self.move_used.effect == "Taunt":
                        self.inflict_taunt() # TODO
                    elif self.move_used.effect == "Charge":
                        pass # TODO
                        if self.visualization:
                            print("Status move's effect is not implemented")
                    elif self.move_used.effect == "Reset_Stat_Changes":
                        pass # TODO
                        if self.visualization:
                            print("Status move's effect is not implemented")
                    elif self.move_used.effect == "Freeze_Flinch":
                        pass # TODO
                        if self.visualization:
                            print("Status move's effect is not implemented")
                    elif self.move_used.effect == "Confuse":
                        if not self.target.is_confused:
                            self.inflict_confusion()
                        else:
                            if self.visualization:
                                print(self.target.name + " is already confused!")
                            self.turn_action_summary.record_move_failed()
                    elif self.move_used.effect == "Paralyze":
                        if not self.target.status_condition:
                            self.inflict_status_condition(PARALYSIS)
                        else:
                            if self.visualization:
                                print("But it failed!")
                            self.turn_action_summary.record_move_failed()
                    elif self.move_used.effect == "Sleep":
                        if not self.target.status_condition: # Status condition cannot overwrite another status condition
                            self.inflict_status_condition(SLEEP)
                        else:
                            if self.visualization:
                                print("But it failed!")
                            self.turn_action_summary.record_move_failed()
                    elif self.move_used.effect == "Burn": # TODO: Implement burn damage
                        if not self.target.status_condition:
                            self.inflict_status_condition(BURN)
                        else:
                            if self.visualization:
                                print("But it failed!")
                            self.turn_action_summary.record_move_failed()
                    elif self.move_used.effect == "Poison": # TODO: Implement poison damage
                        if not self.target.status_condition:
                            self.inflict_status_condition(POISON)
                        else:
                            if self.visualization:
                                print("But it failed!")
                            self.turn_action_summary.record_move_failed()
                    elif self.move_used.effect == "Freeze":
                        if not self.target.status_condition:
                            self.inflict_status_condition(FREEZE)
                        else:
                            if self.visualization:
                                print("But it failed!")
                            self.turn_action_summary.record_move_failed()
                    elif self.move_used.effect == "Set_Hail":
                        pass
                        if self.visualization:
                            print("Status move's effect is not implemented")
                    elif self.move_used.effect == "Set_Sandstorm":
                        pass
                        if self.visualization:
                            print("Status move's effect is not implemented")
                    elif self.move_used.effect == "Set_Sun":
                        pass
                        if self.visualization:
                            print("Status move's effect is not implemented")
                    elif self.move_used.effect == "Set_Rain":
                        pass
                        if self.visualization:
                            print("Status move's effect is not implemented")
                    else:
                        if self.visualization:
                            print("Status move's effect is not implemented")
                    self.expend_pp()

            else:
                pass # Skip turn if user is fainted
        elif self.uinp == STRUGGLE:
            self.turn_action_summary.record_move_as_struggle()
            if self.visualization:
                print(self.user_team.name + "'s " + self.user.name + " used Struggle on " + self.target.name + "!")
            damage = damage_calc(self.user, self.target, self.user_team, self.target_team, Move(160), False, self.visualization)
            self.target.HP -= damage
            self.turn_action_summary.set_damage_dealt(damage)
            if self.target.HP <= 0:
                self.set_target_fainted()
            self.recoil(damage)
        else:
            try:
                if self.visualization:
                    print(self.user_team.name + " switched out " + self.user.name + " for " + self.user_team.get_member(self.uinp - 4).name + "!")
                self.user_team.switch_active_member(self.uinp - 4)
                self.turn_action_summary.record_move_as_switch()
            except:
                print("Switching error")
        return self.turn_action_summary
    
    def inflict_status_condition(self, status_condition, attack_condition = False):
        if self.target.status_condition == None and not self.target.fainted:
            if status_condition == PARALYSIS:
                self.target.set_paralysis()
            elif status_condition == BURN:
                self.target.set_burn()
            elif status_condition == POISON:
                self.target.set_poison()
            elif status_condition == SLEEP:
                self.target.set_sleep()
            elif status_condition == FREEZE:
                self.target.set_freeze()
            if self.visualization:
                if status_condition == PARALYSIS:
                    print(self.target.name + " was paralyzed!")
                elif status_condition == BURN:
                    print(self.target.name + " was burned!")
                elif status_condition == POISON:
                    print(self.target.name + " was poisoned!")
                elif status_condition == SLEEP:
                    print(self.target.name + " fell asleep!")
                elif status_condition == FREEZE:
                    print(self.target.name + " was frozen solid!")
                else:
                    print("Status condition error")
        else:
            if attack_condition: # An attacking move doesn't "fail" if it doesn't inflict a status condition
                pass
            else:
                if self.visualization:
                    print("But it failed!")
                self.turn_action_summary.record_move_failed()

    def inflict_taunt(self):
        pass
    
    def inflict_confusion(self):
        self.target.set_confused()
        if self.visualization:
            print(self.target.name + " became confused!")

    def paralyze(self, attack_condition = False): # attack_condition determines if this method is being called by an attacking or an effect move
        if self.target.status_condition == None and not self.target.fainted:
            self.target.status_condition = PARALYSIS
            if self.visualization:
                print(self.target.name + " was paralyzed!")
        else:
            if attack_condition:
                pass
            else:
                if self.visualization:
                    print("But it failed!")
                self.turn_action_summary.record_move_failed()

    def accuracy_check(self, accuracy):
        if accuracy > 100:
            return True
        elif accuracy >= rng.randint(1,100):
            return True
        else:
            return False

    def shift_gear(self):
        move_target = self.user
        alter_attack_magnitude = 1
        stat = ATTACK
        stat_name = "Attack"
        curr_boost = move_target.get_boost_for_stat(stat)
        if curr_boost + alter_attack_magnitude > 6:
            raised_amount = 6 - curr_boost
        else:
            raised_amount = alter_attack_magnitude
        move_target.set_boost_for_stat(stat, curr_boost + raised_amount)
        if self.visualization:
                    if raised_amount == 1:
                        print(move_target.name + "'s " + stat_name + " rose!")
                    elif raised_amount == 0:
                        print(move_target.name + "'s " + stat_name + " couldn't get any higher!")
                    else:
                        print("Alter_Attack_User error")
        alter_speed_magnitude = 2
        stat = SPEED
        stat_name = "Speed"
        curr_boost = move_target.get_boost_for_stat(stat)

        if curr_boost + alter_speed_magnitude > 6:
            raised_amount = 6 - curr_boost
        else:
            raised_amount = alter_speed_magnitude
        move_target.set_boost_for_stat(stat, curr_boost + raised_amount)
        if self.visualization:
            if raised_amount == 2:
                print(move_target.name + "'s " + stat_name + " rose sharply!")
            elif raised_amount == 1:
                print(move_target.name + "'s " + stat_name + " rose!")
            elif raised_amount == 0:
                print(move_target.name + "'s " + stat_name + " couldn't get any higher!")
            else:
                print("Alter_Attack_User error")

    def alter_boosts(self):
        if "User" in self.move_used.effect: # If 'User' is in the effect string, set a variable to the user
            move_target = self.user
        else: # If not, set a variable ot the target
            move_target = self.target
        # Then figure out what stats are being altered (Create a list object to store all of the stats being altered)
        alter_list = []
        if "Physical_Attack" in self.move_used.effect:
            alter_list.append(ATTACK)
        if "Special_Attack" in self.move_used.effect:
            alter_list.append(SP_ATTACK)
        if "Physical_Defense" in self.move_used.effect:
            alter_list.append(DEFENSE)
        if "Special_Defense" in self.move_used.effect:
            alter_list.append(SP_DEFENSE)
        if "Speed" in self.move_used.effect:
            alter_list.append(SPEED)
        if "Accuracy" in self.move_used.effect:
            alter_list.append(ACCURACY)
        if "Evasion" in self.move_used.effect:
            alter_list.append(EVASION)
        alter_magnitude = self.move_used.effect_magnitude
        for stat in alter_list:
            if stat == ATTACK:
                stat_name = "Attack"
            elif stat == SP_ATTACK:
                stat_name = "Special Attack"
            elif stat == DEFENSE:
                stat_name = "Defense"
            elif stat == SP_DEFENSE:
                stat_name = "Special Defense"
            elif stat == SPEED:
                stat_name = "Speed"
            elif stat == ACCURACY:
                stat_name = "Accuracy"
            elif stat == EVASION:
                stat_name = "Evasion"
            else:
                stat_name = "Error"
            curr_boost = move_target.get_boost_for_stat(stat)
            if alter_magnitude < 0:
                if curr_boost + alter_magnitude < -6:
                    raised_amount = -6 - curr_boost
                else:
                    raised_amount = alter_magnitude
                move_target.set_boost_for_stat(stat, curr_boost + raised_amount)
                # Handle printing
                if self.visualization:
                    if raised_amount == -1:
                        print(move_target.name + "'s " + stat_name + " fell!")
                    elif raised_amount == -2:
                        print(move_target.name + "'s " + stat_name + " harshly fell!")
                    elif raised_amount < 0 :
                        print(move_target.name + "'s " + stat_name + " fell by " + str(raised_amount) + " stages!")
                    elif raised_amount == 0:
                        print(move_target.name + "'s " + stat_name + " couldn't get any lower!")
                    else:
                        print("Alter_Attack_User error")
            elif alter_magnitude > 0:
                if curr_boost + alter_magnitude > 6:
                    raised_amount = 6 - curr_boost
                else:
                    raised_amount = alter_magnitude
                move_target.set_boost_for_stat(stat, curr_boost + raised_amount)
                # Handle printing
                if self.visualization:
                    if raised_amount == 1:
                        print(move_target.name + "'s " + stat_name + " rose!")
                    elif raised_amount == 2:
                        print(move_target.name + "'s " + stat_name + " sharply rose!")
                    elif raised_amount > 0:
                        print(move_target.name + "'s " + stat_name + " rose by " + str(raised_amount) + " stages!")
                    elif raised_amount == 0:
                        print(move_target.name + "'s " + stat_name + " couldn't get any higher!")
                    else:
                        print("Alter_Attack_User error")
            else:
                print("Warning: Alter effect magnitude is 0")

    def moderate_recoil(self, damage_dealt):
        damage = math.floor(damage_dealt / 4)
        self.user.HP -= damage
        if self.user.HP <= 0:
                self.set_user_fainted()
        return damage

    def recoil(self, damage_dealt):
        damage = math.floor(damage_dealt / 3)
        self.user.HP -= damage
        if self.user.HP <= 0:
                self.set_user_fainted()
        return damage

    def do_set_damage(self, damage):
        self.target.HP -= damage
        if self.visualization:
            target_hp_max = self.target.get_stat(MAX_HP)
            print(f"- {(damage / target_hp_max) * 100:.1f} %")
        self.turn_action_summary.set_damage_dealt(damage)
        if self.target.HP <= 0:
            self.set_target_fainted()

    def do_damage(self, crit_chance = DEFAULT_CRIT_CHANCE):
        type_multiplier = get_type_multiplier(self.move_used.type, self.target.type_1, self.target.type_2)
        if self.visualization:
            if type_multiplier > 1:
                print("It's super effective!", end=" ")
            elif type_multiplier == 0:
                print("It doesn't affect " + self.target.name + "...", end=" ")
            elif type_multiplier < 1:
                print("It's not very effective against " + self.target.name + "... ", end=" ")
            #print(self.target.name + " took " + str(damage) + " damage!")    
        damage = damage_calc(self.user, self.target, self.move_used, self.user_team, self.target_team, self.can_crit, self.visualization, crit_chance=crit_chance)
        if self.visualization:
            target_hp_max = self.target.get_stat(MAX_HP)
            print(f"- {(damage / target_hp_max) * 100:.1f} %")
        self.target.HP -= damage
        self.turn_action_summary.set_damage_dealt(damage)
        if self.target.HP <= 0:
            self.set_target_fainted()
        return damage

    def do_confusion_damage(self):
        # User hits themself with a move equivalent to tackle in power. Does not crit
        damage = damage_calc(self.user, self.user, Move(161), self.user_team, self.user_team, visualization=False, is_struggle=False, can_crit=False)
        self.user.HP -= damage
        if self.visualization:
            print(self.user.name + " took " + str(damage) + " damage!")
            target_hp_max = self.user.get_stat(MAX_HP)
            print(f"- {(damage / target_hp_max) * 100:.1f} %")
        if self.user.HP <= 0:
            self.set_user_fainted()
        return damage
    # FIXME: Healing should be added to the TurnActionSummary object
    def synthesis_heal(self): # FIXME: Implement weather
        heal_amount = math.floor(self.user.max_HP * 0.5)
        overheal_amount = heal_amount + self.user.HP - self.user.max_HP
        if overheal_amount < 0:
            overheal_amount = 0
        if self.visualization:
            print(self.user.name + " healed " + str(heal_amount - overheal_amount) + " HP!")
        self.user.HP += heal_amount
        if overheal_amount > 0:
            self.user.HP = self.user.max_HP

    def heal_by_percentage(self,percentage):
        heal_amount = math.floor(self.user.max_HP * (percentage / 100))
        overheal_amount = heal_amount + self.user.HP - self.user.max_HP
        if overheal_amount < 0:
            overheal_amount = 0
        if self.visualization:
            print(self.user.name + " healed " + str(heal_amount - overheal_amount) + " HP!")
        self.user.HP += heal_amount
        if overheal_amount > 0:
            self.user.HP = self.user.max_HP

    def heal_by_amount(self, damage_dealt, heal_percentage):
        heal_amount = math.floor(damage_dealt * (heal_percentage / 100))
        overheal_amount = heal_amount + self.user.HP - self.user.max_HP
        if overheal_amount < 0:
            overheal_amount = 0
        if self.visualization:
            if heal_amount > 0:
                print(self.user.name + " healed " + str(heal_amount - overheal_amount) + " HP!")
        self.user.HP += heal_amount
        if overheal_amount > 0:
            self.user.HP = self.user.max_HP

    def set_user_fainted(self):
        self.user.fainted = True
        self.user.not_fainted = False
        self.user.HP = 0
        self.turn_action_summary.record_fainted_user()

    def set_target_fainted(self):
        self.target.fainted = True
        self.target.not_fainted = False
        self.target.HP = 0
        self.turn_action_summary.record_fainted_target()

    def expend_pp(self): # FIXME: How will pressure work?
        self.move_used.expend_pp()

    def get_action_priority(self): # Priority is a tuple of (speed, priority)
        return (self.priority, self.user.get_experienced_stat(SPEED))

class TurnActionSummary:
    def __init__(self,was_ai_action,damage_dealt = 0,was_switch_after_faint = False, input_number = 0) -> None:
        self.input_number = input_number
        self.was_ai_action = was_ai_action
        self.damage_dealt = damage_dealt
        self.user_missed = False
        self.move_failed = False
        self.move_was_not_very_effective = False
        self.was_effect_move = False
        self.was_attacking_move = False
        self.was_switch = False
        self.was_struggle = False
        self.was_switch_after_faint = was_switch_after_faint
        self.target_fainted = False
        self.user_fainted = False
        self.user_had_to_recharge = False
        self.user_was_fully_paralyzed = False
        self.user_was_asleep_or_frozen = False
        self.move_effect_proced = False
        self.move_crit = False
        self.user_hits_itself = False
        self.user_snapped_out_of_confusion = False
        self.user_woke_up_or_thawed_out = False

    def __str__(self) -> str:
        return f"Input number: {self.input_number}\nWas AI action: {self.was_ai_action}\nDamage dealt: {self.damage_dealt}\nUser missed: {self.user_missed}\nMove failed: {self.move_failed}\nMove was not very effective: {self.move_was_not_very_effective}\nWas effect move: {self.was_effect_move}\nWas attacking move: {self.was_attacking_move}\nWas switch: {self.was_switch}\nWas struggle: {self.was_struggle}\nWas switch after faint: {self.was_switch_after_faint}\nTarget fainted: {self.target_fainted}\nUser fainted: {self.user_fainted}\n"

    def user_attacked_and_did_no_damage(self):
        if self.was_attacking_move and self.damage_dealt == 0:
            return True
        return False

    def record_as_confused(self):
        self.user_hits_itself = True
        self.move_failed = True

    def record_as_asleep_or_frozen(self):
        self.user_was_asleep_or_frozen = True
        self.move_failed = True

    def record_as_snapped_out_of_confusion(self):
        self.user_snapped_out_of_confusion = True

    def record_as_woke_up_or_thawed_out(self):
        self.user_woke_up_or_thawed_out = True

    def record_move_effect_as_successful(self):
        self.move_effect_proced = True

    def record_as_paralyzed(self):
        self.user_was_fully_paralyzed = True

    def record_user_recharging(self):
        self.user_had_to_recharge = True

    def record_move_failed(self):
        self.move_failed = True

    def record_as_not_very_effective(self):
        self.move_was_not_very_effective = True

    def record_as_missed(self):
        self.user_missed = True
        self.move_failed = True

    def record_fainted_target(self):
        self.target_fainted = True
    
    def record_fainted_user(self):
        self.user_fainted = True

    def record_move_as_attacking_move(self):
        self.was_attacking_move = True
        self.was_effect_move = False
        self.was_switch = False
        self.was_struggle = False
    
    def record_move_as_effect_move(self):
        self.was_attacking_move = False
        self.was_effect_move = True
        self.was_switch = False
        self.was_struggle = False
    
    def record_move_as_switch(self):
        self.was_attacking_move = False
        self.was_effect_move = False
        self.was_switch = True
        self.was_struggle = False

    def record_move_as_struggle(self):
        self.was_attacking_move = False
        self.was_effect_move = False
        self.was_switch = False
        self.was_struggle = True

    def set_damage_dealt(self, damage_dealt):
        self.damage_dealt = damage_dealt

class FieldEffects:
    def __init__(self, player_team, ai_team, visualization = False) -> None:
        self.SUN = 0
        self.RAIN = 1
        self.SANDSTORM = 2
        self.HAIL = 3
        self.current_weather = None
        self.current_weather_timer = 0
        self.player_team = player_team
        self.ai_team = ai_team
        self.visualization = visualization
        pass

    def excecute_effects(self):
        pass

    def set_weather(self, weather):
        if weather == self.SUN:
            self.current_weather = self.SUN
        elif weather == self.RAIN:
            self.current_weather = self.RAIN
        elif weather == self.SANDSTORM:
            self.current_weather = self.SANDSTORM
        elif weather == self.HAIL:
            self.current_weather = self.HAIL

    def get_weather_multiplier(self, move_type):
        pass

    def increment_weather_timer(self):
        if self.current_weather_timer > 0:
            self.current_weather_timer -= 1
            if self.current_weather_timer == 0:
                if self.visualization:
                    if self.current_weather == self.SUN:
                        print("The sunlight faded.")
                    elif self.current_weather == self.RAIN:
                        print("The rain stopped.")
                    elif self.current_weather == self.SANDSTORM:
                        print("The sandstorm subsided.")
                    elif self.current_weather == self.HAIL:
                        print("The hail stopped.")
                self.current_weather = None
            else:
                if self.visualization:
                    if self.current_weather == self.SUN:
                        print("The sunlight is strong.")
                    elif self.current_weather == self.RAIN:
                        print("Rain continues to fall.")
                    elif self.current_weather == self.SANDSTORM:
                        print("The sandstorm rages.")
                    elif self.current_weather == self.HAIL:
                        print("Hail continues to fall.")
        else:
            pass
    
    def activate_status_damage(self):
        pass

class FieldEffectsSummary:
    def __init__(self) -> None:
        pass

if __name__ == "__main__":
    TestTeam = Team("TestTeam")
    TestTeam.add_member(Monster(501, 50))
    TestTeam2 = Team("TestTeam2")
    TestTeam2.add_member(Monster(501, 51))
    print(does_first_team_win_matchup(TestTeam, TestTeam2))
