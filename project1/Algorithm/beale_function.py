from abc import abstractmethod, ABC


class Function:

    @staticmethod
    def bale_function(x1, x2):
        return (1.5 - x1 + x1 * x2) ** 2 + (2.25 - x1 + x1 * x2 ** 2) ** 2 + (2.625 - x1 + x1 * x2 ** 3) ** 2
