import numpy as np


class Selection:
    @staticmethod
    def best(pop, evaluated_pop, percent, is_max=True, num=0, is_elite_strategy=False):
        num_of_selected = 0
        pop_not_selected_indexes = [i for i in range(0,pop.shape[0])]
        if num == 0:
            num_of_selected = np.math.ceil(evaluated_pop.size * percent * 0.01)
        else:
            num_of_selected = num
        if is_max:
            indexes = evaluated_pop.argsort()[::-1][:num_of_selected]
        else:
            indexes = evaluated_pop.argsort()[:num_of_selected]
        pop_not_selected_indexes = [x for x in pop_not_selected_indexes if x not in indexes]
        pop_not_selected = np.array([pop[i] for i in pop_not_selected_indexes])
        best_val = np.array([evaluated_pop[i] for i in indexes])
        best = np.array([pop[i] for i in indexes])
        if not is_elite_strategy:
            return best, best_val, pop_not_selected
        return best, best_val

    @staticmethod
    def tournament(pop, evaluated_pop, k, is_max=True):
        pop_not_selected_indexes = [i for i in range(0, pop.shape[0])]
        indexes = np.array([i for i in range(len(evaluated_pop))])
        np.random.shuffle(indexes)
        indexes = np.array_split(indexes, int(len(evaluated_pop) / k))
        if is_max:
            indexes = list(map(lambda x: max(x, key=lambda y: evaluated_pop[y]), indexes))
        else:
            indexes = list(map(lambda x: min(x, key=lambda y: evaluated_pop[y]), indexes))
        pop_not_selected_indexes = [x for x in pop_not_selected_indexes if x not in indexes]
        pop_not_selected = np.array([pop[i] for i in pop_not_selected_indexes])
        best_val = np.array([evaluated_pop[i] for i in indexes])
        best = np.array([pop[i] for i in indexes])
        return best, best_val, pop_not_selected

    @staticmethod
    def roulette(pop, evaluated_pop, percent, is_max=True):
        if np.ndarray.min(evaluated_pop) <= 0:
            evaluated_pop = evaluated_pop + abs(np.ndarray.min(evaluated_pop)) + 1
        if is_max:
            cum_sum = np.cumsum(evaluated_pop)
        else:
            cum_sum = np.cumsum(1 / evaluated_pop)

        cum_sum = np.insert(cum_sum, 0, 0)
        best = []
        best_val = []
        pop_not_selected = []
        i = 1
        counter = 0
        rand = np.random.random_sample()
        while counter < int(evaluated_pop.size * percent * 0.01):
            if (cum_sum[i - 1] / cum_sum[cum_sum.size - 1]) <= rand < (
                    cum_sum[i] / cum_sum[cum_sum.size - 1]):
                best.append(pop[i - 1])
                best_val.append(evaluated_pop[i - 1])
                counter += 1
                i = 1
                rand = np.random.random_sample()
            else:
                i += 1
        best = np.array(best)
        best_val = np.array(best_val)
        pop_not_selected = [pop[np.random.randint(0, pop.shape[0])] for x in range (0, pop.shape[0] - int(evaluated_pop.size * percent * 0.01) )]

        return best, best_val,  np.array(pop_not_selected)
