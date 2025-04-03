# Part 3 - Forward vs. Backward [20 points]: Implement and compare Repeated Forward A* and Repeated Backward A*
# with respect to their runtime or, equivalently, number of expanded cells. Explain your observations in detail, that is, explain
# what you observed and give a reason for the observation. Both versions of Repeated A* should break ties among cells with
# the same f-value in favor of cells with larger g-values and remaining ties in an identical way, for example randomly.

from PriorityQueue import PriorityQueue
from Environments import GridEnvironment
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import Environments
import time
import RepeatedForward

def reconstruct_path(tree, goal):
    if not tree:
        return []
    path = [goal]
    current = goal
    while current in tree:
        current = tree[current]
        path.append(current)
    return path

def compute_path(
        problem, h, counter, search, g, start,
        goal, open_set, closed_set, c, large_g
):

    tree = {} # Search tree representing the shortest unblocked path

    while g[goal] > open_set.peek()[0]:

        current_f, current_g, current = open_set.pop()

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

                if large_g:
                    open_set.push((neighbor_f, -g[neighbor], neighbor))
                else:
                    open_set.push((neighbor_f, g[neighbor], neighbor))

        if not open_set:
            return {}

    return tree

def main_procedure(problem: GridEnvironment , h: {}, visualize: bool, large_g: bool) -> []:

    if visualize:
        cmap = mcolors.ListedColormap(['white', 'black', 'green', 'blue', 'red'])
        bounds = [0, 1, 2, 3, 4, 5]
        norm = mcolors.BoundaryNorm(bounds, cmap.N)
        plt.interactive(True)
        plt.figure(figsize=(6,6))
        image_object = plt.imshow(problem.get_next_frame(None, None), cmap=cmap, norm=norm)  # Initial plot
        plt.xticks([]), plt.yticks([])
        plt.show()

    counter = 0
    search = {}
    g = {}

    c = {}
    for i in range(problem.size):
        for j in range(problem.size):
            state = (i,j)
            search[state] = 0
            c[state] = 1  # c(action: neighbors(state) -> state)

    goal = problem.goal # reverse for backwards
    start = problem.start

    for neighbor in problem.get_actions(start, False):
        if problem.grid[neighbor] == 1:
            c[neighbor] = float('inf')

    main_path = [start]

    while start != goal:

        # counter += 1
        # g[start] = 0
        # search[start] = counter
        # g[goal] = float('inf')
        # search[goal] = counter
        # open_set = PriorityQueue()
        # closed_set = set()
        # start_f = g[start] + h[start]

        counter += 1
        g[goal] = 0
        search[goal] = counter
        g[start] = float('inf')
        search[start] = counter
        open_set = PriorityQueue()
        closed_set = set()
        goal_f = g[goal] + h[goal]

        if large_g:
            open_set.push((goal_f, -g[goal], goal))
        else:
            open_set.push((goal_f, g[goal], goal))

        shortest_unblocked_path = reconstruct_path(compute_path(
            problem, h, counter, search, g, goal, start,
            open_set, closed_set, c, large_g,
        ), start)

        if visualize:
            image_object.set_data(problem.get_next_frame(main_path, shortest_unblocked_path))
            plt.draw()
            plt.pause(0.01)

        if not open_set or not shortest_unblocked_path:
            print("Cannot reach goal.")
            return []

        # Move agent along the path from start to goal until it reaches goal
        # OR one or more action costs on the path increase
        while True:
            next_state = shortest_unblocked_path.pop(0)
            if next_state == start:
                pass
            elif not next_state:
                print("Cannot reach goal.")
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

    if visualize:
        plt.interactive(False)
        plt.imshow(problem.get_next_frame(main_path, None), cmap=cmap, norm=norm)
        plt.draw_all()
        plt.show()

    print("Reached goal.")
    return main_path

if __name__ == "__main__":
    mazes = Environments.load_mazes("test_mazes")
    backwards_heuristic = mazes["maze1"].get_backwards_heuristic() # use backwards heuristic
    heuristic = mazes["maze1"].get_heuristic()

    for maze in mazes:

        # print("Testing: " + maze)
        #
        # forward_start = time.perf_counter()
        # RepeatedForward.main_procedure(mazes[maze], heuristic, True, True)
        # forward_end = time.perf_counter()
        # forward_elapsed = forward_end - forward_start
        #
        # print("Repeated Forward Time Elapsed: " + str(forward_elapsed))

        backward_start = time.perf_counter()
        main_procedure(mazes[maze], backwards_heuristic, True, False)
        backward_end = time.perf_counter()
        backward_elapsed = backward_end - backward_start

        print("Repeated Backward Time Elapsed: " + str(backward_elapsed))