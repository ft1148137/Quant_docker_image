from datetime import datetime
from evaluation_doubleMa_policy import EvaluationDoubleMA_Strategy
from ma14_policy import MA14_Strategy
import akshare as ak
import backtrader as bt 
import matplotlib as plt
import pandas as pd 
import my_plot_interface as myplt


def main(code = "600070", start_cash = 1e5,stake = 100, commission_fee = 0.001):
    cerebro = bt.Cerebro(stdstats = False) 
    cerebro.optstrategy(EvaluationDoubleMA_Strategy)
    stock_hfq_df = ak.stock_zh_a_hist(symbol=code,adjust="hfq",start_date='20000101', end_date='20210617').iloc[:,:6]
    stock_hfq_df.columns = [
        'date',
        'open',
        'close',
        'high',
        'low',
        'volume',
    ]
    stock_hfq_df.index = pd.to_datetime(stock_hfq_df['date'])
    start_date = datetime(2019, 1, 2)
    end_date = datetime(2020, 1, 3)
    data = bt.feeds.PandasData(dataname=stock_hfq_df, fromdate=start_date, todate=end_date) 
    cerebro.adddata(data)
    cerebro.broker.setcash(start_cash)
    cerebro.broker.setcommission(commission= commission_fee)
    cerebro.addobserver(myplt.my_buysell)
    cerebro.addobserver(bt.observers.Trades)
    cerebro.addobserver(bt.observers.TimeReturn)
    # cerebro.addobserver(bt.observers.DrawDown)
    # cerebro.addobserver(bt.observers.TimeReturn)
    # cerebro.addsizer(bt.sizers.FixedSize,stake = stake)
    print("期初总资金: %.2f" % cerebro.broker.getvalue())
    cerebro.run(maxcpus=1,optreturn = False)  # 用单核 CPU 做优化
    print("期末总资金: %.2f" % cerebro.broker.getvalue())
    cerebro.plot()
if __name__ == '__main__':
    main()