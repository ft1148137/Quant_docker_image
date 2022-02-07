import akshare as ak
import baostock as bs
from factor_lib.base_factor_module  import BaseFactor
from factor_lib.get_code_list import GetStockCodeList
from factor_lib.get_stock_em_lrb import GetStockEmLrb
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

    def get_total_share(self,stock_list,date_list):
        share_capital_path = self.data_dict_path + "/share_capital/"
        lg = bs.login()
        for date in date_list:
            operation_list = []
            print(date)
            year_ , quarter_ = super().get_seasons_and_year(date)
            for stock in stock_list:
                if(stock[0] == '6'):
                    stock = "sh."+stock
                else:
                    stock = "sz."+stock
                rs_operation = bs.query_operation_data(code=stock, year=year_, quarter=quarter_)
                print(stock,rs_operation.error_code,rs_operation.next())
                while (rs_operation.error_code == '0') & rs_operation.next():
                    operation_list.append(rs_operation.get_row_data())
            result_operation = pd.DataFrame(operation_list, columns=rs_operation.fields)
            result_operation.to_csv(share_capital_path+date+".csv",index = 0, header = date)
            print(result_operation)
        bs.logout()
        pass

    def get_factor(self,start_date, end_date):
        print("get operating profit per share")
        print(start_date,end_date)
        get_stock_list = GetStockCodeList(self.code_list,start_date,end_date)
        stock_list = get_stock_list.code_list
        date_list = self.calculate_date_time(start_date,end_date)
        print(date_list)
        get_em_lrb = GetStockEmLrb(start_date,end_date)
        # profit_path = self.data_dict_path + "/operating_profit/"
        # if self.mode == "online":
        #     if not os.path.exists(profit_path):
        #         os.mkdir(profit_path)
        #     for date_ in date_list:
        #         print (date_)
        #         data = ak.stock_em_lrb(date=date_)
        #         data.to_csv(profit_path+str(date_)+".csv",index = 0, header = str(date_))
        #     # if not os.path.exists(share_capital_path):
        #     #     os.mkdir(share_capital_path)
        #     # for date_ in date_list:
        #     #     self.get_total_share()
        #         # if(date_[4:6] == "06" or date_[4:6] == "12" ):
        #         #     print(date_)
        #         #     data = ak.stock_em_fhps(date = date_)
        #         #     data.to_csv(share_capital_path+str(date_)+".csv",index = 0, header = str(date_))
        # elif self.mode == "offline":
        #     self.get_total_share(stock_list,date_list)

        # #     for date_ in date_list:
        # #         profit_data = (pd.read_csv(profit_path+str(date_) + ".csv").set_index("股票代码")).iloc[:,-3]
        # #         if(date_[4:6] == "06" or date_[4:6] == "12" ):
        # #             share_capital = (pd.read_csv(share_capital_path+str(date_) + ".csv").set_index("代码")).iloc[:,-8]
        # #             print(share_capital)
        # #         # print(profit_data)
        #     pass
            
        pass