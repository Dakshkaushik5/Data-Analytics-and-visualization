import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Fetch MRF stock data
def fetch_mrf_data(start_date, end_date):
    try:
        mrf_data = yf.download("MRF.BO", start=start_date, end=end_date)
        if mrf_data.empty:
            print("No data found for the specified ticker and date range.")
        else:
            print(f"Data fetched successfully: {len(mrf_data)} records.")
        return mrf_data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

# Calculate RSI
def calculate_rsi(data, period=14):
    if len(data) < period:
        print(f"Insufficient data to calculate RSI. At least {period} records are required.")
        return data
    delta = data['Close'].diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    data['RSI'] = rsi
    print("RSI calculated successfully.")
    return data

# Plot RSI and Price
def plot_rsi(data, ticker):
    if 'RSI' not in data or data['RSI'].isnull().all():
        print("RSI data is not available for plotting.")
        return

    plt.figure(figsize=(12, 6))

    # Subplot for closing price
    plt.subplot(2, 1, 1)
    plt.plot(data['Close'], label=f"{ticker} Close Price", color='blue')
    plt.title(f"{ticker} Closing Price")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid()

    # Subplot for RSI
    plt.subplot(2, 1, 2)
    plt.plot(data['RSI'], label="RSI", color='purple')
    plt.axhline(70, color='red', linestyle='--', label="Overbought (70)")
    plt.axhline(30, color='green', linestyle='--', label="Oversold (30)")
    plt.title("Relative Strength Index (RSI)")
    plt.xlabel("Date")
    plt.ylabel("RSI Value")
    plt.legend()
    plt.grid()

    plt.tight_layout()
    plt.show()

# Main Script
if __name__ == "__main__":
    start_date = "2022-01-01"
    end_date = "2023-01-01"

    mrf_data = fetch_mrf_data(start_date, end_date)
    if mrf_data is not None and not mrf_data.empty:
        mrf_data = calculate_rsi(mrf_data)
        plot_rsi(mrf_data, "MRF")
