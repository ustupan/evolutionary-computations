import numpy as np
from project1.Algorithm.base import *
from project1.Helpers.enums import *
from project1.Algorithm.selection import *
from project1.Algorithm.mutation import *
from project1.Algorithm.crossing import *
from project1.Algorithm.inversion import *
from project1.Algorithm.elite_strategy import *
from project1.Algorithm.beale_function import *


class GeneticAlgorithm:
    def __init__(self, func, num_of_epochs, population_size, num_of_variables, range_min,
                 range_max, precision, selection_type, mutation_type, crossing_type, is_max,
                 selection_prob, mutation_prob, crossing_prob, inversion_prob, tournament_size=0,
                 selection_percent=0, elite_strategy_percent=0, elite_strategy_num=0):
        self.func = func
        self.num_of_epochs = num_of_epochs
        self.population_size = population_size
        self.num_of_variables = num_of_variables
        self.range_min = range_min
        self.range_max = range_max
        self.precision = precision
        self.selection_type = selection_type
        self.mutation_type = mutation_type
        self.crossing_type = crossing_type
        self.is_max = is_max
        self.selection_prob = selection_prob
        self.mutation_prob = mutation_prob
        self.crossing_prob = crossing_prob
        self.inversion_prob = inversion_prob
        self.tournament_size = tournament_size
        self.selection_percent = selection_percent
        self.elite_strategy_percent = elite_strategy_percent
        self.elite_strategy_num = elite_strategy_num

    def run_algorithm(self):

        base = Base(self.func, self.population_size, self.num_of_variables, self.range_min,
                    self.range_max, self.precision)
        pop = base.generate_population()
        evaluated_pop = base.evaluate_population(pop)
        best_solution_in_epochs = []
        solution_mean = [(sum(evaluated_pop) / self.population_size)]
        solution_std = [(sum(evaluated_pop) / self.population_size)]
        for epoch in range(self.num_of_epochs):
            evaluated_pop = base.evaluate_population(pop)
            best, best_val = self.elite_strategy(pop, evaluated_pop)
            selection_pop, _, not_selected_pop = self.selection(pop, evaluated_pop)
            crossed_pop = self.crossing(selection_pop)
            pop = np.concatenate((crossed_pop, not_selected_pop), axis=0)
            pop = self.mutation(pop)
            pop = self.inversion(pop)
            evaluated_pop = base.evaluate_population(pop)

            indexes_to_delete = set()
            while len(indexes_to_delete) != best.shape[0]:
                indexes_to_delete.add(np.random.randint(1, pop.shape[1] - 1))
            indexes_to_delete = list(indexes_to_delete)
            pop = np.delete(pop, indexes_to_delete, axis=0)
            evaluated_pop = np.delete(evaluated_pop, indexes_to_delete, axis=0)
            pop = np.append(pop, best, axis=0)
            evaluated_pop = np.append(evaluated_pop, best_val, axis=0)

            best_solution_in_epochs.append(base.best_value(evaluated_pop, self.is_max))
            solution_mean.append((sum(evaluated_pop) / evaluated_pop.shape[0]))
            solution_std.append(np.std(evaluated_pop))
        return best_solution_in_epochs, solution_mean, solution_std

    def selection(self, pop, evaluated_pop):
        if self.selection_type == SelectionType.BEST:
            return Selection.best(pop, evaluated_pop, self.selection_percent, self.is_max)
        elif self.selection_type == SelectionType.ROULETTE:
            return Selection.roulette(pop, evaluated_pop, self.selection_percent, self.is_max)
        elif self.selection_type == SelectionType.TOURNAMENT:
            return Selection.tournament(pop, evaluated_pop, self.tournament_size, self.is_max)

    def mutation(self, pop):
        if self.mutation_type == MutationType.SINGLE_POINT:
            return Mutation.point_mutation(pop, self.mutation_prob)
        elif self.mutation_type == MutationType.DOUBLE_POINT:
            return Mutation.two_point_mutation(pop, self.mutation_prob)
        elif self.mutation_type == MutationType.EDGE:
            return Mutation.edge_mutation(pop, self.mutation_prob)

    def crossing(self, pop):
        if self.crossing_type == CrossingType.SINGLE_POINT:
            return Crossing.point_crossing(pop, self.crossing_prob)
        elif self.crossing_type == CrossingType.DOUBLE_POINT:
            return Crossing.two_point_crossing(pop, self.crossing_prob)
        elif self.crossing_type == CrossingType.TRIPLE_POINT:
            return Crossing.three_point_crossing(pop, self.crossing_prob)
        elif self.crossing_type == CrossingType.HOMOGENEOUS:
            return Crossing.homogeneous_crossing(pop, self.crossing_prob)

    def inversion(self, pop):
        return Inversion.inversion(pop, self.inversion_prob)

    def elite_strategy(self, pop, evaluated_pop):
        return EliteStrategy.elite_strategy(pop, evaluated_pop,
                                            self.elite_strategy_percent,
                                            self.elite_strategy_num, self.is_max)


#lol = GeneticAlgorithm(bale_function, int(50), int(100), int(2), int(-5), int(5), float(0.0001),
                      # SelectionType.ROULETTE,
                      # MutationType.SINGLE_POINT, CrossingType.SINGLE_POINT,
                      # False, float(0.9), float(0.10), float(0.8), float(0.1), int(3), int(80), int(10), int(0))


