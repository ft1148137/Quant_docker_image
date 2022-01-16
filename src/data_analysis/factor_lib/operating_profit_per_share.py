import akshare as ak
from factor_lib.base_factor_module  import BaseFactor
import datetime

##营业利润/总股本
class OperatingProfitPerShare(BaseFactor):
    operating_porfit_dict = "operating_porfit"
    data_pub_time = ["1231","0331","0630","0930"]
    def __init__(self):
        pass
    def calculate_date_time(self,start_date,end_date):
        start_date = datetime.datetime(2020,1,1)
        end_date = datetime.datetime(2023,1,1)
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
        stock_list = super().get_code_list()
        date_list = self.calculate_date_time(start_date,end_date)
        for date_ in date_list:
            if(self.mode == "offline"):
                print (date_)
                print(ak.stock_em_lrb(date=date_))
        pass