import numpy as np


class Population:

    def count_bits_per_variables(self, max_value, min_value, step):
        bits_per_variables = int((max_value - min_value) / step).bit_length()
        new_step = (max_value - min_value) / (2 ** bits_per_variables - 1)
        return bits_per_variables, new_step

    def generate_population(self, population_size, num_of_variables, bits_per_variables):
        population = np.random.randint(2, size=(population_size, num_of_variables * bits_per_variables))
        return population

    def decode_individual(self, individual, num_of_variables, bits_per_variables, step, min_value):
        temp = individual.reshape((num_of_variables, bits_per_variables))
        decode_individual = np.ndarray(num_of_variables)
        vector = []
        for i in range(0, bits_per_variables):
            vector.insert(0, 2 ** i)

        for j in range(0, num_of_variables):
            decode_individual[j] = sum(np.multiply(vector, temp[j])) * step + min_value
        return decode_individual

    def evaluate_population(self, func, population, num_of_variables, bits_per_variables,):
        evaluated_pop = np.ndarray(int(population.size / (bits_per_variables * num_of_variables)))
        for i in range(int(population.size / (bits_per_variables * num_of_variables))):
            evaluated_pop.pop[i] = func(self.decode_individual(population[i], num_of_variables, bits_per_variables, ))