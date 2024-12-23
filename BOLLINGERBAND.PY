import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

# Fetch Bitcoin data
def fetch_bitcoin_data(start_date, end_date):
    try:
        bitcoin_data = yf.download("BTC-USD", start=start_date, end=end_date)
        if bitcoin_data.empty:
            print("No data found for the specified ticker and date range.")
        else:
            print(f"Data fetched successfully: {len(bitcoin_data)} records.")
        return bitcoin_data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

# Calculate Bollinger Bands
def calculate_bollinger_bands(data, window=20):
    data['SMA'] = data['Close'].rolling(window=window).mean()
    data['StdDev'] = data['Close'].rolling(window=window).std()
    data['Upper_Band'] = data['SMA'] + (2 * data['StdDev'])
    data['Lower_Band'] = data['SMA'] - (2 * data['StdDev'])
    print("Bollinger Bands calculated successfully.")
    return data

# Plot Bollinger Bands
def plot_bollinger_bands(data, ticker):
    if 'Upper_Band' not in data or data['Upper_Band'].isnull().all():
        print("Bollinger Bands data is not available for plotting.")
        return

    plt.figure(figsize=(14, 7))
    plt.plot(data['Close'], label="Closing Price", color='blue', linewidth=1)
    plt.plot(data['Upper_Band'], label="Upper Band", color='orange', linestyle='--', linewidth=1)
    plt.plot(data['SMA'], label="SMA (20)", color='green', linestyle='-', linewidth=1)
    plt.plot(data['Lower_Band'], label="Lower Band", color='red', linestyle='--', linewidth=1)
    plt.fill_between(data.index, data['Lower_Band'], data['Upper_Band'], color='grey', alpha=0.1)
    plt.title(f"Bollinger Bands for {ticker}")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.legend(loc="best")
    plt.grid()
    plt.tight_layout()
    plt.show()

# Main Script
if __name__ == "__main__":
    # Define date range
    start_date = "2023-01-01"
    end_date = "2023-12-31"

    # Fetch data for Bitcoin
    bitcoin_data = fetch_bitcoin_data(start_date, end_date)
    if bitcoin_data is None or bitcoin_data.empty:
        print("Error: No data fetched for Bitcoin.")
    else:
        print(bitcoin_data.head())  # Verify data
        bitcoin_data = calculate_bollinger_bands(bitcoin_data)
        plot_bollinger_bands(bitcoin_data, "Bitcoin (BTC-USD)")

