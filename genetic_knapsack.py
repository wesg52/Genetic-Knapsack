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


def initialize(population_size):
    #Items are (weight value)
    #items = [item(3,4), item(5,6), item(7,2), item(3,5), item(1,9), item(7,1), item(1,3), item(8,2), item(2,4), item(1,2), item(2,2)]
    items = pickle.load(open('items.p', 'rb'))
    #for i in range(0, 100):
        #items.append(item(random.randint(0,10), random.randint(0,9)))
    #pickle.dump(items, open('items.p', 'wb'))
    knapsack = knapSack(100, items)
    chromLen = len(items)
    population = []
    for i in range(0, population_size):
        sol = []
        for i in range(0, chromLen):
            sol.append(random.randint(0,1))
        population.append(chromosome(sol))
    for i in population:
        i.getFitness(items, knapsack)
    return population, items, knapsack

def selectParents(roulette_wheel):
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
    totalFitness = 0
    for chrm in population:
        totalFitness += chrm.fitness
    sorted(population, key= lambda chrm: chrm.fitness, reverse=True)
    roulette_wheel = [(population[0].fitness/totalFitness, population[0])]
    for chrm in population[1:]:
        roulette_wheel.append((roulette_wheel[-1][0] + chrm.fitness/totalFitness, chrm))
    new_population = population[:2]
    while len(new_population) != len(population):
        parent1, parent2 = selectParents(roulette_wheel)
        crossover_point = random.randint(1, len(items) - 2)
        solution1 = parent1.solution[:crossover_point] + parent2.solution[crossover_point:]
        solution2 = parent2.solution[:crossover_point] + parent1.solution[crossover_point:]
        new_population.append(chromosome(solution1))
        new_population.append(chromosome(solution2))
    for chrm in new_population:
        for bit in range(0,len(chrm.solution)):
            mutate = random.random()
            if mutate < .0005:
                chrm.solution[bit] = (chrm.solution[bit]+1)%2
    for chrm in new_population:
        chrm.getFitness(items, knapsack)
    return new_population

def solve(pop_size, iterations):

    population, items, knapsack = initialize(pop_size)
    num_iter = 0
    while num_iter < iterations:
        new_population = evolve(population, items, knapsack)
        new_population = sorted(new_population, key=lambda chrm: chrm.fitness, reverse=True)

        print('Best Solution:   ', new_population[0].solution, '\nValue:  ', new_population[0].fitness)
        population = new_population
        num_iter += 1

if __name__ == '__main__':
    solve(500, 100)