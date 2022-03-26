import matplotlib.pyplot as plt
import numpy as np


class BasePlot():
    def __init__(self,data_):
        pass

    def plot(self):
        plt.show()
        pass

    def save(self,name_):
        plt.savefig(name_)
        pass

    def set_x_scalar(self,range_):
        plt.xlim(range_[0],range_[1]);
        pass

    def set_y_saclar(self,range_):
        plt.ylim(range_[0],range_[1]);
        pass

    def set_x_y_lable(self,x_lable_,y_lable_):
        plt.xlabel(x_lable_)
        plt.ylabel(y_lable_)
        pass

    def add_line(self):
        pass
