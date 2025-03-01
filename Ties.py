# Part 2 - The Effects of Ties [15 points]: Repeated Forward A* needs to break ties to decide which cell to expand next if
# several cells have the same smallest f-value. It can either break ties in favor of cells with smaller g-values or in favor of
# cells with larger g-values. Implement and compare both versions of Repeated Forward A* with respect to their runtime or,
# equivalently, number of expanded cells. Explain your observations in detail, that is, explain what you observed and give a
# reason for the observation.
# [Hint: For the implementation part, priorities can be integers rather than pairs of integers. For example, you can use
# c × f (s) − g(s) as priorities to break ties in favor of cells with larger g-values, where c is a constant larger than the largest
# g-value of any generated cell. For the explanation part, consider which cells both versions of Repeated Forward A* expand
# for the example search problem from Figure 9.]

import heapq
from Environments import GridEnvironment
import numpy as np

class PriorityQueue:
    def __init__(self, items=None):
        self._heap = items if items is not None else []
        heapq.heapify(self._heap)

    def push(self, item):
        heapq.heappush(self._heap, item)

    def pop(self):
        return heapq.heappop(self._heap)

    def peek(self):
      return self._heap[0]

    def __len__(self):
        return len(self._heap)

    def remove(self, neighbor):  # Changed 'item' to 'neighbor' for clarity
        """Removes the first tuple with the given neighbor from the queue."""
        for i, (_, n) in enumerate(self._heap):
            if n == neighbor:
                del self._heap[i]
                heapq.heapify(self._heap)
                return  # Exit after removing the first occurrence
        # If the loop completes, the neighbor was not found

    def contains(self, val):
        return any(n == val for _, n in self._heap)

    def empty(self):
        return len(self._heap) == 0

    def to_string(self):
        output = ""
        for item in self._heap:
            output += str(item)
        return output

def reconstruct_path(tree, goal):
    path = [goal]  # Start with the goal node
    current = goal
    while current in tree:
        current = tree[current]  # Get the parent node
        path.append(current)  # Add the parent to the path
    return path[::-1]  # Reverse the path to get it from start to goal

def main_procedure(maze, h):
    counter = 0  # Maintain count of paths computed
    start = maze.start
    goal = maze.goal
    g =  {} # Cost

    search = {} # Each state stores a search flag that indicates which search iteration last visited it
    for i in range(len(maze.grid)):
        for j in range(len(maze.grid)):
            state = (i,j)
            search[state] = 0
            g[state] = float('inf')

    while start != goal:

        tree = {}
        counter = counter + 1
        g[start] = 0
        search[start] = counter
        g[goal] = float('inf')
        search[goal] = counter
        open_set = PriorityQueue()
        closed_set = set()

        open_set.push(((g[start] + h[start]), start))

        compute_path(maze, open_set, closed_set, search, counter, g, h, goal, tree)

        path = reconstruct_path(tree, goal)
        for i in range(len(path)):

            if maze.grid[path[i]] == 1:
                break

            start = path[i]

def compute_path(maze, open_set, closed_set, search, counter, g, h, goal, tree):

    while not open_set.is_empty():
        current_f, current_state = open_set.pop()
        if current_state == goal:
            break

        current_f, current_state = open_set.pop()
        closed_set.add(current_state)

        for neighbor in maze.get_actions(current_state):

            if search[neighbor] < counter:
                g[neighbor] = float('inf')
                search[neighbor] = counter

            tentative_g = g[current_state] + 1
            if tentative_g < g[neighbor]:
                g[neighbor] = tentative_g
                tree[neighbor] = current_state

                if open_set.contains(neighbor):
                    open_set.remove(neighbor)

                neighbor_f = g[neighbor] + h[neighbor]
                open_set.push((neighbor_f, neighbor))

# def main_procedure(maze, h):
#
#     counter = 0
#     start = maze.start
#     goal = maze.goal
#     g = {}
#     tree = {}
#
#     search = {}
#     for i in range(len(maze.grid)):
#         for j in range(len(maze.grid)):
#             search[(i,j)] = 0
#
#     while start != goal:
#
#         counter = counter + 1
#         g[start] = 0
#         search[start] = counter
#         g[goal] = float('inf')
#         search[goal] = counter
#         open_set = PriorityQueue()
#         closed_set = set()
#
#         f_start = g[start] + h[start]
#         open_set.push((f_start, start))
#
#         path = compute_path(maze, start, goal, g, open_set, h, closed_set, search, counter, tree)
#
#         if not open_set:
#             print("cannot reach target")
#             return None
#
#         for i in range(1, len(path)):
#             if maze.grid[path[i][0]][path[i][1]] == 1:
#                 break
#             else:
#
#                 g[path[i]] = g[start] + i
#                 start = path[i]
#
# def compute_path(maze, start, goal, g, open_set, h, closed_set, search, counter, tree):
#
#     min_f, s  = open_set.peek()
#     while g[goal] > min_f:
#
#         min_f, s = open_set.pop()
#         closed_set.add(s)
#
#         if s == start:
#             all_neighbors = maze.get_actions(s)
#             neighbors = []
#             for neighbor in all_neighbors:
#                 if maze.grid[neighbor[0]][neighbor[1]] != 1:  # check if neighbor is not blocked.
#                     neighbors.append(neighbor)
#         else:
#             neighbors = maze.get_actions(s)
#
#         for neighbor in neighbors:
#
#             if search[neighbor] < counter:
#                 g[neighbor] = float('inf')
#                 search[neighbor] = counter
#             if g[neighbor] > g[s] + 1:
#                 g[neighbor] = g[s] + 1
#                 tree[neighbor] = s
#                 if open_set.contains(neighbor):
#                     open_set.remove(neighbor)
#                 neighbor_f = g[neighbor] + h[neighbor]
#                 open_set.push((neighbor_f, neighbor))
#
#     return reconstruct_path(tree, goal)
#
# env = GridEnvironment(3)
# env.visualize_maze(None)
# main_procedure(env, env.get_heuristic())

# def compute_path(maze, heuristic):
#
#     g_values = {maze.start: 0}
#     open_set = PriorityQueue()
#     closed_set = set()
#     tree = {}
#     open_set.push((heuristic[maze.start], maze.start))
#
#     while open_set:
#         f_value, current = open_set.pop()
#
#         if current == maze.goal:
#             return reconstruct_path(tree, maze.goal)
#
#         closed_set.add(current)
#
#         for neighbor in maze.get_actions(current):
#             tentative_g = g_values[current] + 1
#
#             if neighbor in closed_set and tentative_g >= g_values.get(neighbor, float('inf')):
#                 continue
#
#             if tentative_g < g_values.get(neighbor, float('inf')):
#                 g_values[neighbor] = tentative_g
#                 tree[neighbor] = current
#                 f_neighbor = tentative_g + heuristic[neighbor]
#                 open_set.push((f_neighbor, neighbor))
#
#     return None

que = PriorityQueue()
que.push((10101, (10,10)))

print(que.peek()[0])