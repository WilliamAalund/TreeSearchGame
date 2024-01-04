from random import *

class TurnNode:
    def __init__(self):
        self.children = []
        self.data = GameState()
        self.visits = 0
        self.q = 0
    
    def __init__(self, data):
        self.children = []
        self.data = data

    def setData(self, data):
        self.data = data
    
    def getData(self):
        return self.data
    
    def add_child(self, child: 'TurnNode'):
        self.children.append(child)
    
    def expand(self):
            if not self.children:  # if children list is empty
                for row in range(3):
                    for col in range(3):
                        if self.state.board[row][col] == ' ':
                            new_state = GameState(self.state)
                            new_state.make_move(row, col)
                            self.children.append(TurnNode(new_state, self))
            return random.choice(self.children)

    def print_tree(self, indent=""): # Recursive function
        print(indent + self.data)
        for child in self.children:
            child.print_tree(indent + "  ")

class GameState:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False

    def __init__(self, state: 'GameState'):
        self.board = [list(state.board[row]) for row in range(3)]
        self.current_player = state.current_player
        self.game_over = state.game_over

    def make_move(self, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            self.check_game_over()

    def check_game_over(self):
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] != ' ':
                self.game_over = True
                return

        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != ' ':
                self.game_over = True
                return

        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            self.game_over = True
            return
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            self.game_over = True
            return

        # Check for a tie
        if all(self.board[row][col] != ' ' for row in range(3) for col in range(3)):
            self.game_over = True

    def is_terminal(self):
        return self.game_over
    
    def print_board(self):
        for row in self.board:
            print(' | '.join(row))
            print('-' * 9)

