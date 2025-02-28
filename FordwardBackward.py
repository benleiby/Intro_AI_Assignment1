# Part 3 - Forward vs. Backward [20 points]: Implement and compare Repeated Forward A* and Repeated Backward A*
# with respect to their runtime or, equivalently, number of expanded cells. Explain your observations in detail, that is, explain
# what you observed and give a reason for the observation. Both versions of Repeated A* should break ties among cells with
# the same f-value in favor of cells with larger g-values and remaining ties in an identical way, for example randomly.
import heapq
from Environments import GridEnvironment

class PriorityQueueTwo:
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

def reconstruct_path(tree, start):
    path = [start]
    current = start
    while current in tree:
        current = tree[current] 
        path.append(current)  
    return path[::-1] 

def backward_Path(maze,heuristic):
    g_values = {maze.goal: 0}  
    open_set = PriorityQueueTwo()
    closed_set = set()
    tree = {}
    
    open_set.push((heuristic[maze.goal], maze.goal)) 

    while open_set:
        f_value, current = open_set.pop()

    
        if current == maze.start:
            return reconstruct_path(tree, maze.start)

        closed_set.add(current)

        for neighbor in maze.get_actions(current):

            tentative_g = g_values[current] + 1
            if neighbor in closed_set and tentative_g >= g_values.get(neighbor, float('inf')):
                continue

            if tentative_g < g_values.get(neighbor, float('inf')):
                g_values[neighbor] = tentative_g
                tree[neighbor] = current
                f_neighbor = tentative_g + heuristic[neighbor]  
                open_set.push((f_neighbor, neighbor))

    return None


env = GridEnvironment(101)
env.visualize_maze(None)
