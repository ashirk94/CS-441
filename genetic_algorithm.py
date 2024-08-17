# Programming Assignment 2, 8-Queens Problem
# Alan Shirk, alans@pdx.edu

import random

# Generates a population of random solutions
def generate_population(size):
    return [random.sample(range(8), 8) for _ in range(size)]

# Calculates the fitness of a chromosome
def fitness(chromosome):
    attacks = 0
    n = len(chromosome)
    for i in range(n):
        for j in range(i + 1, n):
            if chromosome[i] == chromosome[j] or abs(chromosome[i] - chromosome[j]) == abs(i - j):
                attacks += 1
    return 28 - attacks  # 28 is the maximum number of non-attacking pairs

# Selects parents based on their fitness
def select_parents(population):
    fitnesses = [fitness(chrom) for chrom in population]
    total_fitness = sum(fitnesses)
    selection_probs = [f / total_fitness for f in fitnesses]
    parents = random.choices(population, weights=selection_probs, k=2)
    return parents

# Performs crossover between two parents to produce two children
def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

# Mutates a chromosome based on the mutation probability
def mutate(chromosome, MutationPct):
    if random.random() < MutationPct:
        idx = random.randint(0, len(chromosome) - 1)
        chromosome[idx] = random.randint(0, len(chromosome) - 1)
    return chromosome

# Main genetic algorithm function
def genetic_algorithm(PopulationSize, NumIterations, MutationPct):
    population = generate_population(PopulationSize)
    best_fitness_over_time = []
    avg_fitness_over_time = []
    sampled_individuals = {}

    for generation in range(NumIterations):
        fitnesses = [fitness(chrom) for chrom in population]
        best_fitness = max(fitnesses)
        avg_fitness = sum(fitnesses) / PopulationSize
        
        best_fitness_over_time.append(best_fitness)
        avg_fitness_over_time.append(avg_fitness)
        
        if generation in [10, 50, 100, 200]:  # Sample individuals at specific generations
            sampled_individuals[generation] = random.choice(population)
        
        new_population = []
        for _ in range(PopulationSize // 2):
            parent1, parent2 = select_parents(population)
            child1, child2 = crossover(parent1, parent2)
            new_population.append(mutate(child1, MutationPct))
            new_population.append(mutate(child2, MutationPct))
        
        population = new_population
        
        if best_fitness == 28:  # Solution found
            sampled_individuals[generation] = random.choice(population)
            break

    best_solution = max(population, key=fitness)
    return best_solution, fitness(best_solution), sampled_individuals

# Parameters
PopulationSize = 100
NumIterations = 10000
MutationPct = 0.1

solution, solution_fitness, sampled_individuals = genetic_algorithm(PopulationSize, NumIterations, MutationPct)

print(f"Best solution: {solution} with fitness: {solution_fitness}")
for gen, individual in sampled_individuals.items():
    print(f"\nGeneration {gen}: {individual}")
