import random as rng
from GameMenus import *
import csv
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

# Game Constants
MAX_TEAM_SIZE = 6
UNOVA_LOWER_BOUND = 494
UNOVA_UPPER_BOUND = 649
TYPE_CHART = {'Normal':{'Normal':1, 'Fire':1, 'Water':1, 'Electric':1, 'Grass':1, 'Ice':1, 'Fighting':2, 'Poison':1, 'Ground':1, 'Flying':1, 'Psychic':1, 'Bug':1, 'Rock':1, 'Ghost':0, 'Dragon':1, 'Dark':1, 'Steel':1, 'Fairy':1},
              'Fire':{'Normal':1, 'Fire':0.5, 'Water':0.5, 'Electric':1, 'Grass':2, 'Ice':2, 'Fighting':1, 'Poison':1, 'Ground':1, 'Flying':1, 'Psychic':1, 'Bug':2, 'Rock':0.5, 'Ghost':1, 'Dragon':0.5, 'Dark':1, 'Steel':2, 'Fairy':1},
              'Water':{'Normal':1, 'Fire':2, 'Water':0.5, 'Electric':1, 'Grass':0.5, 'Ice':1, 'Fighting':1, 'Poison':1, 'Ground':2, 'Flying':1, 'Psychic':1, 'Bug':1, 'Rock':2, 'Ghost':1, 'Dragon':0.5, 'Dark':1, 'Steel':1, 'Fairy':1},
              'Electric':{'Normal':1, 'Fire':1, 'Water':2, 'Electric':0.5, 'Grass':0.5, 'Ice':1, 'Fighting':1, 'Poison':1, 'Ground':0, 'Flying':2, 'Psychic':1, 'Bug':1, 'Rock':1, 'Ghost':1, 'Dragon':0.5, 'Dark':1, 'Steel':1, 'Fairy':1},
              'Grass':{'Normal':1, 'Fire':0.5, 'Water':2, 'Electric':1, 'Grass':0.5, 'Ice':1, 'Fighting':1, 'Poison':0.5, 'Ground':2, 'Flying':0.5, 'Psychic':1, 'Bug':0.5, 'Rock':2, 'Ghost':1, 'Dragon':0.5, 'Dark':1, 'Steel':0.5, 'Fairy':1},
              'Ice':{'Normal':1, 'Fire':0.5, 'Water':0.5, 'Electric':1, 'Grass':2, 'Ice':0.5, 'Fighting':1, 'Poison':1, 'Ground':2, 'Flying':2, 'Psychic':1, 'Bug':1, 'Rock':1, 'Ghost':1, 'Dragon':2, 'Dark':1, 'Steel':0.5, 'Fairy':1},
              'Fighting':{'Normal':2, 'Fire':1, 'Water':1, 'Electric':1, 'Grass':1, 'Ice':2, 'Fighting':1, 'Poison':0.5, 'Ground':1, 'Flying':0.5, 'Psychic':0.5, 'Bug':0.5, 'Rock':2, 'Ghost':0, 'Dragon':1, 'Dark':2, 'Steel':2, 'Fairy':0.5},
              'Poison':{'Normal':1, 'Fire':1, 'Water':1, 'Electric':1, 'Grass':2, 'Ice':1, 'Fighting':1, 'Poison':0.5, 'Ground':0.5, 'Flying':1, 'Psychic':1, 'Bug':1, 'Rock':0.5, 'Ghost':0.5, 'Dragon':1, 'Dark':1, 'Steel':0, 'Fairy':2},
              'Ground':{'Normal':1, 'Fire':2, 'Water':1, 'Electric':2, 'Grass':0.5, 'Ice':1, 'Fighting':1, 'Poison':2, 'Ground':1, 'Flying':0, 'Psychic':1, 'Bug':0.5, 'Rock':2, 'Ghost':1, 'Dragon':1, 'Dark':1, 'Steel':2, 'Fairy':1},
              'Flying':{'Normal':1, 'Fire':1, 'Water':1, 'Electric':0.5, 'Grass':2, 'Ice':1, 'Fighting':2, 'Poison':1, 'Ground':1, 'Flying':1, 'Psychic':1, 'Bug':2, 'Rock':0.5, 'Ghost':1, 'Dragon':1, 'Dark':1, 'Steel':0.5, 'Fairy':1},
              'Psychic':{'Normal':1, 'Fire':1, 'Water':1, 'Electric':1, 'Grass':1, 'Ice':1, 'Fighting':2, 'Poison':2, 'Ground':1, 'Flying':1, 'Psychic':0.5, 'Bug':1, 'Rock':1, 'Ghost':1, 'Dragon':1, 'Dark':0, 'Steel':0.5, 'Fairy':1},
              'Bug':{'Normal':1, 'Fire':0.5, 'Water':1, 'Electric':1, 'Grass':2, 'Ice':1, 'Fighting':0.5, 'Poison':0.5, 'Ground':1, 'Flying':0.5, 'Psychic':2, 'Bug':1, 'Rock':1, 'Ghost':0.5, 'Dragon':1, 'Dark':2, 'Steel':0.5, 'Fairy':0.5},
              'Rock':{'Normal':1, 'Fire':2, 'Water':1, 'Electric':1, 'Grass':1, 'Ice':2, 'Fighting':0.5, 'Poison':1, 'Ground':0.5, 'Flying':2, 'Psychic':1, 'Bug':2, 'Rock':1, 'Ghost':1, 'Dragon':1, 'Dark':1, 'Steel':0.5, 'Fairy':1},
              'Ghost':{'Normal':0, 'Fire':1, 'Water':1, 'Electric':1, 'Grass':1, 'Ice':1, 'Fighting':1, 'Poison':1, 'Ground':1, 'Flying':1, 'Psychic':2, 'Bug':1, 'Rock':1, 'Ghost':2, 'Dragon':1, 'Dark':0.5, 'Steel':1, 'Fairy':1},
              'Dragon':{'Normal':1, 'Fire':1, 'Water':1, 'Electric':1, 'Grass':1, 'Ice':1, 'Fighting':1, 'Poison':1, 'Ground':1, 'Flying':1, 'Psychic':1, 'Bug':1, 'Rock':1, 'Ghost':1, 'Dragon':2, 'Dark':1, 'Steel':0.5, 'Fairy':0},
              'Dark':{'Normal':1, 'Fire':1, 'Water':1, 'Electric':1, 'Grass':1, 'Ice':1, 'Fighting':0.5, 'Poison':1, 'Ground':1, 'Flying':1, 'Psychic':2, 'Bug':1, 'Rock':1, 'Ghost':2, 'Dragon':1, 'Dark':0.5, 'Steel':1, 'Fairy':0.5},
              'Steel':{'Normal':1, 'Fire':0.5, 'Water':0.5, 'Electric':0.5, 'Grass':1, 'Ice':2, 'Fighting':1, 'Poison':1, 'Ground':1, 'Flying':1, 'Psychic':1, 'Bug':1, 'Rock':2, 'Ghost':1, 'Dragon':1, 'Dark':1, 'Steel':0.5, 'Fairy':2},
              'Fairy':{'Normal':1, 'Fire':0.5, 'Water':1, 'Electric':1, 'Grass':1, 'Ice':1, 'Fighting':2, 'Poison':0.5, 'Ground':1, 'Flying':1, 'Psychic':1, 'Bug':1, 'Rock':1, 'Ghost':1, 'Dragon':2, 'Dark':2, 'Steel':0.5, 'Fairy':1}}


# Class constants
ATTACK = 0
DEFENSE = 1
SP_ATTACK = 2
SP_DEFENSE = 3
SPEED = 4
HP = 5

NATURE_DICT = {'Hardy': (ATTACK, ATTACK), 'Lonely': (ATTACK, DEFENSE), 'Adamant': (ATTACK, SP_ATTACK), 'Naughty': (ATTACK, SP_DEFENSE), 'Brave': (ATTACK, SPEED),
              'Bold': (DEFENSE, ATTACK), 'Docile': (DEFENSE, DEFENSE), 'Impish': (DEFENSE, SP_ATTACK), 'Lax': (ATTACK, SP_DEFENSE), 'Relaxed': (DEFENSE, SPEED),
              'Modest': (SP_ATTACK, ATTACK), 'Mild': (SP_ATTACK, DEFENSE), 'Bashful': (SP_ATTACK, SP_ATTACK), 'Rash': (SP_ATTACK, SP_DEFENSE), 'Quiet': (SP_ATTACK, SPEED),
              'Calm': (SP_DEFENSE, ATTACK), 'Gentle': (SP_DEFENSE, DEFENSE), 'Careful': (SP_DEFENSE, SP_ATTACK), 'Quirky': (SP_DEFENSE, SP_DEFENSE), 'Sassy': (SP_DEFENSE, SPEED),
              'Timid': (SPEED, ATTACK), 'Hasty': (SPEED, DEFENSE), 'Jolly': (SPEED, SP_ATTACK), 'Naive': (SPEED, SP_DEFENSE), 'Serious': (SPEED, SPEED)}


class Monster:
    def __init__(self, speed=10, name="Monster") -> None:
        self.name = name
        self.not_fainted = True
        self.health = 100
        self.attack = 10
        self.speed = speed
        self.item = None
        self.moves = []
        self.number_of_moves = 0
        self.status = None
    
class Monster2: #TODO: set up move database for each monster
    def __init__(self, number_id=1, level=1, code=1) -> None:
        # Monster stats
        self.name = None
        self.not_fainted = True
        self.item = None
        self.level = level
        self.HP = 0
        self.attack = 0
        self.defense = 0
        self.special_attack = 0
        self.special_defense = 0
        self.speed = 0
        self.move_1 = None
        self.move_2 = None
        self.move_3 = None
        self.move_4 = None
        self.number_of_moves = 0 #FIXME
        self.item = None
        self.EV_HP = 0
        self.EV_attack = 0
        self.EV_defense = 0
        self.EV_special_attack = 0
        self.EV_special_defense = 0
        self.EV_speed = 0
        self.IV_HP = None
        self.IV_attack = None
        self.IV_defense = None
        self.IV_special_attack = None
        self.IV_special_defense = None
        self.IV_speed = None
        self.nature = None
        self.sex = None
        self.shiny = None
        
        # Monster data
        self.max_HP = None
        self.type_1 = None
        self.type_2 = None
        self.ability = None
        self.alternate_ability = None
        self.hidden_ability = None
        self.weight = None
        self.base_hp = None
        self.base_attack = None
        self.base_defense = None
        self.base_special_attack = None
        self.base_special_defense = None
        self.base_speed = None
        self.can_evolve = None
        self.evolution_method = None

        monster_data = None  # Variable to store the matched row
        with open('monsters.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == str(number_id) and row[1] == str(code):
                    monster_data = row  # Assign the matched row to the variable
                    break  # Terminate the loop when a match is found

        # Use the monster_data variable to calculate stats about the monster
        if monster_data is not None:
            self.name = monster_data[3]
            self.type_1 = monster_data[4]
            if not self.type_1:
                self.type_1 = None
            self.type_2 = monster_data[5]
            if not self.type_2:
                self.type_2 = None
            self.ability = monster_data[7]
            self.alternate_ability = monster_data[8]
            if not self.alternate_ability:
                self.alternate_ability = None
            self.hidden_ability = monster_data[9]
            if not self.hidden_ability:
                self.hidden_ability = None
            self.weight = monster_data[13]
            self.base_hp = int(monster_data[15])
            self.base_attack = int(monster_data[16])
            self.base_defense = int(monster_data[17])
            self.base_special_attack = int(monster_data[18])
            self.base_special_defense = int(monster_data[19])
            self.base_speed = int(monster_data[20])
            self.roll_nature()
            self.roll_IVs()
            self.calculate_stats()
            self.HP = self.max_HP
            self.add_move(1)
            self.add_move(2)
            self.add_move(5)
        else:
            print("Monster not found, object is invalid")
    
    def __str__(self) -> str:
        stats = f"HP: {self.HP}\nAttack: {self.attack}\nDefense: {self.defense}\nSpecial Attack: {self.special_attack}\nSpecial Defense: {self.special_defense}\nSpeed: {self.speed}"
        return f"Name: {self.name}\n{stats}"
    
    def get_list_of_moves(self):
        moves = []
        if self.move_1:
            moves.append(self.move_1.name)
        if self.move_2:
            moves.append(self.move_2.name)
        if self.move_3:
            moves.append(self.move_3.name)
        if self.move_4:
            moves.append(self.move_4.name)
        return moves

    def add_move(self, move_number):
        new_move = Move(move_number)
        if self.number_of_moves == 0:
            self.move_1 = new_move
            self.number_of_moves += 1
        elif self.number_of_moves == 1:
            self.move_2 = new_move
            self.number_of_moves += 1
        elif self.number_of_moves == 2:
            self.move_3 = new_move
            self.number_of_moves += 1
        elif self.number_of_moves == 3:
            self.move_4 = new_move
            self.number_of_moves += 1
        else:
            print("Cannot add move, monster already has 4 moves")

    def print_stats(self, verbosity=0):
        print(self.name, end=' ')
        print("Level: " + str(self.level))
        print(self.type_1, end=' ')
        if self.type_2:
            print(self.type_2, end=' ')
        print(self.nature, end=' ')
        print()
        
        print("HP: " + str(self.HP))
        
        stats = [('Attack', self.attack, ATTACK, self.IV_attack, self.EV_attack), 
                 ('Defense', self.defense, DEFENSE, self.IV_defense, self.EV_defense), 
                 ('Sp. Atk', self.special_attack, SP_ATTACK, self.IV_special_attack, self.EV_special_attack), 
                 ('Sp. Def', self.special_defense, SP_DEFENSE, self.IV_special_defense, self.EV_special_defense), 
                 ('Speed', self.speed, SPEED, self.IV_speed, self.EV_speed)]
    
        for stat_name, stat_value, stat_constant, iv_value, ev_value in stats:
            print(f"{stat_name}: {stat_value}", end='')
            if self.nature:
                if NATURE_DICT[self.nature][0] == stat_constant and NATURE_DICT[self.nature][1] != stat_constant:
                    print(" +", end='')
                elif NATURE_DICT[self.nature][1] == stat_constant and NATURE_DICT[self.nature][0] != stat_constant:
                    print(" -", end='')
            if verbosity == 1:
                print(f" (IV: {iv_value}, EV: {ev_value})", end='')
            print()

    def roll_IVs(self):
        self.IV_HP = rng.randint(0, 31)
        self.IV_attack = rng.randint(0, 31)
        self.IV_defense = rng.randint(0, 31)
        self.IV_special_attack = rng.randint(0, 31)
        self.IV_special_defense = rng.randint(0, 31)
        self.IV_speed = rng.randint(0, 31)

    def roll_nature(self):
        self.nature = rng.choice(list(NATURE_DICT.keys()))

    def get_nature_multiplier(self, stat):
        nature_tuple = NATURE_DICT[self.nature]
        nature_stat_multiplier = 1
        if nature_tuple[0] == stat:
            nature_stat_multiplier += 0.1
        if nature_tuple[1] == stat:
            nature_stat_multiplier -= 0.1
        return nature_stat_multiplier

    def roll_sex(self):
        pass

    def calculate_stats(self):
        self.max_HP = self.calculate_hp()
        self.attack = self.calculate_stat(ATTACK)
        self.defense = self.calculate_stat(DEFENSE)
        self.special_attack = self.calculate_stat(SP_ATTACK)
        self.special_defense = self.calculate_stat(SP_DEFENSE)
        self.speed = self.calculate_stat(SPEED)

    def calculate_hp(self):
        #int((((2 * basestat(self, stat = 'HP') + self.IV_HP + (self.EV_HP / 4)) * self.level) / 100) + self.level + 10)
        return int((((2 * self.base_hp + self.IV_HP + (self.EV_HP / 4)) * self.level) / 100) + self.level + 10)
    
    def calculate_stat(self, stat):
        # 0 = attack, 1 = defense, 2 = special attack, 3 = special defense, 4 = speed
        stat_IV = 0
        stat_EV = 0
        stat_base = 0
        if stat == 0:
            stat_IV = self.IV_attack
            stat_EV = self.EV_attack
            stat_base = self.base_attack
        elif stat == 1:
            stat_IV = self.IV_defense
            stat_EV = self.EV_defense
            stat_base = self.base_defense
        elif stat == 2:
            stat_IV = self.IV_special_attack
            stat_EV = self.EV_special_attack
            stat_base = self.base_special_attack
        elif stat == 3:
            stat_IV = self.IV_special_defense
            stat_EV = self.EV_special_defense
            stat_base = self.base_special_defense
        elif stat == 4:
            stat_IV = self.IV_speed
            stat_EV = self.EV_speed
            stat_base = self.base_speed
        else:
            print("Invalid stat code")
            return 0
        #int(((((2 * basestat(self, stat = 'attack') + self.IV_Attack + (self.EV_Attack / 4)) * self.level) / 100) + 5) * nature_Multiplier(self.nature, 'attack'))
        return int((((((2 * stat_base + stat_IV + (stat_EV / 4)) * self.level) / 100) + 5) * 1) * self.get_nature_multiplier(stat)) # TODO: Implement nature multiplier
    
    def get_stat(self, stat):
        if stat == ATTACK:
            return self.attack
        elif stat == DEFENSE:
            return self.defense
        elif stat == SP_ATTACK:
            return self.special_attack
        elif stat == SP_DEFENSE:
            return self.special_defense
        elif stat == SPEED:
            return self.speed
        elif stat == HP:
            return self.HP
        
    def get_move(self, move_number):
        if move_number == MOVE_1:
            return self.move_1
        elif move_number == MOVE_2:
            return self.move_2
        elif move_number == MOVE_3:
            return self.move_3
        elif move_number == MOVE_4:
            return self.move_4
        else:
            print("Invalid move number")
            return None

    def get_number_of_moves(self): # TODO: Exclude moves with 0 PP
        return self.number_of_moves

    def gain_exp(self, exp):
        # Gain experience
        # Level up if necessary
        pass

    def level_up(self):
        if self.level < 100:
            self.level += 1
            self.calculate_stats()  

    def deep_copy(self):
        new_monster = Monster2()
        new_monster.name = self.name
        new_monster.not_fainted = self.not_fainted
        new_monster.item = self.item
        new_monster.HP = self.HP
        new_monster.level = self.level
        new_monster.move_1 = self.move_1
        new_monster.move_2 = self.move_2
        new_monster.move_3 = self.move_3
        new_monster.move_4 = self.move_4
        new_monster.number_of_moves = self.number_of_moves
        new_monster.EV_HP = self.EV_HP
        new_monster.EV_attack = self.EV_attack
        new_monster.EV_defense = self.EV_defense
        new_monster.EV_special_attack = self.EV_special_attack
        new_monster.EV_special_defense = self.EV_special_defense
        new_monster.EV_speed = self.EV_speed
        new_monster.IV_HP = self.IV_HP
        new_monster.IV_attack = self.IV_attack
        new_monster.IV_defense = self.IV_defense
        new_monster.IV_special_attack = self.IV_special_attack
        new_monster.IV_special_defense = self.IV_special_defense
        new_monster.IV_speed = self.IV_speed
        new_monster.nature = self.nature
        new_monster.sex = self.sex
        new_monster.shiny = self.shiny
        new_monster.calculate_stats()
        return new_monster




class Move:
    def __init__(self, number_id = 1) -> None:
        
        with open('moves.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == str(number_id):
                    move_data = row  # Assign the matched row to the variable
                    break  # Terminate the loop when a match is found
        if move_data: # Check if data is truthy
            self.name = move_data[2]
            self.type = move_data[3]
            self.category = move_data[4]
            self.base_power = int(move_data[5])
            self.accuracy = int(move_data[6])
            self.priority = int(move_data[7])
            self.effect = move_data[8]
            self.effect_chance = int(move_data[9])
            if move_data[10] == "Y":
                self.makes_contact = True
            else:
                self.makes_contact = False
            if move_data[11] == "D":
                self.targets_multiple = True
            else:
                self.targets_multiple = False
            self.base_pp = int(move_data[12])
            self.pp = self.base_pp
            self.description = move_data[13]
            #print("Move read successfully")
            #print(self.name)
        else:
            print("Move not found, object is invalid")

    def get_priority(self):
        return self.priority

    def expend_pp(self):
        self.pp -= 1
        if self.pp < 0:
            self.pp = 0

class Move_With_Effect_Chance(Move):
    def __init__(self) -> None:
        super().__init__()
        self.effect = "Burn"
        self.effect_chance = 10

class Multi_Hit_Move(Move):
    def __init__(self) -> None:
        super().__init__()
        self.min_hits = 2
        self.max_hits = 5

class TurnAction: # Used in turn function to organize actions that need to be taken
    def __init__(self, user, uinp, target, visualization = True) -> None:
        self.user = user
        self.uinp = uinp
        self.target = target
        self.priority = self.set_priority()
        self.visualization = visualization
    
    def set_priority(self): # TODO
        return self.user.get_move(self.uinp).get_priority()
    
    def excecute_action(self):
        if self.user.not_fainted: # Check if user is fainted
            move_used = self.user.get_move(self.uinp)
            if self.visualization:
                print(self.user.name + " used " + move_used.name + " on " + self.target.name)
            if type(move_used) is Move:
                damage = damage_calc(self.user, self.target, move_used, False, self.visualization)
                self.target.HP -= damage
                if self.target.HP <= 0:
                    self.target.not_fainted = False
                    self.target.HP = 0
            else:
                if self.visualization:
                    print("Move class not implemented")
            move_used.expend_pp() # FIXME: How will pressure work?
        else:
            pass # Skip turn if user is fainted
    def get_action_priority(self): # Priority is a tuple of (speed, priority)
        return (self.priority, self.user.speed)

class Item:
    def __init__(self) -> None:
        pass

class Bag:
    def __init__(self) -> None:
        pass

class Team:
    def __init__(self, team_name="Team") -> None:
        self.team_name = team_name
        self.team_members = []
        self.team_size = 0
        self.team_max_size = MAX_TEAM_SIZE
        self.team_level = 1
        self.team_members_healthy = 0
        self.active_member_index = 0
    
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

    def has_non_fainted_members(self):
        self.update_team_members_healthy()
        return self.team_members_healthy > 0

    def update_team_members_healthy(self):
        self.team_members_healthy = 0
        for monster in self.team_members:
            if monster.not_fainted:
                self.team_members_healthy += 1

    def switch_monster_order(self, index1, index2):
        if index1 < self.team_size and index2 < self.team_size:
            temp = self.team_members[index1]
            self.team_members[index1] = self.team_members[index2]
            self.team_members[index2] = temp
        else:
            print("Index out of range")
    
    def get_number_of_members_to_switch_to(self):
        return self.team_members_healthy - 1
    
    def get_list_of_member_names_to_switch_to(self):
        member_names = []
        for i in range(self.team_size):
            if i != self.active_member_index and self.team_members[i].not_fainted:
                member_names.append(self.team_members[i].name)
        return member_names

    def get_initial_active_member_index(self):
        for i in range(self.team_size):
            if self.team_members[i].not_fainted:
                return i
        return -1

    def get_list_of_valid_switch_indices(self):
        valid_indices = []
        for i in range(self.team_size):
            if i != self.active_member_index and self.team_members[i].not_fainted:
                valid_indices.append(i)
        return valid_indices
    
    def is_active_member_fainted(self):
        return not self.team_members[self.active_member_index].not_fainted
    
    def deep_copy(self):
        new_team = Team()
        new_team.team_name = self.team_name
        new_team.team_size = self.team_size
        new_team.active_member_index = self.active_member_index
        new_team.team_level = self.team_level
        new_team.team_members_healthy = self.team_members_healthy
        for monster in self.team_members:
            new_team.add_member(monster.deep_copy())
    
        return new_team


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

class Map: # Will store information about the map such as players size, the map itself, etc.
    def __init__(self) -> None:
        pass     
    
class Game:
    def __init__(self) -> None:
        self.player = Player()
        self.map = Map()
        self.game_over = False
        self.winner = None

def damage_calc(user, target, move: Move, can_crit = True, visualization = True): #TODO: Implement damage calculation
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
        elif type_mult < 1:
            print("It's not very effective...")
        elif type_mult == 0:
            print("It doesn't affect " + target.name + "...")
    raw_calc = ((((2*user.level / 5 + 2) * move.base_power * (user.attack / target.defense)) / 50) + 2)
    multiplier_calc = raw_calc * crit_mult * stab_mult * type_mult
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
    monster = Monster2(monster_id, level)
    # Create a randomly generated monster
    # Return the monster
    return monster

class GameState():
    def __init__(self, player_team, ai_team, turn_count = 0, last_move = 0) -> None:
        self.player_team = player_team
        #print("Does player need to switch?")
        self.player_needs_to_switch = self.player_team.is_active_member_fainted()
        self.ai_team = ai_team
        #print("Does AI need to switch?")
        self.ai_needs_to_switch = self.ai_team.is_active_member_fainted()
        self.turn_count = turn_count
        #print("Turn count: " + str(self.turn_count))
        self.last_move = last_move
        #print("Is this a terminal state?")
        self.game_over = self.is_game_over()
        #print(self.game_over)
        self.winner = None
        self.policy_rating = self.calculate_policy_rating()
    
    def __str__(self) -> str:
        return f"Player team: {self.player_team}\nAI team: {self.ai_team}\nTurn count: {self.turn_count}\nLast move: {self.last_move}\nGame over: {self.game_over}\nWinner: {self.winner}\nPolicy rating: {self.policy_rating}"

    def is_game_over(self):
        if self.player_team.has_non_fainted_members() and self.ai_team.has_non_fainted_members():
            return False
        else:
            self.game_over = True
            return True
        
    def did_ai_win(self):
        if self.is_game_over():
            return self.ai_team.has_non_fainted_members()
        else:
            return False
    
    def get_ai_possible_actions(self):
        if self.ai_needs_to_switch: # If ai needs to switch, return list of inputs representing every valid switch the AI can perform
            #print("AI needs to switch")
            list_of_ai_choices = []
            valid_switch_indices = self.ai_team.get_list_of_valid_switch_indices()
            for i in valid_switch_indices:
                append_state = GameState(self.player_team.deep_copy(), self.ai_team.deep_copy(), self.turn_count).advance_game(i + 4) # 
                list_of_ai_choices.append(append_state)
            #print(len(list_of_ai_choices))
            return list_of_ai_choices
        
        elif self.player_needs_to_switch: # Switch Player monster, then return new state in the list
            #print("Player needs to switch")
            list_of_ai_choices = []
            valid_switch_indices = self.player_team.get_list_of_valid_switch_indices()
            for i in valid_switch_indices:
                print(i)
                append_state = GameState(self.player_team.deep_copy(), self.ai_team.deep_copy(), self.turn_count).advance_game(0, i + 4) # 0, 1, 2, 3, are move choices
                list_of_ai_choices.append(append_state)
            #print(len(list_of_ai_choices))
            return list_of_ai_choices
        
        else: # If no team needs to switch: return list of inputs representing every valid move and switch the AI can perform
            list_of_ai_choices = []
            ai_moves = self.ai_team.get_member(self.ai_team.active_member_index).get_number_of_moves()
            player_moves = self.player_team.get_member(self.player_team.active_member_index).get_number_of_moves()
            for i in range(ai_moves): # Get all 2-16 combinations of moves
                for j in range(player_moves):
                    append_state = GameState(self.player_team.deep_copy(), self.ai_team.deep_copy(), self.turn_count).advance_game(i, j) # 0, 1, 2, 3, are move choices
                    list_of_ai_choices.append(append_state)
            # FIXME: Implement voluntary switching (switching to a better matchup)
            #print(list_of_ai_choices)
            if len(list_of_ai_choices) == 0:
                print("No possible moves")
            return list_of_ai_choices
   
    def advance_game(self, ai_choice, player_choice = 0): # Simulates moving game forward. Will flip switch booleans and if both are False, will run turn
        if self.ai_needs_to_switch  and not self.is_game_over(): # If ai needs to switch, change the active monster according to the ai_choice
            self.ai_team.active_member_index = ai_choice
            self.ai_needs_to_switch = False
        elif self.player_needs_to_switch  and not self.is_game_over(): # If player needs to switch, change the active monster according to the player_choice
            if player_choice == self.player_team.team_size:
                print("Player choice is out of range")
            self.player_team.active_member_index = player_choice # FIXME: Probably getting an index out of range error here
            self.player_needs_to_switch = False
        else: # If no one needs to switch, run turn with inputs according to the ai_choice and player_choice
            visualization = False
            turn(self.player_team, player_choice, self.ai_team, ai_choice, visualization) # Teams passed by reference, will be altered by turn function
            self.is_game_over()
            self.turn_count += 1 # If ran turn, increment turn counter and check if game is over
        self.last_move = ai_choice
        return self

    def calculate_policy_rating(self):
        policy_rating = 0
        # If an ai monster is fainted, decrease policy_rating by 1
        # If a player monster has fainted, increase policy_rating by 1
        # Calculate the matchup strength of the active monsters, add that to policy rating
        return policy_rating # FIXME Provide a policy rating for the AI

    def does_team_need_to_switch(self):
        self.update_team_needs_to_switch_booleans()
        if self.player_needs_to_switch or self.ai_needs_to_switch:
            return True
        else:
            return False

    def update_team_needs_to_switch_booleans(self):
        if self.player_team.get_member(self.player_team.active_member_index).not_fainted == False:
            self.player_needs_to_switch = True
        if self.ai_team.get_member(self.ai_team.active_member_index).not_fainted == False:
            self.ai_needs_to_switch = True
    
def turn(player_team: Team, player_choice, ai_team: Team, ai_choice, visualization = True): # Calculates a turn in the game. Used in the GameState class. Not game agnostic.
    # visualize controls the visualization property of the TurnAction object, which in turn controls the visualization of the damage_calc function
    action_list = []
    player_active_member = player_team.get_member(player_team.active_member_index)
    ai_active_member = ai_team.get_member(ai_team.active_member_index)
    action_list.append(TurnAction(player_active_member, player_choice, ai_active_member, visualization))
    # Game state object could be updated at this point
    action_list.append(TurnAction(ai_active_member, ai_choice, player_active_member, visualization))
    action_list.sort(key=lambda x: (-x.get_action_priority()[0], -x.get_action_priority()[1]), reverse=False) # Sort based on speed tier.
    for turn in action_list:
        turn.excecute_action()
        # turn action excecuted here
    if visualization:
        if player_active_member.not_fainted == False:
            print(player_active_member.name + " fainted")
        elif ai_active_member.not_fainted == False:
            print(ai_active_member.name + " fainted")
        print()

    # Fill game state with information
    # Run monte carlo with the GameState
    # Store player action
    # Monte Carlo Tree Search for the monster action
    # Sort move order (fastest monster goes first)
    # If there is a speed tie, flip a coin to determine order
    # Apply damage to the monsters, if a monster faints, skip their turn
    # Apply field effects, status effects, etc.
    # If all monsters on a team faint, the other team wins
    # Return with the winner
    def deep_copy(self):
        copy_player_team = self.player_team.deep_copy()
        copy_ai_team = self.ai_team.deep_copy()

        new_state = GameState(copy_player_team, copy_ai_team, self.turn_count, self.last_move)
        
        return new_state



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