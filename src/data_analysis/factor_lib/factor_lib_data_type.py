from enum import Enum

class remove_extremum_method(Enum):
    AVG = 1
    MAD = 2
    QUA = 3
    pass

class data_fill_method(Enum):
    DROP = 1
    AVG = 2
    MID = 3
    pass

class remove_extremum_param():
    AVG_kesi = 0
    MAD_kesi = 0
    QUA_upper = 75
    QUA_down = 25
    data_fill = data_fill_method.DROP
