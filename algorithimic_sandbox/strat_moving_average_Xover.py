from gather_stock_info import get_money_closing
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Define the moving average in the crossover strategy
def moving_average_crossover(data, short_window, long_window):
    # Compute the short-term and long-term moving averages
    data['Short_MA'] = data['Close'].rolling(window=short_window, min_periods=1).mean()
    data['Long_MA'] = data['Close'].rolling(window=long_window, min_periods=1).mean()

    # Generate trading signals
    data['Signal'] = np.where(data['Short_MA'] > data['Long_MA'], 1, -1)
    data['Position'] = data['Signal'].diff()
    
    return data

def moving_average_graph(data, short_window, long_window):
    if data is not None:
                # Plot the data
        plt.figure(figsize=(15, 6))
        plt.plot(data['Date'], data['Close'], label='Price')
        plt.plot(data['Date'], data['Short_MA'], label=f'{short_window}-day MA')
        plt.plot(data['Date'], data['Long_MA'], label=f'{long_window}-day MA')
        plt.title('Moving Average Crossover Strategy')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.show()
    else:
        print("Error: Failed to load data from CSV file.")
