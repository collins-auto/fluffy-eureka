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

# Format raw string retrieved from website for processing 
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
   
#Empty dictionary to contain stock price and date 
    data = {"Date": [],
            "Price": []}

#Append stock data to dictionary    
    for b in bb:
        data["Date"].append(b.split(",")[0])
        data["Price"].append(b.split(",")[1])

#Convert dictionary to dataframs        
    df = pd.DataFrame(data)

#Change date from string to datetime object
    df["Date"] = pd.to_datetime(df["Date"])
    df.set_index("Date", inplace=True)

#Change prices from string to float to enable mathematical operations 
    df["Price"] = df["Price"].str.replace(",", "")
    df["Price"] = df["Price"].astype(float)

#Resample dataframe to show prices for specified intervals (i.e. "1D", "1M", "1Y")    
    df = df.resample(interval).ffill()
    
#Slice dataframe to present stock prices for specified dates
    df = df.loc[start:stop]
    
    print("Successful")
    
    return df



#Get stock data for list of tickers
def get_stocks(tickers, start, stop, interval="1D"):
    pf = pd.DataFrame()
    
    for t in tickers:
        pf[t] = get_data(t, start, stop, interval)
    
    return pf


#Get stocks with highest returns for a specific date period
def highest_ngx_returns(ticker_list,top_no, start, stop):

    stock_returns = {}

    for t in ticker_list:
        stock = get_data(t, start, stop)
        returns = stock.pct_change().dropna(how="all")

#Calculate compounded annual growth rate
        CAGR = (1+returns).prod() ** (252 / returns.count()) - 1

        stock_returns[t] = CAGR[0]

#Sort returns from highest to lowest        
    stock_returns = sorted(stock_returns.items(), key=lambda x:x[1], reverse=True)
    stock_returns = dict(stock_returns)

#List of top n performing stocks for the period
    top_list = [stock for stock in stock_returns][:top_no]
        
    return top_list

#Get other details about stocks including Market Capitalization and sector
def stock_info(ticker):
    url = "https://afx.kwayisi.org/ngx/" + ticker
    response = requests.get(url)

    soup = bs(response.text)

    valuation = soup.find_all("table")[1]
    v2 = valuation.find_all("tr")[-2]
    market_cap = v2.find_all("td")[-1].text

    if market_cap[-1] == "T":
        market_cap = float(market_cap[:-1]) * 1000000000000

    elif market_cap[-1] == "B":
        market_cap = float(market_cap[:-1]) * 1000000000

    elif market_cap[-1] == "M":
        market_cap = float(market_cap[:-1]) * 1000000
        
    tables = soup.find_all("div", class_="t")
    sector = tables[3].find_all("dd")[0].text

    return {"Ticker": ticker,  "Sector": sector, "Market Cap": market_cap}
