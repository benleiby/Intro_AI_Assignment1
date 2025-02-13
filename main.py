"""
One potential way to build the environment is the following. You can initially set all the cells as unvisited. Then you
can start from a random cell, mark it as visited and unblocked. Select a random neighbouring cell to visit that has not yet
been visited. With 30% probability mark it as blocked. With 70% mark it as unblocked and in this case add it to the stack.
A cell that has no unvisited neighbours is a dead-end. When at a dead-end, your algorithm must backtrack to parent nodes
on the search tree until it reaches a cell with an unvisited neighbour, continuing the path generation by visiting this new,
unvisited cell. If at some point your stack is empty, and you have not yet visited all the nodes, you repeat the above process
from a node that has not been visited. This process continues until every cell has been visited.
"""

import random as rand
import numpy as np
import matplotlib.pyplot as plt

class GridEnvironment:

    def __init__(self, size):
        self.size = size
        self.grid = np.zeros((size, size))
        self.start = None
        self.goal = None
        self.create_obstacles()

    def get_neighbors(self, node):
        neighbors = []
        for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:
            nr, nc = node[0] + dr, node[1] + dc
            if -1 < nr < self.size and -1 < nc < self.size:
                neighbors.append((nr, nc))
        return neighbors

    def create_obstacles(self):

        vis = np.full((self.size, self.size), False) # Initialize all nodes as unvisited

        while not vis.all():

            start = None
            while not start or vis[start]:
                start = (rand.randint(0, self.size - 1), rand.randint(0, self.size - 1))  # Choose a random unvisited starting node

            stack = [start]

            while stack:

                current = stack.pop()
                vis[current] = True

                # Case: Dead end (All neighbors are visited)
                neighbors = self.get_neighbors(current)
                if all(vis[neighbor] for neighbor in neighbors):
                    continue

                # Consider a random unvisited neighbor
                next_node = None
                while not next_node or vis[next_node]:
                    next_node = rand.choice(neighbors)

                # Decide whether to block the node
                if rand.random() <= 0.7:
                    stack.append(next_node)
                else:
                    self.grid[next_node] = 1
                    vis[next_node] = True

env = GridEnvironment(101)
print(env.grid)

plt.imshow(env.grid, cmap='gray_r', origin='lower')  # Use 'gray' colormap for 0 and 1
plt.title("Generated Grid")
plt.xticks([])  # Remove x-axis ticks
plt.yticks([])  # Remove y-axis ticks
plt.show()