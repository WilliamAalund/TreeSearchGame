from random import *

def get_current_game_state(): # Non game agnostic function, encapsulates the game state and returns it. To be used in the monte carlo tree search class
    current_state = GameState()
    return current_state

# --- MONTE CARLO TREE SEARCH CLASS ---
class MonteCarloTreeSearch:
    def __init__(self, game_state):
        self.root = Node(game_state)
    
    def get_best_move(self):
        ai_intelligence = 1000
        i = 0
        while i < ai_intelligence:
            leaf = self.traverse(self.root) # Selection. leaf equals a node that does not have children, and conforms to the rollout policy. (Rollout policy detailed in node class)
            result = self.rollout(leaf) # Expansion/Simulation. Picks random unexpanded child of leaf, and simulates a game from there. Returns result of game.
            self.backpropagate(leaf, result) # Backpropagation. Updates the stats of the nodes from the leaf to the root.
            i += 1
        return self.root.best_child()
    
    def traverse(self, node):
        while node.is_expanded():
            node = node.best_child()

        # if no children, or if node is terminal
        return node.rollout_policy() or node

    def rollout(node):
        while not node.is_terminal():
            node = node.rollout_policy()
        return node.result()

    def backpropagate(self, node, result):
        if node.is_root():
            return
        node.update_stats(result)
        self.backpropagate(node.get_parent(), result)

# --- NODE CLASS ---
class Node: # Class designed in a game state agnostic way
    def __init__(self, game_state, parent = None):
        self.children = []
        self.state = game_state
        self.ucb = 0
        self.visits = 0
        self.node_expanded = False
        self.parent = parent

    def is_expanded(self):
        return self.node_expanded
    
    def is_root(self):
        return self.parent == None
    
    def get_parent(self):
        if self.is_root():
            return None
        else:
            return self.parent

    def expand(self):
        for i in range(self.state.get_possible_actions()):
            self.children.append(Node(self.state.make_move(i)))
        self.node_expanded = True
    
    def result(self):
        return self.state.is_terminal()
    
    def rollout_policy(self):
        if not self.node_expanded:
            self.expand()
        return random.choice(self.children)

    def best_child(self):
        return max(self.children, key=lambda child: child.ucb)
    
    def update_stats(self, result):
        self.visits += 1
        self.ucb = result
    

# --- GAME STATE CLASS ---
class GameState: # Game state class will contain the non-agnostic specifics, higher level classes will not need to know this information
    def __init__(self):
        self.value = 0
        self.game_over = False
        self.winner = None

    def is_terminal(self):
        return self.game_over

    def get_possible_actions(self): # Returns integer representing of possible actions
        return 2
    
    def make_move(self, move):
        self.check_game_over()
        return 1

my_tree_search = MonteCarloTreeSearch(get_current_game_state())
my_tree_search.get_best_move()