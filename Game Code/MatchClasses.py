import random as rng
from GameMenus import *
from MoveClasses import Move
from MonsterClass import * # Monster class, constants, nature dictionary
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

def damage_calc(user, target, move: Move, user_team, target_team, can_crit = True, visualization = True, is_struggle = False, crit_chance = DEFAULT_CRIT_CHANCE):
    if can_crit:
        roll = rng.randint(1,100)
        #if visualization:
        #    print("Roll: " + str(roll))
        #    print("Crit chance: " + str(crit_chance))
        # One in 24 chance of critical hit
        if roll < crit_chance:
            crit_mult = CRIT_MULTIPLIER
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
        stab_mult = STAB_MULTIPLIER
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
        used_attack_multiplier = user.get_multiplier_for_stat(ATTACK)
        used_defense = target.defense
        if crit_mult == CRIT_MULTIPLIER and target.get_multiplier_for_stat(DEFENSE) > 0: # Critical hits negate defense boosts/drops
            used_defense_multiplier = 1
        else:
            used_defense_multiplier = target.get_multiplier_for_stat(DEFENSE)
    elif move.category == 'Special':
        used_attack = user.special_attack
        used_attack_multiplier = user.get_multiplier_for_stat(SP_ATTACK)
        used_defense = target.special_defense
        if crit_mult == CRIT_MULTIPLIER and target.get_multiplier_for_stat(SP_DEFENSE) > 0: # Critical hits negate defense boosts/drops
            used_defense_multiplier = 1
        else:
            used_defense_multiplier = target.get_multiplier_for_stat(SP_DEFENSE)
    else:
        if visualization:
            print("damage_calc error: calling damage_calc() on an effect move. Returning 0")
        return 0    
    raw_calc = ((((2*user.level / 5 + 2) * move.base_power * (used_attack / used_defense)) / 50) + 2)
    multiplier_calc = (raw_calc * crit_mult * stab_mult * type_mult * used_attack_multiplier) / used_defense_multiplier
    return math.ceil(multiplier_calc)

class GameState():
    def __init__(self, player_team, ai_team, turn_count = 0, last_move = 0) -> None:
        self.player_team = player_team
        self.player_needs_to_switch = self.player_team.is_active_member_fainted()
        self.ai_team = ai_team
        self.ai_needs_to_switch = self.ai_team.is_active_member_fainted()
        self.ai_has_switched_after_fainting = False
        self.turn_count = turn_count
        self.last_move = last_move
        self.game_over = self.is_game_over()
        self.winner = None
        self.last_turn_summary = None
        self.policy_rating = self.calculate_policy_rating()
    
    def __str__(self) -> str:
        return f"Player team: {self.player_team}\nAI team: {self.ai_team}\nTurn count: {self.turn_count}\nLast move: {self.last_move}\nGame over: {self.game_over}\nWinner: {self.winner}\nPolicy rating: {self.policy_rating}"

    def calculate_policy_rating(self):
        policy_rating = 0
        if self.player_needs_to_switch: # If a player monster has fainted, increase policy_rating by 1
            policy_rating += 1
        if self.ai_needs_to_switch: # If an ai monster is fainted, decrease policy_rating by 1
            policy_rating -= 1
        if self.last_turn_summary: # Increase policy rating depending on the amount of damage dealt to the active player monster. Prevents throwing in unwinnable situations
            for action in self.last_turn_summary:
                if action.was_ai_action:
                    policy_rating += action.damage_dealt / self.player_team.get_active_member().get_stat(MAX_HP)
                elif not action.was_ai_action:
                    policy_rating -= action.damage_dealt / self.ai_team.get_active_member().get_stat(MAX_HP)
         
            

        if self.last_turn_summary: # If a turn was run, calculate the matchup strength of the active monsters, add that to policy rating
            for action in self.last_turn_summary:
                if action.was_ai_action and action.user_attacked_and_did_no_damage():
                    policy_rating -= 1

        if self.game_over and self.did_ai_win(): # If the node is a victory for the AI, policy rating is 100
            policy_rating = 100
        elif self.game_over and not self.did_ai_win(): # If the node is a victory for the player, policy rating is -100
            policy_rating = -100

        return policy_rating 
    
    '''def get_outcome_dents(self): # Number that represents magnitude by which the AI's victory should be lowered.
        victory_dent = 0
        # FIXME: The more fainted members, the bigger the dent.
        victory_dent += self.player_team.get_active_member().get_stat(HP) / self.player_team.get_active_member().get_stat(MAX_HP)
        return victory_dent'''

    def get_outcome_reward(self): # Number that represents magnitude by which the AI won.
        victory_polish = 0
        victory_polish += (self.ai_team.get_active_member().get_stat(HP) / self.ai_team.get_active_member().get_stat(MAX_HP)) * 2 # Reward AI for minimizing damage taken
        victory_polish += (1 - (self.player_team.get_active_member().get_stat(HP) / self.player_team.get_active_member().get_stat(MAX_HP))) * 2 # Reward AI for maximizing damage dealt
        victory_polish -= self.turn_count / 10
        return victory_polish

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
                elif not action.was_ai_action and action.target_fainted:
                    return False
            return False
    
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
            if self.turn_count != 0 or self.ai_has_switched_after_fainting:
                ai_switches = []
            else:
                ai_switches = self.ai_team.get_list_of_valid_switch_indices()
                for i in range(len(ai_switches)):
                    ai_switches[i] += 4 # Convert switch indices to switch inputs
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
            #if len(list_of_ai_choices) > 9:
            #    print(len(list_of_ai_choices))
            return list_of_ai_choices
   
    def advance_game(self, ai_choice, player_choice = 0): # Simulates moving game forward. Will flip switch booleans and if both are False, will run turn
        if self.ai_needs_to_switch  and not self.is_game_over(): # If ai needs to switch, change the active monster according to the ai_choice
            self.ai_team.switch_active_member(ai_choice - 4) 
            self.ai_needs_to_switch = False
            self.last_turn_summary = [TurnActionSummary(was_ai_action=True,was_switch_after_faint=True)]
            self.ai_has_switched_after_fainting = True
        elif self.player_needs_to_switch and not self.is_game_over(): # If player needs to switch, change the active monster according to the player_choice
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
            self.is_game_over()
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
        print(switching_team.name, "sent out", switching_team.get_member(switch_index).name)
    switching_team.switch_active_member(switch_index)

def turn(player_team: Team, player_choice, ai_team: Team, ai_choice, visualization = True, rng = True): # Calculates a turn in the game. Used in the GameState class, as well as by the game when a player makes an input
    # visualize controls the visualization property of the TurnAction object, which in turn controls the visualization of the damage_calc function
    action_summaries = []
    action_list = []

    player_active_member = player_team.get_active_member()
    ai_active_member = ai_team.get_active_member()

    if player_choice > MOVE_4 and not player_choice == 10: # Switch if necessary
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
                print(player_active_member.name + " fainted")
            elif ai_active_member.fainted:
                print(ai_active_member.name + " fainted")
            print()
    # Apply field effects, status effects, etc.
    return action_summaries
        
    

class TurnAction: # Used in turn function to organize actions that need to be taken
    def __init__(self, user, user_team, uinp, target, target_team, was_ai_action, visualization = True, can_crit = True) -> None:
        self.was_ai_action = was_ai_action
        self.user = user
        self.user_team = user_team
        self.uinp = uinp
        self.target = target
        self.target_team = target_team
        self.priority = self.set_priority()
        self.visualization = visualization
        self.turn_action_summary = TurnActionSummary(self.was_ai_action)
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
                    if self.move_used.effect == "High_Crit":
                        elevated_crit_chance = float(self.move_used.effect_chance)
                        result = self.do_damage(crit_chance=elevated_crit_chance)
                    else: # None effect move, or move that hasn't been implemented
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
                    elif self.move_used.effect == "Heal_User":
                        heal_percentage = self.move_used.effect_magnitude
                        self.heal(heal_percentage)

                    elif "Alter" in self.move_used.effect: # FIXME: Theres probably a better way to do this
                        # Determine if 'User' is in the effect string
                        # If it is in the string, set a variable to the user
                        # If not, set a variable ot the target
                        # Then figure out what stats are being altered (Create a list object to store all of the stats being altered)
                        # Special exception for Gear Shift which raises attack by one stage and speed by two stages
                        # Then figure out the magnitude of the alteration
                        # Then alter the stat
                        
                        if self.move_used.effect == "Alter_Attack":
                            alter_magnitude = self.move_used.effect_magnitude
                            if self.target.attack_boost > -6:
                                self.target.attack_boost += alter_magnitude
                            if self.visualization:
                                print(self.target.name + "'s attack fell!")
                        elif self.move_used.effect == "Alter_Attack_User":
                            alter_magnitude = self.move_used.effect_magnitude
                            if self.user.attack_boost > -6 and self.user.attack_boost < 6:
                                self.user.attack_boost += alter_magnitude
                                if self.user.attack_boost > 6:
                                    self.user.attack_boost = 6
                            if self.visualization:
                                if alter_magnitude == 1:
                                    print(self.user_team.name + "'s " + self.user.name + "'s attack rose!")
                                elif alter_magnitude == 2:
                                    print(self.user_team.name + "'s " + self.user.name + "'s attack sharply rose!")
                                elif alter_magnitude > 0:
                                    print(self.user_team.name + "'s " + self.user.name + "'s attack rose by " + str(alter_magnitude) + " stages!")
                                elif alter_magnitude == -1:
                                    print(self.user_team.name + "'s " + self.user.name + "'s attack fell!")
                                elif alter_magnitude == -2:
                                    print(self.user_team.name + "'s " + self.user.name + "'s attack harshly fell!")
                                elif alter_magnitude < 0 :
                                    print(self.user_team.name + "'s " + self.user.name + "'s attack fell by " + str(alter_magnitude) + " stages!")
                                else:
                                    print("Alter_Attack_User error")
                        elif self.move_used.effect == "Alter_Defense_User":
                            alter_magnitude = self.move_used.effect_magnitude
                            if self.user.defense_boost > -6 and self.user.defense_boost < 6:
                                self.user.defense_boost += alter_magnitude
                                if self.user.defense_boost > 6:
                                    self.user.defense_boost = 6
                            if self.visualization: # FIXME: If a move sharply raises the defense of a pokemon but they have stage 5 boost it will still say sharply rose
                                if alter_magnitude == 1:
                                    print(self.user_team.name + "'s " + self.user.name + "'s defense rose!")
                                elif alter_magnitude == 2:
                                    print(self.user_team.name + "'s " + self.user.name + "'s defense sharply rose!")
                                elif alter_magnitude > 0:
                                    print(self.user_team.name + "'s " + self.user.name + "'s defense rose by " + str(alter_magnitude) + " stages!")
                                elif alter_magnitude == -1:
                                    print(self.user_team.name + "'s " + self.user.name + "'s defense fell!")
                                elif alter_magnitude == -2:
                                    print(self.user_team.name + "'s " + self.user.name + "'s defense harshly fell!")
                                elif alter_magnitude < 0 :
                                    print(self.user_team.name + "'s " + self.user.name + "'s defense fell by " + str(alter_magnitude) + " stages!")
                                else:
                                    print("Alter_Defense_User error")

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

    def do_damage(self, crit_chance = DEFAULT_CRIT_CHANCE):
        damage = damage_calc(self.user, self.target, self.move_used, self.user_team, self.target_team, self.can_crit, self.visualization, crit_chance=crit_chance)
        if self.move_used.accuracy >= rng.randint(1,100):
            #if self.visualization:
            #    print(self.target.name + " took " + str(damage) + " damage!")
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

    def heal(self,percentage):
        heal_amount = math.floor(self.user.max_HP * (percentage / 100))
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
        return (self.priority, self.user.speed * self.user.get_multiplier_for_stat(SPEED))

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
