import random
import pickle

class item():
    def __init__(self, w, v):
        self.weight = w
        self.value = v

class knapSack():
    def __init__(self, cap, itemList):
        self.capacity = cap
        self.items = itemList

class chromosome():
    def __init__(self, sol):
        self.solution = sol
        self.fitness = 0

    def getFitness(self, items, knapsack):
        """Return the fitness of a solution, if not feasible, randomly flip ones until feasible"""
        totalFitness = 0
        totalWeight = 0
        for bit, item in zip(self.solution, items):
            if bit == 1:
                totalFitness += item.value
                totalWeight += item.weight
        while totalWeight > knapsack.capacity:
            onesList = []
            for i in range(0, len(self.solution)):
                if self.solution[i] == 1:
                    onesList.append(i)
            sel = random.choice(onesList)
            self.solution[sel] -= 1
            totalFitness -= items[sel].value
            totalWeight -= items[sel].weight
        self.fitness = totalFitness

def consoleInput():
    """User input to determine Items, Knapsack and algorithm parameters"""
    items = []
    knapsack = None
    print('Genetic Algorithms for Knapsack')
    print('Please choose a method for item input:')
    mode = input('Type u for user input, r for random input, and p for pickled input: ')
    if mode == 'u':
        while 2 == 2:
            status = input('Type n to add new item, k to make the knapsack, s to save to the item pickle file: ')
            if status == 'n':
                weight = int(input('Weight for this item: '))
                value = int(input('Value for this item: '))
                items.append(item(weight,value))
            elif status == 'p':
                pickle.dump(items, open('items.p', 'wb'))
            elif status == 'k':
                break
            else:
                'Not a valid input'
    elif mode == 'r':
        num = int(input('How many items should be available: '))
        for i in range(0, num):
            items.append(item(random.randint(0,10), random.randint(0,10)))
        save = input('Type y/n to save random item list to pickle file: ')
        if save == 'y':
            pickle.dump(items, open('items.p', 'wb'))
    elif mode == 'p':
        items = pickle.load(open('items.p', 'rb'))
    else:
        print('Not a valid input')
    cap = int(input('Capacity of the Knapsack: '))
    knapsack = knapSack(cap, items)
    print('#####Algorithm Parameters#####')
    pop_size = int(input('Enter the chromosome population size: '))
    iterations = int(input('Enter the number of iterations: '))
    return items, knapsack, pop_size, iterations


def initialize(population_size, items, knapsack):
    """Initialize the population with random solutions."""
    chromLen = len(items)
    population = []
    for i in range(0, population_size):
        sol = []
        for i in range(0, chromLen):
            sol.append(random.randint(0,1))
        population.append(chromosome(sol))
    for i in population:
        i.getFitness(items, knapsack)
    return population

def selectParents(roulette_wheel):
    """Select two parents based on the probability distribution corresponding to the roulette wheel."""
    sel1 = random.random()
    sel2 = random.random()
    parent1 = None
    parent2 = None
    for chance in roulette_wheel:
        if sel1 < chance[0]:
            parent1 = chance[1]
            break
    for chance in roulette_wheel:
        if sel2 < chance[0]:
            parent2 = chance[1]
            break
    return parent1, parent2


def evolve(population, items, knapsack):
    """Create a new population of solutions based on the fitness of the previous generation."""
    #Step 1: Selection
    totalFitness = 0
    for chrm in population:
        totalFitness += chrm.fitness
    sorted(population, key= lambda chrm: chrm.fitness, reverse=True)
    roulette_wheel = [(population[0].fitness/totalFitness, population[0])]
    for chrm in population[1:]:
        roulette_wheel.append((roulette_wheel[-1][0] + chrm.fitness/totalFitness, chrm))
    #Elitism to retain best solutions
    new_population = population[:2]
    #Step 2: Crossover
    while len(new_population) != len(population):
        parent1, parent2 = selectParents(roulette_wheel)
        crossover_point = random.randint(1, len(items) - 2)
        solution1 = parent1.solution[:crossover_point] + parent2.solution[crossover_point:]
        solution2 = parent2.solution[:crossover_point] + parent1.solution[crossover_point:]
        new_population.append(chromosome(solution1))
        new_population.append(chromosome(solution2))
    #Step 3: Mutation
    for chrm in new_population:
        for bit in range(0,len(chrm.solution)):
            mutate = random.random()
            if mutate < .0005:
                chrm.solution[bit] = (chrm.solution[bit]+1)%2
    for chrm in new_population:
        chrm.getFitness(items, knapsack)
    return new_population

def solve():
    """Main method for running the program."""
    items, knapsack, pop_size, iterations = consoleInput()
    population = initialize(pop_size, items, knapsack)
    num_iter = 0
    while num_iter < iterations:
        new_population = evolve(population, items, knapsack)
        new_population = sorted(new_population, key=lambda chrm: chrm.fitness, reverse=True)
        print('Best Solution:   ', new_population[0].solution, '\nValue:  ', new_population[0].fitness)
        population = new_population
        num_iter += 1

if __name__ == '__main__':
    solve()