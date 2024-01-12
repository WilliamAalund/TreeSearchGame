import csv
import random as rng
from MoveClasses import *

# Constants
MOVE_1 = 0
MOVE_2 = 1
MOVE_3 = 2
MOVE_4 = 3

ATTACK = 0
DEFENSE = 1
SP_ATTACK = 2
SP_DEFENSE = 3
SPEED = 4
HP = 5
MAX_HP = 6

NATURE_DICT = {'Hardy': (ATTACK, ATTACK), 'Lonely': (ATTACK, DEFENSE), 'Adamant': (ATTACK, SP_ATTACK), 'Naughty': (ATTACK, SP_DEFENSE), 'Brave': (ATTACK, SPEED),
              'Bold': (DEFENSE, ATTACK), 'Docile': (DEFENSE, DEFENSE), 'Impish': (DEFENSE, SP_ATTACK), 'Lax': (ATTACK, SP_DEFENSE), 'Relaxed': (DEFENSE, SPEED),
              'Modest': (SP_ATTACK, ATTACK), 'Mild': (SP_ATTACK, DEFENSE), 'Bashful': (SP_ATTACK, SP_ATTACK), 'Rash': (SP_ATTACK, SP_DEFENSE), 'Quiet': (SP_ATTACK, SPEED),
              'Calm': (SP_DEFENSE, ATTACK), 'Gentle': (SP_DEFENSE, DEFENSE), 'Careful': (SP_DEFENSE, SP_ATTACK), 'Quirky': (SP_DEFENSE, SP_DEFENSE), 'Sassy': (SP_DEFENSE, SPEED),
              'Timid': (SPEED, ATTACK), 'Hasty': (SPEED, DEFENSE), 'Jolly': (SPEED, SP_ATTACK), 'Naive': (SPEED, SP_DEFENSE), 'Serious': (SPEED, SPEED)}


class Monster: #TODO: set up move database for each monster
    def __init__(self, number_id=1, level=1, code=1) -> None:
        # Monster stats
        self.name = None
        self.not_fainted = True
        self.fainted = False
        self.status = None
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

    def calculate_stats(self): # All stats use calculation formulas here
        self.max_HP = self.calculate_hp()
        self.attack = self.calculate_stat(ATTACK)
        self.defense = self.calculate_stat(DEFENSE)
        self.special_attack = self.calculate_stat(SP_ATTACK)
        self.special_defense = self.calculate_stat(SP_DEFENSE)
        self.speed = self.calculate_stat(SPEED)

    def calculate_hp(self): # HP is calculated here. HP uses a different formula than the other stats
        return int((((2 * self.base_hp + self.IV_HP + (self.EV_HP / 4)) * self.level) / 100) + self.level + 10)
    
    def calculate_stat(self, stat): 
        stat_IV = 0
        stat_EV = 0
        stat_base = 0
        if stat == ATTACK:
            stat_IV = self.IV_attack
            stat_EV = self.EV_attack
            stat_base = self.base_attack
        elif stat == DEFENSE:
            stat_IV = self.IV_defense
            stat_EV = self.EV_defense
            stat_base = self.base_defense
        elif stat == SP_ATTACK:
            stat_IV = self.IV_special_attack
            stat_EV = self.EV_special_attack
            stat_base = self.base_special_attack
        elif stat == SP_DEFENSE:
            stat_IV = self.IV_special_defense
            stat_EV = self.EV_special_defense
            stat_base = self.base_special_defense
        elif stat == SPEED:
            stat_IV = self.IV_speed
            stat_EV = self.EV_speed
            stat_base = self.base_speed
        else:
            print("Invalid stat code")
            return 0
        return int((((((2 * stat_base + stat_IV + (stat_EV / 4)) * self.level) / 100) + 5) * 1) * self.get_nature_multiplier(stat))
    
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
        elif stat == 6:
            return self.max_HP
        
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

    def gain_exp(self, exp): # FIXME: Implement experience gain
        # Gain experience
        # Level up if necessary
        # Do not gain experience if monster is fainted, or level is 100
        # level up if experience is enough
        pass

    def level_up(self): # Levels up the monster by 1
        if self.level < 100:
            self.level += 1
            self.calculate_stats()  
            # Reset exp to 0
            # Calculate exp to next level, assign it to a parameter

    def deep_copy(self): # Returns a deep copy of the monster, used in Monte Carlo Tree Search
        new_monster = Monster()
        new_monster.name = self.name
        new_monster.not_fainted = self.not_fainted
        new_monster.fainted = self.fainted
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