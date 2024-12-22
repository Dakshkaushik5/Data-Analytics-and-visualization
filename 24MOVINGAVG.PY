import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

# Fetch Kotak Mahindra stock data
def fetch_kotakmahindra_data(start_date, end_date):
    try:
        kotak_data = yf.download("KOTAKBANK.BO", start=start_date, end=end_date, interval="1h")
        if kotak_data.empty:
            print("No data found for the specified ticker and date range.")
        else:
            print(f"Data fetched successfully: {len(kotak_data)} records.")
        return kotak_data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

# Calculate 24-hour Moving Volume Average
def calculate_24hr_moving_volume(data):
    data['24H_Moving_Volume'] = data['Volume'].rolling(window=24).mean()  # 24-hour moving volume average
    print("24-hour Moving Volume Average calculated successfully.")
    return data

# Plot with Cursor Interactivity
def plot_volume_and_price_with_cursor(data, ticker):
    if '24H_Moving_Volume' not in data or data['24H_Moving_Volume'].isnull().all():
        print("24-hour Moving Volume Average data is not available for plotting.")
        return

    # Create a dual-axis plot
    fig, ax1 = plt.subplots(figsize=(14, 7))

    # Plot Closing Price on primary Y-axis
    line1, = ax1.plot(data.index, data['Close'], label="Closing Price", color='blue', linewidth=1.5)
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Price (INR)", color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.legend(loc="upper left")

    # Plot 24-hour Moving Volume Average on secondary Y-axis
    ax2 = ax1.twinx()
    line2, = ax2.plot(data.index, data['24H_Moving_Volume'], label="24-Hour Moving Volume Avg", color='red', linewidth=1.5, linestyle='--')
    ax2.set_ylabel("Volume", color='red')
    ax2.tick_params(axis='y', labelcolor='red')
    ax2.legend(loc="upper right")

    # Cursor Interactivity
    cursor_text = plt.text(0.02, 0.95, "", transform=plt.gcf().transFigure, fontsize=10, bbox=dict(facecolor='white', alpha=0.8))

    def on_mouse_move(event):
        if event.inaxes == ax1 or event.inaxes == ax2:
            # Find the closest index
            x_index = int(round(event.xdata))
            if 0 <= x_index < len(data):
                price = data['Close'].iloc[x_index]
                volume = data['24H_Moving_Volume'].iloc[x_index]
                cursor_text.set_text(f"Price: {price:.2f} INR\n24H Avg Volume: {volume:.2f}")
                cursor_text.set_position((event.x, event.y))
                plt.draw()

    plt.connect('motion_notify_event', on_mouse_move)
    plt.title(f"24-Hour Moving Volume Average with Price for {ticker}")
    plt.grid()
    plt.tight_layout()
    plt.show()

# Main Script
if __name__ == "__main__":
    # Define date range
    start_date = "2023-01-01"
    end_date = "2023-12-31"

    # Fetch data for Kotak Mahindra Bank
    kotak_data = fetch_kotakmahindra_data(start_date, end_date)
    if kotak_data is None or kotak_data.empty:
        print("Error: No data fetched for Kotak Mahindra Bank.")
    else:
        print(kotak_data.head())  # Verify data
        kotak_data = calculate_24hr_moving_volume(kotak_data)
        plot_volume_and_price_with_cursor(kotak_data, "Kotak Mahindra Bank (KOTAKBANK.BO)")

