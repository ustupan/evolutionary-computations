import numpy as np


class Real_Representation_Base:
    def __init__(self, function, population_size, num_of_variables, range_min, range_max, precision):
        self.function = function
        self.population_size = population_size
        self.num_of_variables = num_of_variables
        self.range_min = range_min
        self.range_max = range_max
        self.precision = precision

    def generate_population(self):
        return np.random.randint(low=self.range_min, high=self.range_max,
                                 size=(self.population_size, self.num_of_variables))

    def evaluate_population(self, population):
        evaluated_pop = np.ndarray(population.shape[0])
        for i in range(population.shape[0]):
            evaluated_pop[i] = self.function(population[i])
        return evaluated_pop

    def best_individual(self, population, evaluated_population, is_max=True):
        if is_max:
            return population[np.argmax(evaluated_population)]
        else:
            return population[np.argmin(evaluated_population)]

    def best_value(self, evaluated_population, is_max=True):
        if is_max:
            return max(evaluated_population)
        else:
            return min(evaluated_population)
