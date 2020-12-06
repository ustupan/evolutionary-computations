import numpy as np


class Crossing:
    @staticmethod
    def point_crossing(pop, probability):
        new_pop = []
        for i in range(0, pop.shape[0], 2):
            if i == pop.shape[0] - 1:
                new_pop.append(pop[i])
                break
            rnd = np.random.random()
            if rnd < probability:
                pivot = np.random.randint(1, pop.shape[1] - 1)
                new_pop.append(np.concatenate((pop[i][:pivot], pop[i + 1][pivot:])))
                new_pop.append(np.concatenate((pop[i + 1][:pivot], pop[i][pivot:])))
            else:
                new_pop.append(pop[i])
                new_pop.append(pop[i + 1])
        return np.array(new_pop)

    @staticmethod
    def two_point_crossing(pop, probability):
        new_pop = []
        for i in range(0, pop.shape[0], 2):
            if i == pop.shape[0] - 1:
                new_pop.append(pop[i])
                break
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
                new_pop.append(pop[i + 1])
        return np.array(new_pop)

    @staticmethod
    def three_point_crossing(pop, probability):
        new_pop = []
        for i in range(0, pop.shape[0], 2):
            if i == pop.shape[0] - 1:
                new_pop.append(pop[i])
                break
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
                new_pop.append(pop[i + 1])
        return np.array(new_pop)

    @staticmethod
    def homogeneous_crossing(pop, probability):
        new_pop = []
        for i in range(0, pop.shape[0], 2):
            if i == pop.shape[0] - 1:
                new_pop.append(pop[i])
                break
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
                new_pop.append(ch1)
                new_pop.append(ch2)
            else:
                new_pop.append(pop[i])
                new_pop.append(pop[i + 1])
        return np.array(new_pop)

    @staticmethod
    def arithmetic_crossing(pop, probability):
        new_pop = []
        counter = 0
        k = np.random.random()

        while counter < pop.shape[0]:
            rnd = np.random.random()
            first = pop[np.random.randint(0, pop.shape[0] - 1)]
            second = pop[np.random.randint(0, pop.shape[0] - 1)]
            if rnd < probability:
                x1 = k * first[0] + (1 - k) * second[0]
                y1 = k * first[1] + (1 - k) * second[1]
                x2 = (1 - k) * first[0] + k * second[0]
                y2 = (1 - k) * first[1] + k * second[1]
                new_pop.append([x1, y1])
                new_pop.append([x2, y2])
            else:
                new_pop.append(first)
                new_pop.append(second)
            counter += 2
        new_pop = np.array(new_pop)
        if new_pop.shape[0] > pop.shape[0]:
            new_pop = new_pop[:-1, :]

        return new_pop

    @staticmethod
    def heuristic_crossing(pop, probability):
        new_pop = []
        counter = 0
        k = np.random.random()

        while counter < pop.shape[0]:
            rnd = np.random.random()
            if rnd < probability:
                first = pop[np.random.randint(0, pop.shape[0] - 1)]
                second = pop[np.random.randint(0, pop.shape[0] - 1)]
                while second[0] < first[0] and second[1] < first[1]:
                    first = pop[np.random.randint(0, pop.shape[0] - 1)]
                    second = pop[np.random.randint(0, pop.shape[0] - 1)]
                new_x = k * (second[0] - first[0]) + first[0]
                new_y = k * (second[1] - first[1]) + first[1]
                new_pop.append([new_x, new_y])
                counter += 1
            else:
                first = pop[np.random.randint(0, pop.shape[0] - 1)]
                second = pop[np.random.randint(0, pop.shape[0] - 1)]
                new_pop.append(first)
                new_pop.append(second)
                counter += 2

        new_pop = np.array(new_pop)
        if new_pop.shape[0] > pop.shape[0]:
            new_pop = new_pop[:-1, :]

        return new_pop
