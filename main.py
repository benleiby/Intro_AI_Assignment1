import random as rand
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

class GridEnvironment:

    def __init__(self, size):
        self.size = size
        self.grid = np.ones((size, size))
        self.start = (0,0)
        self.goal = (size - 1, size - 1)
        self.create_maze()

    def get_neighbors(self, node):
        neighbors = []
        for dr, dc in [(0,2), (0,-2), (2,0), (-2,0)]:
            nr, nc = node[0] + dr, node[1] + dc
            if -1 < nr < self.size and -1 < nc < self.size:
                neighbors.append((nr, nc))
        return neighbors

    def create_obstacles_badly(self):
        for i in range(self.size):
            for j in range(self.size):
                if rand.random() > 0.7:
                    self.grid[i,j] = 1

    def create_maze(self):
        start = (rand.randint(0, (self.size - 1) // 2) * 2, rand.randint(0, (self.size - 1) // 2) * 2)
        stack = [start]
        self.grid[start] = 0

        while stack:
            current = stack.pop()
            neighbors = self.get_neighbors(current)
            unvisited_neighbors = [n for n in neighbors if self.grid[n] == 1]

            if unvisited_neighbors:

                stack.append(current)
                next_cell = rand.choice(unvisited_neighbors)

                # Remove wall
                wall_row = (current[0] + next_cell[0]) // 2
                wall_col = (current[1] + next_cell[1]) // 2
                self.grid[wall_row, wall_col] = 0

                # Mark cell as visited
                self.grid[next_cell] = 0
                stack.append(next_cell)

    def visualize_maze(self):
        cmap = mcolors.ListedColormap(['white', 'black', 'blue', 'green'])
        bounds = [0, 1, 2, 3, 4]
        norm = mcolors.BoundaryNorm(bounds, cmap.N)

        visualization_grid = np.copy(self.grid)
        visualization_grid[self.start] = 2
        visualization_grid[self.goal] = 3

        plt.figure(figsize=(6, 6))
        plt.imshow(visualization_grid, cmap=cmap, norm=norm)
        plt.xticks([]), plt.yticks([])
        plt.show()

env = GridEnvironment(101)
env.visualize_maze()