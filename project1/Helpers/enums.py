from enum import Enum


class SelectionType(Enum):
    BEST = 1
    ROULETTE = 2
    TOURNAMENT = 3


class CrossingType(Enum):
    SINGLE_POINT = 1
    DOUBLE_POINT = 2
    TRIPLE_POINT = 3
    HOMOGENEOUS = 4


class MutationType(Enum):
    EDGE = 1
    SINGLE_POINT = 2
    DOUBLE_POINT = 3

