from __future__ import division
from __future__ import print_function
from collections import deque

import sys
import math
import time
import resource
import queue

## The Class that Represents the Puzzle
class PuzzleState(object):
    """
    The PuzzleState stores a board configuration and implements
    movement instructions to generate valid children.
    """

    def __init__(
        self, config, n, parent=None, action="Initial", cost=0, blank_index=-1
    ):
        """
        :param config->List(int): Represents the n*n board, for e.g. [0,1,2,3,4,5,6,7,8] represents the goal state.
        :param n->int : Size of the board
        :param parent->PuzzleState
        :param action->string
        :param cost->int
        :param blank_index->int: Index of the empty block
        """
        if n * n != len(config) or n < 2:
            raise Exception("The length of config is not correct!")

        self.n = n
        self.cost = cost
        self.parent = parent
        self.action = action
        self.config = config
        self.children = []
        self.blank_index = blank_index if blank_index > -1 else self.config.index(0)

    def __lt__(self, other):
        return self.cost > other.cost

    def display(self):
        """Display this Puzzle state as a n*n board"""
        # need to change this to new format
        for i in range(self.n):
            print(self.config[self.n * i : self.n * (i + 1)])

    def move_helper(self, position, move):
        """
        Helper function for move
        :return a PuzzleState with the new configuration
        """
        new_config = self.config[:]
        new_config[self.blank_index], new_config[position] = new_config[position], 0
        new_state = PuzzleState(new_config, self.n, self, move, self.cost + 1, position)
        self.children.append(new_state)
        return new_state

    def move_up(self):
        """
        Moves the blank tile one row up.
        :return a PuzzleState with the new configuration
        """
        if self.blank_index < self.n:
            return None

        return self.move_helper(self.blank_index - self.n, "Up")

    def move_down(self):
        """
        Moves the blank tile one row down.
        :return a PuzzleState with the new configuration
        """
        if len(self.config) - self.blank_index <= self.n:
            return None

        return self.move_helper(self.blank_index + self.n, "Down")

    def move_left(self):
        """
        Moves the blank tile one column to the left.
        :return a PuzzleState with the new configuration
        """
        if self.blank_index % self.n == 0:
            return None

        return self.move_helper(self.blank_index - 1, "Left")

    def move_right(self):
        """
        Moves the blank tile one column to the right.
        :return a PuzzleState with the new configuration
        """
        if (self.blank_index + 1) % self.n == 0:
            return None

        return self.move_helper(self.blank_index + 1, "Right")

    def expand(self):
        """Generate the child nodes of this node"""

        # Node has already been expanded
        if len(self.children) != 0:
            return self.children

        # Add child nodes in order of UDLR
        children = [
            self.move_up(),
            self.move_down(),
            self.move_left(),
            self.move_right(),
        ]

        # Compose self.children of all non-None children states
        self.children = [state for state in children if state is not None]
        return self.children


def get_path(puzzle_state):
    """
    Reconstructs path to the final puzzle state
    :return an array of moves ['Left', 'Right', ..., 'Up']
    """

    path = []
    current_state = puzzle_state
    while current_state.parent:
        path.append(current_state.action)
        current_state = current_state.parent

    path.reverse()
    return path


def write_output(results, running_time, max_ram_usage):
    """Writes output to output.txt"""

    current_state, nodes_expanded, search_depth, max_search_depth = results

    f = open("output.txt", "w")
    print("path_to_goal:", get_path(current_state), file=f)
    f.write("cost_of_path: " + str(current_state.cost) + "\n")
    f.write("nodes_expanded: " + str(nodes_expanded) + "\n")
    f.write("search_depth: " + str(search_depth) + "\n")
    f.write("max_search_depth: " + str(max_search_depth) + "\n")
    f.write("running_time: %.8f \n" % running_time)
    f.write("max_ram_usage: %.8f \n" % max_ram_usage)
    f.close()

    return


def bfs_search(initial_state):
    """BFS search"""

    frontier, explored = deque([initial_state]), set()
    current_state, found, search_depth = None, False, 0

    # level-order traversal BFS
    while frontier:
        for _ in range(len(frontier)):
            current_state = frontier.popleft()
            if test_goal(current_state):
                found = True
                break
            if tuple(current_state.config) not in explored:
                explored.add(tuple(current_state.config))
                for child in current_state.expand():
                    frontier.append(child)
        if found:
            break
        search_depth += 1

    if not current_state:
        return None
    max_search_depth = search_depth if not frontier else search_depth + 1
    return current_state, len(explored), search_depth, max_search_depth


def dfs_search(initial_state):
    """DFS search"""

    nodes_expanded = max_search_depth = 0
    frontier, explored, current_state = deque([initial_state]), set(), None

    while frontier:
        current_state = frontier.pop()
        explored.add(tuple(current_state.config))
        max_search_depth = max(max_search_depth, current_state.cost)
        if test_goal(current_state):
            break
        for child in reversed(current_state.expand()):
            if tuple(child.config) not in explored:
                frontier.append(child)
                explored.add(tuple(child.config))
        nodes_expanded += 1

    if not current_state:
        return None
    return current_state, nodes_expanded, current_state.cost, max_search_depth


def A_star_search(initial_state):
    """A * search"""

    nodes_expanded = max_search_depth = 0
    frontier, explored, current_state = queue.PriorityQueue(), set(), None
    frontier.put((0, initial_state))

    while frontier:
        _, current_state = frontier.get()
        max_search_depth = max(max_search_depth, current_state.cost)
        explored.add(tuple(current_state.config))
        if test_goal(current_state):
            break
        for child in reversed(current_state.expand()):
            state = tuple(child.config)
            if state not in explored:
                explored.add(state)
                frontier.put((calculate_total_cost(child) + child.cost, child))
        nodes_expanded += 1

    if not current_state:
        return None
    return current_state, nodes_expanded, current_state.cost, max_search_depth


def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""

    estimated_cost = 0
    for idx, value in enumerate(state.config):
        if value != 0:
            estimated_cost += calculate_manhattan_dist(idx, int(value), state.n)
    return estimated_cost


def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""

    return abs(value - idx) // n + abs(value - idx) % n


def test_goal(puzzle_state):
    """test the state is the goal state or not"""

    return puzzle_state.config == goal_state


goal_state = []
# Main Function that reads in Input and Runs corresponding Algorithm
def main():
    global goal_state
    search_mode = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    board_size = int(math.sqrt(len(begin_state)))
    goal_state = [v for v in range(board_size * board_size)]

    # check if input is valid
    if set(map(int, begin_state)) != set(range(board_size * board_size)):
        raise Exception("Config contains invalid/duplicate entries: ", begin_state)

    begin_state = list(map(int, begin_state))
    hard_state = PuzzleState(begin_state, board_size)
    start_ram, start_time, results = (
        resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        time.time(),
        None,
    )

    if search_mode == "bfs":
        results = bfs_search(hard_state)
    elif search_mode == "dfs":
        results = dfs_search(hard_state)
    elif search_mode == "ast":
        results = A_star_search(hard_state)

    running_time, max_ram_usage = (
        resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - start_ram
    ) / (2**20), (time.time() - start_time)

    if not results:
        print("Puzzle is unsolvable!")
    else:
        write_output(results, running_time, max_ram_usage)

    end_time = time.time()
    print("Program completed in %.3f second(s)" % (end_time - start_time))


if __name__ == "__main__":
    main()
