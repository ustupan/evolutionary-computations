import numpy as np

from Algorithm.beale_function import Function


class Base:
    def __init__(self, population_size, num_of_variables, range_min, range_max, precision):
        self.function = Function.bale_function()
        self.population_size = population_size
        self.num_of_variables = num_of_variables
        self.range_min = range_min
        self.range_max = range_max
        self.precision = precision
        self.num_of_bits = self.get_num_of_bits()
        self.new_step = self.new_step()
        self.population = self.generate_population()

    def get_num_of_bits(self):
        return int((self.range_max - self.range_min) / self.precision).bit_length()

    def new_step(self):
        return (self.range_max - self.range_min) / (2 ** self.num_of_bits - 1)

    def generate_population(self):
        return np.randint(2, size=(self.population_size, self.num_of_variables * self.num_of_bits))

    def decode_individual(self, individual):
        temp = individual.reshape((self.num_of_variables, self.num_of_bits))
        decode_individual = np.ndarray(self.num_of_variables)
        vector = []
        for i in range(0, self.num_of_bits):
            vector.insert(0, 2 ** i)

        for j in range(0, self.num_of_variables):
            decode_individual[j] = sum(np.multiply(vector, temp[j])) * self.new_step + self.range_min
        return decode_individual

    def evaluate_population(self, population, amount_variables, amount_of_bits, a, step):
        evaluated_pop = np.ndarray(int(population.size / (amount_of_bits * amount_variables)))
        for i in range(int(population.size / (amount_of_bits * amount_variables))):
            evaluated_pop[i] = self.function(self.decode_individual(population[i]))
        return evaluated_pop

    def best_individual(self, evaluated_population):
        return self.population[np.argmax(evaluated_population)]

    def best_value(self, evaluated_population):
        return max(evaluated_population)
