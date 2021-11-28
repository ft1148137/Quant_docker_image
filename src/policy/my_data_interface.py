import backtrader as bt

class my_PandasData(bt.feeds.PandasData):
    lines = ('pe','pb','roe',)
    params = (('pe',-1),('pb',-1),('roe',-1),) 

