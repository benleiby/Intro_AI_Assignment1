import Environments
from Adaptive import main_procedure as adaptive
from RepeatedForward import main_procedure as repeated_forward
from FordwardBackward import main_procedure as repeated_backward

mazes = Environments.load_mazes("test_mazes")
test = mazes["maze10"]

repeated_forward(test, test.get_heuristic(), True, True)
repeated_forward(test, test.get_heuristic(), True, False)

repeated_backward(test, test.get_backwards_heuristic(), True, True)

adaptive(test, test.get_heuristic(), True, True)