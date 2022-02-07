from factor_lib.base_data_grep import BaseDataGrep
import pandas as pd
import baostock as bs
import akshare as ak

class GetStockEmLrb(BaseDataGrep):
    stock_em_lrb = dict()
    def __init__(self,start_date,end_date):
        self.get_data(start_date,end_date)
        pass

    def get_data(self,start_date,end_date):
        date_list = super().get_date_list("session",start_date,end_date)
        print(date_list)
        if not super().check_data_exist("stock_em_lrb"):
            super().create_dict("stock_em_lrb")
        for date_ in date_list:
            file_path_ = "stock_em_lrb/" + date_+".csv"
            print (date_)
            if not super().check_data_exist(file_path_):
                df = ak.stock_em_lrb(date=(date_.replace("-",'')))
                super().save_data(df,file_path_)
                self.stock_em_lrb[date_] = df
                print (df)
            else:
                self.stock_em_lrb[date_] = (super().read_data(file_path_))
        print(self.stock_em_lrb)
        pass