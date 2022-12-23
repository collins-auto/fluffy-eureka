import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from datetime import datetime
from datetime import date
import plotly.express as px

#funtion takes in parameters:dataframe, number of predictions, and period or number of years of forecast
def monte_carlo(dataframe, preds, period):
    
    #Calculate log returns, mean of returns, variance, and standard deviation
    log_returns = np.log(dataframe).diff()
    u = log_returns.mean()
    var = log_returns.var()
    drift = u - (0.5 * var)
    stdev = log_returns.std()
    
    #Get list dates of working days for the forecast period
    dates = pd.bdate_range(start=str(dataframe.index[-1]), end=str(dataframe.index[-1] + datetime.timedelta(days=365*period))).to_list()
    
    pred = preds
    t_intervals = len(dates)
    
    #Calculate daily returns using stochastic differential equation
    daily_returns = np.exp(drift.values + stdev.values * norm.ppf(np.random.rand(t_intervals, pred)))
    
    #Create empty array and assign current price to first row of array
    S0 = dataframe.iloc[-1]
    price_list = np.zeros_like(daily_returns)
    price_list[0] = S0
    
    #Calculate price predictions
    for t in range(1, t_intervals):
        price_list[t] = price_list[t - 1] * daily_returns[t]
        
    price_df = pd.DataFrame(price_list)
    

    for i in range(len(dates)):
        dates[i] = str(dates[i])[:-9]
        
    price_df.index = dates
    
    
    for i in range(len(price_df.columns)):
        price_df.rename(columns={i: "Pred"+str(i+1)}, inplace=True)
        
    
    forecast = pd.concat([dataframe, price_df])
    
    forecast.index = pd.to_datetime(forecast.index)
    
    
    legend = list(price_df.columns.values)
    legend.insert(0, "Historical Data")
    
    #Visualize forecast
    fig = px.line(forecast, labels={"index": "Date", "value": "Price"})
    fig.show()
    
    print(f"Expected Price: ₦{round(forecast.iloc[-1].mean(), 2)} +/- ₦{round(forecast.iloc[-1].std(), 2)}")
