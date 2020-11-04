import numpy as np


class Crossing:
    @staticmethod
    def point_crossing(pop, probability):
        new_pop = []
        for i in range(0, (pop.shape[0] // 2) + 1, 2):
            rnd = np.random.random()
            if rnd < probability:
                pivot = np.random.randint(1, pop.shape[1] - 1)
                new_pop.append(np.concatenate((pop[i][:pivot], pop[i + 1][pivot:])))
                new_pop.append(np.concatenate((pop[i + 1][:pivot], pop[i][pivot:])))
            else:
                new_pop.append(pop[i])
                new_pop.append(pop[i+1])
        return new_pop

    @staticmethod
    def two_point_crossing(pop, probability):
        new_pop = []
        for i in range(0, (pop.shape[0] // 2) + 1, 2):
            rnd = np.random.random()
            if rnd < probability:
                pivot1 = np.random.randint(1, pop.shape[1] - 1)
                pivot2 = np.random.randint(1, pop.shape[1] - 1)
                while pivot1 == pivot2:
                    pivot2 = np.random.randint(1, pop.shape[1] - 1)
                pivots = [pivot1, pivot2]
                pivots.sort()
                new_pop.append(
                    np.concatenate((pop[i][:pivots[0]], pop[i + 1][pivots[0]:pivots[1]], pop[i][pivots[1]:])))
                new_pop.append(
                    np.concatenate((pop[i + 1][:pivots[0]], pop[i][pivots[0]:pivots[1]], pop[i][pivots[1]:])))
            else:
                new_pop.append(pop[i])
                new_pop.append(pop[i+1])
        return new_pop

    @staticmethod
    def three_point_crossing(pop, probability):
        new_pop = []
        for i in range(0, (pop.shape[0] // 2) + 1, 2):
            rnd = np.random.random()
            if rnd < probability:
                pivots = set()
                while len(pivots) != 3:
                    pivots.add(np.random.randint(1, pop.shape[1] - 1))
                pivots = list(pivots)
                pivots.sort()
                new_pop.append(np.concatenate((pop[i][:pivots[0]], pop[i + 1][pivots[0]:pivots[1]],
                                               pop[i][pivots[1]:pivots[2]], pop[i + 1][pivots[2]:])))
                new_pop.append(np.concatenate((pop[i + 1][:pivots[0]], pop[i][pivots[0]:pivots[1]],
                                               pop[i + 1][pivots[1]:pivots[2]], pop[i][pivots[2]:])))
            else:
                new_pop.append(pop[i])
                new_pop.append(pop[i+1])
        return new_pop

    @staticmethod
    def homogeneous_crossing(pop, probability):
        new_pop = []
        for i in range(0, (pop.shape[0] // 2) + 1, 2):
            rnd = np.random.random()
            ch1 = []
            ch2 = []
            if rnd < probability:
                for j in range(pop.shape[1]):
                    coin_flip = np.random.random()
                    if coin_flip > 0.5:
                        ch1.append(pop[i][j])
                        ch2.append(pop[i + 1][j])
                    else:
                        ch1.append(pop[i + 1][j])
                        ch2.append(pop[i][j])
                new_pop.append(ch1, ch2)
            else:
                new_pop.append(pop[i])
                new_pop.append(pop[i+1])
        return new_pop
