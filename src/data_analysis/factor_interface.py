import pandas as pd 
import factor_lib
from datetime import datetime

##########data dict############
# 0: operating_profit_per_share
# 1: net_asset_per_share
# 2: financial_expense_rate
# 3: long_term_debt_to_asset_ratio
# 4: cash_flow_to_price_ratio
#######################
factor_function = [
    factor_lib.operating_profit_per_share.OperatingProfitPerShare,
    factor_lib.net_asset_per_share,
    factor_lib.financial_expense_rate,
    factor_lib.long_term_debt_to_asset_ratio,
    factor_lib.cash_flow_to_price_ratio
]

def get_factor_data(factor_index,start_date,end_date):
    if factor_index >= len(factor_function):
        print("index out of range")
        return 
    factor = factor_function[factor_index]()
    return factor.get_factor(start_date,end_date);


def factor_workflow(start_date,end_date):
    get_factor_data(0,start_date,end_date)
    pass

def get_factor(factor_index,start_date,end_date):

    pass

def calculate_factor_IR(data):
    
    pass

def calculate_factor_IC(data):
    
    pass

def remove_extremum(data,used_method):

    pass

def data_normalized(data,used_method):

    pass

def data_filled(data,used_method):

    pass

def data_neutralize(data,used_method):

    pass

start = datetime(2010,1,1)
end = datetime(2020,1,1)
factor_workflow(start,end)