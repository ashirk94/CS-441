import heapq

class PuzzleState:
    def __init__(self, board, parent=None, action=None, path_cost=0):
        self.board = board
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0 if parent is None else parent.depth + 1
        self.f_cost = 0  # This will be used for the heuristic cost

    def __lt__(self, other):
        return self.f_cost < other.f_cost

    def __eq__(self, other):
        return self.board == other.board

    def __hash__(self):
        return hash(str(self.board))

def heuristic_misplaced_tiles(state):
    """Number of misplaced tiles heuristic."""
    goal_state = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 'b']
    ]
    misplaced_tiles = sum(
        1 for i in range(3) for j in range(3) 
        if state.board[i][j] != 'b' and state.board[i][j] != goal_state[i][j]
    )
    return misplaced_tiles

def heuristic_manhattan_distance(state):
    """Manhattan distance heuristic for the 8-puzzle problem."""
    goal_state = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 'b']
    ]
    distance = 0
    for i in range(3):
        for j in range(3):
            if state.board[i][j] != 'b':
                x, y = divmod(state.board[i][j] - 1, 3)
                distance += abs(x - i) + abs(y - j)
    return distance

def heuristic_misplaced_row_column(state):
    """Heuristic counting the number of tiles misplaced in their row and column."""
    goal_state = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 'b']
    ]
    misplaced_row_column = 0
    for i in range(3):
        for j in range(3):
            if state.board[i][j] != 'b':
                correct_i, correct_j = divmod(state.board[i][j] - 1, 3)
                if correct_i != i or correct_j != j:
                    if correct_i != i:
                        misplaced_row_column += 1
                    if correct_j != j:
                        misplaced_row_column += 1
    return misplaced_row_column

def goal_test(state):
    return state.board == [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 'b']
    ]

def get_successors(state):
    """Generate successors of the given state."""
    successors = []
    board = state.board
    i, j = next((i, j) for i, row in enumerate(board) for j, val in enumerate(row) if val == 'b')
    actions = [(-1, 0, 'up'), (1, 0, 'down'), (0, -1, 'left'), (0, 1, 'right')]
    
    for di, dj, action in actions:
        ni, nj = i + di, j + dj
        if 0 <= ni < 3 and 0 <= nj < 3:
            new_board = [row[:] for row in board]
            new_board[i][j], new_board[ni][nj] = new_board[ni][nj], new_board[i][j]
            successors.append(PuzzleState(new_board, state, action, state.path_cost + 1))
    
    return successors

def best_first_search(initial_state, heuristic_fn, max_steps=1000):
    """Best-first search algorithm."""
    fringe = []
    initial_state.f_cost = heuristic_fn(initial_state)
    heapq.heappush(fringe, initial_state)
    explored = set()
    steps = 0

    while fringe and steps < max_steps:
        node = heapq.heappop(fringe)
        if goal_test(node):
            return node
        
        explored.add(node)
        for successor in get_successors(node):
            if successor not in explored:
                successor.f_cost = heuristic_fn(successor)
                heapq.heappush(fringe, successor)
        
        steps += 1

    return None

def print_solution(solution):
    """Print the solution steps."""
    steps = []
    while solution:
        steps.append(solution)
        solution = solution.parent
    steps.reverse()
    
    solution_path = " → ".join(
        f"({' '.join(str(num) for row in step.board for num in row)})"
        for step in steps
    )
    return solution_path, len(steps) - 1

def run_experiments(initial_states, heuristics, max_steps=1000):
    for heuristic_fn in heuristics:
        print(f"Using {heuristic_fn.__name__}:")
        total_steps = 0
        solution_count = 0
        
        for i, initial_board in enumerate(initial_states):
            initial_state = PuzzleState(initial_board)
            solution = best_first_search(initial_state, heuristic_fn, max_steps)
            
            print(f"Initial State {i + 1}:")
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
        print("=" * 40)

# Initial states of the 8-puzzle problem
initial_states = [
    [
        [7, 2, 4],
        [5, 6, 'b'],
        [8, 3, 1]
    ],
    [
        [1, 2, 3],
        [4, 5, 6],
        [7, 'b', 8]
    ],
    [
        [8, 6, 7],
        [2, 5, 4],
        [3, 'b', 1]
    ],
    [
        [1, 3, 4],
        [8, 'b', 2],
        [7, 6, 5]
    ],
    [
        [2, 8, 1],
        [ 'b', 4, 3],
        [7, 6, 5]
    ]
]

# Heuristics to use
heuristics = [heuristic_misplaced_tiles, heuristic_manhattan_distance, heuristic_misplaced_row_column]

# Run the experiments
run_experiments(initial_states, heuristics)
