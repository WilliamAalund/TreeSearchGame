from math import *
import random as rng
from MatchClasses import GameState # Dependency for Node class

# --- GLOBAL VARIABLES ---
exploration_parameter = 1.5 # Exploration parameter for UCB formula. Higher value means more exploration. 
ai_intelligence = 16000 # Number of iterations of the monte carlo tree search. Higher value means more accurate results, but more time taken.
search_depth = 15 # Depth of the search tree. Higher value means more accurate results, but more time taken.

# --- MONTE CARLO TREE SEARCH CLASS ---
class MonteCarloTreeSearch:
    def __init__(self, game_state, verbose = False, random_policy = True):
        self.root = Node(game_state, verbose=verbose)
        self.verbose = verbose
        self.random_policy = random_policy
    
    def get_best_move(self):
        i = 0
        while i < ai_intelligence:
            if i % 600 == 0:
                print(".", end="")
            leaf = self.traverse_tree(self.root) # Selection. leaf equals a node that does not have children, and conforms to the rollout policy. (Rollout policy detailed in node class)
            result = self.rollout(leaf) # Expansion/Simulation. Picks random unexpanded child of leaf, and simulates a game from there. Choice of nodes is based on the rollout policy.
            self.backpropagate_tree(leaf, result) # Backpropagation. Updates the stats of the nodes from the leaf to the root.
            i += 1
        if self.verbose:
            pass
        print()
        return self.root.best_child_last_move()
    
    def traverse_tree(self, node): # Modified traversal function. Evenly spreads traversals between nodes with high ucb values and nodes with low visits. Game agnostic.
        while node.node_is_expanded():
            node = node.best_child()
        # if no children, or if node is terminal
        if not node.node_is_terminal():
            return node.rollout_policy(random_policy=self.random_policy)
        return node

    def rollout(self, node):
        while not node.node_is_terminal():
            node = node.rollout_policy(random_policy=self.random_policy)
        if node.is_game_won(): # Not game agnostic, score returned is based on number of turns taken to win
            return 1 + node.state.get_victory_reward()
        else:
            return 0 + node.state.get_loss_penalty()

    def backpropagate_tree(self, node, result):
        node.update_stats(result)
        node.node_children_calculate_ucbs()
        if not node.node_is_root() == True:
            self.backpropagate_tree(node.node_get_parent(), result)

#
# --- NODE CLASS ---
class Node: # Class designed in a game state agnostic way
    def __init__(self, game_state, parent = None, verbose = False):
        self.children = []
        self.state = game_state
        self.ucb = float('inf') # If a node hasn't been explored yet, we want to explore it first. This value is set to 999 so that it will be explored first.
        self.wins = 0
        self.visits = 0
        self.node_expanded = False
        self.parent = parent
        self.is_terminal = self.set_node_terminality() # WHEN REFERRING TO THIS VARIABLE, USE THE METHOD, NOT THE VARIABLE ITSELF. This is because the variable is set when the node is initialized, and will not change if the state changes.
        self.verbose = verbose
        #self.is_terminal = self.state.is_game_over()
        #self.is_terminal = self.state.did_ai_get_an_elimination() or self.state.did_player_get_an_elimination() # FIXME: Will encourage AI to use a move like explosion if it is the only way to win. Should be changed to is_game_over() when that is implemented.
        # TODO: Integrate both forms of MTCS into node: one that simulates the whole game, and one that simulates until an elimination is achieved.

    def __str__(self):
        return str(self.state)

    def node_is_expanded(self):
        return self.node_expanded
    
    def node_is_root(self): # Root if parent is None
        return self.parent is None
    
    def set_node_terminality(self): # Method to be called when initializing node. Will set the self.is_terminal property
        return self.state.state_is_terminal() or self.state.turn_count > search_depth

    def node_is_terminal(self):
        #if self.verbose:
        #    print("node_is_terminal called")
        #    print("Is terminal: " + str(self.is_terminal) + ", turn count: " + str(self.state.turn_count) + ", search depth: " + str(search_depth))
        return self.is_terminal

    def is_game_won(self): # TODO: Integrate both forms of MTCS into node: one that simulates the whole game, and one that simulates until an elimination is achieved.
        return self.state.state_is_victory()
    
    def node_get_parent(self):
        if self.node_is_root():
            return None
        else:
            return self.parent
        
    def get_policy_rating(self):
        return self.state.calculate_policy_rating()

    def expand(self): # Expands the node by creating children. Children represent all possible moves from the current state. Partially game agnostic, generates choices depending on the possible actions you could take in game state.
        if self.node_is_terminal():
            print("I am a terminal node that is being expanded")
        for state in self.state.get_ai_possible_actions():
            self.children.append(Node(state,self, verbose=self.verbose))
        self.node_expanded = True
    
    def rollout_policy(self, random_policy = True):
        if not self.node_expanded and not self.node_is_terminal():
            self.expand() # Flips node_expanded to True
            if self.verbose:
                self.print_children()
            if len(self.children) == 0:
                if self.verbose:
                    print("WARNING: No children, but node is not terminal, and rollout policy is being called.")
                    print("self.is_terminal: ", self.node_is_terminal())
                    print("Conditional: not self.node_expanded and not self.node_is_terminal(): ", not self.node_expanded and not self.node_is_terminal())
                    print(self)
        else:
            return
        if random_policy:
            return rng.choice(self.children) if self.children else None
        else: 
            #print(self.is_terminal, self.state.did_ai_get_an_elimination(), self.state.turn_count, search_depth)
            return max(self.children, key=lambda child: (child.get_policy_rating(), child.ucb))

    def best_child(self):
        return max(self.children, key=lambda child: child.ucb)
    
    def best_child_last_move(self):
        child_names = {}  # Dictionary to store unique child names and their corresponding ucb values
        for child in self.children:
            if child.state.last_move not in child_names:
                child_names[child.state.last_move] = child.ucb
            else:
                child_names[child.state.last_move] += child.ucb
        return max(child_names, key=child_names.get)

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
        self.ucb = self.wins / self.visits
        if parent_visits > 0:
            self.ucb += exploration_parameter * sqrt(log(parent_visits) / self.visits)
    
    def print_children(self):
        child_num = 0
        for child in self.children:
            print("Child: " + str(child_num) + "\n" + str(self.state) + " with ucb value of: " + str(child.ucb) + " and visits of: " + str(child.visits))
            child_num += 1