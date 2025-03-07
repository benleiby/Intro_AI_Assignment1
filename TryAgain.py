import PriorityQueue
import Environments
from Environments import GridEnvironment
import matplotlib as plt

def reconstruct_path(tree, goal):
    if not tree:
        return []
    path = [goal]
    current = goal
    while current in tree:
        current = tree[current]
        path.append(current)
    return path[::-1]

def compute_path(
        problem, h, counter, search, g, start,
        goal, open_set, closed_set, c
):

    tree = {} # Search tree representing the shortest unblocked path

    while g[goal] > open_set.peek()[0]:
        current_f, current = open_set.pop()
        closed_set.add(current)

        for neighbor in problem.get_actions(current, False):
            if search[neighbor] < counter:
                g[neighbor] = float('inf')
                search[neighbor] = counter

            if g[neighbor] > g[current] + c[neighbor]:
                g[neighbor] = g[current] + c[neighbor]
                tree[neighbor] = current
                if open_set.contains(neighbor):
                    open_set.remove(neighbor)

                neighbor_f = g[neighbor] + h[neighbor]
                open_set.push((neighbor_f, neighbor))

        if not open_set:
            return {}

    return tree

def main(problem: GridEnvironment , h: {}) -> []:
    counter = 0
    search = {}
    g = {}

    c = {}
    for i in range(problem.size):
        for j in range(problem.size):
            state = (i,j)
            search[state] = 0
            c[state] = 1  # c(action: neighbors(state) -> state)

    start = problem.start
    for neighbor in problem.get_actions(start, False):
        if problem.grid[neighbor] == 1:
            c[neighbor] = float('inf')

    goal = problem.goal

    main_path = [start]

    while start != goal:
        counter += 1
        g[start] = 0
        search[start] = counter
        g[goal] = float('inf')
        search[goal] = counter
        open_set = PriorityQueue.PriorityQueue()
        closed_set = set()
        start_f = g[start] + h[start]
        open_set.push((start_f, start))

        shortest_unblocked_path = reconstruct_path(compute_path(
            problem, h, counter, search, g, start, goal, open_set, closed_set, c
        ), goal)

        print(shortest_unblocked_path)

        if not open_set or not shortest_unblocked_path:
            print("Cannot reach goal")
            return []

        # Move agent along the path from start to goal until it reaches goal
        # OR one or more action costs on the path increase
        while True:
            next_state = shortest_unblocked_path.pop(0)
            if next_state == start:
                pass
            elif not next_state:
                print("Cannot reach goal")
                return []
            elif next_state == goal:
                start = goal
                break
            elif problem.grid[next_state] == 1:
                c[next_state] = float('inf')
                break
            else:
                main_path.append(next_state)
                start = next_state

    print("reached goal")
    return main_path

test = Environments.GridEnvironment(9)
test.visualize_maze(None)
heuristic = test.get_heuristic()
test_path = main(test, heuristic)
test.visualize_maze(test_path)