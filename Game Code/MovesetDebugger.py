import csv
from MoveClasses import Move

STATUS_NOT_IMPLEMENTED = ['Poison','Burn','Paralysis','Sleep','Frozen', 'Confusion', 'Taunt']


def print_movesets(lower_bound, upper_bound):
    with open('monsters.csv', 'r') as file:
        reader = csv.reader(file)
        id = lower_bound
        for row in reader:
            if row[0] == str(id):
                name = row[3]
                ability = row[7]
                moveset = row[24]
                print(name, end=': ')
                if ability:
                    print("(",ability,")", end=' ')
                for i in moveset.split(','):
                    if i:
                        move = Move(int(i))
                        print(move.name, end=', ')
                    else:
                        print("No moves", end=' ')
                print()
                id += 1
            if id > upper_bound:
                break


# Call the function with the desired range
print_movesets(494, 649)