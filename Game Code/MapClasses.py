import random as rng

class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.graph = Graph(width, height)
        self.current_position = self.graph.current_position

    def get_nodes_to_travel_to(self):
        return self.current_position.neighbors
    
    def move_to(self, i, j):
        # Check if the node is adjacent to the current position
        if self.graph.nodes[i][j] in self.current_position.neighbors:
            self.current_position = self.graph.nodes[i][j]
        else:
            print('Cannot move to a node that is not connected to the current position.')
    
    def print_map(self): # FIXME: Make this print the map in a more readable way
        for i, row in enumerate(self.graph.nodes):
            for j, node in enumerate(row):
                if node == self.current_position:
                    print('X', end=' ')
                else:
                    print('O', end=' ')
            print()

# ------------- GRAPH CLASSES -------------

def weighted_random_choice(choices, weights):
    total_weight = sum(weights)
    random_num = rng.random() * total_weight
    for choice, weight in zip(choices, weights):
        if random_num < weight:
            return choice
        random_num -= weight
    return choice

class Location:
    def __init__(self, location_type):
        self.location_type = location_type
        self.pokemon_roster = []
        self.item_roster = []
        self.trainer_roster = []
    
    def __str__(self):
        return self.location_type

class GraphNode:
    def __init__(self, location_type, distance_from_center) -> None:
        self.location_type = Location(location_type)
        self.neighbors = []
        self.visited = False
        self.distance_from_center = distance_from_center
    
class Graph:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        center_x, center_y = width // 2, height // 2
        self.nodes = [[self.create_node(i, j, center_x, center_y) for j in range(min(i+1 if i < width else 2*width-i-1, width))] for i in range(2*height-1)]
        self.nodes[-1][-1].location_type = 'gym'  # Make the final node a gym
        self.connect_nodes()
        self.current_position = self.nodes[0][0]

    def create_node(self, i, j, center_x, center_y):
        distance_from_center = ((center_x - i)**2 + (center_y - j)**2)**0.5
        location_type = self.select_location_type(distance_from_center)
        return GraphNode(location_type, distance_from_center)

    def select_location_type(self, distance_from_center):
        choices = ['town', 'road', 'city', 'grassland', 'cave', 'lake']
        if distance_from_center <= 1:
            weights = [0.3, 0.35, 0.2, 0.1, 0, 0.05]
        elif distance_from_center <= 2:
            weights = [0.1, 0.1, 0.1, 0.4, 0.1, 0.2]
        else:
            weights = [0.05, 0.1, 0, 0.4, 0.3, 0.15]
        return weighted_random_choice(choices, weights)

    def connect_nodes(self):
        for i in range(len(self.nodes) - 1):  # No need to connect the last row
            for j in range(len(self.nodes[i])):
                # Connect to the node directly in front, if it exists
                if j < len(self.nodes[i+1]):
                    self.nodes[i][j].neighbors.append(self.nodes[i+1][j])
                # Connect to the node to the right in the next row, if it exists
                if j + 1 < len(self.nodes[i+1]):
                    self.nodes[i][j].neighbors.append(self.nodes[i+1][j+1])
                # Connect to the node to the left in the next row, if it exists
                if j - 1 >= 0:
                    self.nodes[i][j].neighbors.append(self.nodes[i+1][j-1])

    def list_adjacent_nodes(self):
        for neighbor in self.current_position.neighbors:
            ni = next(i for i, row in enumerate(self.nodes) if neighbor in row)
            nj = self.nodes[ni].index(neighbor)
            print(f'Adjacent node: {ni},{nj} ({neighbor.location_type}, distance from center: {neighbor.distance_from_center})')

    def move_to(self, i, j):
        if self.nodes[i][j] in self.current_position.neighbors:
            self.current_position = self.nodes[i][j]
        else:
            print('Cannot move to a node that is not connected to the current position.')

    def print_graph(self):
        for i, row in enumerate(self.nodes):
            for j, node in enumerate(row):
                print(f'Node {i},{j} ({node.location_type}, distance from center: {node.distance_from_center}):', end=' ')
                for neighbor in node.neighbors:
                    ni = next(i for i, row in enumerate(self.nodes) if neighbor in row)
                    nj = self.nodes[ni].index(neighbor)
                    print(f'{ni},{nj}', end=' ')
                print() 

if __name__ == '__main__':
    test_map = Map(10, 10)
    test_map.print_map()
