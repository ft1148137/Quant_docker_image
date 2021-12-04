import backtrader as bt  

class MadcPlusROEStrategy(bt.Strategy):
    params = dict(rebal_monthday = [1],pe_volume = 5,ma_slow = 26, ma_fast = 12,)
    def __init__(self):
        self.last_ranks = []
        self.stocks = self.datas[:]
        self.order_list = []
        self.macd={d:bt.ind.MACDHisto(d, period_me1=self.params.ma_fast, period_me2 = self.params.ma_slow)
        for d in self.stocks}
        self.add_timer(
            when = bt.Timer.SESSION_START,
            monthdays=self.params.rebal_monthday,
            monthcarry=True,
        )
    
    def notify_timer(self,time,when,*args,**kwargs):
        self.reblance_with_pe()

    def next(self):
        portfolio_value = self.broker.get_value()
        for stock_ in self.ranks:
            stock_value = self.broker.get_value([stock_])
            stock_precentage = stock_value/portfolio_value
            target_precent = 0
            if(self.macd[stock_] > 0 and stock_precentage < 0.2):
                target_precent = 0.2 if 0.01 + stock_precentage >0.2 else 0.01 + stock_precentage 
            elif(self.macd[stock_] < 0 and stock_precentage >0):
                target_precent = 0 if stock_precentage - 0.01 < 0 else stock_precentage -0.01
            else: 
                continue
            self.order_target_percent(data = stock_,target = target_precent)

    def reblance_with_pe(self):
        self.currDate = self.data0.datetime.date(0)
        for od in self.order_list:
            self.cancel(od)
        self.order_list = []
        self.ranks = [d for d in self.stocks if
                     len(d) > 0
                     and d.datetime.date(0) == self.currDate
                     ]
        self.ranks.sort(key = lambda d:d.roe, reverse = True)
        self.ranks = self.ranks[0:self.params.pe_volume-1]
        if len(self.ranks) ==0 :
            return
        
        data_toclose = set(self.last_ranks) - set(self.ranks)
        for d in data_toclose:
            print("平仓:",d._name)
            self.order_target_percent(data = d,target = 0)
        self.last_ranks = self.ranks
        return
    def stop(self):
        print("策略结束， 总资产: ",self.broker.get_value())