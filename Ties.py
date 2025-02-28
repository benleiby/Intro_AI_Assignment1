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

def reconstruct_path(tree, goal):
    path = [goal]  # Start with the goal node
    current = goal
    while current in tree:
        current = tree[current]  # Get the parent node
        path.append(current)  # Add the parent to the path
    return path[::-1]  # Reverse the path to get it from start to goal

def main_procedure(maze, h):

    counter = 0
    start = maze.start
    goal = maze.goal
    g = {}

    search = {}
    for i in range(len(maze.grid)):
        for j in range(len(maze.grid)):
            search[(i,j)] = 0

    while start != goal:

        counter += 1
        g[start] = 0
        search[start] = counter
        g[goal] = float('inf')
        search[goal] = counter
        open_set = PriorityQueue()
        closed_set = set()

        f_start = g[start] + h[start]
        open_set.push((f_start, start))

        path = compute_path(maze, goal, g, open_set, h, closed_set, search, counter)

        print(path)


        if not open_set:
            print("cannot reach target")
            return None

        for i in range(1, len(path)):  # start at 1 to avoid index error.
            if maze.grid[path[i][0]][path[i][1]] == 1:
                print("breaking")
                break
            else:
                start = path[i]


def compute_path(maze, goal, g, open_set, h, closed_set, search, counter):

    tree = {}

    min_f, s  = open_set.peek()
    while g[goal] > min_f:

        min_f, s = open_set.pop()
        closed_set.add(s)

        for neighbor in maze.get_actions(s):

            if search[neighbor] < counter:
                g[neighbor] = float('inf')
                search[neighbor] = counter
            if g[neighbor] > g[s] + 1:
                g[neighbor] = g[s] + 1
                tree[neighbor] = s
                if open_set.contains(neighbor):
                    open_set.remove(neighbor)
                neighbor_f = g[neighbor] + h[neighbor]
                open_set.push((neighbor_f, neighbor))

    return reconstruct_path(tree, goal)

env = GridEnvironment(9)
env.visualize_maze(None)
main_procedure(env, env.get_heuristic())

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



