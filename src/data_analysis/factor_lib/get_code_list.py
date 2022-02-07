from factor_lib.base_data_grep import BaseDataGrep
import pandas as pd
import baostock as bs
class GetStockCodeList(BaseDataGrep):
    code_list = pd.DataFrame()
    def __init__(self,code_list_name,date_start,date_end):
        self.get_data(code_list_name,date_start,date_end)

    def get_data(self,code_list_name,date_start,date_end):
        if code_list_name == "hs300":
            date_list = super().get_date_list("year",date_start,date_end)
            if not super().check_data_exist("hs300"):
                super().create_dict("hs300")
            self.code_list = self.get_list_with_date(date_list,"hs300")
        else:
            print("ERROR, please check code list name")

    def get_list_with_date(self,date_list,date_dict):
        lg = bs.login()
        hs300_stocks = pd.DataFrame()
        for date_ in date_list:
            file_path_ = "hs300/" + date_+".csv"
            if not super().check_data_exist(file_path_):
                rs = bs.query_hs300_stocks(date_)
                df = rs.get_data()
                super().save_data(df,file_path_)
                hs300_stocks[date_]=df.iloc[:,1]
            else:
                hs300_stocks[date_] = (super().read_data(file_path_).iloc[:,1])
        bs.logout()
        return hs300_stocks