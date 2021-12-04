from datetime import datetime
from macd_plus_pe_strategy import MadcPlusROEStrategy
from my_data_interface import my_PandasData
from my_commission_interface import ChinaStockCommission
import akshare as ak
import backtrader as bt 
import matplotlib as plt
import pandas as pd 
import my_plot_interface as myplt
import os.path
import glob

def grep_data_to_local(code_list,data_start,data_end,path):
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
        path_name = path + code
        data_.to_csv(path_name)

def grep_data_online(code_list,data_start,data_end):
    data_return = []
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
        data_return.append(data_return)
    return data_return

# def get_data(code_list,data_start,data_end):
#     data_return = []
#     # file = open(path,"w")
#     for code in code_list:
#         stock_hfq_df = ak.stock_zh_a_hist(symbol=code,adjust="hfq",start_date=data_start, end_date=data_end).iloc[:,:6]
#         stock_indicator = ak.stock_a_lg_indicator(stock=code).iloc[:,0:5]
#         stock_indicator['pe'].fillna(0,inplace = True)
#         stock_indicator['pb'].fillna(999,inplace = True)
#         stock_indicator = stock_indicator.set_index('trade_date')
#         pd_date_start = pd.to_datetime(data_start,format='%Y%m%d')
#         pd_date_end = pd.to_datetime(data_end,format='%Y%m%d')
#         stock_indicator = stock_indicator.loc[pd_date_end : pd_date_start]
#         data_ = pd.concat([stock_hfq_df,stock_indicator.reset_index()[['pe','pb']]],axis=1);
#         data_['roe'] = data_['pb']/data_['pe']
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
    # return data_return
def read_local_data(path):
    data_return = []
    name_return = []
    datafilelist = glob.glob(os.path.join(path, '*'))
    for stock_name in datafilelist:
        df = pd.read_csv(stock_name)
        data_return.append(df)
        name_return.append(stock_name[13:])
    return data_return, name_return


def main(start_cash = 1e5):
    cerebro = bt.Cerebro(stdstats = False) 
    # cerebro.addobserver(bt.observers.Broker)
    # cerebro.addobserver(bt.observers.Trades)
    cerebro.addstrategy(MadcPlusROEStrategy)
    stock_pool,name_pool = read_local_data("./hs300_data")
    st_date = datetime(2020,1,19)
    ed_date = datetime(2020,11,20)
    for i in range(len(stock_pool)):
        stock_ = stock_pool[i].iloc[:,1:]
        if(len(stock_) < 219):
            continue
        stock_.columns = [
        'date',
        'open',
        'close',
        'high',
        'low',
        'volume',
        'pe',
        'pb',
        'roe',
        ]
        stock_.index = pd.to_datetime(stock_['date'])
        test = pd.to_datetime(stock_['date'])
        data = my_PandasData(dataname=stock_, fromdate=st_date, todate=ed_date) 
        cerebro.adddata(data,name = name_pool[i])
        
    cerebro.broker.setcash(start_cash)
    comminfo = ChinaStockCommission(stamp_duty=0.001, commission=0.0005, transfer_fee = 0.0006)
    cerebro.broker.addcommissioninfo(comminfo)
    print("期初总资金: %.2f" % cerebro.broker.getvalue())
    result = cerebro.run(maxcpus=4,optreturn = False)  
    print("期末总资金: %.2f" % cerebro.broker.getvalue())
    # cerebro.plot();

if __name__ == '__main__':
    main()