# CS 441 Programming Assignment 1
# Alan Shirk - alans@pdx.edu

import heapq

goal_state = ['b', 1, 2, 3, 4, 5, 6, 7, 8]
max_steps = 1000000

class PuzzleState:
    def __init__(self, board, parent=None, action=None, path_cost=0):
        self.board = board
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0 if parent is None else parent.depth + 1
        self.g_cost = path_cost 
        self.h_cost = 0
        self.f_cost = 0

    def __lt__(self, other):
        return self.f_cost < other.f_cost

    def __eq__(self, other):
        return self.board == other.board

    def __hash__(self):
        return hash(str(self.board))

def heuristic_misplaced_tiles(state):
    """Number of misplaced tiles heuristic."""
    misplaced_tiles = sum(
        1 for i in range(9) 
        if state.board[i] != 'b' and state.board[i] != goal_state[i]
    )
    return misplaced_tiles

def heuristic_manhattan_distance(state):
    """Manhattan distance heuristic for the 8-puzzle problem."""
    distance = 0
    for i in range(9):
        if state.board[i] != 'b':
            x, y = divmod(state.board[i] - 1, 3)
            curr_x, curr_y = divmod(i, 3)
            distance += abs(x - curr_x) + abs(y - curr_y)
    return distance

def heuristic_misplaced_row_column(state):
    """Heuristic counting the number of tiles misplaced in their row and column."""
    misplaced_row_column = 0
    for i in range(9):
        if state.board[i] != 'b':
            correct_i, correct_j = divmod(state.board[i] - 1, 3)
            curr_i, curr_j = divmod(i, 3)
            if correct_i != curr_i:
                misplaced_row_column += 1
            if correct_j != curr_j:
                misplaced_row_column += 1
    return misplaced_row_column

def goal_test(state):
    return state.board == goal_state

def expand(node):
    """Expands the given node to generate successors."""
    successors = []
    board = node.board
    i = board.index('b')
    actions = [(-1, 0, 'up'), (1, 0, 'down'), (0, -1, 'left'), (0, 1, 'right')]
    x, y = divmod(i, 3)
    
    for dx, dy, action in actions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            ni = nx * 3 + ny
            new_board = board[:]
            new_board[i], new_board[ni] = new_board[ni], new_board[i]
            successors.append(PuzzleState(new_board, node, action, node.path_cost + 1))
    
    return successors


def tree_search(initial_state, heuristic_fn, max_steps, use_a_star=False):
    """Best first search based on the general tree search algorithm."""
    fringe = []
    fringe_dict = {}
    initial_state.h_cost = heuristic_fn(initial_state)
    initial_state.f_cost = initial_state.g_cost + initial_state.h_cost if use_a_star else initial_state.h_cost
    heapq.heappush(fringe, (initial_state.f_cost, initial_state))
    fringe_dict[tuple(initial_state.board)] = initial_state
    explored = set()
    steps = 0

    while fringe and steps < max_steps:
        _, node = heapq.heappop(fringe)
        fringe_dict.pop(tuple(node.board), None)
        
        if goal_test(node):
            return node
        
        explored.add(tuple(node.board))
        for successor in expand(node):
            if tuple(successor.board) not in explored and tuple(successor.board) not in fringe_dict:
                successor.g_cost = node.g_cost + 1
                successor.h_cost = heuristic_fn(successor)
                successor.f_cost = successor.g_cost + successor.h_cost if use_a_star else successor.h_cost
                heapq.heappush(fringe, (successor.f_cost, successor))
                fringe_dict[tuple(successor.board)] = successor
        
        steps += 1

    print(f"Reached max steps: {max_steps}")
    return None

def print_solution(solution):
    """Prints the solution path."""
    steps = []
    while solution:
        steps.append(solution)
        solution = solution.parent
    steps.reverse()
    
    solution_path = " → ".join(
        f"({' '.join(str(num) for num in step.board)})"
        for step in steps
    )
    return solution_path, len(steps) - 1

def run_experiments(initial_states, heuristics, max_steps):
    print("Best-First Search:")
    print("=" * 50)
    for heuristic_fn in heuristics:
        if (heuristic_fn.__name__ == 'heuristic_misplaced_row_column'):
            print("Number misplaced in row and column heuristic:")
        elif (heuristic_fn.__name__ == 'heuristic_misplaced_tiles'):
            print("Total number misplaced heuristic:")
        elif (heuristic_fn.__name__ == 'heuristic_manhattan_distance'):
            print("Manhattan distance heuristic:")
        print("=" * 50)
        total_steps = 0
        solution_count = 0
        
        for i, initial_board in enumerate(initial_states):
            initial_state = PuzzleState(initial_board)
            solution = tree_search(initial_state, heuristic_fn, max_steps, use_a_star=False)
            
            print(f"Solution Path {i + 1}:")
            if solution:
                solution_path, steps = print_solution(solution)
                print(solution_path)
                total_steps += steps
                solution_count += 1
            else:
                print("No solution found or maximum steps reached.")
            print("=" * 20)
        
        if solution_count > 0:
            average_steps = total_steps / solution_count
        else:
            average_steps = float('inf')
        
        print(f"Average number of steps: {average_steps}")
        print("=" * 50)

    print("A* Search:")
    print("=" * 50)
    for heuristic_fn in heuristics:
        if (heuristic_fn.__name__ == 'heuristic_misplaced_row_column'):
            print("Number misplaced in row and column heuristic:")
        elif (heuristic_fn.__name__ == 'heuristic_misplaced_tiles'):
            print("Total number misplaced heuristic:")
        elif (heuristic_fn.__name__ == 'heuristic_manhattan_distance'):
            print("Manhattan distance heuristic:")
        print("=" * 50)
        total_steps = 0
        solution_count = 0
        
        for i, initial_board in enumerate(initial_states):
            initial_state = PuzzleState(initial_board)
            solution = tree_search(initial_state, heuristic_fn, max_steps, use_a_star=True)
            
            print(f"Solution Path {i + 1}:")
            if solution:
                solution_path, steps = print_solution(solution)
                print(solution_path)
                total_steps += steps
                solution_count += 1
            else:
                print("No solution found or maximum steps reached.")
            print("=" * 20)
        
        if solution_count > 0:
            average_steps = total_steps / solution_count
        else:
            average_steps = 0
        
        print(f"Average number of steps: {average_steps}")
        print("=" * 50)

# Setting up and running the 8-puzzle simulation

initial_states = [
    [1, 2, 'b', 3, 4, 5, 6, 7, 8],
    [1, 2, 3, 4, 5, 6, 'b', 7, 8],
    [8, 6, 7, 2, 5, 4, 3, 'b', 1],
    ['b', 3, 4, 8, 1, 2, 7, 6, 5],
    [5, 4, 'b', 6, 1, 8, 7, 3, 2]
]

heuristics = [heuristic_misplaced_tiles, heuristic_manhattan_distance, heuristic_misplaced_row_column]

run_experiments(initial_states, heuristics, max_steps)
