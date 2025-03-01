import Environments
import Ties

def main():

    print("Intro to AI Assignment 1: Using a* variations to navigate maze like structures.")
    print("-------------------------------------------------------------------------------")

    # Dictionary to store maze objects. Keys: [maze0...maze49]
    mazes = Environments.load_mazes("test_mazes")
    test = mazes["maze10"]
    test.visualize_maze(None)

    ''' RUN REGULAR A* '''
    path = Ties.compute_path(test, test.get_heuristic())
    test.visualize_maze(path)


if __name__ == "__main__":
    main()