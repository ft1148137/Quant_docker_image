import akshare as ak
import baostock as bs
from factor_lib.base_factor_module  import BaseFactor
from factor_lib.get_code_list import GetStockCodeList
from factor_lib.get_stock_em_lrb import GetStockEmLrb
from factor_lib.get_query_profit_data import GetQueryProfitData
import datetime
import os
import pandas as pd
from factor_lib.factor_lib_data_type import *
from factor_lib.base_plot import BasePlot

##营业利润/总股本
class OperatingProfitPerShare(BaseFactor):
    operating_porfit_dict = "operating_porfit"
    data_pub_time = ["1231","0331","0630","0930"]
    def __init__(self,start_date, end_date,data_save_name):
        self.get_factor(start_date,end_date,data_save_name)
        pass

    def get_factor(self,start_date, end_date,data_save_name):
        print("get operating profit per share")
        get_stock_list = GetStockCodeList(self.code_list,start_date,end_date)
        stock_list = get_stock_list.code_list
        get_em_lrb = GetStockEmLrb(start_date,end_date,stock_list,"hs300_2010_to_2020")
        operating_profit = get_em_lrb.get_operating_profit()
        get_query_profit = GetQueryProfitData(start_date,end_date,stock_list,"hs300_2010_to_2020")
        total_share=get_query_profit.get_total_share()
        matching_result = super().index_matching(operating_profit,total_share)  
        operating_profit_per_share = pd.to_numeric(matching_result["operating profit"],errors='coerce')/pd.to_numeric(matching_result["total share"],errors='coerce')
        operating_profit_per_share.rename("operating profit per share",inplace = True)
        param = remove_extremum_param();
        param.data_fill = data_fill_method.MID
        plt = BasePlot()
        plt.set_x_scalar(len(operating_profit_per_share))
        # plt.add_pts(operating_profit_per_share.tolist())
        super().remove_extremum(operating_profit_per_share,remove_extremum_method.AVG,param)
        # plt.add_pts(operating_profit_per_share.tolist())
        super().data_normalized(operating_profit_per_share);
        print(operating_profit_per_share)
        # plt.add_line(operating_profit_per_share.tolist(),'data')
        plt.add_pts(operating_profit_per_share.tolist())
        plt.save("test")
        pass