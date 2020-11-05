import numpy as np


class Inversion:

    @staticmethod
    def inversion(pop, probability):
        new_pop = []
        for i in range(pop.shape[0]):
            random = np.random.random()
            if random < probability:
                random_index1 = np.random.randint(pop.shape[1])
                random_index2 = np.random.randint(pop.shape[1])
                while random_index1 == random_index2:
                    random_index2 = np.random.randint(pop.shape[1])
                indexes = [random_index1, random_index2]
                indexes.sort()
                part_to_invert = pop[i][indexes[0]:indexes[1]]
                part_to_invert = [0 if x == 1 else 1 for x in part_to_invert]
                new_pop.append(np.concatenate((pop[i][:indexes[0]], part_to_invert, pop[i][indexes[1:]])))
            else:
                new_pop.append(pop[i])
        return new_pop
