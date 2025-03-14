# Part 2 - The Effects of Ties [15 points]: Repeated Forward A* needs to break ties to decide which cell to expand next if
# several cells have the same smallest f-value. It can either break ties in favor of cells with smaller g-values or in favor of
# cells with larger g-values. Implement and compare both versions of Repeated Forward A* with respect to their runtime or,
# equivalently, number of expanded cells. Explain your observations in detail, that is, explain what you observed and give a
# reason for the observation.
# [Hint: For the implementation part, priorities can be integers rather than pairs of integers. For example, you can use
# c × f (s) − g(s) as priorities to break ties in favor of cells with larger g-values, where c is a constant larger than the largest
# g-value of any generated cell. For the explanation part, consider which cells both versions of Repeated Forward A* expand
# for the example search problem from Figure 9.]

import Environments
import time
import RepeatedForward

mazes = Environments.load_mazes("test_mazes")
heuristic = mazes["maze1"].get_heuristic()

for maze in mazes:

    print("Testing: " + maze)

    large_g_start = time.perf_counter()
    RepeatedForward.main_procedure(mazes[maze], heuristic, False, True)
    large_g_end = time.perf_counter()
    large_g_elapsed = large_g_end - large_g_start

    print("Large G Time Elapsed: " + str(large_g_elapsed))

    small_g_start = time.perf_counter()
    RepeatedForward.main_procedure(mazes[maze], heuristic, False, False)
    small_g_end = time.perf_counter()
    small_g_elapsed = small_g_end - small_g_start

    print("Small G Time Elapsed: " + str(small_g_elapsed))

 