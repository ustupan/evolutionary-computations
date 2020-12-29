
import random
from typing import List, Any

from deap import base
from deap import creator
from deap import tools
import matplotlib.pyplot as plt


def individual(icls, min_val, max_val):
    genome = list()
   # genome.append(random.uniform(min_val, max_val))
   # genome.append(random.uniform(min_val, max_val))
    genome = [random.uniform(min_val, max_val), random.uniform(min_val, max_val)]
    return icls(genome)


def fitness(individual):
    result = (1.5 - individual[0] + individual[0] * individual[1]) ** 2 + (
            2.25 - individual[0] + individual[0] * individual[1] ** 2) ** 2 + (
                   2.625 - individual[0] + individual[0] * individual[1] ** 3) ** 2
    return result,


def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def user_input():
    min_max = '0'
    selection = '0'
    tournament_size = '0'
    crossing = '0'
    indpb = '0'
    mu = '0'
    sigma = '0'
    mutation = '0'
    pop_size = '0'
    prob_mut = '0'
    prob_cross = '0'
    num_of_iter = '0'

    while is_float(prob_mut) is False or (0 >= float(prob_mut) or float(prob_mut) > 1):
        prob_mut = input('Prawdopodobieństwo mutacji, wybierz: ')

    while is_float(prob_cross) is False or (0 >= float(prob_cross) or float(prob_cross) > 1):
        prob_cross = input('Prawdopodobieństwo krzyżowania, wybierz: ')

    while num_of_iter.isnumeric() is False or (0 >= int(num_of_iter) or int(num_of_iter) > 1000):
        num_of_iter = input('Liczba iteracji, wybierz: ')

    while pop_size.isnumeric() is False or (0 >= int(pop_size) or int(pop_size) > 1000):
        pop_size = input('Wielkość populacji, wybierz: ')

    while min_max.isnumeric() is False or (0 >= int(min_max) or int(min_max) > 3):
        min_max = input('Wybierz:\n1. Minimalizacja \n2. Maksymalizacja \n')

    while selection.isnumeric() is False or (0 >= int(selection) or int(selection) > 8):
        selection = input('Selekcja, wybierz:\n1. Turniejowa \n2. Losowa \n3. Najlepszych \n4. Najgorszych \n5. '
                          'Ruletki\n6. Leksykazy\n7. Automatycznej Leksykazy epsilon\n8. Stochastyczne '
                          'uniwersalne próbkowanie\n')

    if int(selection) == 1:
        while tournament_size.isnumeric() is False or (
                0 >= int(tournament_size) or int(tournament_size) > int(pop_size) / 2):
            tournament_size = input('Wielkość turnieju, wybierz: ')

    while crossing.isnumeric() is False or (0 >= int(crossing) or int(crossing) > 5):
        crossing = input(
            'Krzyżowanie, wybierz:\n1. Dwupunktowe \n2. Jednopunktowe \n3. Jednorodne \n4. Częściowo dopasowane \n5. '
            'Uporządkowane\n6. Symulowanie binarne\n')

    while is_float(indpb) is False or (0 >= float(indpb) or float(indpb) > 1):
        indpb = input('Niezależne prawdopodobieństwo wymiany każdego atrybutu, wybierz: ')

    while mutation.isnumeric() is False or (0 >= int(mutation) or int(mutation) > 4):
        mutation = input(
            'Mutacja, wybierz:\n1. Mutacja Gaussa \n2. Tasowanie indeksów\n3. Flip bit \n4. Polynomial bounded \n')

    if int(mutation) == 1:
        while is_float(mu) is False or (0 >= float(mu) or float(mu) > 100):
            mu = input('Średnia, wybierz: ')
        while is_float(sigma) is False or (0 >= float(sigma) or float(sigma) > 100):
            sigma = input('Standardowe odchylenie, wybierz: ')

    return int(min_max), int(selection), int(tournament_size), int(crossing), float(indpb), int(mutation), int(
        pop_size), float(prob_mut), float(prob_cross), int(num_of_iter), float(sigma), float(mu)


def genetics(min_max, min_val, max_val, selection, k, crossing, indpb, mutation, pop_size, prob_mut, prob_cross,
             num_of_iter, mu, sigma):
    listMin = []
    listMax = []
    listMean = []
    listStd = []
    listBest = []

    if min_max == 1:
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)
    else:
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()

    toolbox.register("individual", individual, creator.Individual, min_val=min_val, max_val=max_val)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", fitness)

    toolbox = set_selection(toolbox, selection, 0.1)
    toolbox = set_crossing(toolbox, crossing, indpb)
    toolbox = set_mutation(toolbox, mutation, mu, sigma, indpb)

    sizePopulation = 100
    probabilityMutation = 0.2
    probabilityCrossover = 0.8
    numberIteration = 100

    pop = toolbox.population(n=sizePopulation)
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    g = 0
    numberElitism = 1
    while g < num_of_iter:
        g = g + 1

        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        listElitism = []
        for x in range(0, numberElitism):
            listElitism.append(tools.selBest(pop, 1)[0])
        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            # cross two individuals with probability CXPB
            if random.random() < prob_cross:
                toolbox.mate(child1, child2)
                # fitness values of the children
                # must be recalculated later
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            # mutate an individual with probability MUTPB
            if random.random() < prob_mut:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        print(" Evaluated %i individuals" % len(invalid_ind))
        pop[:] = offspring + listElitism
        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]
        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x * x for x in fits)
        std = abs(sum2 / length - mean ** 2) ** 0.5

        listMin.append(min(fits))
        listMax.append(max(fits))
        listMean.append(mean)
        listStd.append(std)
        best_ind = tools.selBest(pop, 1)[0]
        listBest.append(best_ind.fitness.values)

    return listMin, listMax, listMean, listStd, listBest


def set_selection(toolbox, selection, k):
    if selection == 1:
        toolbox.register("select", tools.selTournament, tournsize=k)
    elif selection == 2:
        toolbox.register("select", tools.selRandom)
    elif selection == 3:
        toolbox.register("select", tools.selBest)
    elif selection == 4:
        toolbox.register("select", tools.selWorst)
    elif selection == 5:
        toolbox.register("select", tools.selRoulette)
    elif selection == 6:
        toolbox.register("select", tools.selLexicase)
    elif selection == 7:
        toolbox.register("select", tools.selAutomaticEpsilonLexicase)
    elif selection == 8:
        toolbox.register("select", tools.selStochasticUniversalSampling)

    return toolbox


def set_crossing(toolbox, crossing, indpb):
    if crossing == 1:
        toolbox.register("mate", tools.cxTwoPoint)
    elif crossing == 2:
        toolbox.register("mate", tools.cxOnePoint)
    elif crossing == 3:
        indpb = float(indpb)
        toolbox.register("mate", tools.cxUniform, indpb=indpb)
    elif crossing == 4:
        toolbox.register("mate", tools.cxPartialyMatched)
    elif crossing == 5:
        toolbox.register("mate", tools.cxOrdered)

    return toolbox


def set_mutation(toolbox, mutation, mu, sigma, indpb):
    if mutation == 1:
        toolbox.register("mutate", tools.mutGaussian, mu=float(mu), sigma=float(sigma), indpb=float(indpb))
    elif mutation == 2:
        toolbox.register("mutate", tools.mutShuffleIndexes, indpb=float(indpb))
    elif mutation == 3:
        toolbox.register("mutate", tools.mutFlipBit, indpb=float(indpb))
    elif mutation == 4:
        toolbox.register("mutate", tools.mutPolynomialBounded, indpb=float(indpb))

    return toolbox


def savePlots(graphList, graphType):
    if graphType == 1:
        plt.plot(graphList, label="sredni osobnik")
        name = "srednia-osobnik"
    elif graphType == 2:
        plt.plot(graphList, label="Srednie odchylenie")
        name = "srednie-odchylenie-osobnik"
    elif graphType == 3:
        plt.plot(graphList, label="Max funkcji celu")
        name = "max-funkcji-celu"
    elif graphType == 4:
        plt.plot(graphList, label="Min funkcji celu")
        name = "min-funkcji-celu"
    else:
        plt.plot(graphList, label="najlepszy osobnik w danej populacji")
        name = "najlepszy-populacja-osobnik"

    leg = plt.legend(loc='best', ncol=2, mode="expand", shadow=True, fancybox=True)
    leg.get_frame().set_alpha(0.5)
    plt.savefig('saved/' + name + '.png', bbox_inches='tight')
    plt.close()


if __name__ == '__main__':
    min_max, selection, tournament_size, crossing, indpb, mutation, pop_size, prob_mut, prob_cross, num_of_iter, sigma, mu = user_input()
    listMin, listMax, listMean, listStd, listBest = genetics(min_max, -5, 5, selection, tournament_size, crossing,
                                                             indpb, mutation, pop_size, prob_mut, prob_cross,
                                                             num_of_iter, mu, sigma)

    savePlots(listMean, 1)
    savePlots(listStd, 2)
    savePlots(listMax, 3)
    savePlots(listMin, 4)
    savePlots(listBest, 5)
