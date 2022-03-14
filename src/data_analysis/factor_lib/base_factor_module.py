import akshare as ak
import pandas as pd
import os
from factor_lib.factor_lib_data_type import *
class BaseFactor(object):
    data_dict_path = "./factor_lib/data_dict"
    code_list = "hs300"
    def __init__(self):
        pass

    # def get_trade_date(self):
    #     if self.mode == "online":
    #         df = ak.tool_trade_date_hist_sina()
    #         df.to_csv(self.data_dict_path + "/trade_date.csv",index = 0)
    #         return df
    #     elif self.mode == "offline":
    #         return pd.read_csv(self.data_dict_path+"/trade_date.csv")["trade_date"]

    # def get_seasons_and_year(self,date_string): 
    #     year_ = int(date_string[0:4])
    #     month = int(date_string[4:6])
    #     season = 1 if month>=1 and month <4 else 2 if month >=4 and month < 7 else 3 if month >=7 and month < 10 else 4 if month >=10 and month <= 12 else 0
    #     return year_ , season

    # def search_time_range(self,start_date,end_date):
    #     trade_date = self.get_trade_date()
    #     trade_date.index = pd.to_datetime(trade_date)
    #     start_date_corrected = trade_date.index.searchsorted(start_date)
    #     end_date_corrected = trade_date.index.searchsorted(end_date)
    #     return [date.replace('-','') for date in trade_date.iloc[start_date_corrected:end_date_corrected].tolist()]

    def index_matching(self,pd_data_src,pd_data_tar):
        # print(pd_data_src,pd_data_tar)
        if not (pd_data_src.index.levels[0].values == pd_data_tar.index.levels[0].values).all():
            print("date error by matching index")
        dates_ = pd_data_src.index.levels[0].values
        result = pd.DataFrame()
        for date_ in dates_:
            data_ = pd.merge(pd_data_src[date_],pd_data_tar[date_],left_index = True,right_index=True, how = "inner")
            data_.index = pd.MultiIndex.from_product([[date_],data_.index.to_list()])
            result = result.append(data_)
        return (result)

    def calculate_factor_IR(self,data):
        
        pass

    def calculate_factor_IC(self,data):
    
        pass

    def remove_extremum(self,data,used_method,param):
        if used_method == remove_extremum_method.AVG:
            mean = data.mean()
            std_dev = data.std()
            print(mean + param.AVG_kesi * std_dev)
            for i in range(len(data)):
                if data[i] >= mean + param.AVG_kesi * std_dev :
                    data[i] =  mean + param.AVG_kesi * std_dev
            print (mean,std_dev)
            pass
        elif used_method == remove_extremum_method.MAD:
            midian = data.median()
            data_div = pd.Series([x- midian for x in data])
            print (data_div)
            midian_div = data_div.median()
            print(midian_div)
            pass
        elif used_method == remove_extremum_method.MID:
            pass
        else:
            print("ERROR, wrong method when remove extremum")
        pass

    def data_normalized(self,data,used_method):

        pass

    def data_filled(self,data,used_method):

        pass

    def data_neutralize(self,data,used_method):

        pass
