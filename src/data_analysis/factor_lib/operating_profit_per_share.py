import akshare as ak
import baostock as bs
from factor_lib.base_factor_module  import BaseFactor
from factor_lib.get_code_list import GetStockCodeList
from factor_lib.get_stock_em_lrb import GetStockEmLrb
from factor_lib.get_query_profit_data import GetQueryProfitData
import datetime
import os
import pandas as pd

##营业利润/总股本
class OperatingProfitPerShare(BaseFactor):
    operating_porfit_dict = "operating_porfit"
    data_pub_time = ["1231","0331","0630","0930"]
    def __init__(self):
        pass
    def calculate_date_time(self,start_date,end_date):
        period = ((end_date.month - start_date.month) + 12 * (end_date.year - start_date.year))/3
        start_month = int(start_date.month/4)
        start_year = start_date.year
        date_return = []
        for x in range(int(period+1)):
            if start_month == 0:
                date_return.append(str(start_year-1)+self.data_pub_time[start_month])
            else:
                date_return.append(str(start_year)+self.data_pub_time[start_month])
            start_month +=1
            if start_month > 3:
                start_month = 0
                start_year +=1
        return date_return

    def get_factor(self,start_date, end_date):
        print("get operating profit per share")
        # print(start_date,end_date)
        get_stock_list = GetStockCodeList(self.code_list,start_date,end_date)
        stock_list = get_stock_list.code_list
        get_em_lrb = GetStockEmLrb(start_date,end_date,stock_list,"hs300_2010_to_2020")
        operating_profit = get_em_lrb.get_operating_profit()
        print(operating_profit)
        get_query_profit = GetQueryProfitData(start_date,end_date,stock_list,"hs300_2010_to_2020")
        total_share=get_query_profit.get_total_share()
        print(total_share) 
        super().index_matching(operating_profit,total_share)  
        pass