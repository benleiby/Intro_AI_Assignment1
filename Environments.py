import random as rand
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import os
import pickle

class GridEnvironment:

    def __init__(self, size):
        self.size = size
        self.grid = np.ones((size, size))
        self.start = (0,0)
        self.goal = (size - 1, size - 1)
        self.create_maze()

    # Used for maze generation.
    # Neighbors are separated from current by 1 wall node.
    def get_neighbors(self, node):
        neighbors = []
        for dr, dc in [(0,2), (0,-2), (2,0), (-2,0)]:
            nr, nc = node[0] + dr, node[1] + dc
            if -1 < nr < self.size and -1 < nc < self.size:
                neighbors.append((nr, nc))
        return neighbors

    # Used for calculating shortest paths in a*.
    # Actions are defined by the next nodes an agent can move to (in 4 directions).
    def get_actions(self, node, consider_obstacles):
        actions = []
        r, c = node
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if -1 < nr < self.size and -1 < nc < self.size:
                if consider_obstacles and self.grid[nr, nc] != 1:
                    actions.append((nr, nc))
                elif not consider_obstacles:
                    actions.append((nr, nc))
        return actions

    def create_random_environment(self):
        for i in range(self.size):
            for j in range(self.size):
                node = (i,j)
                if node != self.start and node != self.goal:
                    if rand.random() < 0.8:
                        self.grid[node] = 0


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

    def get_next_frame(self, walk, calculated_path):
        visualization_grid = np.copy(self.grid)
        visualization_grid[self.start] = 2
        visualization_grid[self.goal] = 2
        if walk:
            for node in walk:
                if node != self.start and node != self.goal:
                    visualization_grid[node] = 4
        if calculated_path:
            for node in calculated_path:
                if node != self.start and node != self.goal:
                    visualization_grid[node] = 3
        return visualization_grid

    def get_heuristic(self):
        h = {}
        for i in range(len(self.grid)):
            for j in range(len(self.grid)):
                h[(i,j)] = abs(i - self.goal[0]) + abs(j - self.goal[1])
        return h

def create_mazes(count, output_directory):

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for i in range(count):
        env = GridEnvironment(101)
        filepath = os.path.join(output_directory, "maze" + str(i) + ".pkl")

        try:
            with open(filepath, "wb") as file:
                pickle.dump(env, file, pickle.HIGHEST_PROTOCOL)
            del env
        except Exception as e:
            print("Error loading objects: " + e)

def load_mazes(directory):

    loaded_mazes = {}

    if not os.path.exists(directory):
        print("Invalid directory")
        return loaded_mazes

    for filename in os.listdir(directory):
        if filename.endswith(".pkl"):
            name = filename[:-4]
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'rb') as file:
                    loaded_mazes[name] = pickle.load(file)
            except Exception as e:
                print(f"Error loading object '{name}': {e}")
    print("Success loading " + str(len(loaded_mazes)) + " objects.")
    return loaded_mazes