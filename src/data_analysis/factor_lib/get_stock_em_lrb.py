from factor_lib.base_data_grep import BaseDataGrep
import pandas as pd
import baostock as bs
import akshare as ak
import datetime

class GetStockEmLrb(BaseDataGrep):
    stock_em_lrb = pd.DataFrame()
    def filter_data_with_stock_list(self,stock_list):
        date_search_stock = self.stock_em_lrb.index.values
        # aim_index = 0
        # # print(date_search_stock)
        # for date_aim_stock in stock_list.columns:
        #     if datetime.datetime.strptime(date_aim_stock, "%Y-%m-%d") > date_search_stock[search_index][0]:
        #         for 
        #         print(date_aim_stock) 
        #         search_index+=1
        #         print(datetime.datetime.strptime(date_aim_stock, "%Y-%m-%d"))
        #         pass
        #     print(date_aim_stock)
            # print(stock_list[date_aim_stock])

            # print(stock_list.iloc[:,i])
        # stock_em_lrb_panel = pd.DataFrame(self.stock_em_lrb,index=[0,self.stock_em_lrb])
        # print(stock_em_lrb_panel.minor_xs(1))

        # for stock in stock_list:
        #     if(stock[0] == "s"):
            # stock = super().remove_stock_title(stock)
        pass
    def __init__(self,start_date,end_date,stock_list):
        self.get_data(start_date,end_date)
        self.filter_data_with_stock_list(stock_list)
        pass

    def get_data(self,start_date,end_date):
        date_list = super().get_date_list("session",start_date,end_date)
        # print(date_list)
        if not super().check_data_exist("stock_em_lrb"):
            super().create_dict("stock_em_lrb")
        for date_ in date_list:
            file_path_ = "stock_em_lrb/" + date_+".csv"
            # print (date_)
            if not super().check_data_exist(file_path_):
                df = ak.stock_em_lrb(date=(date_.replace("-",'')))
                super().save_data(df,file_path_)
                df["date"] = datetime.datetime.strptime(date_, "%Y-%m-%d")
                self.stock_em_lrb = pd.concat([self.stock_em_lrb,df])
            else:
                df = (super().read_data(file_path_))
                df["date"] = datetime.datetime.strptime(date_, "%Y-%m-%d")
                df.append(self.stock_em_lrb)
                self.stock_em_lrb = pd.concat([self.stock_em_lrb,df])
        self.stock_em_lrb = self.stock_em_lrb.set_index(["date",1])
        pass