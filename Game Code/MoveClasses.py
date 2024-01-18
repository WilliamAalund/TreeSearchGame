import csv
import random as rng

# --- Effect Constants ---
PARALYSIS = 0
BURN = 1
POISON = 2
TOXIC_POISON = 3
SLEEP = 4
FROZEN = 5
CONFUSION = 6

IMPLEMENTED_EFFECTS = ['None']


class Move:
    def __init__(self, number_id = 1, deep_copy = None) -> None:
        if deep_copy:
            self.number_id = deep_copy.number_id
            self.name = deep_copy.name
            self.type = deep_copy.type
            self.category = deep_copy.category
            self.base_power = deep_copy.base_power
            self.accuracy = deep_copy.accuracy
            self.base_pp = deep_copy.base_pp
            self.effect_chance = deep_copy.effect_chance
            self.priority = deep_copy.priority
            self.effect = deep_copy.effect
            self.effect_magnitude = deep_copy.effect_magnitude
            self.makes_contact = deep_copy.makes_contact
            self.targets_multiple = deep_copy.targets_multiple
            self.description = deep_copy.description
            self.pp = deep_copy.pp
            return
        else:
            move_data = 0
            with open('moves.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == str(number_id):
                        move_data = row  # Assign the matched row to the variable
                        break  # Terminate the loop when a match is found
            if move_data: # Check if data is truthy
                self.number_id = number_id
                self.name = move_data[1]
                self.type = move_data[2]
                self.category = move_data[3]
                self.base_power = int(move_data[4])
                self.accuracy = int(move_data[5])
                self.base_pp = int(move_data[6])
                self.effect_chance = float(move_data[7])
                self.priority = int(move_data[8])
                self.effect = move_data[9]
                if self.effect not in IMPLEMENTED_EFFECTS and __name__ == "__main__":
                    print("The effect '", self.effect, "' is not implemented")
                self.effect_magnitude = float(move_data[10])
                if move_data[11] == "Y":
                    self.makes_contact = True
                else:
                    self.makes_contact = False
                self.targeting = move_data[12]
                if self.targeting == "D":
                    self.targets_multiple = True
                else:
                    self.targets_multiple = False
                self.description = move_data[13]
                self.pp = self.base_pp
            else:
                print("Move not found, object is invalid")

    def __str__(self) -> str:
        return self.name + " | PP: " + str(self.pp) + "/" + str(self.base_pp) + " | " + self.type + " | " + self.category + " | Base Power: " + str(self.base_power) + " | Accuracy: " + (str(self.accuracy) if self.accuracy != 101 else "-") + " | " + ((str(self.description)) if self.description else "")

    def is_move_usable(self):
        if self.pp > 0:
            return True
        else:
            return False

    def get_priority(self):
        return self.priority
    
    def get_accuracy_check(self):
        if self.accuracy == 101:
            return True
        else:
            roll = rng.randint(1,100)
            if roll <= self.accuracy:
                return True
            else:
                return False

    def expend_pp(self):
        self.pp -= 1
        if self.pp < 0:
            self.pp = 0
    
    def deep_copy(self):
        copy_move = Move(deep_copy=self)
        return copy_move

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

if __name__ == "__main__":
    Tackle = Move(2)
    print(Tackle)
