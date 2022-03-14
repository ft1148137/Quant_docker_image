from factor_lib.base_data_grep import BaseDataGrep
import pandas as pd
import baostock as bs
import datetime

class GetQueryProfitData(BaseDataGrep):
    query_profit_data = pd.DataFrame()
    def get_total_share(self):
        return (self.query_profit_data.iloc[:,-2]).rename('total share',inplace=True)

    def __init__(self,start_date,end_date,stock_list,stock_list_name):
        self.get_data(start_date,end_date,stock_list,stock_list_name)
        pass

    def get_data(self,start_date,end_date,stock_list,stock_list_name):
        if(not super().check_data_exist("query_profit_data/"+stock_list_name)):
            super().create_dict("query_profit_data/" + stock_list_name)
        lg = bs.login()
        date_list = super().get_date_list("session",start_date,end_date)
        stock_date_index = 0
        for date_ in date_list:
            path = "query_profit_data/"+stock_list_name+"/"+date_+".csv"
            if datetime.datetime.strptime(date_, "%Y-%m-%d") >= datetime.datetime.strptime(stock_list.columns[stock_date_index+1], "%Y-%m-%d") - datetime.timedelta(days = 1):
                stock_date_index+=1
            if not super().check_data_exist(path):
                data_list = []
                stock_list_now = stock_list.iloc[:,stock_date_index].tolist()
                for stock_ in stock_list_now:
                    rs_profit = bs.query_profit_data(code=stock_, year=int(date_[0:4]),quarter = super().transfer_session_to_quarter(date_[5:7]))
                    while (rs_profit.error_code == '0') & rs_profit.next():
                        data_list.append(rs_profit.get_row_data())
                result_profit = pd.DataFrame(data_list, columns=rs_profit.fields)
                super().save_data(result_profit,path)
                result_profit[0] = [code[3:9] for code in result_profit[0]]
                result_profit.insert(loc = 0, column = 'date',value = datetime.datetime.strptime(date_, "%Y-%m-%d"))
                self.query_profit_data = self.query_profit_data.append(result_profit)
            else:
                result_profit = super().read_data(path)
                result_profit[0] = [code[3:9] for code in result_profit[0]]
                result_profit.insert(loc = 0, column = 'date',value = datetime.datetime.strptime(date_, "%Y-%m-%d"))
                self.query_profit_data = self.query_profit_data.append(result_profit)
        bs.logout()
        self.query_profit_data=self.query_profit_data.set_index(['date',0])
        pass
    pass