from PriorityQueue import PriorityQueue
from Environments import GridEnvironment
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def reconstruct_path(tree, goal):
    if not tree:
        return []
    path = [goal]
    current = goal
    while current in tree:
        current = tree[current]
        path.append(current)
    return path[::-1]

# Just running normal a*
def compute_path(
        problem, h, counter, search, g, start,
        goal, open_set, closed_set, c, large_g
):

    tree = {} # Search tree representing the shortest unblocked path

    while g[goal] > open_set.peek()[0]: # while the f(goal) / g(goal) (same thing) is not smallest in que

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

    if visualize: # initialize visualization
        cmap = mcolors.ListedColormap(['white', 'black', 'green', 'blue', 'red'])
        bounds = [0, 1, 2, 3, 4, 5]
        norm = mcolors.BoundaryNorm(bounds, cmap.N)
        plt.interactive(True)
        plt.figure(figsize=(6,6))
        image_object = plt.imshow(problem.get_next_frame(None, None), cmap=cmap, norm=norm)  # Initial plot
        plt.xticks([]), plt.yticks([])
        plt.show()

    counter = 0 # iteration count
    search = {} # which iteration each state was last reached
    g = {}

    c = {} # action cost
    for i in range(problem.size):
        for j in range(problem.size):
            state = (i,j)
            search[state] = 0
            c[state] = 1  # c(action: neighbors(state) -> state)

    start = problem.start
    for neighbor in problem.get_actions(start, False):
        if problem.grid[neighbor] == 1: # if blocked state, cost is infinity (unreachable)
            c[neighbor] = float('inf')

    goal = problem.goal

    main_path = [start]

    while start != goal: # main while loop
        counter += 1
        g[start] = 0
        search[start] = counter
        g[goal] = float('inf')
        search[goal] = counter
        open_set = PriorityQueue()
        closed_set = set()
        start_f = g[start] + h[start]

        if large_g: # open set maintains priority que which orders by f and then g
            open_set.push((start_f, -g[start], start))
        else:
            open_set.push((start_f, g[start], start))

        shortest_unblocked_path = reconstruct_path(compute_path( # compute the path from the agents current position to the goal
            problem, h, counter, search, g, start, goal,
            open_set, closed_set, c, large_g,
        ), goal)

        if visualize: # update visualization
            image_object.set_data(problem.get_next_frame(main_path, shortest_unblocked_path))
            plt.draw()
            plt.pause(0.01)

        if not open_set or not shortest_unblocked_path: # no solution if no path
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
            elif problem.grid[next_state] == 1: # increasing action cost on path, break and re-calculate
                c[next_state] = float('inf')
                break
            else:
                main_path.append(next_state) # continue moving along path
                start = next_state

    if visualize: # final visualization
        plt.interactive(False)
        plt.imshow(problem.get_next_frame(main_path, None), cmap=cmap, norm=norm)
        plt.draw_all()
        plt.show()

    print("Reached goal.")
    return main_path