import random

import pandas as pd
from deap import base
from deap import creator
from deap import tools

from SVC_classifier import SVCParametersFeatureFitness
from SVC_classifier import SVCParametersFeatures
from SVC_classifier import mutationSVC
from decision_tree_classifier import DecisionTreeClassifierFitness
from decision_tree_classifier import DecisionTreeParametersFeatures
from decision_tree_classifier import mutationDecisionTree
from radius_neighbors_classifier import RadiusNeighborsParametersFeatures
from radius_neighbors_classifier import RadiusNeighborsParametersFeatureFitness
from radius_neighbors_classifier import mutationRNeighbors
from k_neighbors_classifier import KNeighborsParametersFeatureFitness
from k_neighbors_classifier import KNeighborsParametersFeatures
from k_neighbors_classifier import mutationKNeighbors
from linear_svc_classifier import LinearSVCParametersFeatureFitness
from linear_svc_classifier import LinearSVCParametersFeatures
from linear_svc_classifier import mutationLinearSVC
from random_forest_classifier import RandomForestParametersFeatureFitness
from random_forest_classifier import RandomForestParametersFeatures
from random_forest_classifier import mutationRandomForest


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
    pop_size = '0'
    prob_mut = '0'
    prob_cross = '0'
    num_of_iter = '0'
    classifier = '0'

    while classifier.isnumeric() is False or (0 >= int(classifier) or int(classifier) > 6):
        classifier = input('Klasyfikator, wybierz:\n1. DecisionTree \n2. Radius Neighbors \n'
                           '3. KNeighbors \n4. LinearSVC \n'
                           '5. RandomForest\n6. SVC\n')

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

    while crossing.isnumeric() is False or (0 >= int(crossing) or int(crossing) > 3):
        crossing = input(
            'Krzyżowanie, wybierz:\n1. Dwupunktowe \n2. Jednopunktowe \n3. Jednorodne \n')

    while is_float(indpb) is False or (0 >= float(indpb) or float(indpb) > 1):
        indpb = input('Niezależne prawdopodobieństwo wymiany każdego atrybutu, wybierz: ')

    return int(selection), int(tournament_size), int(crossing), float(indpb), int(
        pop_size), float(prob_mut), float(prob_cross), int(num_of_iter), int(classifier)


def set_toolbox(toolbox, classifier, number_of_atributtes, df, y):
    if classifier == 1:
        toolbox.register("individual", DecisionTreeParametersFeatures, number_of_atributtes, creator.Individual)
        toolbox.register("evaluate", DecisionTreeClassifierFitness, y, df, number_of_atributtes)
        toolbox.register("mutate", mutationDecisionTree)

    elif classifier == 2:
        toolbox.register("individual", RadiusNeighborsParametersFeatures, number_of_atributtes, creator.Individual)
        toolbox.register("evaluate", RadiusNeighborsParametersFeatureFitness, y, df, number_of_atributtes)
        toolbox.register("mutate", mutationRNeighbors)

    elif classifier == 3:
        toolbox.register("individual", KNeighborsParametersFeatures, number_of_atributtes, creator.Individual)
        toolbox.register("evaluate", KNeighborsParametersFeatureFitness, y, df, number_of_atributtes)
        toolbox.register("mutate", mutationKNeighbors)

    elif classifier == 4:
        toolbox.register("individual", LinearSVCParametersFeatures, number_of_atributtes, creator.Individual)
        toolbox.register("evaluate", LinearSVCParametersFeatureFitness, y, df, number_of_atributtes)
        toolbox.register("mutate", mutationLinearSVC)

    elif classifier == 5:
        toolbox.register("individual", RandomForestParametersFeatures, number_of_atributtes, creator.Individual)
        toolbox.register("evaluate", RandomForestParametersFeatureFitness, y, df, number_of_atributtes)
        toolbox.register("mutate", mutationRandomForest)

    elif classifier == 6:
        toolbox.register("individual", SVCParametersFeatures, number_of_atributtes, creator.Individual)
        toolbox.register("evaluate", SVCParametersFeatureFitness, y, df, number_of_atributtes)
        toolbox.register("mutate", mutationSVC)

    return toolbox


def genetics(selection, k, crossing, indpb, pop_size, prob_mut, prob_cross,
             num_of_iter, classifier, number_of_atributtes, df, y):
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    toolbox = set_toolbox(toolbox, classifier, number_of_atributtes, df, y)
    toolbox = set_selection(toolbox, selection, k)
    toolbox = set_crossing(toolbox, crossing, indpb)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    pop = toolbox.population(n=pop_size)
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

        print("Generation " + str(g))
        print(" Min %s" % min(fits))
        print(" Max %s" % max(fits))
        print(" Avg %s" % mean)
        print(" Std %s" % std)
        best_ind = tools.selBest(pop, 1)[0]
        print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))

    print("-- End of (successful) evolution --")


def set_selection(toolbox, selection, k):
    if selection == 1:
        toolbox.register("select", tools.selTournament, tournsize=int(k))
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
    return toolbox


if __name__ == '__main__':
    df = pd.read_csv('ReplicatedAcousticFeatures-ParkinsonDatabase.csv')
    y = df['Status']
    df.drop('Status', axis=1, inplace=True)
    df.drop('ID', axis=1, inplace=True)
    df.drop('Recording', axis=1, inplace=True)
    number_of_atributtes = len(df.columns)

    selection, tournament_size, crossing, indpb, pop_size, prob_mut, prob_cross, num_of_iter, classifier = user_input()
    genetics(selection, tournament_size, crossing,
             indpb, pop_size, prob_mut, prob_cross,
             num_of_iter, classifier, number_of_atributtes, df, y)

    '''
    
    Do testow zeby nie wpisywac
    selection = 5
    crossing = 1
    indpb = 0.5
    pop_size = 10
    prob_mut = 0.2
    prob_cross = 0.8
    num_of_iter = 10
    classifier = 1

    '''
