from gather_stock_info import get_money_closing
from strat_moving_average_Xover import moving_average_crossover, moving_average_graph
from strat_mean_reversion import mean_reversion, mean_reversion_graph
from strat_ml_ensemble_methods import ml_ensamble
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # Load data from CSV file
    data = pd.read_csv('algorithimic_sandbox/historical_data.csv')

    # Check if data is loaded correctly
    if data is not None:
        print("Data loaded successfully:")
        print(data.head())  # Print first few rows of data for verification

        # Convert 'Date' column to datetime object if needed
        data['Date'] = pd.to_datetime(data['Date'])
        """
       Moving Average Crossover Strategy
        """
        # Apply the moving average crossover strategy
        #data = moving_average_crossover(data, short_window=50, long_window=200)

        #moving_average_graph(data, short_window=50, long_window=200)
        """
       Mean Reversion Strategy
        """
       # data = mean_reversion(data, window=20, threshold=1.0)
       # mean_reversion_graph(data, threshold=1.0)

        """
       ML Ensemble Strategy
        """
        ml_ensamble(data)

    else:
        print("Error: Failed to load data from CSV file.")
