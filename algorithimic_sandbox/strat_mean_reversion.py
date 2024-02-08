import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#define the mean reversion strategy

def mean_reversion(data, window, threshold):
    data['Mean'] = data['Close'].rolling(window=window, min_periods=1).mean()
    
    data['Std'] = data['Close'].rolling(window=window, min_periods=1).std()

    data['ZScore'] =(data['Close']-data['Mean'])/data['Std']

    #denerate trading signals

    data['Signal'] = np.where(data['ZScore'] >threshold, -1, np.where(data['ZScore'] < -threshold, 1, 0))

    data['Position'] = data['Signal'].diff()

    return data

def mean_reversion_graph(data, threshold):
    if data is not None:
                # Plot the data
        plt.figure(figsize=(15, 6))
        plt.plot(data['Date'], data['Close'], label='Price')
        plt.plot(data['Date'], data['Mean'], label='Mean')

        plt.axhline(threshold, color='r', linestyle='--', label='Upper Threshold')
        plt.axhline(-threshold, color='g', linestyle='--', label='Lower Threshold')

        plt.title('Mean Reversion Strategy')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.show()
    else:
        print("Error: Failed to load data from CSV file.")
