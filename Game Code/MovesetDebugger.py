import csv
from MoveClasses import Move

STATUS_NOT_IMPLEMENTED = ['Poison','Burn','Paralysis','Sleep','Frozen', 'Confusion', 'Taunt']

DATA_LOWER_BOUND = 494
DATA_UPPER_BOUND = 649

TEST_DATA_LOWER_BOUND = 1
TEST_DATA_UPPER_BOUND = 649

NAME_COLUMN = 3
ABILITY_COLUMN = 7
MOVES_COLUMN = 24

SPREADSHEET_NAME = 'monsterstest.csv'
MOVE_SPREADSHEET_NAME = 'Moves.csv'

MOVE_SPREADSHEET_LOWER_BOUND = 1
MOVE_SPREADSHEET_UPPER_BOUND = 160

def print_moves_and_ids(lower_bound, upper_bound, row_number_of_entries = 10):
    with open(MOVE_SPREADSHEET_NAME, 'r') as file:
        reader = csv.reader(file)
        id = lower_bound
        curr_type = "TYPE"
        curr_row_number_of_entries = 0
        for row in reader:
            if curr_type != row[2]:
                curr_type = row[2]
                print()
                print("\033[33m" + row[2] + ": \033[0m", end='')
                curr_row_number_of_entries = 0
            curr_row_number_of_entries += 1
            if curr_row_number_of_entries == row_number_of_entries:
                print()
                curr_row_number_of_entries = 0
            print(row[0], end=': ')
            print(row[1], end=' | ')
        print()



def print_movesets(lower_bound, upper_bound):
    with open(SPREADSHEET_NAME, 'r') as file:
        reader = csv.reader(file)
        id = lower_bound
        for row in reader:
            if row[0] == str(id):
                name = row[NAME_COLUMN]
                ability = row[ABILITY_COLUMN]
                moveset = row[MOVES_COLUMN]
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

def print_names_and_ids(lower_bound, upper_bound, row_number_of_entries = 10):
    with open(SPREADSHEET_NAME, 'r') as file:
        reader = csv.reader(file)
        id = lower_bound
        curr_row_number_of_entries = 0
        for row in reader:
            if row[0] == str(id):
                print(row[NAME_COLUMN], end=': ')
                print(id, end= ' | ')
                id += 1
                curr_row_number_of_entries += 1
                if curr_row_number_of_entries == row_number_of_entries:
                    print()
                    curr_row_number_of_entries = 0
            if id > upper_bound:
                break
    print()

def open_and_edit_row_of_entry(id):
    if id.isnumeric():
        int_id = int(id)
        if int_id < DATA_LOWER_BOUND or int_id > DATA_UPPER_BOUND:
            print("Numeric entry out of bounds")
            return None

    data = []
    data_entry = None
    with open(SPREADSHEET_NAME, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if not data_entry:
                if id.isnumeric() and row[0] == str(id):
                    data_entry = row
                elif row[3] == str(id):
                    data_entry = row
            data.append(row)

    if data_entry:
        print("Data entry found")
        uinp = ''
        while uinp != 'q' and uinp != 'z':
            print()
            metadata = format_data_entry(data_entry)
            number_of_moves = metadata[0]
            uinp = input("Actions: 'a': add, 'r': remove, 'e' + number: edit a move, 'z': end + save, 'q': end: ")
            if uinp == 'a':
                if number_of_moves == 4:
                    print("Cannot add more moves")
                    continue
                print("Adding a move")
                print()
                print_moves_and_ids(MOVE_SPREADSHEET_LOWER_BOUND, MOVE_SPREADSHEET_UPPER_BOUND)
                new_move_id = input("Enter the number of the move you want to add: ")
                # Validate new_move_id
                if new_move_id.isnumeric():
                    int_new_move_id = int(new_move_id)
                    if not int_new_move_id < MOVE_SPREADSHEET_LOWER_BOUND and not int_new_move_id > MOVE_SPREADSHEET_UPPER_BOUND:
                        # Validate that move is not already in moveset
                        if new_move_id in data_entry[MOVES_COLUMN].split(','):
                            print("Move already in moveset")
                            continue
                        print("Valid move id: " + new_move_id)
                        # TODO: Add move to moveset
                        moves = data_entry[MOVES_COLUMN].split(',')
                        moves.append(str(new_move_id))
                        data_entry[MOVES_COLUMN] = ','.join(moves)
                    else:
                        print("Invalid move id, id out of bounds")
                        continue
                else:
                    print("Invalid move id, id is not a number")
                    continue
            elif uinp == 'r':
                if number_of_moves == 0:
                    print("Cannot remove more moves")
                    continue
                print("Removing a move")
                moves = data_entry[MOVES_COLUMN].split(',')
                moves.remove(moves[-1])
                data_entry[MOVES_COLUMN] = ','.join(moves)
            elif uinp[0] == 'e' and len(uinp) == 2 and uinp[1].isnumeric():
                
                
                move_number_to_edit = int(uinp[1])
                if move_number_to_edit > number_of_moves or move_number_to_edit < 1:
                    print("Invalid number for selecting move to edit")
                    continue
                index = move_number_to_edit - 1
                print("Editing move " + metadata[1][index])
                print()
                print_moves_and_ids(MOVE_SPREADSHEET_LOWER_BOUND, MOVE_SPREADSHEET_UPPER_BOUND)
                new_move_id = input(f"Enter the number of the move you want to change {metadata[1][index]} to: ")
                if new_move_id.isnumeric():
                    int_new_move_id = int(new_move_id)
                    if not int_new_move_id < MOVE_SPREADSHEET_LOWER_BOUND and not int_new_move_id > MOVE_SPREADSHEET_UPPER_BOUND:
                        # Validate that move is not already in moveset
                        if new_move_id in data_entry[MOVES_COLUMN].split(','):
                            print("Move already in moveset")
                            continue
                        print("Valid move id: " + new_move_id)
                        # TODO: Add move to moveset
                        moves = data_entry[MOVES_COLUMN].split(',')
                        moves[index] = str(new_move_id)
                        data_entry[MOVES_COLUMN] = ','.join(moves)
                    else:
                        print("Invalid move id, id out of bounds")
                        continue
                else:
                    print("Invalid move id, id is not a number")
                    continue
            elif uinp == 'z':
                print("Updating data")
                with open(SPREADSHEET_NAME, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(data)
                break
            elif uinp == 'q':
                print("Quitting data edit without saving")
            else:
                print("Invalid input")
    else:
        print("No entry found: invalid input")

    return None

def format_data_entry(data_entry):
    print("Name: " + data_entry[NAME_COLUMN])
    print("Ability: " + data_entry[ABILITY_COLUMN])
    print("Moveset: ", end='')
    number_of_moves = 0
    moveset_string = ""
    moveset_names = []
    for move_number in data_entry[MOVES_COLUMN].split(','):
        if move_number:
            move = Move(int(move_number))
            moveset_names.append(move.name)
            print(move.name, end=', ')
            number_of_moves += 1
    print()
    return [number_of_moves, moveset_names]

def ui():
    print("Moveset Editor")
    uinp = ''
    while uinp != 'q':
        print_names_and_ids(DATA_LOWER_BOUND, DATA_UPPER_BOUND)
        uinp = input("Enter the number or name of the Pokemon you want to see the moveset of. Type 'all' if you would like a printout of every pokemon and moveset, or enter 'q' to quit: ")
        if uinp == 'all':
            print_movesets(DATA_LOWER_BOUND, DATA_LOWER_BOUND)
        else:
            monster_row = open_and_edit_row_of_entry(uinp)
            if not monster_row:
                continue

ui()