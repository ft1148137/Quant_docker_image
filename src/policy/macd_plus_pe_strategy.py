import backtrader as bt  

class MadcPlusPeStrategy(bt.Strategy):
    params = (rebal_monthday = [1],pe_volume = 5,ma_slow = 26, ma_fast = 12,)
    def __init__(self):
        self.last_ranks = []
        self.stocks = self.datas[:]
        self.order_list = []
        self.macd={d:bt.ind.MACDHisto(d, period_me1=self.params.ma_fast, period_me2 = self.params.ma_slow)\ 
        for d in self.stocks}
        self.add_timer(
            When = bt.Timer.SESSION_START,
            monthdays=self.params.rebal_monthday,
            monthcarry=True,
        )
        return
    
    def notify_timer(self,time,when,*args,**kwargs):
        return
    def next(self):
        return
    def reblance_with_pe():
        return