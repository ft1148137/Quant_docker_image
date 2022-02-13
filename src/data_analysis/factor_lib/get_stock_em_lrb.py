from factor_lib.base_data_grep import BaseDataGrep
import pandas as pd
import baostock as bs
import akshare as ak
import datetime

class GetStockEmLrb(BaseDataGrep):
    stock_em_lrb = pd.DataFrame()
    def operate_data_with_stock_list(self,stock_list,stock_list_name):
        if not super().check_data_exist("operate_stock_em_lrb"):
            super().create_dict("operate_stock_em_lrb")
        file_path_ = "operate_stock_em_lrb/" + stock_list_name +".csv"
        if not super().check_data_exist(file_path_):
            date_stock_em_lrb = self.stock_em_lrb.index.levels[0]
            stock_date_index = 0
            # # print(date_search_stock)
            stock_em_lrb_all = pd.DataFrame()
            for date_search_stock in date_stock_em_lrb:
                print(date_search_stock)
                if stock_date_index >= len(date_stock_em_lrb):
                    print("index error in stock list")
                    return
                if date_search_stock >= datetime.datetime.strptime(stock_list.columns[stock_date_index+1], "%Y-%m-%d") - datetime.timedelta(days = 1):
                    stock_date_index+=1
                    # print(date_search_stock, stock_list.columns[stock_date_index])
                stocks_code = stock_list.iloc[:,stock_date_index].tolist()
                stock_em_lrb_ = pd.DataFrame()
                # print(self.stock_em_lrb.loc[date_search_stock].index.tolist())
                for  stock_code in stocks_code:
                    super().remove_stock_title(stock_code)
                    if super().remove_stock_title(stock_code) in (self.stock_em_lrb.loc[date_search_stock].index.tolist()):
                        stock_em_lrb_ = stock_em_lrb_.append(self.stock_em_lrb.loc[date_search_stock,super().remove_stock_title(stock_code)][1:13])
                stock_em_lrb_.index =  pd.MultiIndex.from_tuples(stock_em_lrb_.index.values)
                stock_em_lrb_all = pd.concat([stock_em_lrb_all,stock_em_lrb_])
            super().save_data(stock_em_lrb_all,file_path_,index_ = True)
            self.stock_em_lrb = stock_em_lrb_all
        else:
            self.stock_em_lrb = super().read_data(file_path_).set_index([0,1])
        print(self.stock_em_lrb)
        pass
    def __init__(self,start_date,end_date,stock_list,stock_list_name):
        self.get_data(start_date,end_date)
        self.operate_data_with_stock_list(stock_list,stock_list_name)
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