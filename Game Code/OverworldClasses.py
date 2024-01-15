from TeamClass import Team

# ------------- UNIMPLEMENTED CLASSES -------------
class Item:
    def __init__(self) -> None:
        pass

class Bag:
    def __init__(self) -> None:
        pass   

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