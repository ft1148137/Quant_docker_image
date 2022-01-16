import akshare as ak
import pandas as pd
class BaseFactor(object):
    data_dict_path = "./factor_lib/data_dict"
    code_list = "hs300"
    mode = "offline"
    def __init__(self):
        pass
    def get_code_list(self):
        if self.code_list == "hs300":
            if self.mode == "online":
                index_stock_cons_df = ak.index_stock_cons(index="000300").iloc[:,0]
                index_stock_cons_df.to_csv(self.data_dict_path + "/hs300.csv",index = 0, header = 0)
                return index_stock_cons_df.tolist()
            elif self.mode == "offline":
                return pd.read_csv(self.data_dict_path+"/hs300.csv",dtype=object).iloc[:,0].tolist()
            else:
                print("ERROR,please choose online or offline")
        else:
            print("ERROR, please check code list name")

    def get_trade_date(self):
        if self.mode == "online":
            df = ak.tool_trade_date_hist_sina()
            df.to_csv(self.data_dict_path + "/trade_date.csv",index = 0)
            return df
        elif self.mode == "offline":
            return pd.read_csv(self.data_dict_path+"/trade_date.csv")["trade_date"]

    def search_time_range(self,start_date,end_date):
        trade_date = self.get_trade_date()
        trade_date.index = pd.to_datetime(trade_date)
        start_date_corrected = trade_date.index.searchsorted(start_date)
        end_date_corrected = trade_date.index.searchsorted(end_date)
        return [date.replace('-','') for date in trade_date.iloc[start_date_corrected:end_date_corrected].tolist()]
    
    def get_factor(self,start_date, end_date):
        pass

    def calculate_factor_IR(self,data):
        
        pass

    def calculate_factor_IC(self,data):
    
        pass

    def remove_extremum(self,data,used_method):

        pass

    def data_normalized(self,data,used_method):

        pass

    def data_filled(self,data,used_method):

        pass

    def data_neutralize(self,data,used_method):

        pass
