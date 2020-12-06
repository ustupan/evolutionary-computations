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
        return np.array(new_pop)

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
        return np.array(new_pop)

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
        return np.array(new_pop)

    @staticmethod
    def even_mutation(pop, probability, min_val, max_val):
        new_pop = np.array(pop, copy=True)
        for i in range(pop.shape[0]):
            rnd = np.random.rand()
            if rnd < probability:
                index = np.random.choice([0, 1])
                new_val = np.random.randint(low=min_val, high=max_val)
                new_pop[i][index] = new_val
        return new_pop