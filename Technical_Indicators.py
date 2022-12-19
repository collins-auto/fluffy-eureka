import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



def ema(dataframe, ema_size):
    ema_name = "ema_" + str(ema_size)
    multiplier = 2/(ema_size + 1)
    initial_mean = dataframe["Price"].head(ema_size).mean()
    
    gg = dataframe.index
    
    for i in range(len(dataframe)):
        if i == ema_size:
            dataframe.loc[gg[i], ema_name] = initial_mean
        elif i > ema_size:
            ema_value = dataframe.loc[gg[i], 'Price'] * multiplier + dataframe.loc[gg[i-1], ema_name]*(1-multiplier)
            dataframe.loc[gg[i], ema_name] = ema_value
        else:
            dataframe.loc[gg[i], ema_name] = None


def ema_analysis(dataframe, timeperiod):
    gg = dataframe.index
    
    if timeperiod == "Long":
        ema(dataframe, 50)
        ema(dataframe, 200)
        
        for i in range(len(dataframe)):
            if dataframe.loc[gg[i], "Price"] > dataframe.loc[gg[i], "ema_50"]:
                dataframe.loc[gg[i], "Signal"] = "Buy"
            elif dataframe.loc[gg[i], "Price"] < dataframe.loc[gg[i], "ema_50"]:
                dataframe.loc[gg[i], "Signal"] = "Sell"
    
    elif timeperiod == "Short":
        ema(dataframe, 9)
        ema(dataframe, 13)

        for i in range(len(dataframe)):
            if dataframe.loc[gg[i], "Price"] > dataframe.loc[gg[i], "ema_9"]:
                dataframe.loc[gg[i], "Signal"] = "Buy"
            elif dataframe.loc[gg[i], "Price"] < dataframe.loc[gg[i], "ema_9"]:
                dataframe.loc[gg[i], "Signal"] = "Sell"
                
    else:
        return "Enter timeperiod Short or Long"
    
    dataframe.plot(figsize=(14, 6))




def bollinger_bands(dataframe, rate):
    dataframe.index = np.arange(dataframe.shape[0])
    
    sma = dataframe.rolling(rate).mean()
    std = dataframe.rolling(rate).std()
    
    bol_up = sma + std * 2
    bol_down = sma - std * 2
    
    plt.title('Bollinger Bands')
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.plot(dataframe, label='Prices')
    plt.plot(bol_up, label='Bollinger up', c='r')
    plt.plot(bol_down, label='Bollinger down', c='r')
    plt.legend()
    plt.show()
