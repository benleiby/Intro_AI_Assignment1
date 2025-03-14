import Environments
from Adaptive import main_procedure


print("Intro to AI Assignment 1: Using a* variations to navigate maze like structures.")
print("-------------------------------------------------------------------------------")

# Dictionary to store maze objects. Keys: [maze0...maze49]
# mazes = Environments.load_mazes("test_mazes")
# test = mazes["maze10"]
test = Environments.GridEnvironment(21)

main_procedure(test, test.get_heuristic(), True, True)