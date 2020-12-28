from random import random

from deap import base
from deap import creator
from deap import tools


def individual(icls, min_val, max_val):
    genome = list()
    genome.append(random.uniform(min_val, max_val))
    genome.append(random.uniform(min_val, max_val))
    return icls(genome)


def fitness(individual):
    return (1.5 - individual[0] + individual[0] * individual[1]) ** 2 + (
            2.25 - individual[0] + individual[0] * individual[1] ** 2) ** 2 + (
                   2.625 - individual[0] + individual[0] * individual[1] ** 3) ** 2


def user_input():
    min_max = '0'
    selection = '0'
    tournament_size = '0'
    crossing = '0'
    algorithm = '0'
    pop_size = '0'
    prob_mut = '0'
    prob_cross = '0'
    num_of_iter = '0'

    while prob_mut.isnumeric() is False or (0 >= float(prob_mut) or float(prob_mut) > 1):
        prob_mut = input('Prawdopodobieństwo mutacji, wybierz:\n')

    while prob_cross.isnumeric() is False or (0 >= float(prob_cross) or float(prob_cross) > 1):
        prob_cross = input('Prawdopodobieństwo krzyżowania, wybierz:\n')

    while num_of_iter.isnumeric() is False or (0 >= int(num_of_iter) or int(num_of_iter) > 1000):
        num_of_iter = input('Liczba iteracji, wybierz:\n')

    while min_max.isnumeric() is False or (0 >= int(min_max) or int(min_max) > 3):
        min_max = input('Wybierz:\n1. Minializacja \n2. Maksymalizacja \n')

    while selection.isnumeric() is False or (0 >= int(selection) or int(selection) > 9):
        selection = input('Selekcja, wybierz:\n1. Turniejowa \n2. Losowa \n3. Najlepszych \n4. Najgorszych \n5. '
                          'Ruletki\n6. Leksykazy\n7. Podwójna Turniejowa\n8. Leksykazy epsilon\n9. Stochastyczna '
                          'uniwersalna')

    if selection == 1:
        while num_of_iter.isnumeric() is False or (0 >= int(num_of_iter) or int(num_of_iter) > int(pop_size) / 2):
            tournament_size = input('Wielkość turnieju, wybierz:\n')

    while crossing.isnumeric() is False or (0 >= int(crossing) or int(crossing) > 6):
        crossing = input(
            'Krzyżowanie, wybierz:\n1. Dwupunktowe \n2. Jednopunktowe \n3. Jednorodne \n4. Częściowo dopasowane \n5. '
            'Uporządkowane\n6. Mieszane\n')

    while algorithm.isnumeric() is False or (0 >= int(algorithm) or int(algorithm) > 4):
        algorithm = input(
            'Mutacja, wybierz:\n1. Mutacja Gaussa \n2. Tasowanie indeksów\n3. Flip bit \n4. Polynomial bounded \n')

    return min_max, selection, tournament_size, crossing, algorithm, pop_size, prob_mut, prob_cross, num_of_iter


def genetics(min_max, min_val, max_val, selection, crossing, algorithm, pop_size, prob_mut, prob_cross, num_of_iter):
    if min_max == 1:
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    else:
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)
    toolbox = base.Toolbox()
    toolbox.register("individual", individual, creator.Individual, min_val=min_val, max_val=max_val)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", fitness)


def set_selection(toolbox, selection, k=0):
    if selection == 1:
        pass
    elif selection == 2:
        pass
    elif selection == 3:
        pass
    elif selection == 4:
        pass
    elif selection == 5:
        pass
    elif selection == 6:
        pass
    elif selection == 7:
        pass
    elif selection == 8:
        pass
    elif selection == 9:
        pass

    return toolbox


def set_crossing(toolbox, crossing):
    if crossing == 1:
        pass
    elif crossing == 2:
        pass
    elif crossing == 3:
        pass
    elif crossing == 4:
        pass
    elif crossing == 5:
        pass
    elif crossing == 6:
        pass

    return toolbox


def set_mutation(toolbox, mutation):
    if mutation == 1:
        pass
    elif mutation == 2:
        pass
    elif mutation == 3:
        pass
    elif mutation == 4:
        pass

    return toolbox


if __name__ == '__main__':
    min_max, selection, tournament_size, crossing, algorithm, pop_size, prob_mut, prob_cross, num_of_iter = user_input()
