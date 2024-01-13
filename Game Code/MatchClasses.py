import random as rng
from GameMenus import *
from MoveClasses import Move
from MonsterClass import * # Monster class, constants, nature dictionary
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

# Game Constants
MAX_TEAM_SIZE = 6
UNOVA_LOWER_BOUND = 494
UNOVA_UPPER_BOUND = 649
TYPE_CHART = {'Normal':{'Normal':1, 'Fire':1, 'Water':1, 'Electric':1, 'Grass':1, 'Ice':1, 'Fighting':2, 'Poison':1, 'Ground':1, 'Flying':1, 'Psychic':1, 'Bug':1, 'Rock':1, 'Ghost':0, 'Dragon':1, 'Dark':1, 'Steel':1, 'Fairy':1, 'Typeless':1},
              'Fire':{'Normal':1, 'Fire':0.5, 'Water':0.5, 'Electric':1, 'Grass':2, 'Ice':2, 'Fighting':1, 'Poison':1, 'Ground':1, 'Flying':1, 'Psychic':1, 'Bug':2, 'Rock':0.5, 'Ghost':1, 'Dragon':0.5, 'Dark':1, 'Steel':2, 'Fairy':1, 'Typeless':1},
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

class Team:
    def __init__(self, name="Team") -> None:
        self.name = name
        self.team_members = []
        self.team_size = 0
        self.team_level = 1
        self.team_members_healthy = 0
        self.active_member_index = 0
        self.active_member_attack_multiplier = 1
        self.active_member_defense_multiplier = 1
        self.active_member_special_attack_multiplier = 1
        self.active_member_special_defense_multiplier = 1
        self.active_member_speed_multiplier = 1
        self.active_member_accuracy_multiplier = 1
        self.active_member_evasion_multiplier = 1

    def add_member(self, monster):
        if self.team_size <= MAX_TEAM_SIZE:
            self.team_members.append(monster)
            self.team_size += 1
            self.update_team_members_healthy()
            return 0
        else:
            print("Team is full")
            return 1
    
    def pop_member(self, index):
        if index < self.team_size:
            self.team_size -= 1
            return self.team_members.pop(index)
        else:
            print("pop_member error: index out of range")
            return -1

    def get_member(self, index):
        if index < self.team_size:
            return self.team_members[index]
        else:
            print("get_member error: index out of range")
            print("Index: " + str(index))
            print("Team size: " + str(self.team_size))

    def get_active_member(self):
        return self.team_members[self.active_member_index]

    def has_non_fainted_members(self):
        self.update_team_members_healthy()
        return self.team_members_healthy > 0

    def update_team_members_healthy(self):
        self.team_members_healthy = 0
        for monster in self.team_members:
            if not monster.fainted:
                self.team_members_healthy += 1

    def change_monster_order_in_team(self, index1, index2):
        if index1 < self.team_size and index2 < self.team_size:
            temp = self.team_members[index1]
            self.team_members[index1] = self.team_members[index2]
            self.team_members[index2] = temp
        else:
            print("Index out of range")
    
    def switch_active_member(self, index, reset_boosts = True):
        if index in self.get_list_of_valid_switch_indices():
            self.active_member_index = index
            if reset_boosts:
                self.reset_boosts()
        else:
            print(self.name, " switch_active_member error: invalid switch index: " , index)

    def get_number_of_members_to_switch_to(self):
        return self.team_members_healthy - 1
    
    def get_list_of_member_names_to_switch_to(self):
        member_names = []
        for i in range(self.team_size):
            if i != self.active_member_index and not self.team_members[i].fainted:
                member_names.append(self.team_members[i].name)
        return member_names

    def get_initial_active_member_index(self):
        for i in range(self.team_size):
            if not self.team_members[i].fainted:
                return i
        return -1

    def get_list_of_valid_switch_indices(self):
        valid_indices = []
        for i in range(self.team_size):
            if i != self.active_member_index and not self.team_members[i].fainted:
                valid_indices.append(i)
        return valid_indices
    
    def reset_boosts(self):
        self.active_member_attack_multiplier = 1
        self.active_member_defense_multiplier = 1
        self.active_member_special_attack_multiplier = 1
        self.active_member_special_defense_multiplier = 1
        self.active_member_speed_multiplier = 1
        self.active_member_accuracy_multiplier = 1
        self.active_member_evasion_multiplier = 1


    def is_active_member_fainted(self):
        return self.team_members[self.active_member_index].fainted
    
    def deep_copy(self):
        new_team = Team()
        new_team.name = self.name
        new_team.active_member_index = self.active_member_index
        new_team.team_level = self.team_level
        new_team.team_members_healthy = self.team_members_healthy
        for monster in self.team_members:
            new_team.add_member(monster.deep_copy())
        new_team.team_size = self.team_size
        return new_team

def damage_calc(user, target, move: Move, user_team, target_team, can_crit = True, visualization = True, is_struggle = False):
    if can_crit:
        roll = rng.randint(1,16)
        # One in 16 chance of critical hit
        if roll == 16:
            crit_mult = 1.5
            if visualization:
                print("Critical hit!")
        else:
            crit_mult = 1
    else:
        crit_mult = 1
    if is_struggle:
        stab_mult = 1
        type_mult = 1
        power = 50
        used_attack = user.attack
        used_defense = target.defense
        raw_calc = ((((2*user.level / 5 + 2) * move.base_power * (used_attack / used_defense)) / 50) + 2)
        multiplier_calc = raw_calc * crit_mult * stab_mult * type_mult
        return math.ceil(multiplier_calc)
    if move.type == user.type_1 or move.type == user.type_2:
        stab_mult = 1.5
    else:
        stab_mult = 1 # Same type attack bonus
    type_mult = 1
    type_mult *= TYPE_CHART[move.type][target.type_1]
    if target.type_2:
        type_mult *= TYPE_CHART[move.type][target.type_2]
    if visualization:
        if type_mult > 1:
            print("It's super effective!")
        elif type_mult == 0:
            print("It doesn't affect " + target.name + "...")
        elif type_mult < 1:
            print("It's not very effective...")
    if move.category == 'Physical':
        used_attack = user.attack
        used_attack_multiplier = user_team.active_member_attack_multiplier
        used_defense = target.defense
        used_defense_multiplier = target_team.active_member_defense_multiplier
    elif move.category == 'Special':
        used_attack = user.special_attack
        used_attack_multiplier = user_team.active_member_special_attack_multiplier
        used_defense = target.special_defense
        used_defense_multiplier = target_team.active_member_special_defense_multiplier
    else:
        if visualization:
            print("damage_calc error: calling damage_calc() on an effect move. Returning 0")
        return 0    
    raw_calc = ((((2*user.level / 5 + 2) * move.base_power * (used_attack / used_defense)) / 50) + 2)
    multiplier_calc = (raw_calc * crit_mult * stab_mult * type_mult * used_attack_multiplier) / used_defense_multiplier
    return math.ceil(multiplier_calc)

    # return math.ceil(((((2*attacker.level / 5 + 2) * crit_mult * base_power * (used_Attack / used_Defense)) / 50) + 2)) * typechart[typedict[attacker.type]][typedict[defender.type]] * typechart[typedict[attacker.type]][typedict[defender.type_2]]

def generated_monster(id = 0, level_parameter = 1): #TODO: Implement monster generation
    if id == -1:
        monster_id = rng.randint(UNOVA_LOWER_BOUND,UNOVA_UPPER_BOUND)
    else:
        monster_id = id
    if level_parameter > 0 and level_parameter < 101:
        level = level_parameter
    else:
        print("Invalid level parameter, setting to 1")
        level = 1
    monster = Monster(monster_id, level)
    # Create a randomly generated monster
    # Return the monster
    return monster

class GameState():
    def __init__(self, player_team, ai_team, turn_count = 0, last_move = 0) -> None:
        self.player_team = player_team
        self.player_needs_to_switch = self.player_team.is_active_member_fainted()
        self.ai_team = ai_team
        self.ai_needs_to_switch = self.ai_team.is_active_member_fainted()
        self.turn_count = turn_count
        self.last_move = last_move
        self.game_over = self.is_game_over()
        self.winner = None
        self.last_turn_summary = None
        self.policy_rating = self.calculate_policy_rating()
    
    def __str__(self) -> str:
        return f"Player team: {self.player_team}\nAI team: {self.ai_team}\nTurn count: {self.turn_count}\nLast move: {self.last_move}\nGame over: {self.game_over}\nWinner: {self.winner}\nPolicy rating: {self.policy_rating}"

    def is_game_over(self):
        if self.player_team.has_non_fainted_members() and self.ai_team.has_non_fainted_members():
            return False
        else:
            self.game_over = True
            return True
        
    def did_elimination_occur_and_ai_caused_it(self): # May be a redundant function
        if self.did_ai_win_a_matchup() and self.did_elimination_occur():
            return True
        else:
            return False
    
    def did_ai_win_a_matchup(self):
        if not self.last_turn_summary:
            return False
        else:
            for action in self.last_turn_summary:
                if action.was_ai_action and action.target_fainted: # Potential bug with precedence checking.
                    return True
                elif not action.was_ai_action and action.user_fainted:
                    return False
            return False
        # Conditions to win matchup:
    
    def did_elimination_occur(self):
        if not self.last_turn_summary:
            return False
        for action in self.last_turn_summary:
            # If the action was an opponent switching in after fainting, return true
            if action.target_fainted:
                return True

    def did_ai_win(self):
        if self.is_game_over():
            return self.ai_team.has_non_fainted_members()
        else:
            return False
    
    def get_ai_possible_actions(self):
        if self.ai_needs_to_switch: # If ai needs to switch, return list of inputs representing every valid switch the AI can perform
            list_of_ai_choices = []
            valid_switch_indices = self.ai_team.get_list_of_valid_switch_indices()
            for i in valid_switch_indices:
                append_state = GameState(self.player_team.deep_copy(), self.ai_team.deep_copy(), self.turn_count).advance_game(i + 4) # 
                list_of_ai_choices.append(append_state)
            return list_of_ai_choices
        
        elif self.player_needs_to_switch: # Switch Player monster, then return new state in the list
            list_of_ai_choices = []
            valid_switch_indices = self.player_team.get_list_of_valid_switch_indices()
            for i in valid_switch_indices:
                append_state = GameState(self.player_team.deep_copy(), self.ai_team.deep_copy(), self.turn_count).advance_game(0, i + 4) # 0, 1, 2, 3, are move choices
                list_of_ai_choices.append(append_state)
            return list_of_ai_choices
        
        else: # If no team needs to switch: return list of inputs representing every valid move and switch the AI can perform
            list_of_ai_choices = []
            # Alter ai_moves to be a list of valid moves
            '''ai_switches = self.ai_team.get_list_of_valid_switch_indices()
            for i in range(len(ai_switches)):
                ai_switches[i] += 4 # Convert switch indices to switch inputs'''
            ai_switches = []
            ai_moves_list = self.ai_team.get_member(self.ai_team.active_member_index).get_list_of_valid_move_numbers()
            ai_combination_list = ai_moves_list + ai_switches
            # Alter player_moves to be a list of valid moves
            player_moves_list = self.player_team.get_member(self.player_team.active_member_index).get_list_of_valid_move_numbers()
            for i in ai_combination_list: # Get all 2-16 combinations of moves
                for j in player_moves_list:
                    # Check if the move combination is valid (Neither move has 0 pp)
                    append_state = GameState(self.player_team.deep_copy(), self.ai_team.deep_copy(), self.turn_count).advance_game(i, j) # 0, 1, 2, 3, are move choices
                    list_of_ai_choices.append(append_state)
            # FIXME: Implement voluntary switching (switching to a better matchup)
            if len(list_of_ai_choices) == 0:
                print("No possible moves")
            return list_of_ai_choices
   
    def advance_game(self, ai_choice, player_choice = 0): # Simulates moving game forward. Will flip switch booleans and if both are False, will run turn
        if self.ai_needs_to_switch  and not self.is_game_over(): # If ai needs to switch, change the active monster according to the ai_choice
            self.ai_team.switch_active_member(ai_choice - 4) 
            self.ai_needs_to_switch = False
            self.last_turn_summary = [TurnActionSummary(was_ai_action=True,was_switch_after_faint=True)]
        elif self.player_needs_to_switch and not self.is_game_over(): # If player needs to switch, change the active monster according to the player_choice
            if player_choice == self.player_team.team_size:
                print("Player choice is out of range")
                print("Debug variables: player_choice: " + str(player_choice) + " ai_choice: " + str(ai_choice))
            switch_after_fainting(self.player_team, player_choice - 4, False)
            self.player_needs_to_switch = False
            self.last_turn_summary = [TurnActionSummary(was_ai_action=False,was_switch_after_faint=True)]
        else: # If no one needs to switch, run turn with inputs according to the ai_choice and player_choice
            visualization = False
            self.last_turn_summary = turn(self.player_team, player_choice, self.ai_team, ai_choice, visualization) # Teams passed by reference, will be altered by turn function
            self.update_team_needs_to_switch_booleans() # The line that saved the world
            self.is_game_over()
            self.turn_count += 1 # If ran turn, increment turn counter and check if game is over
        self.last_move = ai_choice
        return self

    def calculate_policy_rating(self):
        policy_rating = 0
        if self.player_needs_to_switch: # If a player monster has fainted, increase policy_rating by 1
            policy_rating += 1
        if self.ai_needs_to_switch: # If an ai monster is fainted, decrease policy_rating by 1
            policy_rating -= 1

        if self.last_turn_summary: # If a turn was run, calculate the matchup strength of the active monsters, add that to policy rating
            for action in self.last_turn_summary:
                if action.was_ai_action and action.user_attacked_and_did_no_damage():
                    policy_rating -= 1

        if self.game_over and self.did_ai_win(): # If the node is a victory for the AI, policy rating is 100
            policy_rating = 100
        elif self.game_over and not self.did_ai_win(): # If the node is a victory for the player, policy rating is -100
            policy_rating = -100

        return policy_rating 

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
        print(switching_team.get_member(switch_index).name + " switched out for " + switching_team.get_active_member().name)
    switching_team.switch_active_member(switch_index)

def turn(player_team: Team, player_choice, ai_team: Team, ai_choice, visualization = True): # Calculates a turn in the game. Used in the GameState class. Not game agnostic.
    # visualize controls the visualization property of the TurnAction object, which in turn controls the visualization of the damage_calc function
    action_summaries = []
    action_list = []

    player_active_member = player_team.get_active_member()
    ai_active_member = ai_team.get_active_member()

    if player_choice > MOVE_4 and not player_choice == 10: # Switch if necessary
        player_turn_action = TurnAction(player_active_member, player_team, player_choice, ai_active_member, ai_team, False, visualization)
        player_turn_action.excecute_action()
        player_active_member = player_team.get_active_member() # FIXME: This is a hacky way to update the active member
    
    if ai_choice > MOVE_4 and not ai_choice == 10: # Switch if necessary
        ai_turn_action = TurnAction(ai_active_member, ai_team, ai_choice, player_active_member, player_team, True,visualization)
        ai_turn_action.excecute_action()
        ai_active_member = ai_team.get_active_member()

    if not player_choice > MOVE_4:
        player_turn_action = TurnAction(player_active_member, player_team, player_choice, ai_active_member, ai_team, False, visualization)
        action_list.append(player_turn_action)
    
    if not ai_choice > MOVE_4:
        ai_turn_action = TurnAction(ai_active_member, ai_team, ai_choice, player_active_member, player_team, True,visualization)
        action_list.append(ai_turn_action)


    if action_list: # For each pokemon, if they haven't fainted, deal damage
        action_list.sort(key=lambda x: (-x.get_action_priority()[0], -x.get_action_priority()[1]), reverse=False) # Sort based on speed tier.        
        # Execute moves
        for turn in action_list: # turn action excecuted here
            action_summaries.append(turn.excecute_action())
        if visualization:
            if player_active_member.fainted:
                print(player_active_member.name + " fainted")
            elif ai_active_member.fainted:
                print(ai_active_member.name + " fainted")
            print()
    return action_summaries
        # If there is a speed tie, flip a coin to determine order
        # Apply field effects, status effects, etc.
    

class TurnAction: # Used in turn function to organize actions that need to be taken
    def __init__(self, user, user_team, uinp, target, target_team, was_ai_action, visualization = True) -> None:
        self.was_ai_action = was_ai_action
        self.user = user
        self.user_team = user_team
        self.uinp = uinp
        self.target = target
        self.target_team = target_team
        self.priority = self.set_priority()
        self.visualization = visualization
        self.turn_action_summary = TurnActionSummary(self.was_ai_action)
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
        if self.uinp <= MOVE_4:
            self.turn_action_summary.record_move_as_attacking_move()
            if not self.user.fainted: # Check if user is fainted                
                if self.move_used.pp == 0:
                    print("But it failed! Move is out of PP:",self.move_used.pp)
                    self.turn_action_summary.record_move_failed()
                    return self.turn_action_summary
                if self.visualization:
                    print(self.user_team.name + "'s " + self.user.name + " used " + self.move_used.name, end="")
                    if self.move_used.targeting == "U":
                        print("!")
                    else:
                        print(" on " + self.target.name + "!")
                
                if self.move_used.category == 'Physical' or self.move_used.category == 'Special':
                    result = self.do_damage()
                    if result: # If the move misses, no effect should occur
                        if self.move_used.effect == "Recoil":
                            recoil_result = self.recoil(result)
                            if self.visualization:
                                print(self.user_team.name + "'s " + self.user.name + " took " + str(recoil_result) + " damage from recoil!")
                    self.expend_pp()
                else:
                    if self.move_used.effect == "Synthesis_Heal":
                        self.synthesis_heal()
                    elif self.move_used.effect == "Alter_Attack_User": # FIXME: Handle lowering stats
                        if self.user_team.active_member_attack_multiplier < 4 or self.user_team.active_member_attack_multiplier > 0:
                            self.user_team.active_member_attack_multiplier += self.move_used.effect_magnitude / 2
                            if self.visualization:
                                if self.move_used.effect_magnitude > 0:
                                    print(self.user_team.name + "'s " + self.user.name + "'s attack rose by " + str(self.move_used.effect_magnitude) + " stages!")
                                if self.move_used.effect_magnitude < 0:
                                    print(self.user_team.name + "'s " + self.user.name + "'s attack fell by " + str(self.move_used.effect_magnitude) + " stages!")
                    elif self.move_used.effect == "Alter_Defense_User":
                        self.user_team.active_member_defense_multiplier += self.move_used.effect_magnitude / 2
                        if self.visualization:
                            if self.move_used.effect_magnitude > 0:
                                print(self.user_team.name + "'s " + self.user.name + "'s defense rose by " + str(self.move_used.effect_magnitude) + " stages!")
                            if self.move_used.effect_magnitude < 0:
                                print(self.user_team.name + "'s " + self.user.name + "'s defense fell by " + str(self.move_used.effect_magnitude) + " stages!")
                    elif self.move_used.effect == "Alter_Special_Attack_User":
                        self.user_team.active_member_special_attack_multiplier += self.move_used.effect_magnitude / 2
                        if self.visualization:
                            if self.move_used.effect_magnitude > 0:
                                print(self.user_team.name + "'s " + self.user.name + "'s special attack rose by " + str(self.move_used.effect_magnitude) + " stages!")
                            if self.move_used.effect_magnitude < 0:
                                print(self.user_team.name + "'s " + self.user.name + "'s special attack fell by " + str(self.move_used.effect_magnitude) + " stages!")
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
            damage = damage_calc(self.user, self.target, self.user_team, self.target_team, Move(157), False, self.visualization)
            self.target.HP -= damage
            self.turn_action_summary.set_damage_dealt(damage)
            if self.target.HP <= 0:
                self.target.not_fainted = False
                self.target.fainted = True
                self.target.HP = 0
                self.turn_action_summary.record_fainted_target()
            self.recoil(damage)
        else:
            try:
                if self.visualization:
                    print(self.user.name + " switched out for " + self.user_team.get_member(self.uinp - 4).name)
                self.user_team.switch_active_member(self.uinp - 4)
                self.turn_action_summary.record_move_as_switch()
            except:
                print("Switching error")
        return self.turn_action_summary
    
    def recoil(self, damage_dealt):
        damage = math.floor(damage_dealt / 3)
        self.user.HP -= damage
        if self.user.HP <= 0:
                self.user.not_fainted = False
                self.user.fainted = True
                self.user.HP = 0
                self.turn_action_summary.record_fainted_user()
        return damage

    def do_damage(self):
        damage = damage_calc(self.user, self.target, self.move_used, self.user_team, self.target_team, False, self.visualization)
        if self.move_used.accuracy >= rng.randint(1,100):
            if self.visualization:
                print(self.target.name + " took " + str(damage) + " damage!")
            self.target.HP -= damage
            self.turn_action_summary.set_damage_dealt(damage)
            if self.target.HP <= 0:
                self.target.not_fainted = False
                self.target.fainted = True
                self.target.HP = 0
                self.turn_action_summary.record_fainted_target()
        else:
            if self.visualization:
                print("The attack missed!")
            damage = 0
            self.turn_action_summary.set_damage_dealt(damage)
            self.turn_action_summary.record_as_missed()
        return damage

    def synthesis_heal(self):
        heal_amount = math.floor(self.user.max_HP * 0.5)
        overheal_amount = heal_amount + self.user.HP - self.user.max_HP
        if overheal_amount < 0:
            overheal_amount = 0
        if self.visualization:
            print(self.user.name + " healed " + str(heal_amount - overheal_amount) + " HP!")
        self.user.HP += heal_amount
        if overheal_amount > 0:
            self.user.HP = self.user.max_HP

    def expend_pp(self): # FIXME: How will pressure work?
        self.move_used.expend_pp()

    def get_action_priority(self): # Priority is a tuple of (speed, priority)
        return (self.priority, self.user.speed)

class TurnActionSummary:
    def __init__(self,was_ai_action,damage_dealt = 0,was_switch_after_faint = False) -> None:
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

    def user_attacked_and_did_no_damage(self):
        if self.was_attacking_move and self.damage_dealt == 0:
            return True
        return False

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



# ------------- GRAPH CLASSES -------------
def weighted_random_choice(choices, weights):
    total_weight = sum(weights)
    random_num = rng.random() * total_weight
    for choice, weight in zip(choices, weights):
        if random_num < weight:
            return choice
        random_num -= weight
    return choice

class Location:
    def __init__(self, location_type):
        self.location_type = location_type
        self.pokemon_roster = []
        self.item_roster = []
        self.trainer_roster = []
    
    def __str__(self):
        return self.location_type

class GraphNode:
    def __init__(self, location_type, distance_from_center) -> None:
        self.location_type = Location(location_type)
        self.neighbors = []
        self.visited = False
        self.distance_from_center = distance_from_center
    
class Graph:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        center_x, center_y = width // 2, height // 2
        self.nodes = [[self.create_node(i, j, center_x, center_y) for j in range(min(i+1 if i < width else 2*width-i-1, width))] for i in range(2*height-1)]
        self.nodes[-1][-1].location_type = 'gym'  # Make the final node a gym
        self.connect_nodes()
        self.current_position = self.nodes[0][0]

    def create_node(self, i, j, center_x, center_y):
        distance_from_center = ((center_x - i)**2 + (center_y - j)**2)**0.5
        location_type = self.select_location_type(distance_from_center)
        return GraphNode(location_type, distance_from_center)

    def select_location_type(self, distance_from_center):
        choices = ['town', 'road', 'city', 'grassland', 'cave', 'lake']
        if distance_from_center <= 1:
            weights = [0.3, 0.35, 0.2, 0.1, 0, 0.05]
        elif distance_from_center <= 2:
            weights = [0.1, 0.1, 0.1, 0.4, 0.1, 0.2]
        else:
            weights = [0.05, 0.1, 0, 0.4, 0.3, 0.15]
        return weighted_random_choice(choices, weights)

    def connect_nodes(self):
        for i in range(len(self.nodes) - 1):  # No need to connect the last row
            for j in range(len(self.nodes[i])):
                # Connect to the node directly in front, if it exists
                if j < len(self.nodes[i+1]):
                    self.nodes[i][j].neighbors.append(self.nodes[i+1][j])
                # Connect to the node to the right in the next row, if it exists
                if j + 1 < len(self.nodes[i+1]):
                    self.nodes[i][j].neighbors.append(self.nodes[i+1][j+1])
                # Connect to the node to the left in the next row, if it exists
                if j - 1 >= 0:
                    self.nodes[i][j].neighbors.append(self.nodes[i+1][j-1])

    def list_adjacent_nodes(self):
        for neighbor in self.current_position.neighbors:
            ni = next(i for i, row in enumerate(self.nodes) if neighbor in row)
            nj = self.nodes[ni].index(neighbor)
            print(f'Adjacent node: {ni},{nj} ({neighbor.location_type}, distance from center: {neighbor.distance_from_center})')

    def move_to(self, i, j):
        if self.nodes[i][j] in self.current_position.neighbors:
            self.current_position = self.nodes[i][j]
        else:
            print('Cannot move to a node that is not connected to the current position.')

    def print_graph(self):
        for i, row in enumerate(self.nodes):
            for j, node in enumerate(row):
                print(f'Node {i},{j} ({node.location_type}, distance from center: {node.distance_from_center}):', end=' ')
                for neighbor in node.neighbors:
                    ni = next(i for i, row in enumerate(self.nodes) if neighbor in row)
                    nj = self.nodes[ni].index(neighbor)
                    print(f'{ni},{nj}', end=' ')
                print() 

# ------------- UNIMPLEMENTED CLASSES -------------
class Item:
    def __init__(self) -> None:
        pass

class Bag:
    def __init__(self) -> None:
        pass

class Map: # Will store information about the map such as players size, the map itself, etc.
    def __init__(self) -> None:
        pass     

class Game:
    def __init__(self) -> None:
        self.player = Player()
        self.map = Map()
        self.game_over = False
        self.winner = None

class Player: # General player class. Used to keep bag, team, and other attributes together

    def __init__(self) -> None:
        self.name = "Player"
        self.team = Team()
        self.bag = Bag()
    
    def add_monster_to_team(self, monster):
        add = self.team.add_member(monster)
        if add == 0:
            print("Added monster to team")
            # TODO: update pokedex

class Trainer: # Class that will store AI player information.
    def __init__(self) -> None:
        self.name = "Trainer"
        self.team = Team()

    def generate_trainer(self):
        pass

    def generate_trainer_from_template(self):
        pass