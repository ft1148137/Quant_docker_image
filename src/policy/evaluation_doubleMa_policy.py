import backtrader as bt

# plt.rcParams["font.sans-serif"] = ["SimHei"]
#  plt.rcParams["axes.unicode_minus"] = False
class EvaluationDoubleMA_Strategy(bt.Strategy):
    params = (("maperiod", 5), ('printlog', False),)
    frozen_trade = False    
    value_buffer = 0;
    def __init__(self):
        self.data_close= self.datas[0].close
        self.order = None
        self.buy_price = None
        self.buy_comm = None
        self.value_buffer = self.broker.get_value()
        self.sma_fast = bt.ind.SimpleMovingAverage(self.datas[0],period = self.params.maperiod)
        self.sma_slow = bt.ind.SimpleMovingAverage(self.datas[0],period = 4*self.params.maperiod)
        self.crossover = bt.ind.CrossOver(self.sma_fast,self.sma_slow)
    
    def next(self):
        portfolio_value = self.broker.get_value()
        if self.crossover > 0:
            self.frozen_trade = False
        if(portfolio_value/self.value_buffer < 0.9):
            self.order = self.order_target_percent(target = 0)
            self.log("止损")
            self.value_buffer = portfolio_value
            self.frozen_trade = True
            return
        if(portfolio_value/self.value_buffer > 1.3):
            self.order = self.order_target_percent(target = 0)
            self.log("止盈")
            self.value_buffer = portfolio_value
            self.frozen_trade = True
            return
        stock_value = self.broker.get_value([self.datas[0]])
        stock_precentage = stock_value/portfolio_value
        self.log("total Value, %.2f , stock value, %.2f stock precentage, %.3f" % (portfolio_value,stock_value,stock_precentage))
        target_precent = stock_precentage
        if(self.sma_fast[0] > self.sma_slow[0] and stock_precentage < 1 and self.frozen_trade == False):
                self.log("buy create, %.2f"%self.data_close[0])
                target_precent = 1 if 0.1 + stock_precentage >=1 else 0.1 + stock_precentage 
        elif (self.sma_fast[0] < self.sma_slow[0] and stock_precentage > 0 and self.frozen_trade == False):
                self.log("sell create, %2f" % self.data_close[0])
                target_precent = 0 if  stock_precentage - 0.2 <= 0 else stock_precentage - 0.2 
        else:
            return
        self.order = self.order_target_percent(target = target_precent)
    
    def log(self,txt,dt = None,do_print = False):
        if self.params.printlog or do_print:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))


    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        
        if(order.status in [order.Completed]):
            if order.isbuy():
                self.log(
                f"买入:\n价格:{order.executed.price},\
                成本:{order.executed.value},\
                手续费:{order.executed.comm}"
                )
                self.buy_price = order.executed.price
                self.buy_comm = order.executed.comm
            else:
                self.log(
                f"卖出:\n价格：{order.executed.price},\
                成本: {order.executed.value},\
                手续费{order.executed.comm}"
                )
                self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
                self.log("交易失败")
        self.order = None

    def notify_trade(self,trade):
        if not trade.isclosed:
            return 
        self.log(f"策略收益：\n毛收益 {trade.pnl:.2f}, 净收益 {trade.pnlcomm:.2f}")

    def stop(self):
        self.log("(MA均线： %2d日) 期末总资金 %.2f" % (self.params.maperiod, self.broker.getvalue()), do_print=True)