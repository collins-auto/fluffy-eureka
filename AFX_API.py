import requests
import pandas as pd
import re
import numpy as np
from datetime import datetime

# retrieve stock data, date format: yyyy-mm-dd
def get_data(ticker, start, stop, interval="1D"):
    url = "https://afx.kwayisi.org/chart/ngx/" + ticker
    r = requests.get(url)
    js = r.text
    
    bb = re.split("data:", js)[1]
    bb = bb[1:-9]
    bb = bb.split("],")
    
    for i in range(len(bb)):
        bb[i] = bb[i].replace(r"[", "")
        bb[i] = bb[i].replace(r"]", "")
        bb[i] = bb[i].replace("d", "")
        bb[i] = bb[i].replace(r"(", "")
        bb[i] = bb[i].replace(r")", "")
        bb[i] = bb[i].replace(r'"', '')
    
    data = {"Date": [],
            "Price": []}
    
    for b in bb:
        data["Date"].append(b.split(",")[0])
        data["Price"].append(b.split(",")[1])
        
    df = pd.DataFrame(data)
    df["Date"] = pd.to_datetime(df["Date"])
    df.set_index("Date", inplace=True)
    df["Price"] = df["Price"].str.replace(",", "")
    df["Price"] = df["Price"].astype(float)
    
    df = df.resample(interval).ffill()
    
    df = df.loc[start:stop]
    
    print("Successful")
    
    return df




def get_stocks(tickers, start, stop):
    pf = pd.DataFrame()
    
    for t in tickers:
        pf[t] = get_data(t, start, stop)
    
    return pf



def highest_ngx_returns(ticker_list,top_no, start, stop):

    stock_returns = {}

    for t in ticker_list:
        stock = get_data(t, start, stop)
        returns = stock.pct_change().dropna(how="all")
        CAGR = (1+returns).prod() ** (252 / returns.count()) - 1

        stock_returns[t] = CAGR[0]
        
    stock_returns = sorted(stock_returns.items(), key=lambda x:x[1], reverse=True)
    stock_returns = dict(stock_returns)
    top_list = [stock for stock in stock_returns][:top_no]
        
    return top_list
