import random

# Constants
GRID_SIZE = 3
MAX_STEPS = 100
DIRECTIONS = ["UP", "DOWN", "LEFT", "RIGHT"]

# Environment class
class Environment:
    def __init__(self, num_dirt_piles):
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.agent_pos = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
        self.dirt_piles = num_dirt_piles
        self.place_dirt_piles()

    def place_dirt_piles(self):
        for _ in range(self.dirt_piles):
            while True:
                x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
                if self.grid[x][y] == 0:
                    self.grid[x][y] = 1
                    break

    def is_dirty(self, pos):
        x, y = pos
        return self.grid[x][y] == 1

    def clean(self, pos):
        x, y = pos
        self.grid[x][y] = 0

    def move_agent(self, direction):
        x, y = self.agent_pos
        if direction == "UP" and x > 0:
            self.agent_pos = (x-1, y)
        elif direction == "DOWN" and x < GRID_SIZE-1:
            self.agent_pos = (x+1, y)
        elif direction == "LEFT" and y > 0:
            self.agent_pos = (x, y-1)
        elif direction == "RIGHT" and y < GRID_SIZE-1:
            self.agent_pos = (x, y+1)

    def get_percept(self):
        return self.agent_pos, self.is_dirty(self.agent_pos)

# Simple Reflex Agent
def simple_reflex_agent(percept):
    pos, dirty = percept
    if dirty:
        return "SUCK"
    else:
        return random.choice(DIRECTIONS)

# Randomized Agent
def randomized_agent(percept):
    if random.random() < 0.5:
        return "SUCK"
    else:
        return random.choice(DIRECTIONS)

# Reflex Agent with Murphy's Law
def murphy_reflex_agent(percept):
    pos, dirty = percept
    if dirty:
        if random.random() < 0.75:
            return "SUCK"
        else:
            return random.choice(DIRECTIONS)
    else:
        return random.choice(DIRECTIONS)

# Randomized Agent with Murphy's Law
def murphy_randomized_agent(percept):
    if random.random() < 0.5:
        if random.random() < 0.75:
            return "SUCK"
        else:
            return "SUCK"  # Murphy's Law: 25% chance to deposit dirt if clean
    else:
        return random.choice(DIRECTIONS)

# Function to run simulation
def run_simulation(agent_fn, num_dirt_piles, trials):
    total_moves = 0
    total_sucks = 0

    for _ in range(trials):
        env = Environment(num_dirt_piles)
        steps = 0
        while steps < MAX_STEPS:
            percept = env.get_percept()
            action = agent_fn(percept)
            if action == "SUCK":
                total_sucks += 1
                if random.random() > 0.1:  # Murphy's Law: 10% chance dirt sensor fails
                    if percept[1]:  # If dirty
                        if agent_fn != murphy_reflex_agent and agent_fn != murphy_randomized_agent:
                            env.clean(env.agent_pos)
                        elif random.random() < 0.75:
                            env.clean(env.agent_pos)
            else:
                env.move_agent(action)
            steps += 1
            total_moves += 1

    return total_moves / trials, total_sucks / trials

# Main function to execute all experiments
def main():
    trials = 100
    dirt_cases = [1, 3, 5]
    agents = [simple_reflex_agent, randomized_agent, murphy_reflex_agent, murphy_randomized_agent]
    agent_names = ["Simple Reflex", "Randomized", "Murphy's Reflex", "Murphy's Randomized"]

    results = {agent: {dirt: (0, 0) for dirt in dirt_cases} for agent in agent_names}

    for agent_fn, agent_name in zip(agents, agent_names):
        for num_dirt_piles in dirt_cases:
            avg_moves, avg_sucks = run_simulation(agent_fn, num_dirt_piles, trials)
            results[agent_name][num_dirt_piles] = (avg_moves, avg_sucks)

    # Print results
    for agent_name in agent_names:
        print(f"Results for {agent_name}:")
        for num_dirt_piles in dirt_cases:
            avg_moves, avg_sucks = results[agent_name][num_dirt_piles]
            print(f"  Dirt Piles: {num_dirt_piles}, Avg Moves: {avg_moves:.2f}, Avg Sucks: {avg_sucks:.2f}")

if __name__ == "__main__":
    main()
