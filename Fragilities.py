

import pandas as pd
import numpy as np
from blp import blp
import datetime 
import matplotlib.pyplot as plt



startDate = '20050102'
endDate = datetime.date.today().strftime('%Y%m%d')


ticker_rates = ['G1O2 Index']
ticker_eq = ["SPX Index"]

def import_data(start_date, end_date, tickers, fields):
    
    bquery = blp.BlpQuery().start()
    df_pull = bquery.bdh(tickers, fields,
                         start_date=start_date, end_date=end_date,)
    
    return df_pull

def calc_frag(ticker):
    
    df_data = import_data(startDate, endDate, ticker, ['PX_Last'])
    
    df_data.set_index("date", inplace=True)
    df_data = df_data.drop('security', axis=1)
    
    df_data["weekly_return"] = df_data["PX_Last"].pct_change(periods=1)
    
    df_data["rolling_kurtosis"] = df_data["weekly_return"].rolling(window=252).kurt()
    
    return df_data


df_rates = calc_frag(ticker_rates)
df_eq = calc_frag(ticker_eq)


plt.figure(figsize=(10, 6))
plt.plot(df_rates.index, df_rates["rolling_kurtosis"])
plt.title("Rolling 1-Year Kurtosis of US Equities")
plt.axhline(y=0, color='black', linestyle='-')
plt.xlabel("Date")
plt.ylabel("Kurtosis")
plt.show()