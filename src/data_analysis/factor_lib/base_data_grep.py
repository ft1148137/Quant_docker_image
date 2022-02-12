import akshare as ak
import pandas as pd
import os
import datetime
from dateutil.relativedelta import relativedelta

class BaseDataGrep(object):
    data_dict_path = "./factor_lib/data_dict/"
    session_data_pub_time = ["12-31","03-31","06-30","09-30"]

    def calculate_date_time(self,start_date,end_date):
        period = ((end_date.month - start_date.month) + 12 * (end_date.year - start_date.year))/3
        start_month = int(start_date.month/4)
        start_year = start_date.year
        date_return = []
        for x in range(int(period+1)):
            if start_month == 0:
                date_return.append(str(start_year-1)+"-"+self.session_data_pub_time[start_month])
            else:
                date_return.append(str(start_year)+"-"+self.session_data_pub_time[start_month])
            start_month +=1
            if start_month > 3:
                start_month = 0
                start_year +=1
        return date_return

    def check_data_exist(self,dict_name):
        return os.path.exists(self.data_dict_path + dict_name)
    def create_dict(self,dict_name):
        os.mkdir(self.data_dict_path + dict_name)
    
    def save_data(self,data_,dict_name):
        data_.to_csv(self.data_dict_path + dict_name,index = 0, header = 0)

    def read_data(self,dict_name):
        return pd.read_csv(self.data_dict_path + dict_name,dtype=object, header = None)

    def get_date_list(self,time_delta,date_start,date_end):
        date_start_ = date_start
        date_list = []
        if time_delta == "year":
            while date_start_<= date_end:
                date_list.append(date_start_.strftime('%Y-%m-%d')) 
                date_start_ += relativedelta(years=1)
        elif time_delta == "month":
            while date_start_<= date_end:
                date_list.append(date_start_.strftime('%Y-%m-%d')) 
                date_start_ += relativedelta(months=1)
        elif time_delta == "session":
                date_list = self.calculate_date_time(date_start,date_end)
        else: 
            while date_start_<= date_end:
                date_list.append(date_start_.strftime('%Y-%m-%d')) 
                date_start_ += relativedelta(days=1)
        return date_list
        
    def remove_stock_title(self,stock):
        return stock[3:8]

    def add_stock_title(self,stock):
        if(stock[0] == '6'):
            return "sh."+stock
        else:
            return "sz."+stock
    
    def get_data(self):
        pass
