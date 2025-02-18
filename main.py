import random as rand
import numpy as np
import matplotlib.pyplot as plt

class GridEnvironment:

    def __init__(self, size):
        self.size = size
        self.grid = np.ones((size, size))
        self.start = None
        self.goal = None
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
        """Generate a maze using iterative DFS."""
        # Choose a random starting cell (ensure it's on an even index)
        start = (rand.randint(0, (self.size - 1) // 2) * 2, rand.randint(0, (self.size - 1) // 2) * 2)
        self.start = start
        stack = [start]
        self.grid[start] = 0  # Mark the starting cell as a passage

        while stack:
            current = stack.pop()
            neighbors = self.get_neighbors(current)
            unvisited_neighbors = [n for n in neighbors if self.grid[n] == 1]

            if unvisited_neighbors:
                # Push the current cell back to the stack
                stack.append(current)

                # Choose a random unvisited neighbor
                next_cell = rand.choice(unvisited_neighbors)

                # Remove the wall between the current cell and the chosen neighbor
                wall_row = (current[0] + next_cell[0]) // 2
                wall_col = (current[1] + next_cell[1]) // 2
                self.grid[wall_row, wall_col] = 0  # Carve a passage

                # Mark the chosen cell as visited and push it to the stack
                self.grid[next_cell] = 0
                stack.append(next_cell)

env = GridEnvironment(101)
print(env.grid)

plt.imshow(env.grid, cmap='gray_r', origin='upper')  # Use 'gray' colormap for 0 and 1
plt.title("Generated Grid")
plt.xticks([])  # Remove x-axis ticks
plt.yticks([])  # Remove y-axis ticks
plt.show()