import networkx as nx
import matplotlib.pyplot as plt

class DeliveryRoutePlanner:
    def _init_(self, graph):
        self.graph = graph
        self.num_locations = len(graph)
        self.path = [-1] * self.num_locations
        self.path[0] = 0  # Start at the first location (index 0)

    def is_safe(self, v, pos):
        # Check if there is an edge from the last location in the path to this location
        if self.graph[self.path[pos - 1]][v] == 0:
            return False
        # Check if the location has already been included in the path
        if v in self.path:
            return False
        return True

    def find_route(self, pos):
        # If all locations are in the path, check for a return path to the starting location
        if pos == self.num_locations:
            return self.graph[self.path[pos - 1]][self.path[0]] == 1
        for v in range(1, self.num_locations):
            if self.is_safe(v, pos):
                self.path[pos] = v
                if self.find_route(pos + 1):
                    return True
                # Backtrack
                self.path[pos] = -1
        return False

    def get_optimal_route(self):
        if self.find_route(1):
            return self.path + [self.path[0]]  # Add the start location at the end to complete the cycle
        else:
            return None

def visualize_graph(graph, route=None):
    G = nx.Graph()
    num_nodes = len(graph)
    
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if graph[i][j] == 1:
                G.add_edge(i, j)
    
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=1000, font_size=15)
    
    if route:
        cycle_edges = [(route[i], route[i + 1]) for i in range(len(route) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=cycle_edges, edge_color='red', width=2)
        plt.title("Graph with Hamiltonian Cycle Highlighted", fontsize=15)
    else:
        plt.title("Graph", fontsize=15)
    
    plt.show()

graph = [
    [0, 1, 1, 0, 1],
    [1, 0, 1, 1, 0],
    [1, 1, 0, 1, 1],
    [0, 1, 1, 0, 1],
    [1, 0, 1, 1, 0]
]

planner = DeliveryRoutePlanner(graph)

route = planner.get_optimal_route()

if route:
    print("Optimal delivery route:", route)
else:
    print("No Hamiltonian Cycle found.")

visualize_graph(graph, route)
  graph output program