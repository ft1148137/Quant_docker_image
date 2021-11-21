import backtrader as bt

class my_PandasData(bt.feeds.PandasData):
    lines = ('pe',)
    params = (('pe',-1),) 