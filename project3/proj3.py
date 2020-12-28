from random import random

from deap import base
from deap import creator
from deap import tools


def individual(icls, min_val, max_val):
    genome = list()
    genome.append(random.uniform(min_val, max_val))
    genome.append(random.uniform(min_val, max_val))
    return icls(genome)


def fitness_function(individual):
    return (1.5 - individual[0] + individual[0] * individual[1]) ** 2 + (
            2.25 - individual[0] + individual[0] * individual[1] ** 2) ** 2 + (
                   2.625 - individual[0] + individual[0] * individual[1] ** 3) ** 2

def user_input():
    min_max = '0'
    selection = '0'
    crossing = '0'
    algorithm = '0'
    pop_size = '0'
    prob_mut = '0'
    prob_cross = '0'
    num_of_iter = '0'

    while min_max.isnumeric() is False or (0 >= int(min_max) or int(min_max) > 3):
        min_max = input('Wybierz:\n1. Maksymalizacja \n2. Minializacja \n')

    while selection.isnumeric() is False or (0 >= int(selection) or int(selection) > 9):
        selection = input('Selekcja, wybierz:\n1. Turniejowa \n2. Losowa \n3. Najlepszych \n4. Najgorszych \n5. '
                          'Ruletki\n6. Leksykazy\n7. Podwójna Turniejowa\n8. Leksykazy epsilon\n9. Stochastyczna '
                          'uniwersalna')
    while crossing.isnumeric() is False or (0 >= int(crossing) or int(crossing) > 6):
        crossing = input(
            'Krzyżowanie, wybierz:\n1. Dwupunktowe \n2. Jednopunktowe \n3. Jednorodne \n4. Częściowo dopasowane \n5. '
            'Uporządkowane\n6. Mieszane\n')

    while algorithm.isnumeric() is False or (0 >= int(algorithm) or int(algorithm) > 4):
        algorithm = input(
            'Mutacja, wybierz:\n1. Mutacja Gaussa \n2. Tasowanie indeksów\n3. Flip bit \n4. Polynomial bounded \n')

    while prob_mut.isnumeric() is False or (0 >= float(prob_mut) or float(prob_mut) > 1):
        prob_mut = input('Prawdopodobieństwo mutacji, wybierz:\n')

    while prob_cross.isnumeric() is False or (0 >= float(prob_cross) or float(prob_cross) > 1):
        prob_cross = input('Prawdopodobieństwo krzyżowania, wybierz:\n')

    while num_of_iter.isnumeric() is False or (0 >= int(num_of_iter) or int(num_of_iter) > 1000):
        num_of_iter = input('Liczba iteracji, wybierz:\n')

    return min_max, selection, crossing, algorithm, pop_size, prob_mut, prob_cross, num_of_iter


if __name__ == '__main__':
    min_max, selection, crossing, algorithm, pop_size, prob_mut, prob_cross, num_of_iter = user_input()


