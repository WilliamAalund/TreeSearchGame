import csv
import random as rng
from MoveClasses import *

# Constants
MOVE_1 = 0
MOVE_2 = 1
MOVE_3 = 2
MOVE_4 = 3
STRUGGLE = 10

ATTACK = 0
DEFENSE = 1
SP_ATTACK = 2
SP_DEFENSE = 3
SPEED = 4
HP = 5
MAX_HP = 6
ACCURACY = 7
EVASION = 8

UNOVA_LOWER_BOUND = 494
UNOVA_UPPER_BOUND = 649

STARTER_1 = 495
STARTER_2 = 498
STARTER_3 = 501

POISON = 0
TOXIC_POISON = 1
PARALYSIS = 2
BURN = 3
FREEZE = 4
SLEEP = 5

SNAP_OUT_OF_CONFUSION = 0
CONFUSED_NO_DAMAGE = 1
CONFUSED_DAMAGE = 2

NATURE_DICT = {'Hardy': (ATTACK, ATTACK), 'Lonely': (ATTACK, DEFENSE), 'Adamant': (ATTACK, SP_ATTACK), 'Naughty': (ATTACK, SP_DEFENSE), 'Brave': (ATTACK, SPEED),
              'Bold': (DEFENSE, ATTACK), 'Docile': (DEFENSE, DEFENSE), 'Impish': (DEFENSE, SP_ATTACK), 'Lax': (ATTACK, SP_DEFENSE), 'Relaxed': (DEFENSE, SPEED),
              'Modest': (SP_ATTACK, ATTACK), 'Mild': (SP_ATTACK, DEFENSE), 'Bashful': (SP_ATTACK, SP_ATTACK), 'Rash': (SP_ATTACK, SP_DEFENSE), 'Quiet': (SP_ATTACK, SPEED),
              'Calm': (SP_DEFENSE, ATTACK), 'Gentle': (SP_DEFENSE, DEFENSE), 'Careful': (SP_DEFENSE, SP_ATTACK), 'Quirky': (SP_DEFENSE, SP_DEFENSE), 'Sassy': (SP_DEFENSE, SPEED),
              'Timid': (SPEED, ATTACK), 'Hasty': (SPEED, DEFENSE), 'Jolly': (SPEED, SP_ATTACK), 'Naive': (SPEED, SP_DEFENSE), 'Serious': (SPEED, SPEED)}

EVOLVE_VIA_TRADE = 'T'
EVOLVE_VIA_LEAF_STONE = 'LS'
EVOLVE_VIA_FIRE_STONE = 'FS'
EVOLVE_VIA_WATER_STONE = 'WS'
EVOLVE_VIA_THUNDER_STONE = 'TS'
EVOLVE_VIA_MOON_STONE = 'MS'
EVOLVE_VIA_DUSK_STONE = 'DS'
EVOLVE_VIA_SUN_STONE = 'SU'
EVOLVE_VIA_ICE_STONE = 'IS'
EVOLVE_VIA_SHINY_STONE = 'SH'
EVOLVE_VIS_DUSTY_BOWL = 'DB'
EVOLVE_VIA_FRIENDSHIP = 'FR'

MONSTER_DATA_DIRECTORY = 'monsterdata.csv'

UNIQUE_EVOLUTION_METHODS = [EVOLVE_VIA_TRADE, EVOLVE_VIA_LEAF_STONE, EVOLVE_VIA_FIRE_STONE, EVOLVE_VIA_WATER_STONE, EVOLVE_VIA_THUNDER_STONE, EVOLVE_VIA_MOON_STONE, EVOLVE_VIA_DUSK_STONE, EVOLVE_VIA_SUN_STONE, EVOLVE_VIA_ICE_STONE, EVOLVE_VIA_SHINY_STONE, EVOLVE_VIS_DUSTY_BOWL, EVOLVE_VIA_FRIENDSHIP]


class Monster: #TODO: set up move database for each monster
    def __init__(self, number_id=1, level=1, code=1, deep_copy=None, perfect_IVs = False) -> None:

        if deep_copy:
            self.id = deep_copy.id
            self.code = deep_copy.code
            self.name = deep_copy.name
            self.not_fainted = deep_copy.not_fainted
            self.fainted = deep_copy.fainted
            self.status_condition = deep_copy.status_condition
            self.item = deep_copy.item
            self.level = deep_copy.level
            self.HP = deep_copy.HP
            self.attack = deep_copy.attack
            self.defense = deep_copy.defense
            self.special_attack = deep_copy.special_attack
            self.special_defense = deep_copy.special_defense
            self.speed = deep_copy.speed
            self.move_1 = None
            self.move_2 = None
            self.move_3 = None
            self.move_4 = None
            try:
                self.move_1 = deep_copy.move_1.deep_copy()
                self.move_2 = deep_copy.move_2.deep_copy()
                self.move_3 = deep_copy.move_3.deep_copy()
                self.move_4 = deep_copy.move_4.deep_copy()
            except:
                pass
            self.number_of_moves = deep_copy.number_of_moves
            self.item = deep_copy.item
            self.EV_HP = deep_copy.EV_HP
            self.EV_attack = deep_copy.EV_attack
            self.EV_defense = deep_copy.EV_defense
            self.EV_special_attack = deep_copy.EV_special_attack
            self.EV_special_defense = deep_copy.EV_special_defense
            self.EV_speed = deep_copy.EV_speed
            self.IV_HP = deep_copy.IV_HP
            self.IV_attack = deep_copy.IV_attack
            self.IV_defense = deep_copy.IV_defense
            self.IV_special_attack = deep_copy.IV_special_attack
            self.IV_special_defense = deep_copy.IV_special_defense
            self.IV_speed = deep_copy.IV_speed
            self.nature = deep_copy.nature
            self.sex = deep_copy.sex
            self.shiny = deep_copy.shiny
            self.max_HP = deep_copy.max_HP
            self.type_1 = deep_copy.type_1
            self.type_2 = deep_copy.type_2
            self.ability = deep_copy.ability
            self.alternate_ability = deep_copy.alternate_ability
            self.hidden_ability = deep_copy.hidden_ability
            self.weight = deep_copy.weight
            self.base_hp = deep_copy.base_hp
            self.base_attack = deep_copy.base_attack
            self.base_defense = deep_copy.base_defense
            self.base_special_attack = deep_copy.base_special_attack
            self.base_special_defense = deep_copy.base_special_defense
            self.base_speed = deep_copy.base_speed
            self.can_evolve = deep_copy.can_evolve
            self.evolution_method = deep_copy.evolution_method
            self.evolve_id = deep_copy.evolve_id
            self.learn_set = deep_copy.learn_set

            self.attack_boost = deep_copy.attack_boost
            self.defense_boost = deep_copy.defense_boost
            self.special_attack_boost = deep_copy.special_attack_boost
            self.special_defense_boost = deep_copy.special_defense_boost
            self.speed_boost = deep_copy.speed_boost
            self.accuracy_boost = deep_copy.accuracy_boost
            self.evasion_boost = deep_copy.evasion_boost
            self.crit_chance = deep_copy.crit_chance
            self.must_recharge = deep_copy.must_recharge
            self.status_turns = deep_copy.status_turns
            self.is_taunted = deep_copy.is_taunted
            self.taunted_turns = deep_copy.taunted_turns
            self.is_confused = deep_copy.is_confused
            self.confused_turns = deep_copy.confused_turns

            return
        else: # Case where not deep copying

            self.attack_boost = 0
            self.defense_boost = 0
            self.special_attack_boost = 0
            self.special_defense_boost = 0
            self.speed_boost = 0
            self.accuracy_boost = 0
            self.evasion_boost = 0
            self.crit_chance = 0
            self.must_recharge = False
            self.status_turns = 0
            self.is_taunted = False
            self.taunted_turns = 0
            self.is_confused = False
            self.confused_turns = 0

            # Monster stats
            self.id = None
            self.code = code
            self.name = None
            self.not_fainted = True
            self.fainted = False
            self.status_condition = None
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
            self.evolve_id = None

            monster_data = None  # Variable to store the matched row
            with open("monsterdata.csv", 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == str(number_id) and row[1] == str(code):
                        monster_data = row  # Assign the matched row to the variable
                        break  # Terminate the loop when a match is found

            # Use the monster_data variable to calculate stats about the monster
            if monster_data is not None:
                self.id = monster_data[0]
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
                self.evolution_method = monster_data[22]
                if self.evolution_method:
                    self.can_evolve = True
                else:
                    self.can_evolve = False
                self.evolve_id = monster_data[23]
                self.roll_nature()
                if perfect_IVs:
                    self.roll_IVs(31)
                else:
                    self.roll_IVs()
                self.calculate_stats()
                self.HP = self.max_HP
                self.learn_set = monster_data[24].split(',')
                
                for move in self.learn_set:
                    self.add_move(int(move))
                if self.number_of_moves == 0:
                    self.add_move(1)
            else:
                print("Monster not found, object is invalid")
    
    def __str__(self) -> str:
        stats = f"Attack: {self.attack} {'+' if self.get_nature_multiplier(ATTACK) > 1 else ''}{'-' if self.get_nature_multiplier(ATTACK) < 1 else ''}\nDefense: {self.defense} {'+' if self.get_nature_multiplier(DEFENSE) > 1 else ''}{'-' if self.get_nature_multiplier(DEFENSE) < 1 else ''}\nSpecial Attack: {self.special_attack} {'+' if self.get_nature_multiplier(SP_ATTACK) > 1 else ''}{'-' if self.get_nature_multiplier(SP_ATTACK) < 1 else ''}\nSpecial Defense: {self.special_defense} {'+' if self.get_nature_multiplier(SP_DEFENSE) > 1 else ''}{'-' if self.get_nature_multiplier(SP_DEFENSE) < 1 else ''}\nSpeed: {self.speed} {'+' if self.get_nature_multiplier(SPEED) > 1 else ''}{'-' if self.get_nature_multiplier(SPEED) < 1 else ''}"
        if self.move_1:
            stats += f"\n{self.move_1}"
        else:
            stats += "\n --- "
        if self.move_2:
            stats += f"\n{self.move_2}"
        else:
            stats += "\n --- "
        if self.move_3:
            stats += f"\n{self.move_3}"
        else:
            stats += "\n --- "
        if self.move_4:
            stats += f"\n{self.move_4}"
        else:
            stats += "\n --- "
        return f"\n{self.name} | Lv.{self.level} | HP: {self.HP}/{self.max_HP} {(self.get_status_string() + ' ') if self.get_status_string() else ''}| {self.type_1} {self.type_2 + ' ' if self.type_2 else ''}| {self.nature} | {('Evolution: ' + self.get_evolution_method()) if self.get_evolution_method() else ''}\n{stats}\n"
    
    def get_base_stat_total(self):
        return self.base_hp + self.base_attack + self.base_defense + self.base_special_attack + self.base_special_defense + self.base_speed

    def get_list_of_moves(self):
        moves = []
        if self.move_1:
            move_text = self.move_1.name + " PP: " + str(self.move_1.pp) + "/" + str(self.move_1.base_pp)
            moves.append(move_text)
        if self.move_2:
            move_text = self.move_2.name + " PP: " + str(self.move_2.pp) + "/" + str(self.move_2.base_pp)
            moves.append(move_text)
        if self.move_3:
            move_text = self.move_3.name + " PP: " + str(self.move_3.pp) + "/" + str(self.move_3.base_pp)
            moves.append(move_text)
        if self.move_4:
            move_text = self.move_4.name + " PP: " + str(self.move_4.pp) + "/" + str(self.move_4.base_pp)
            moves.append(move_text)
        return moves

    def get_evolution_method(self):
        if self.evolution_method in UNIQUE_EVOLUTION_METHODS:
            if self.evolution_method == EVOLVE_VIA_TRADE:
                return "Trade"
            elif self.evolution_method == EVOLVE_VIA_LEAF_STONE:
                return "Leaf Stone"
            elif self.evolution_method == EVOLVE_VIA_FIRE_STONE:
                return "Fire Stone"
            elif self.evolution_method == EVOLVE_VIA_WATER_STONE:
                return "Water Stone"
            elif self.evolution_method == EVOLVE_VIA_THUNDER_STONE:
                return "Thunder Stone"
            elif self.evolution_method == EVOLVE_VIA_MOON_STONE:
                return "Moon Stone"
            elif self.evolution_method == EVOLVE_VIA_DUSK_STONE:
                return "Dusk Stone"
            elif self.evolution_method == EVOLVE_VIA_SUN_STONE:
                return "Sun Stone"
            elif self.evolution_method == EVOLVE_VIA_ICE_STONE:
                return "Ice Stone"
            elif self.evolution_method == EVOLVE_VIA_SHINY_STONE:
                return "Shiny Stone"
            elif self.evolution_method == EVOLVE_VIS_DUSTY_BOWL:
                return "Dusty Bowl"
            elif self.evolution_method == EVOLVE_VIA_FRIENDSHIP:
                return "Friendship"
            else:
                return "Unknown"
        elif self.evolution_method.isnumeric():
            return "Level " + self.evolution_method
        else:
            return ""

    def reset_boosts(self):
        self.attack_boost = 0
        self.defense_boost = 0
        self.special_attack_boost = 0
        self.special_defense_boost = 0
        self.speed_boost = 0
        self.accuracy_boost = 0
        self.evasion_boost = 0
        self.crit_chance = 0
        self.must_recharge = False

    def reset_semi_permanent_status_conditions(self):
        self.is_confused = False
        self.confused_turns = 0
        self.is_taunted = False
        self.taunted_turns = 0

    def check_if_wakes_up_or_thaws(self):
        if self.status_condition == SLEEP:
            self.status_turns -= 1
            if self.status_turns == 0:
                self.status_condition = None
                return True
            else:
                return False
        elif self.status_condition == FREEZE:
            self.status_turns -= 1
            if self.status_turns == 0:
                self.status_condition = None
                return True
            else:
                return False

    # Status condition methods: Called by other methods to set status conditions. Effects are applied in other methods.
    def set_sleep(self):
        self.status_condition = SLEEP
        self.status_turns = rng.randint(1, 7)
    
    def set_freeze(self):
        self.status_condition = FREEZE
        self.status_turns = rng.randint(1, 7)

    def set_poison(self):
        self.status_condition = POISON
    
    def set_toxic_poison(self):
        self.status_condition = TOXIC_POISON

    def set_paralysis(self):
        self.status_condition = PARALYSIS
    
    def set_burn(self):
        self.status_condition = BURN

    def set_taunted(self):
        self.is_taunted = True
        self.taunted_turns = rng.randint(3,5)

    def set_confused(self):
        self.is_confused = True
        self.confused_turns = rng.randint(2,4)

    def set_recharge(self):
        self.must_recharge = not self.must_recharge

    def get_confusion_result(self):
        SNAP_OUT_OF_CONFUSION = 0
        CONFUSED_NO_DAMAGE = 1
        CONFUSED_DAMAGE = 2
        self.confused_turns -= 1
        if self.confused_turns == 0:
            self.is_confused = False
            return SNAP_OUT_OF_CONFUSION
        else:
            return rng.choice([CONFUSED_DAMAGE, CONFUSED_NO_DAMAGE])

    def get_sleep_or_freeze_result(self):
        WAKE_UP = True
        SLEEP_OR_FREEZE = False
        self.status_turns -= 1
        if self.status_turns <= 0:
            self.status_condition = None
            return WAKE_UP
        else:
            return SLEEP_OR_FREEZE

    def set_boost_for_stat(self, stat, boost): # Sets the boost value for a particular stat
        if stat == ATTACK:
            self.attack_boost = boost
        elif stat == DEFENSE:
            self.defense_boost = boost
        elif stat == SP_ATTACK:
            self.special_attack_boost = boost
        elif stat == SP_DEFENSE:
            self.special_defense_boost = boost
        elif stat == SPEED:
            self.speed_boost = boost
        elif stat == ACCURACY:
            self.accuracy_boost = boost
        elif stat == EVASION:
            self.evasion_boost = boost
        else:
            print("Invalid stat code")
            return 0

    def get_boost_for_stat(self, stat):
        if stat == ATTACK:
            return self.attack_boost
        elif stat == DEFENSE:
            return self.defense_boost
        elif stat == SP_ATTACK:
            return self.special_attack_boost
        elif stat == SP_DEFENSE:
            return self.special_defense_boost
        elif stat == SPEED:
            return self.speed_boost
        elif stat == ACCURACY:
            return self.accuracy_boost
        elif stat == EVASION:
            return self.evasion_boost
        else:
            print("Invalid stat code")
            return 0

    def get_multiplier_for_stat(self, stat): # Returns the multiplier that a stat receives from a particular boost level
        if stat == ATTACK:
            curr_boost = self.attack_boost
        elif stat == DEFENSE:
            curr_boost = self.defense_boost
        elif stat == SP_ATTACK:
            curr_boost = self.special_attack_boost
        elif stat == SP_DEFENSE:
            curr_boost = self.special_defense_boost
        elif stat == SPEED:
            curr_boost = self.speed_boost
        if curr_boost == 1:
            return 1.5
        elif curr_boost == 2:
            return 2
        elif curr_boost == 3:
            return 2.5
        elif curr_boost == 4:
            return 3
        elif curr_boost == 5:
            return 3.5
        elif curr_boost == 6:
            return 4
        elif curr_boost == -1:
            return 0.66
        elif curr_boost == -2:
            return 0.5
        elif curr_boost == -3:
            return 0.4
        elif curr_boost == -4:
            return 0.33
        elif curr_boost == -5:
            return 0.28
        elif curr_boost == -6:
            return 0.25
        else:
            return 1

    def get_stat_after_status_condition(self, stat): # Returns the stat value after status conditions are applied
        if stat == ATTACK:
            if self.status_condition == BURN:
                return int(self.attack * 0.5)
            return self.attack
        elif stat == DEFENSE:
            return self.defense
        elif stat == SP_ATTACK:
            return self.special_attack
        elif stat == SP_DEFENSE:
            return self.special_defense
        elif stat == SPEED:
            if self.status_condition == PARALYSIS:
                return int(self.speed * 0.25)
            return self.speed
        
    def get_experienced_stat(self, stat): # Returns the stat value after boosts are applied
        # FIXME: May deprecate this method. damage_calc() already applies boosts. 
        if stat == ATTACK:
            if self.status_condition == BURN:
                return int(self.attack * self.get_multiplier_for_stat(ATTACK) * 0.5)
            return int(self.attack * self.get_multiplier_for_stat(ATTACK)), 42
        elif stat == DEFENSE:
            return int(self.defense * self.get_multiplier_for_stat(DEFENSE))
        elif stat == SP_ATTACK:
            return int(self.special_attack * self.get_multiplier_for_stat(SP_ATTACK))
        elif stat == SP_DEFENSE:
            return int(self.special_defense * self.get_multiplier_for_stat(SP_DEFENSE))
        elif stat == SPEED:
            if self.status_condition == PARALYSIS:
                return int(self.speed * 0.25)
            return int(self.speed * self.get_multiplier_for_stat(SPEED))

    def get_status_string(self):
        if self.status_condition == PARALYSIS:
            return "\033[33mPAR\033[0m"  # Yellow
        elif self.status_condition == POISON:
            return "\033[35mPSN\033[0m"  # Purple
        elif self.status_condition == TOXIC_POISON:
            return "\033[35mTOX\033[0m"  # Purple
        elif self.status_condition == BURN:
            return "\033[31mBRN\033[0m"  # Red
        elif self.status_condition == SLEEP:
            return "\033[34mSLP\033[0m"  # Blue
        elif self.status_condition == FREEZE:
            return "\033[36mFRZ\033[0m"  # Cyan
        else:
            return ""

    def get_list_of_valid_attack_move_numbers(self): # Returns a list of moves that are not effect moves
        moves = []
        if self.move_1:
            if self.move_1.pp > 0 and self.move_1.category == 'Physical' or self.move_1.category == 'Special': 
                moves.append(MOVE_1)
        if self.move_2:
            if self.move_2.pp > 0 and self.move_2.category == 'Physical' or self.move_2.category == 'Special':
                moves.append(MOVE_2)
        if self.move_3:
            if self.move_3.pp > 0 and self.move_3.category == 'Physical' or self.move_3.category == 'Special':
                moves.append(MOVE_3)
        if self.move_4:
            if self.move_4.pp > 0 and self.move_4.category == 'Physical' or self.move_4.category == 'Special':
                moves.append(MOVE_4)
        if moves:
            return moves
        else:
            moves.append(STRUGGLE)
            return moves

    def get_list_of_valid_move_numbers(self): # Used in getting a list of valid moves to choose from in MatchClasses.py
        moves = []
        if self.move_1:
            if self.move_1.pp > 0:
                moves.append(MOVE_1)
        if self.move_2:
            if self.move_2.pp > 0:
                moves.append(MOVE_2)
        if self.move_3:
            if self.move_3.pp > 0:
                moves.append(MOVE_3)
        if self.move_4:
            if self.move_3.pp > 0:
                moves.append(MOVE_4)
        if moves:
            return moves
        else:
            moves.append(STRUGGLE)
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

    def roll_IVs(self, floor = 0):
        self.IV_HP = rng.randint(floor, 31)
        self.IV_attack = rng.randint(floor, 31)
        self.IV_defense = rng.randint(floor, 31)
        self.IV_special_attack = rng.randint(floor, 31)
        self.IV_special_defense = rng.randint(floor, 31)
        self.IV_speed = rng.randint(floor, 31)

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

    def level_up(self, increment_level_amount = 1, visualization = True): # Levels up the monster by 1
        level_increase = increment_level_amount
        if self.level + level_increase > 100:
            level_increase = 100 - self.level
        if self.level + level_increase <= 100 and level_increase > 0:
            old_max_hp = self.max_HP
            old_attack = self.attack
            old_defense = self.defense
            old_special_attack = self.special_attack
            old_special_defense = self.special_defense
            old_speed = self.speed
            self.level += level_increase
            self.calculate_stats() 
            if visualization:
                print(f"\33[36m{self.name} leveled up to level {self.level}!\33[0m", end=' ( ')
                print(f"HP: {old_max_hp} -> {self.max_HP}", end=' | ')
                print(f"Attack: {old_attack} -> {self.attack}", end=' | ')
                print(f"Defense: {old_defense} -> {self.defense}", end=' | ')
                print(f"Special Attack: {old_special_attack} -> {self.special_attack}", end=' | ')
                print(f"Special Defense: {old_special_defense} -> {self.special_defense}", end=' | ')
                print(f"Speed: {old_speed} -> {self.speed}", end=' )')
                print()
            hp_difference = self.max_HP - old_max_hp
            self.HP += hp_difference
            if self.fainted:
                self.fainted = False
                self.not_fainted = True
            if self.level_condition_met_to_evolve():
                self.evolve(visualization=visualization)
            # Reset exp to 0
            # Calculate exp to next level, assign it to a parameter

    def level_condition_met_to_evolve(self):
        if self.evolution_method.isnumeric():
            if self.level >= int(self.evolution_method):
                return True
        else:
            return False

    def evolve(self, visualization = True):
        if self.evolve_id:
            new_mon_id = self.evolve_id
        else:
            new_mon_id = str(int(self.id) + 1)
        monster_data = None  # Variable to store the matched row
        with open(MONSTER_DATA_DIRECTORY, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == str(new_mon_id) and row[1] == str(self.code):
                    monster_data = row  # Assign the matched row to the variable
                    break  # Terminate the loop when a match is found
        if monster_data is not None:
            self.id = monster_data[0]
            old_name = self.name
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
            self.evolution_method = monster_data[22]
            if self.evolution_method:
                self.can_evolve = True
            else:
                self.can_evolve = False
            self.evolve_id = monster_data[23]
            old_max_hp = self.max_HP
            self.calculate_stats()
            hp_difference = self.max_HP - old_max_hp
            self.HP += hp_difference
            self.learn_set = monster_data[24].split(',')
            # Delete old moves
            self.move_1 = None
            self.move_2 = None
            self.move_3 = None
            self.move_4 = None
            self.number_of_moves = 0
            # Learn new moves
            for move in self.learn_set:
                self.add_move(int(move))
            if self.number_of_moves == 0:
                self.add_move(1)
                print("No moves found, learned Tackle")
            if visualization:
                print(f"\33[35m{old_name} evolved into {self.name}!", end='\33[0m ')
                print("( HP: " + str(self.max_HP), end=' | ')
                print("Attack: " + str(self.attack), end=' | ')
                print("Defense: " + str(self.defense), end=' | ')
                print("Special Attack: " + str(self.special_attack), end=' | ')
                print("Special Defense: " + str(self.special_defense), end=' | ')
                print("Speed: " + str(self.speed), end=' | ')
                print("+ New moves learned )")
                #print(self)
        else:
            print("No evolution data found")       

    def fully_heal(self): # Fully heals the monster
        self.HP = self.max_HP
        if self.move_1:
            self.move_1.pp = self.move_1.base_pp
        if self.move_2:
            self.move_2.pp = self.move_2.base_pp
        if self.move_3:
            self.move_3.pp = self.move_3.base_pp
        if self.move_4:
            self.move_4.pp = self.move_4.base_pp
        self.status_condition = None
        self.reset_boosts()
        self.fainted = False
        self.not_fainted = True
        
    def deep_copy(self): # Returns a deep copy of the monster, used in Monte Carlo Tree Search
        new_monster = Monster(deep_copy=self)
        return new_monster

def generated_monster(number_id, level):
    new_monster = Monster(number_id, 1)
    levels_to_add = level - 1
    while levels_to_add > 0:
        new_monster.level_up(visualization=False)
        levels_to_add -= 1

VICTINI = 494
SNIVY = 495
SERVINE = 496
SERPERIOR = 497
TEPIG = 498
PIGNITE = 499
EMBOAR = 500
OSHAWOTT = 501
DEWOTT = 502
SAMUROTT = 503
PATRAT = 504
WATCHOG = 505
LILLIPUP = 506
HERDIER = 507
STOUTLAND = 508
PURRLOIN = 509
LIEPARD = 510
PANSAGE = 511
SIMISAGE = 512
PANSEAR = 513
SIMISEAR = 514
PANPOUR = 515
SIMIPOUR = 516
MUNNA = 517
MUSHARNA = 518
PIDOVE = 519
TRANQUILL = 520
UNFEZANT = 521
BLITZLE = 522
ZEBSTRIKA = 523
ROGGENROLA = 524
BOLDORE = 525
GIGALITH = 526
WOOBAT = 527
SWOOBAT = 528
DRILBUR = 529
EXCADRILL = 530
AUDINO = 531
TIMBURR = 532
GURDURR = 533
CONKELDURR = 534
TYMPOLE = 535
PALPITOAD = 536
SEISMITOAD = 537
THROH = 538
SAWK = 539
SEWADDLE = 540
SWADLOON = 541
LEAVANNY = 542
VENIPEDE = 543
WHIRLIPEDE = 544
SCOLIPEDE = 545
COTTONEE = 546
WHIMSICOTT = 547
PETILIL = 548
LILLIGANT = 549
BASCULIN = 550
SANDILE = 551
KROKOROK = 552
KROOKODILE = 553
DARUMAKA = 554
DARMANITAN = 555
MARACTUS = 556
DWEBBLE = 557
CRUSTLE = 558
SCRAGGY = 559
SCRAFTY = 560
SIGILYPH = 561
YAMASK = 562
COFAGRIGUS = 563
TIRTOUGA = 564
CARRACOSTA = 565
ARCHEN = 566
ARCHEOPS = 567
TRUBBISH = 568
GARBODOR = 569
ZORUA = 570
ZOROARK = 571
MINCCINO = 572
CINCCINO = 573
GOTHITA = 574
GOTHORITA = 575
GOTHITELLE = 576
SOLOSIS = 577
DUOSION = 578
REUNICLUS = 579
DUCKLETT = 580
SWANNA = 581
VANILLITE = 582
VANILLISH = 583
VANILLUXE = 584
DEERLING = 585
SAWSBUCK = 586
EMOLGA = 587
KARRABLAST = 588
ESCAVALIER = 589
FOONGUS = 590
AMOONGUSS = 591
FRILLISH = 592
JELLICENT = 593
ALOMOMOLA = 594
JOLTIK = 595
GALVANTULA = 596
FERROSEED = 597
FERROTHORN = 598
KLINK = 599
KLANG = 600
KLINKLANG = 601
TYNAMO = 602
EELEKTRIK = 603
EELEKTROSS = 604
ELGYEM = 605
BEHEEYEM = 606
LITWICK = 607
LAMPENT = 608
CHANDELURE = 609
AXEW = 610
FRAXURE = 611
HAXORUS = 612
CUBCHOO = 613
BEARTIC = 614
CRYOGONAL = 615
SHELMET = 616
ACCELGOR = 617
STUNFISK = 618
MIENFOO = 619
MIENSHAO = 620
DRUDDIGON = 621
GOLETT = 622
GOLURK = 623
PAWNIARD = 624
BISHARP = 625
BOUFFALANT = 626
RUFFLET = 627
BRAVIARY = 628
VULLABY = 629
MANDIBUZZ = 630
HEATMOR = 631
DURANT = 632
DEINO = 633
ZWEILOUS = 634
HYDREIGON = 635
LARVESTA = 636
VOLCARONA = 637
COBALION = 638
TERRAKION = 639
VIRIZION = 640
TORNADUS = 641
THUNDURUS = 642
RESHIRAM = 643
ZEKROM = 644
LANDORUS = 645
KYUREM = 646
KELDEO = 647
MELOETTA = 648
GENESECT = 649

STARTERS = [SNIVY, TEPIG, OSHAWOTT]
MYTHICALS = [VICTINI, COBALION, TERRAKION, VIRIZION, TORNADUS, THUNDURUS, LANDORUS, KELDEO, MELOETTA, GENESECT]
MYTHICAL_1 = [VICTINI,MELOETTA,GENESECT]
MYTHICAL_2 = [COBALION,TERRAKION,VIRIZION,KELDEO]
MYTHICAL_3 = [TORNADUS,THUNDURUS,LANDORUS]
LEGENDARIES = [RESHIRAM, ZEKROM, KYUREM]

# When generating roster, flip coin for each pair. Tally up number of heads and tails. if heads > tails, region legendary is RESHIRAM, else ZEKROM
STARTER_ENVIRONMENT = ['Pasture']
COMMON_ENVIRONMENTS = ['Pasture', 'Forest', 'Urban']
UNCOMMON_ENVIRONMENTS = ['Desert', 'Cave', 'Ocean']
RARE_ENVIRONMENTS = ['Mountain', 'Charge Cave', 'Ruins', 'Rugged']
ELEMENTAL_ENVIRONMENTS = ['Wet', 'Heat', 'Lush', 'Energised']
ENVIRONMENTS = ['Pasture', 'Forest', 'Town', 'Desert', 'Cave', 'Charge Cave', 'Mountain', 'Ocean', 'Ruins', 'Rugged']

MYTHICAL_EXCLUSIVES = [TORNADUS,THUNDURUS]
FOREST_EXCLUSIVES_1 = [SAWK,THROH]
FOREST_EXCLUSIVES_2 = [PETILIL,COTTONEE]
TOWN_EXCLUSIVES = [GOTHITA, SOLOSIS]
MOUNTAIN_EXCLUSIVES = [VULLABY, RUFFLET]
FOSSIL_EXCLUSIVES = [TIRTOUGA, ARCHEN]
RUGGED_EXCLUSIVES = [HEATMOR, DURANT]

LEGENDARY_EXCLUSIVE = [RESHIRAM, ZEKROM]


PASTURE_COMMON_1 = [PATRAT, LILLIPUP, PIDOVE]
PASTURE_UNCOMMON_1 = [MINCCINO, PURRLOIN]
PASTURE_RARE_1 = [AUDINO, MUNNA]

FOREST_COMMON_1 = [PANSAGE, SEWADDLE, TYMPOLE, BLITZLE, PANSAGE]
FOREST_UNCOMMON_1 = [WOOBAT, VENIPEDE, TIMBURR]
FOREST_RARE_1 = [AUDINO,FOONGUS]

TOWN_COMMON_1 = [TRUBBISH,VANILLITE,DUCKLETT,PIDOVE]
TOWN_UNCOMMON_1 = [EMOLGA, MINCCINO]
TOWN_RARE_1 = [ZORUA]

DESERT_COMMON_1 = [SCRAGGY, DWEBBLE, SANDILE]
DESERT_UNCOMMON_1 = [MARACTUS, DARUMAKA]
DESERT_RARE_1 = [SIGILYPH, YAMASK]

CAVE_COMMON_1 = [ROGGENROLA, TIMBURR, TYMPOLE]
CAVE_UNCOMMON_1 = [WOOBAT]
CAVE_RARE_1 = [DRILBUR]

CHARGE_CAVE_COMMON_1 = [JOLTIK, KLINK, ROGGENROLA]
CHARGE_CAVE_UNCOMMON_1 = [FERROSEED, TYNAMO]
CHARGE_CAVE_RARE_1 = [DRILBUR]

MOUNTAIN_COMMON_1 = [CUBCHOO, ROGGENROLA, WOOBAT, DEERLING, PANSEAR]
MOUNTAIN_UNCOMMON_1 = [MIENFOO, CRYOGONAL, KARRABLAST, SHELMET]
MOUNTAIN_RARE_1 = [DRILBUR, AXEW]

OCEAN_COMMON_1 = [BASCULIN, PANPOUR]
OCEAN_UNCOMMON_1 = [FRILLISH]
OCEAN_RARE_1 = [ALOMOMOLA]

RUINS_COMMON_1 = [LITWICK, ELGYEM, WOOBAT]
RUINS_UNCOMMON_1 = [YAMASK,GOLETT]
RUINS_RARE_1 = [DRUDDIGON,LARVESTA]

RUGGED_COMMON_1 = [PAWNIARD, BOUFFALANT]
RUGGED_UNCOMMON_1 = [DWEBBLE, SCRAFTY, VENIPEDE]
RUGGED_RARE_1 = [DRILBUR, DEINO]

HEAT_COMMON_1 = [DARUMAKA,ROGGENROLA,PANSEAR,SANDILE,DWEBBLE]
HEAT_UNCOMMON_1 = [MARACTUS, HEATMOR]
HEAT_RARE_1 = [TEPIG,LARVESTA]
WET_COMMON_1 = [DUCKLETT,FRILLISH,STUNFISK,TYMPOLE,ALOMOMOLA,BASCULIN]
WET_UNCOMMON_1 = [STUNFISK,PANPOUR]
WET_RARE_1 = [OSHAWOTT,TIRTOUGA]
LUSH_COMMON_1 = [DEERLING,SEWADDLE,PETILIL,COTTONEE,FOONGUS]
LUSH_UNCOMMON_1 = [MARACTUS,PANSAGE]
LUSH_RARE_1 = [SNIVY,FERROSEED]
ENERGISED_COMMON_1 = [BLITZLE,JOLTIK,KLINK,TYNAMO,MIENFOO]
ENERGISED_UNCOMMON_1 = [EMOLGA,SAWK,THROH]
ENERGISED_RARE_1 = [DRILBUR,AXEW]

BLACK_EXCLUSIVE = 0
WHITE_EXCLUSIVE = 1

if __name__ == "__main__":
    TestMonster = Monster(DEWOTT, 35)
    print(TestMonster)
    TestMonster.level_up()
    TestMonster.set_poison()
    print(TestMonster)