# Sliding Puzzle Solver

## An n x n grid sliding puzzle solver.

The N-puzzle problem is played on a N-by-N grid with square tiles labeled 1 through (N*N)-1 and a blank tile labeled 0.

Implemented with BFS, DFS, and A* search algorithms.

A* search uses Manhattan priority function.

## Usage
### Initial Puzzle
6 1 8

4 0 2

7 3 5
### Input
```
$python3 puzzle.py ast 6,1,8,4,0,2,7,3,5
```
### Output
```
path_to_goal: ['Down', 'Right', 'Up', 'Up', 'Left', 'Down', 'Right',
                'Down', 'Left', 'Up', 'Left', 'Up', 'Right', 'Right', 
                'Down', 'Down', 'Left', 'Left', 'Up', 'Up']
cost_of_path: 20
nodes_expanded: 843
search_depth: 20
max_search_depth: 20
```
