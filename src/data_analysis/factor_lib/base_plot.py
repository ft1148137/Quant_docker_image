import matplotlib.pyplot as plt
import numpy as np


class BasePlot():
    x_axis = []
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        pass

    def plot(self):
        plt.show()
        pass

    def save(self,name_):
        plt.savefig(name_+".png")
        pass

    def set_x_scalar(self,range_):
        self.x_axis = np.arange(0,range_,1);
        pass

    def set_x_y_lable(self,x_lable_,y_lable_):
        plt.xlabel(x_lable_)
        plt.ylabel(y_lable_)
        pass

    def add_line(self,data_,label):
        self.ax.plot(self.x_axis, data_, label = label)
        pass
    def add_pts(self,data_,):
        plt.scatter(self.x_axis, data_, s=0.1)
        pass
