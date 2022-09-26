from __future__ import division
from __future__ import print_function
from collections import deque

import sys
import math
import time
import resource

# import queue as Q


#### SKELETON CODE ####
## The Class that Represents the Puzzle
class PuzzleState(object):
    """
    The PuzzleState stores a board configuration and implements
    movement instructions to generate valid children.
    """

    # target puzzle state:
    # idx: 0, 1, 2, 3, 4, 5, 6, 7, 8
    # val:[0, 1, 2, 3, 4, 5, 6, 7, 8]

    def __init__(
        self, config, n, parent=None, action="Initial", cost=0, blank_index=-1
    ):
        """
        :param config->str: Represents the n*n board, for e.g. [0,1,2,3,4,5,6,7,8] represents the goal state.
        :param n->int : Size of the board
        :param parent->PuzzleState
        :param action->string
        :param cost->int
        :param blank_index->int: Index of the empty block
        """
        if n * n != len(config) or n < 2:
            raise Exception("The length of config is not correct!")

        # if set(config) != set(range(n * n)):
        #     raise Exception("Config contains invalid/duplicate entries : ", config)

        self.n = n
        self.cost = cost
        self.parent = parent
        self.action = action
        self.config = config
        self.children = []
        # Get the index and (row, col) of empty block
        self.blank_index = blank_index if blank_index > -1 else self.config.index("0")

    def display(self):
        """Display this Puzzle state as a n*n board"""
        # need to change this to new format
        tmp = list(int(c) for c in self.config)

        for i in range(self.n):
            print(tmp[self.n * i : self.n * (i + 1)])

    def move_up(self):
        """
        Moves the blank tile one row up.
        :return a PuzzleState with the new configuration
        """
        if self.blank_index < self.n:
            return None

        # switch position
        new_pos = self.blank_index - self.n
        new_config = list(self.config)
        new_config[self.blank_index], new_config[new_pos] = new_config[new_pos], "0"
        # create new state
        new_state = PuzzleState(
            "".join(new_config), self.n, self, "Up", self.cost + 1, new_pos
        )
        self.children.append(new_state)

        return new_state

    def move_down(self):
        """
        Moves the blank tile one row down.
        :return a PuzzleState with the new configuration
        """
        if len(self.config) - self.blank_index <= self.n:
            return None

        # switch position
        new_position = self.blank_index + self.n
        new_config = list(self.config)
        new_config[self.blank_index], new_config[new_position] = (
            new_config[new_position],
            "0",
        )
        # create new state
        new_state = PuzzleState(
            "".join(new_config), self.n, self, "Down", self.cost + 1, new_position
        )
        self.children.append(new_state)

        return new_state

    def move_left(self):
        """
        Moves the blank tile one column to the left.
        :return a PuzzleState with the new configuration
        """
        if self.blank_index % self.n == 0:
            return None

        # switch position
        new_position = self.blank_index - 1
        new_config = list(self.config)
        new_config[self.blank_index], new_config[new_position] = (
            new_config[new_position],
            "0",
        )
        # create new state
        new_state = PuzzleState(
            "".join(new_config), self.n, self, "Left", self.cost + 1, new_position
        )
        self.children.append(new_state)

        return new_state

    def move_right(self):
        """
        Moves the blank tile one column to the right.
        :return a PuzzleState with the new configuration
        """
        if (self.blank_index + 1) % self.n == 0:
            return None

        # switch position
        newpos = self.blank_index + 1
        new_config = list(self.config)
        new_config[self.blank_index], new_config[newpos] = new_config[newpos], "0"
        # create new state
        new_state = PuzzleState(
            "".join(new_config), self.n, self, "Right", self.cost + 1, newpos
        )
        self.children.append(new_state)

        return new_state

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


goal_state = ""

# Function that Writes to output.txt
def getPath(puzzle_state):
    path = []
    current_state = puzzle_state
    while current_state.parent:
        path.append(current_state.action)
        current_state = current_state.parent

    path.reverse()
    return path


def writeOutput(
    current_state,
    nodes_expanded,
    search_depth,
    max_search_depth,
    running_time,
    max_ram_usage,
):
    path_to_goal = getPath(current_state)
    cost_of_path = str(current_state.cost)

    f = open("result.txt", "w")
    print("path_to_goal:", path_to_goal, file=f)
    f.write("cost_of_path: " + cost_of_path + "\n")
    f.write("nodes_expanded: " + nodes_expanded + "\n")
    f.write("search_depth: " + search_depth + "\n")
    f.write("max_search_depth: " + max_search_depth + "\n")
    f.write("running_time: " + running_time + "\n")
    f.write("max_ram_usage: " + max_ram_usage + "\n")

    f.close()

    f = open("result.txt", "r")
    print(f.read())
    current_state.display()


def bfs_search(initial_state):
    """BFS search"""

    start_ram, start_time = (
        resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        time.time(),
    )
    q, visited = deque([initial_state]), set()
    current_state, found, search_depth = None, False, 0

    while q:
        for _ in range(len(q)):
            current_state = q.popleft()
            if test_goal(current_state):
                found = True
                break
            if current_state.config not in visited:
                visited.add(current_state.config)
                children = current_state.expand()
                for child in children:
                    q.append(child)
        if found:
            break
        search_depth += 1

    running_time = time.time() - start_time
    max_search_depth = search_depth if not q else search_depth + 1
    max_ram_usage = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - start_ram) / (
        2**20
    )
    if not current_state:
        print("Could not found puzzle!")
    else:
        writeOutput(
            current_state,
            str(len(visited)),
            str(search_depth),
            str(max_search_depth),
            str(running_time),
            str(max_ram_usage),
        )

    return


def dfs_search(initial_state):
    """DFS search"""
    start_ram, start_time = (
        resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        time.time(),
    )
    nodes_expanded = max_search_depth = 0
    stack, visited, current_state = deque([initial_state]), set(), None

    while stack:
        current_state = stack.pop()
        visited.add(current_state.config)
        max_search_depth = max(max_search_depth, current_state.cost)
        if test_goal(current_state):
            break

        for child in reversed(current_state.expand()):
            if child.config not in visited:
                stack.append(child)
                visited.add(child.config)
        nodes_expanded += 1

    running_time = time.time() - start_time
    max_ram_usage = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - start_ram) / (
        2**20
    )
    if not current_state:
        print("Could not solve puzzle!")
    else:
        writeOutput(
            current_state,
            str(nodes_expanded),
            str(current_state.cost),
            str(max_search_depth),
            str(running_time),
            str(max_ram_usage),
        )
    return


def A_star_search(initial_state):
    """A * search"""
    ### STUDENT CODE GOES HERE ###
    pass


def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""
    ### STUDENT CODE GOES HERE ###
    pass


def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""
    ### STUDENT CODE GOES HERE ###
    pass


def test_goal(puzzle_state):
    """test the state is the goal state or not"""
    ### STUDENT CODE GOES HERE ###
    return puzzle_state.config == goal_state


# Main Function that reads in Input and Runs corresponding Algorithm
def main():
    global goal_state
    search_mode = sys.argv[1].lower()
    begin_state = sys.argv[2].replace(",", "")
    board_size = int(math.sqrt(len(begin_state)))
    goal_state = "".join([str(x) for x in range(board_size * board_size)])

    # check if input is valid
    if set(map(int, sys.argv[2].split(","))) != set(range(board_size * board_size)):
        raise Exception(
            "Config contains invalid/duplicate entries : ", sys.argv[2].split(",")
        )

    hard_state = PuzzleState(begin_state, board_size)
    start_time = time.time()

    if search_mode == "bfs":
        bfs_search(hard_state)
    elif search_mode == "dfs":
        dfs_search(hard_state)
    elif search_mode == "ast":
        A_star_search(hard_state)
    # for debugging
    elif search_mode == "test":
        hard_state.display()
        new_state = hard_state.move_right()
        if new_state:
            print("moved up")
            new_state.display()
        else:
            print("could not move up")

    end_time = time.time()
    print("Program completed in %.3f second(s)" % (end_time - start_time))


if __name__ == "__main__":
    main()
