import project1.Algorithm.selection


class EliteStrategy:

    @staticmethod
    def elite_strategy(pop, evaluated_pop, percent=0, num=0, is_max=True):
        if percent != 0:
            return project1.Algorithm.selection.Selection.best(pop, evaluated_pop, percent, is_max, 0, True)
        else:
            return project1.Algorithm.selection.Selection.best(pop, evaluated_pop, 0, is_max, num, True)
