from TeamClass import *
from MonsterClasses import *
from ItemClasses import *
import GameMenus as gm

class Player:
    def __init__(self):
        self.name = "Player"
        self.team = Team(self.name, level=5)
        self.bag = Bag()
        self.pick_starter()

    def pick_starter(self):
        starter_1 = Monster(STARTER_1, self.team.team_level)
        starter_2 = Monster(STARTER_2, self.team.team_level)
        starter_3 = Monster(STARTER_3, self.team.team_level)
        starter_choice = gm.starter_menu(starter_1.name, starter_2.name, starter_3.name)
        if starter_choice == 0:
            self.team.add_member(starter_1)
        elif starter_choice == 1:
            self.team.add_member(starter_2)
        elif starter_choice == 2:
            self.team.add_member(starter_3)
        else:
            print("Error: Invalid starter choice")
            return
        print("Player picked " + self.team.get_active_member().name + " as their starter")
        print(self.team)

if __name__ == "__main__":
    test_player = Player()
