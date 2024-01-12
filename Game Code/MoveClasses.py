import csv

# --- Effect Constants ---
PARALYSIS = 0
BURN = 1
POISON = 2
TOXIC_POISON = 3
SLEEP = 4
FROZEN = 5
CONFUSION = 6




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
