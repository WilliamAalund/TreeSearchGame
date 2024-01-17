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

NATURE_DICT = {'Hardy': (ATTACK, ATTACK), 'Lonely': (ATTACK, DEFENSE), 'Adamant': (ATTACK, SP_ATTACK), 'Naughty': (ATTACK, SP_DEFENSE), 'Brave': (ATTACK, SPEED),
              'Bold': (DEFENSE, ATTACK), 'Docile': (DEFENSE, DEFENSE), 'Impish': (DEFENSE, SP_ATTACK), 'Lax': (ATTACK, SP_DEFENSE), 'Relaxed': (DEFENSE, SPEED),
              'Modest': (SP_ATTACK, ATTACK), 'Mild': (SP_ATTACK, DEFENSE), 'Bashful': (SP_ATTACK, SP_ATTACK), 'Rash': (SP_ATTACK, SP_DEFENSE), 'Quiet': (SP_ATTACK, SPEED),
              'Calm': (SP_DEFENSE, ATTACK), 'Gentle': (SP_DEFENSE, DEFENSE), 'Careful': (SP_DEFENSE, SP_ATTACK), 'Quirky': (SP_DEFENSE, SP_DEFENSE), 'Sassy': (SP_DEFENSE, SPEED),
              'Timid': (SPEED, ATTACK), 'Hasty': (SPEED, DEFENSE), 'Jolly': (SPEED, SP_ATTACK), 'Naive': (SPEED, SP_DEFENSE), 'Serious': (SPEED, SPEED)}

class Monster: #TODO: set up move database for each monster
    def __init__(self, number_id=1, level=1, code=1, deep_copy=None) -> None:
        
        self.attack_boost = 0
        self.defense_boost = 0
        self.special_attack_boost = 0
        self.special_defense_boost = 0
        self.speed_boost = 0
        self.accuracy_boost = 0
        self.evasion_boost = 0
        self.crit_chance = 0

        if deep_copy:
            self.name = deep_copy.name
            self.not_fainted = deep_copy.not_fainted
            self.fainted = deep_copy.fainted
            self.status = deep_copy.status
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
            self.learn_set = deep_copy.learn_set


            return
        else:
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
                self.learn_set = monster_data[24].split(',')
                
                for move in self.learn_set:
                    self.add_move(int(move))
                if self.number_of_moves == 0:
                    self.add_move(1)
            else:
                print("Monster not found, object is invalid")
    
    def __str__(self) -> str:
        stats = f"HP: {self.HP}\nAttack: {self.attack}\nDefense: {self.defense}\nSpecial Attack: {self.special_attack}\nSpecial Defense: {self.special_defense}\nSpeed: {self.speed}"
        if self.move_1:
            stats += f"\n{self.move_1.name} (PP: {self.move_1.pp})"
        else:
            stats += "\n - "
        if self.move_2:
            stats += f" {self.move_2.name} (PP: {self.move_2.pp})"
        else:
            stats += " - "
        if self.move_3:
            stats += f" {self.move_3.name} (PP: {self.move_3.pp})"
        else:
            stats += " - "
        if self.move_4:
            stats += f" {self.move_4.name} (PP: {self.move_4.pp})"
        else:
            stats += " - "
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

    def reset_boosts(self):
        self.attack_boost = 0
        self.defense_boost = 0
        self.special_attack_boost = 0
        self.special_defense_boost = 0
        self.speed_boost = 0
        self.accuracy_boost = 0
        self.evasion_boost = 0
        self.crit_chance = 0

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
        self.status = None
        self.reset_boosts()
        self.fainted = False
        self.not_fainted = True
        
    def deep_copy(self): # Returns a deep copy of the monster, used in Monte Carlo Tree Search
        new_monster = Monster(deep_copy=self)
        return new_monster

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





if __name__ == "__main__":
    TestMonster = Monster(501, 50)
    TestMonster2 = Monster(501, 50)
    print(TestMonster.get_strongest_move_against(TestMonster2))


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
MYTHICAL_EXCLUSIVES = [TORNADUS,THUNDURUS]
FOREST_EXCLUSIVES_1 = [SAWK,THROH]
FOREST_EXCLUSIVES_2 = [PETILIL,COTTONEE]
TOWN_EXCLUSIVES = [GOTHITA, SOLOSIS]
MOUNTAIN_EXCLUSIVES = [VULLABY, RUFFLET]
FOSSIL_EXCLUSIVES = [TIRTOUGA, ARCHEN]
RUGGED_EXCLUSIVES = [HEATMOR, DURANT]

PASTURE_COMMON_1 = [PATRAT, LILLIPUP, PURRLOIN, PIDOVE]
PASTURE_UNCOMMON_1 = [MINCCINO, PANSAGE, PANSEAR, PANPOUR]
PASTURE_RARE_1 = [AUDINO, MUNNA]

FOREST_COMMON_1 = [PANSAGE, SEWADDLE, TYMPOLE, BLITZLE]
FOREST_UNCOMMON_1 = [WOOBAT, VENIPEDE, TIMBURR]
FOREST_RARE_1 = [AUDINO,FOONGUS]

FOREST_COMMON_2 = [DEERLING, KARRABLAST, SHELMET]

CITY_COMMON_1 = [PIDOVE, TRUBBISH, MINCCINO]

TOWN_COMMON_1 = [TRUBBISH,VANILLITE,DUCKLETT]
TOWN_UNCOMMON_1 = [EMOLGA]
TOWN_RARE_1 = [ZORUA]

DESERT_COMMON_1 = [SCRAGGY, DWEBBLE, SANDILE]
DESERT_UNCOMMON_1 = [MARACTUS, DARUMAKA]
DESERT_RARE_1 = [SIGILYPH, YAMASK]

CAVE_COMMON_1 = [ROGGENROLA, WOOBAT, TIMBURR, TYMPOLE]
CAVE_UNCOMMON_1 = [DRILBUR]
CAVE_RARE_1 = [AXEW, DEINO]

CHARGE_CAVE_COMMON_1 = [JOLTIK, TYNAMO, KLINK]
CHARGE_CAVE_UNCOMMON_1 = [FERROSEED]

MOUNTAIN_COMMON_1 = [CRYOGONAL,CUBCHOO]
MOUNTAIN_UNCOMMON_1 = [DEINO, MIENFOO]

OCEAN_COMMON_1 = [BASCULIN]
OCEAN_UNCOMMON_1 = [FRILLISH]
OCEAN_RARE_1 = [ALOMOMOLA]

RUINS_COMMON_1 = [LITWICK, ELGYEM]
RUINS_UNCOMMON_1 = [YAMASK,DRUDDIGON,GOLETT]
RUINS_RARE_1 = [LARVESTA]

RUGGED_COMMON_1 = [PAWNIARD, BOUFFALANT]

HEAT = [TEPIG,DARUMAKA,HEATMOR,LARVESTA,MARACTUS,ROGGENROLA,PANSEAR,SANDILE,DWEBBLE]
WET = [OSHAWOTT,DUCKLETT,FRILLISH,STUNFISK,TYMPOLE,TIRTOUGA,ALOMOMOLA,PANPOUR,BASCULIN]
LUSH = [SNIVY,DEERLING,SEWADDLE,PETILIL,COTTONEE,PANSAGE,MARACTUS,FOONGUS,FERROSEED]
ENERGISED = [BLITZLE,EMOLGA,JOLTIK,KLINK,TYNAMO,DRILBUR,AXEW,MIENFOO,SAWK,THROH]

