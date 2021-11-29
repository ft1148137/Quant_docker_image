import backtrader as bt

class my_PandasData(bt.feeds.PandasData):
    lines = ('pe','pb','roe',)
    params = (('pe',6),('pb',7),('roe',8),) 

