import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from math import sqrt
import heapq

class Node:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.parent = None
        self.g = float('inf')
        self.h = 0
        self.f = float('inf')

    def __lt__(self, other):
        return self.f < other.f

    def distance_to(self, other):
        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2)

def a_star(start, goal, neighbors_func):
    open_set = []
    heapq.heappush(open_set, start)
    start.g = 0
    start.f = start.h = start.distance_to(goal)
    closed_set = set()

    while open_set:
        current = heapq.heappop(open_set)
        if current == goal:
            return reconstruct_path(goal), closed_set

        closed_set.add(current)

        for neighbor in neighbors_func(current):
            if neighbor in closed_set:
                continue

            tentative_g_score = current.g + current.distance_to(neighbor)

            if neighbor not in open_set:
                heapq.heappush(open_set, neighbor)
            elif tentative_g_score >= neighbor.g:
                continue

            neighbor.parent = current
            neighbor.g = tentative_g_score
            neighbor.h = neighbor.distance_to(goal)
            neighbor.f = neighbor.g + neighbor.h

def reconstruct_path(node):
    path = []
    while node:
        path.append((node.x, node.y, node.z))
        node = node.parent
    return path[::-1]

def get_neighbors(node):
    directions = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    neighbors = []
    for dx, dy, dz in directions:
        nx, ny, nz = node.x + dx, node.y + dy, node.z + dz
        if 0 <= nx < 10 and 0 <= ny < 10 and 0 <= nz < 10:  # Assuming grid limits
            neighbors.append(Node(nx, ny, nz))
    return neighbors

def visualize_path(path, closed_set):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plotting all evaluated nodes
    for node in closed_set:
        ax.scatter(node.x, node.y, node.z, color='yellow', s=10)

    # Plotting the path
    if path:
        px, py, pz = zip(*path)
        ax.plot(px, py, pz, color='blue', marker='o')

    # Plotting start and goal
    ax.scatter(path[0][0], path[0][1], path[0][2], color='green', s=100, label='Start')
    ax.scatter(path[-1][0], path[-1][1], path[-1][2], color='red', s=100, label='Goal')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()

    plt.savefig('Pathfinding3D.png')
    plt.show()

# Example usage
start_node = Node(0, 0, 0)
goal_node = Node(9, 9, 9)
path, evaluated_nodes = a_star(start_node, goal_node, get_neighbors)
visualize_path(path, evaluated_nodes)
