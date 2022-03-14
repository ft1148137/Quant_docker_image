from enum import Enum

class remove_extremum_method(Enum):
    AVG = 1
    MID = 2
    MAD = 3
    pass

class remove_extremum_param():
    AVG_kesi = 0
    MAD_kesi = 0