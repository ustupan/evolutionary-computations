import numpy as np


class Mutation:
    @staticmethod
    def point_mutation(pop, probability):
        new_pop = []
        for i in range(pop.shape[0]):
            new_pop.append(pop[i])
            random = np.random.random()
            if random < probability:
                random_locus = np.random.randint(pop.shape[1])
                if new_pop[i][random_locus] == 0:
                    new_pop[i][random_locus] = 1
                else:
                    new_pop[i][random_locus] = 0
        return new_pop

    @staticmethod
    def two_point_mutation(pop, probability):
        new_pop = []
        for i in range(pop.shape[0]):
            new_pop.append(pop[i])
            random = np.random.random()
            if random < probability:
                random_locus1 = np.random.randint(pop.shape[1])
                random_locus2 = np.random.randint(pop.shape[1])
                while random_locus1 == random_locus2:
                    random_locus2 = np.random.randint(pop.shape[1])
                if new_pop[i][random_locus1] == 0:
                    new_pop[i][random_locus1] = 1
                else:
                    new_pop[i][random_locus1] = 0
                if new_pop[i][random_locus2] == 0:
                    new_pop[i][random_locus2] = 1
                else:
                    new_pop[i][random_locus2] = 0
        return new_pop

    @staticmethod
    def edge_mutation(pop, probability):
        new_pop = []
        for i in range(pop.shape[0]):
            new_pop.append(pop[i])
            random = np.random.random()
            if random < probability:
                if pop[i][pop.shape[1] - 1] == 0:
                    new_pop[i][pop.shape[1] - 1] = 1
                else:
                    new_pop[i][pop.shape[1] - 1] = 0
        return new_pop
