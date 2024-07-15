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
        [7, 8, 0]
    ]
    misplaced_tiles = sum(
        1 for i in range(3) for j in range(3) 
        if state.board[i][j] != 0 and state.board[i][j] != goal_state[i][j]
    )
    return misplaced_tiles

def heuristic_manhattan_distance(state):
    """Manhattan distance heuristic for the 8-puzzle problem."""
    goal_state = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]
    distance = 0
    for i in range(3):
        for j in range(3):
            if state.board[i][j] != 0:
                x, y = divmod(state.board[i][j] - 1, 3)
                distance += abs(x - i) + abs(y - j)
    return distance

def goal_test(state):
    return state.board == [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]

def get_successors(state):
    """Generate successors of the given state."""
    successors = []
    board = state.board
    i, j = next((i, j) for i, row in enumerate(board) for j, val in enumerate(row) if val == 0)
    actions = [(-1, 0, 'up'), (1, 0, 'down'), (0, -1, 'left'), (0, 1, 'right')]
    
    for di, dj, action in actions:
        ni, nj = i + di, j + dj
        if 0 <= ni < 3 and 0 <= nj < 3:
            new_board = [row[:] for row in board]
            new_board[i][j], new_board[ni][nj] = new_board[ni][nj], new_board[i][j]
            successors.append(PuzzleState(new_board, state, action, state.path_cost + 1))
    
    return successors

def best_first_search(initial_state, heuristic_fn):
    """Best-first search algorithm."""
    fringe = []
    initial_state.f_cost = heuristic_fn(initial_state)
    heapq.heappush(fringe, initial_state)
    explored = set()

    while fringe:
        node = heapq.heappop(fringe)
        if goal_test(node):
            return node
        
        explored.add(node)
        for successor in get_successors(node):
            if successor not in explored:
                successor.f_cost = heuristic_fn(successor)
                heapq.heappush(fringe, successor)

    return None

def print_solution(solution):
    """Print the solution steps."""
    steps = []
    while solution:
        steps.append(solution)
        solution = solution.parent
    steps.reverse()
    for step in steps:
        for row in step.board:
            print(row)
        print()

# Initial state of the 8-puzzle problem
initial_board = [
    [7, 2, 4],
    [5, 6, 0],
    [8, 3, 1]
]

initial_state = PuzzleState(initial_board)

# Choose the heuristic function to use: heuristic_misplaced_tiles or heuristic_manhattan_distance
heuristic_fn = heuristic_manhattan_distance

# Solve the puzzle
solution = best_first_search(initial_state, heuristic_fn)

# Print the solution steps
if solution:
    print("Solution found!")
    print_solution(solution)
else:
    print("No solution found.")
