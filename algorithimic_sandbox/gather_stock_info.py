import yfinance as yf
import pandas as pd


def get_money_closing(ticket, timeframe="3mo"):
    # Fetch historical data for the past 1 year
    sp500 = yf.Ticker(ticket)
    sp500_history = sp500.history(period=timeframe)

    # Extract closing prices and their corresponding dates
    closing_prices = sp500_history["Close"]
    dates = sp500_history.index

    # Create a DataFrame with Date and Close columns
    data = pd.DataFrame({"Date": dates, "Close": closing_prices})

    # Save the DataFrame to a CSV file
    data.to_csv("algorithimic_sandbox\historical_data.csv", index=False)

    print("Data saved to 'historical_data.csv'.")

