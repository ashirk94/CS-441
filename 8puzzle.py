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
        self.g_cost = path_cost  # Actual cost to reach this node
        self.h_cost = 0  # Heuristic cost to reach the goal
        self.f_cost = 0  # Total cost (g_cost + h_cost)

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
    """Expand the given node to generate successors."""
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
    """General tree search algorithm."""
    fringe = []
    initial_state.h_cost = heuristic_fn(initial_state)
    initial_state.f_cost = initial_state.g_cost + initial_state.h_cost if use_a_star else initial_state.h_cost
    heapq.heappush(fringe, (initial_state.f_cost, initial_state))
    explored = set()
    steps = 0

    while fringe and steps < max_steps:
        _, node = heapq.heappop(fringe)
        if goal_test(node):
            return node
        
        explored.add(node)
        for successor in expand(node):
            if successor not in explored:
                successor.g_cost = node.g_cost + 1
                successor.h_cost = heuristic_fn(successor)
                successor.f_cost = successor.g_cost + successor.h_cost if use_a_star else successor.h_cost
                heapq.heappush(fringe, (successor.f_cost, successor))
        
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
        f"({' '.join(str(num) for num in step.board)})"
        for step in steps
    )
    return solution_path, len(steps) - 1

def run_experiments(initial_states, heuristics, max_steps):
    print("Best-First Search:")
    for heuristic_fn in heuristics:
        print(f"Heuristic - {heuristic_fn.__name__}:")
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
            average_steps = 0
        
        print(f"Average number of steps: {average_steps}")
        print("=" * 40)

    print("A* Search:")
    for heuristic_fn in heuristics:
        print(f"Heuristic - {heuristic_fn.__name__}:")
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
        print("=" * 40)

# Initial states
initial_states = [
    [1, 2, 'b', 3, 4, 5, 6, 7, 8],
    [1, 2, 3, 4, 5, 6, 'b', 7, 8],
    [8, 6, 7, 2, 5, 4, 3, 'b', 1],
    ['b', 3, 4, 8, 1, 2, 7, 6, 5],
    [5, 4, 'b', 6, 1, 8, 7, 3, 2]
]

# Heuristics
heuristics = [heuristic_misplaced_tiles, heuristic_manhattan_distance, heuristic_misplaced_row_column]

# Run the experiments
run_experiments(initial_states, heuristics, max_steps)
