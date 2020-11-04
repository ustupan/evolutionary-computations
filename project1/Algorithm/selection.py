import numpy as np


class Selection:
    @staticmethod
    def best(pop, evaluated_pop, percent, is_max):
        num_of_selected = int(evaluated_pop.size * percent * 0.01)
        if is_max:
            indexes = evaluated_pop.argsort()[:num_of_selected]
        else:
            indexes = evaluated_pop.argsort()[::-1][:num_of_selected]
        best_val = [evaluated_pop[i] for i in indexes]
        best = [pop[i] for i in indexes]
        return best, best_val

    @staticmethod
    def tournament(pop, evaluated_pop, k, is_max):
        indexes = np.array([i for i in range(len(evaluated_pop))])
        np.random.shuffle(indexes)
        indexes = np.array_split(indexes, int(len(evaluated_pop) / k))
        if is_max:
            indexes = list(map(lambda x: max(x, key=lambda y: evaluated_pop[y]), indexes))
        else:
            indexes = list(map(lambda x: min(x, key=lambda y: evaluated_pop[y]), indexes))
        best_val = [evaluated_pop[i] for i in indexes]
        best = [pop[i] for i in indexes]
        return best, best_val

    @staticmethod
    def roulette(pop, evaluated_pop, percent, is_max):
        if np.ndarray.min(evaluated_pop) <= 0:
            evaluated_pop = evaluated_pop + abs(np.ndarray.min(evaluated_pop)) + 1
        if is_max:
            cum_sum = np.cumsum(evaluated_pop)
        else:
            cum_sum = np.cumsum(1 / evaluated_pop)

        cum_sum = np.insert(cum_sum, 0, 0)
        best = []
        best_val = []
        i = 1
        counter = 0

        while counter < int(evaluated_pop.size * percent * 0.01):
            if (cum_sum[i - 1] / cum_sum[cum_sum.size - 1]) <= np.random.random_sample() < (
                    cum_sum[i] / cum_sum[cum_sum.size - 1]):
                best.append(pop[i - 1])
                best_val.append(evaluated_pop[i-1])
                counter += 1
                i = 1
            else:
                i += 1
        best = np.array(best)
        best_val = np.array(best_val)

        return best, best_val

