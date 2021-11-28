from datetime import datetime
from macd_plus_pe_strategy import MadcPlusROEStrategy
from my_data_interface import my_PandasData
from my_commission_interface import ChinaStockCommission
import akshare as ak
import backtrader as bt 
import matplotlib as plt
import pandas as pd 
import my_plot_interface as myplt

def get_data(code_list,data_start,data_end):
    data_return = []
    path= "data.csv"
    # file = open(path,"w")
    for code in code_list:
        stock_hfq_df = ak.stock_zh_a_hist(symbol=code,adjust="hfq",start_date=data_start, end_date=data_end).iloc[:,:6]
        stock_indicator = ak.stock_a_lg_indicator(stock=code).iloc[:,0:5]
        stock_indicator['pe'].fillna(0,inplace = True)
        stock_indicator['pb'].fillna(999,inplace = True)
        stock_indicator = stock_indicator.set_index('trade_date')
        pd_date_start = pd.to_datetime(data_start,format='%Y%m%d')
        pd_date_end = pd.to_datetime(data_end,format='%Y%m%d')
        stock_indicator = stock_indicator.loc[pd_date_end : pd_date_start]
        data_ = pd.concat([stock_hfq_df,stock_indicator.reset_index()[['pe','pb']]],axis=1);
        data_['roe'] = data_['pb']/data_['pe']
    #     data_.columns = [
    #     'date',
    #     'open',
    #     'close',
    #     'high',
    #     'low',
    #     'volume',
    #     'pe',
    #     'pb',
    #     'roe',
    #     ]
    #     data_.index = pd.to_datetime(data_['date'])
    #     data_return.append(data_)
    return data_return

def main(code = "000300", start_cash = 1e5,stake = 100, commission_fee = 0.001):
    cerebro = bt.Cerebro(stdstats = False) 
    cerebro.optstrategy(MadcPlusROEStrategy)
    hs300_stock = ak.index_stock_cons(index = "000300").iloc[:,0].tolist()
    stock_pool = get_data(hs300_stock,'20201102','20201201')
    st_date = datetime.datetime(2020,11,2)
    ed_date = datetime.datetime(2020,12,1)
    for i in range(len(stock_pool)):
        data = bt.feeds.PandasData(dataname=stock_pool[i], fromdate=st_date, todate=ed_date) 
        cerebro.adddata(data,name = hs300_stock[i])
    cerebro.broker.setcash(start_cash)
    cerebro.broker.setcommission(commission = ChinaStockCommission)
    print("期初总资金: %.2f" % cerebro.broker.getvalue())
    cerebro.run(maxcpus=1,optreturn = False)  # 用单核 CPU 做优化
    print("期末总资金: %.2f" % cerebro.broker.getvalue())
# stock_hfq_df.columns = [
    #     'date',
    #     'open',
    #     'close',
    #     'high',
    #     'low',
    #     'volume',
    # ]
    # stock_hfq_df.index = pd.to_datetime(stock_hfq_df['date'])
    # start_date = datetime(2019, 1, 2)
    # end_date = datetime(2020, 1, 3)
    # data = bt.feeds.PandasData(dataname=stock_hfq_df, fromdate=start_date, todate=end_date) 
    # cerebro.adddata(data)
    # cerebro.broker.setcash(start_cash)
    # cerebro.broker.setcommission(commission= commission_fee)
    # cerebro.addobserver(myplt.my_buysell)
    # cerebro.addobserver(bt.observers.Trades)
    # cerebro.addobserver(bt.observers.TimeReturn)
    # # cerebro.addobserver(bt.observers.DrawDown)
    # # cerebro.addobserver(bt.observers.TimeReturn)
    # # cerebro.addsizer(bt.sizers.FixedSize,stake = stake)
    # print("期初总资金: %.2f" % cerebro.broker.getvalue())
    # cerebro.run(maxcpus=1,optreturn = False)  # 用单核 CPU 做优化
    # print("期末总资金: %.2f" % cerebro.broker.getvalue())
    # cerebro.plot()
if __name__ == '__main__':
    main()