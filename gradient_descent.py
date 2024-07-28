# Homework 2 Artificial Intelligence
# alans@pdx.edu

import numpy as np # type: ignore

def f(x, y):
    return 5*x**2 + 40*x + y**2 - 12*y + 127

def gradient(x, y):
    df_dx = 10*x + 40
    df_dy = 2*y - 12
    return np.array([df_dx, df_dy])

# Gradient Descent implementation
def gradient_descent(eta, steps, init_range, trials):
    best_result = None
    best_f_value = float('inf')
    
    for _ in range(trials):
        x, y = np.random.uniform(init_range[0], init_range[1], 2)
        for _ in range(steps):
            grad = gradient(x, y)
            x -= eta * grad[0]
            y -= eta * grad[1]
        
        current_f_value = f(x, y)
        if current_f_value < best_f_value:
            best_f_value = current_f_value
            best_result = (x, y)
    
    return best_result, best_f_value

# Parameters
etas = [0.1, 0.01, 0.001]
steps = 500
init_range = [-10, 10]
trials = 10

# Runs the experiments
results = []
for eta in etas:
    result, f_value = gradient_descent(eta, steps, init_range, trials)
    results.append((eta, result, f_value))
    print(f"Best result for eta={eta}: x={result[0]:.4f}, y={result[1]:.4f}, f(x,y)={f_value:.4f}")

