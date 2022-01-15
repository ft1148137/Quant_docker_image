import akshare as ak
from factor_lib.base_factor_module  import BaseFactor
import datetime

##营业利润/总股本
class OperatingProfitPerShare(BaseFactor):
    operating_porfit_dict = "operating_porfit"
    def __init__(self):
        pass

    def get_factor(self,start_date, end_date):
        print("get operating profit per share")
        stock_list = super().get_code_list()
        # print(stock_list)
        tmp_start_date = start_date
        print(super().get_trade_date())
        while tmp_start_date<=end_date:
            # print (tmp_start_date.strftime('%Y-%m-%d'))
            tmp_start_date+=datetime.timedelta(days=1)
        # for stock in stock_list:
        #     pass

        pass
    
    def get_operating_profit_online(start_date,end_date):
        pass