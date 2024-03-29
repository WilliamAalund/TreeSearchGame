from TeamClass import *
from MonsterClasses import *
from ItemClasses import *
import GameMenus as gm

class Player:
    def __init__(self):
        self.name = "Player"
        self.trainer_level = 13
        self.experience = 0
        self.experience_needed_to_level_up = 4
        self.team: Team = Team(self.name, 5)
        self.bag = Bag()
        self.pick_starter()

    def pick_starter(self):
        starter_1 = Monster(STARTER_1, self.team.team_level)
        starter_2 = Monster(STARTER_2, self.team.team_level)
        starter_3 = Monster(STARTER_3, self.team.team_level)
        starter_1_name = "\33[32m" + starter_1.name + "\33[0m"
        starter_2_name = "\33[31m" + starter_2.name + "\33[0m"
        starter_3_name = "\33[34m" + starter_3.name + "\33[0m"
        starter_choice = gm.starter_menu(starter_1_name, starter_2_name, starter_3_name)
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
        print(self.team.get_active_member())
        gm.generic_continue()

    def heal_team(self):
        self.team.fully_heal_team()

    def level_up(self, level):
        self.team.level_up(level)

    def add_experience(self, experience):
        self.experience += experience
        if self.experience >= self.experience_needed_to_level_up:
            self.experience -= self.experience_needed_to_level_up
            if self.experience < 0:
                self.experience = 0
            self.level_up(1)

    def view_team(self):
        in_menu = True
        names = self.team.get_member_names_and_hp()
        while in_menu:
            print()
            message = "Party level: " + str(self.team.team_level) + " | Experience to party level up: " + str(self.experience_needed_to_level_up - self.experience)
            print(message)
            if len(names) == 0:
                print("No team members")
                in_menu = False
            elif len(names) == 1:
                choice = gm.generic_input("Choose a monster to view:", names[0], "Back")
            elif len(names) == 2:
                choice = gm.generic_input("Choose a monster to view:", names[0], names[1], "Back")
            elif len(names) == 3:
                choice = gm.generic_input("Choose a monster to view:", names[0], names[1], names[2], "Back")
            elif len(names) == 4:
                choice = gm.generic_input("Choose a monster to view:", names[0], names[1], names[2], names[3], "Back")
            elif len(names) == 5:
                choice = gm.generic_input("Choose a monster to view:", names[0], names[1], names[2], names[3], names[4], "Back")
            elif len(names) == 6:
                choice = gm.generic_input("Choose a monster to view:", names[0], names[1], names[2], names[3], names[4], names[5], "Back")
            if choice in range(len(names)):
                print(self.team.get_member(choice))
            else:
                in_menu = False


    def get_amount_of_pokeballs(self):
        return self.bag.get_pokeballs()

    def get_name(self):
        return self.name

    def get_trainer_level(self):
        return self.trainer_level

    def get_team(self):
        return self.team

if __name__ == "__main__":
    test_player = Player()
