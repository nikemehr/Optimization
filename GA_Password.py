# I want to find the given password by using the genetic algorithm. let's assume the password consists of a
# combination of uppercase letters, lowercase letters, digits, and special characters.
# The length of the password is also unknown, however we know the minimum and maximum length of the password.

import random
import string

# Constants
TARGET_STRING = '4t9eEGuiX'
POPULATION_SIZE = 100
MUTATION_RATE = 0.01
GENERATIONS = 1000
min_len = 5
max_len = 10


# Creating a random string with a random length
full_string = string.ascii_letters +string.digits + string.punctuation
def create_random_string(min_length, max_length):
    length = random.randint(min_length, max_length)
    return ''.join(random.choice(full_string) for _ in range(length))


# calculating the fitness of a string (number of matching characters)
def calculate_fitness(candidate):
    return sum(1 for a, b in zip(candidate, TARGET_STRING) if a == b)


# Initializing the population with random strings
population = [create_random_string(min_len, max_len) for _ in range(POPULATION_SIZE)]

# Genetic Algorithm
for generation in range(GENERATIONS):
    # Evaluating fitness for each individual in the population
    fitness_scores = [calculate_fitness(individual) for individual in population]

    # Checking if we have found the target string
    if TARGET_STRING in population:
        print(f"Target string '{TARGET_STRING}' found in generation {generation}")
        break

    # Selecting parents based on fitness
    total_fitness = sum(fitness_scores)
    if total_fitness == 0:
        # Prevent division by zero if all fitness scores are zero
        probabilities = [1 / POPULATION_SIZE for _ in range(POPULATION_SIZE)]
    else:
        probabilities = [score / total_fitness for score in fitness_scores]

    parents = random.choices(population, probabilities, k=POPULATION_SIZE)

    # Creating new population through crossover
    new_population = []
    for i in range(0, POPULATION_SIZE, 2):
        parent1 = parents[i]
        parent2 = parents[i + 1]
        crossover_point1 = random.randint(0, len(parent1) - 1)
        crossover_point2 = random.randint(0, len(parent2) - 1)
        offspring1 = parent1[:crossover_point1] + parent2[crossover_point2:]
        offspring2 = parent2[:crossover_point2] + parent1[crossover_point1:]
        new_population.extend([offspring1, offspring2])

    # Applying mutation
    for i in range(POPULATION_SIZE):
        if random.random() < MUTATION_RATE:
            mutation_point = random.randint(0, len(new_population[i]) - 1)
            new_population[i] = (
                    new_population[i][:mutation_point] +
                    random.choice(full_string) +
                    new_population[i][mutation_point + 1:]
            )

    # Replacing old population with new population
    population = new_population

else:
    print(f"Target string '{TARGET_STRING}' not found within {GENERATIONS} generations.")
