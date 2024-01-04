from math import *
from random import *

# --- GLOBAL VARIABLES ---
exploration_parameter = 1 # Exploration parameter for UCB formula. Higher value means more exploration. 
ai_intelligence = 500 # Number of iterations of the monte carlo tree search. Higher value means more accurate results, but more time taken.
game_number = 1


# --- MONTE CARLO TREE SEARCH CLASS ---
class MonteCarloTreeSearch:
    def __init__(self, game_state):
        self.root = Node(game_state)
    
    def get_best_move(self):
        i = 0
        while i < ai_intelligence:
            leaf = self.traverse_tree(self.root) # Selection. leaf equals a node that does not have children, and conforms to the rollout policy. (Rollout policy detailed in node class)
            result = self.rollout(leaf) # Expansion/Simulation. Picks random unexpanded child of leaf, and simulates a game from there. Returns result of game.
            self.backpropagate_tree(leaf, result) # Backpropagation. Updates the stats of the nodes from the leaf to the root.
            i += 1
        #self.root.print_children()
        #print("Best move is: " + str(self.root.best_child().state.last_move) + " with a ucb value of: " + str(self.root.best_child().ucb))
        return self.root.best_child()
    
    def traverse_tree(self, node): # Modified traversal function. Evenly spreads traversals between nodes with high ucb values and nodes with low visits. Game agnostic.
        while node.node_is_expanded():
            node = node.best_child()
        # if no children, or if node is terminal
        return node.rollout_policy() or node

    def rollout(self, node):
        while not node.node_is_terminal():
            node = node.rollout_policy()
        if node.is_game_won():
            return 1
        else:
            return 0

    def backpropagate_tree(self, node, result):
        node.update_stats(result)
        node.node_children_calculate_ucbs()
        if not node.node_is_root() == True:
            self.backpropagate_tree(node.node_get_parent(), result)

#
#
#
#
# --- NODE CLASS ---
class Node: # Class designed in a game state agnostic way
    def __init__(self, game_state, parent = None):
        self.children = []
        self.state = game_state
        self.ucb = float('inf') # If a node hasn't been explored yet, we want to explore it first. This value is set to 999 so that it will be explored first.
        self.wins = 0
        self.visits = 0
        self.node_expanded = False
        self.parent = parent

    def node_is_expanded(self):
        return self.node_expanded
    
    def node_is_root(self): # Root if parent is None
        return self.parent is None
    
    def node_is_terminal(self):
        return self.state.is_game_over()

    def is_game_won(self):
        return self.state.did_ai_win()
    
    def node_get_parent(self):
        if self.node_is_root():
            return None
        else:
            return self.parent
        
    def get_policy_rating(self):
        return self.state.calculate_policy_rating()

    def expand(self): # Expands the node by creating children. Children represent all possible moves from the current state. Partially game agnostic, generates choices depending on the possible actions you could take in game state.
        for i in range(self.state.get_possible_actions()):
            self.children.append(Node(self.state.make_move(i), self))
        self.node_expanded = True
    
    def result(self): # Returns if the AI won or lost on a terminal node. Game agnostic. Called in MonteCarloTreeSearch class
        return self.state.did_ai_win()
    
    def rollout_policy(self, random_policy = True):
        if not self.node_expanded:
            self.expand() # Flips node_expanded to True
        if random_policy:
            return choice(self.children) if self.children else None
        else: # Not working properly
            return min(self.children, key=lambda child: (child.get_policy_rating(), child.visits))

    def best_child(self):
        return max(self.children, key=lambda child: child.ucb)
    
    def node_get_parent_visits(self):
        return self.parent.visits

    def node_children_calculate_ucbs(self):
        for child in self.children:
            child.node_calculate_ucb()

    def node_calculate_ucb(self):
        if self.visits > 0:
            self.ucb = self.wins / self.visits
            if self.parent:
                self.ucb += exploration_parameter * sqrt(log(self.node_get_parent_visits()) / self.visits)
        else:
            self.ucb = float('inf')

    def update_stats(self, result): # Calculated ucb value for node. Will not be called on root node. Game agnostic.
        self.wins += result
        self.visits += 1
        parent_visits = 0
        if self.parent:
            parent_visits = self.node_get_parent_visits()
        #print(str(self.wins) + " " + str(self.visits) + " " + str(parent_visits))
        self.ucb = self.wins / self.visits
        if parent_visits > 0:
            self.ucb += exploration_parameter * sqrt(log(parent_visits) / self.visits)
    
    def print_children(self):
        for child in self.children:
            print("Child: " + str(child.state.state_value) + " with ucb value of: " + str(child.ucb) + " and visits of: " + str(child.visits))

#
#
#
#
# --- GAME STATE CLASS ---
# TODO: Integrate get_current_game_state() into this class
class GameState: # Game state class will contain the non-agnostic specifics, higher level classes will not need to know this information
    def __init__(self, state = None, last_move = None):
        self.state_value = state
        self.game_over = False
        self.winner = False
        self.last_move = last_move
        self.policy_rating = None

    def is_game_over(self):
        return self.game_over

    def did_ai_win(self):
        return self.winner

    def check_game_over(self): # Alters the game_over variable depending on state requirements. Called in make_move(). Not game agnostic.
        if self.state_value <= 0:
            if self.state_value == 0:
                self.winner = True
            else:
                self.winner = False
            self.game_over = True

    def get_possible_actions(self): # Returns integer representing of possible actions. Not game agnostic.
        return 4

    def calculate_policy_rating(self): # Returns a float representing how good the current state is for the AI. Not game agnostic.
        if self.last_move != None:
            if self.last_move == 0:
                self.policy_rating = 0
            elif self.last_move == 1:
                self.policy_rating = 1
            return self.policy_rating
        return -1 # If no move has been made, return -1

    def make_move(self, move): # Returns a new game state with the move made. Not game agnostic.
        #print("Making move: " + str(move))
        new_state = GameState(self.state_value, move)
        if new_state.state_value != None:
            if move == 0:
                new_state.state_value -= 1
            elif move == 1:
                new_state.state_value -= 2
            elif move == 2:
                new_state.state_value -= 3
            elif move == 3:
                new_state.state_value -= 4
            new_state.calculate_policy_rating()
            new_state.check_game_over()
            return new_state

def get_current_game_state(): # Non game agnostic function, encapsulates the game state and returns it. To be used in the monte carlo tree search class
    state_object = GameState(game_number)
    return state_object

my_tree_search = MonteCarloTreeSearch(get_current_game_state())
best_move = my_tree_search.get_best_move()
print(best_move)