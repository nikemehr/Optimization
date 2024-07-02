import numpy as np
import random

num_cities = 100

# We populate cities by generating random x and y coordinates.
def population_distance_matrix(num_cities):
    coords = np.random.rand(num_cities, 2) * 100
    distance_matrix = np.zeros((num_cities, num_cities))

    for i in range(num_cities):
        for j in range(i + 1, num_cities):
            distance = np.linalg.norm(coords[i] - coords[j])
            distance_matrix[i][j] = distance_matrix[j][i] = distance

# To make sure that it satisfies the triangle inequality
    def check_triangle_inequality(matrix):
        n = matrix.shape[0]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if matrix[i, j] + matrix[j, k] < matrix[i, k]:
                        return False, (i, j, k)
        return True, None

    satisfies_triangle_inequality, indices = check_triangle_inequality(distance_matrix)

    if satisfies_triangle_inequality:
        return distance_matrix
    else:
        return population_distance_matrix(num_cities)

distance_matrix = population_distance_matrix(num_cities)

def create_random_route():
    route = list(range(num_cities))
    random.shuffle(route)
    return route

def calculate_route_length(route, distance_matrix):
    return sum(distance_matrix[route[i], route[(i + 1) % num_cities]] for i in range(num_cities))

def fitness(route, distance_matrix):
    return 1 / calculate_route_length(route, distance_matrix)

population_size = 10
generations = 100
mutation_rate = 0.1

population = [create_random_route() for _ in range(population_size)]
fitness_scores = [fitness(route, distance_matrix) for route in population]

fitness_scores = [score if score > 0 else 1e-6 for score in fitness_scores]
total_fitness = sum(fitness_scores)

for generation in range(generations):

    selection_probs = [f / total_fitness for f in fitness_scores]
    #print(f"Generation {generation} selection probabilities: {selection_probs}")
    selected_indices = np.random.choice(range(population_size), size=population_size, replace=True, p=selection_probs)
    #print(f"Generation {generation} selected indices: {selected_indices}")
    #assert all(0 <= i < population_size for i in selected_indices), "Selected indices out of range"
    mating_pool = [population[i] for i in selected_indices]

    new_population = []
    for i in range(0, population_size - 1, 2):
        parent1, parent2 = mating_pool[i], mating_pool[i + 1]
        cross_pt = random.randint(0, num_cities - 1)
        child = parent1[:cross_pt] + [x for x in parent2 if x not in parent1[:cross_pt]]
        new_population.append(child)
    if population_size % 2 == 1:
        new_population.append(mating_pool[-1])

    # Ensure new_population has the correct size
    while len(new_population) < population_size:
        new_population.append(create_random_route())
    #new_population = new_population[:population_size]

    for route in new_population:
        if random.random() < mutation_rate:
            swap_idx1, swap_idx2 = random.sample(range(num_cities), 2)
            route[swap_idx1], route[swap_idx2] = route[swap_idx2], route[swap_idx1]

    population = new_population
    fitness_scores = [fitness(route, distance_matrix) for route in population]
    #fitness_scores = [score if score > 0 else 1e-6 for score in fitness_scores]
    total_fitness = sum(fitness_scores)

    if generation == generations - 1:
        best_route_index = np.argmax(fitness_scores)
        best_route = population[best_route_index]
        print("Best route:", best_route)
        print("Minimum distance:", calculate_route_length(best_route, distance_matrix))
