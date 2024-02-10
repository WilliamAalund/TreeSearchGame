import math

MAX_TEAM_SIZE = 6

class Team:
    def __init__(self, name="Team", level=1, wild = False) -> None:
        self.name = name
        self.team_members = []
        self.team_size = 0
        self.team_level = level
        self.team_members_healthy = 0
        self.active_member_index = 0
        self.wild = wild

    def __str__(self) -> str:
        result = ''
        for monster in self.team_members:
            result += str(monster) + '\n'
        return result
        team_members_names = [str(member.name) for member in self.team_members]
        return f"Team: {self.name} | Team size: {self.team_size} | Team level: {self.team_level} | Team members: {', '.join(team_members_names)}"

    def small_str(self):
        result = ''
        for monster in self.team_members:
            result += monster.name + '\n'
        return result

    def calculate_team_level(self):
        team_level = 1
        collective_monster_level = 0
        if self.team_size > 0:
            for monster in self.team_members:
                collective_monster_level += monster.level
            team_level = collective_monster_level / self.team_size
        self.team_level = math.floor(team_level)


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

    def get_members(self):
        print(len(self.team_members))
        return self.team_members

    def get_member_names(self):
        names = []
        for monster in self.team_members:
            names.append(monster.name)
        return names
    
    def get_member_names_and_hp(self):
        names = []
        for monster in self.team_members:
            names.append(monster.name + " " + str(monster.HP) + "/" + str(monster.max_HP))
        return names

    def get_active_member(self):
        return self.team_members[self.active_member_index]

    def has_non_fainted_members(self):
        self.update_team_members_healthy()
        return self.team_members_healthy > 0

    def update_team_members_healthy(self):
        self.team_members_healthy = 0
        for monster in self.team_members:
            if not monster.fainted:
                self.team_members_healthy += 1

    def change_monster_order_in_team(self, index1, index2):
        if index1 < self.team_size and index2 < self.team_size:
            temp = self.team_members[index1]
            self.team_members[index1] = self.team_members[index2]
            self.team_members[index2] = temp
        else:
            print("Index out of range")
    
    def switch_active_member(self, index, reset_boosts = True):
        if index in self.get_list_of_valid_switch_indices():
            self.get_active_member().reset_boosts()
            self.get_active_member().reset_semi_permanent_status_conditions()
            self.active_member_index = index
        else:
            #print(self.name, "switch_active_member error: invalid switch index:" , index)
            pass

    def get_number_of_members_to_switch_to(self):
        return self.team_members_healthy - 1
    
    def get_list_of_member_names_to_switch_to(self):
        member_names = []
        for i in range(self.team_size):
            if i != self.active_member_index and not self.team_members[i].fainted:
                member_names.append(self.team_members[i].name)
        return member_names

    def get_list_of_members_to_switch_to(self):
        members = []
        for i in range(self.team_size):
            if i != self.active_member_index and not self.team_members[i].fainted:
                members.append(self.team_members[i])
        return members
    
    def get_initial_active_member_index(self):
        for i in range(self.team_size):
            if not self.team_members[i].fainted:
                return i
        return -1

    def reset_active_member_boosts(self):
        self.team_members[self.active_member_index].reset_boosts()

    def get_list_of_valid_switch_indices(self):
        valid_indices = []
        for i in range(self.team_size):
            if i != self.active_member_index and not self.team_members[i].fainted:
                valid_indices.append(i)
        return valid_indices

    def get_number_of_members_fainted(self):
        return self.team_size - self.team_members_healthy

    def get_leading_member_index(self):
        curr_index = 0
        for monster in self.team_members:
            if not monster.fainted:
                return curr_index
            curr_index += 1
        print("Error: No leading member found")
        return -1

    def is_active_member_fainted(self):
        return self.team_members[self.active_member_index].fainted
    
    def fully_heal_team(self):
        for monster in self.team_members:
            monster.fully_heal()

    def level_up(self, level):
        for monster in self.team_members:
            if not monster.fainted:
                if monster.level < self.team_level:
                    monster.level_up(level * 2)
                else:
                    monster.level_up(level)
        self.calculate_team_level()

    def deep_copy(self):
        new_team = Team()
        new_team.name = self.name
        new_team.active_member_index = self.active_member_index
        new_team.team_level = self.team_level
        new_team.team_members_healthy = self.team_members_healthy
        for monster in self.team_members:
            new_team.add_member(monster.deep_copy())
        new_team.team_size = self.team_size
        return new_team