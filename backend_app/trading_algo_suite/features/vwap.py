import matplotlib.pyplot as plt


def calculate_standard_vwap(df):
    df['typical_price'] = (df['high'] + df['low'] + df['close']) / 3
    df['cum_typical_price_volume'] = (df['typical_price'] * df['volume']).cumsum()
    df['cum_volume'] = df['volume'].cumsum()
    df['vwap'] = df['cum_typical_price_volume'] / df['cum_volume']
    return df


def calculate_rolling_vwap(df, window):
    df['typical_price'] = (df['high'] + df['low'] + df['close']) / 3
    df['rolling_typical_price_volume'] = df['typical_price'] * df['volume']
    df['rolling_vwap'] = df['rolling_typical_price_volume'].rolling(window=window).sum() / df['volume'].rolling(
        window=window).sum()
    return df


def calculate_intraday_vwap(df):
    df['typical_price'] = (df['high'] + df['low'] + df['close']) / 3
    df['date'] = df['timestamp'].dt.date
    df['cum_typical_price_volume'] = df.groupby('date')['typical_price'].transform(
        lambda x: (x * df['volume']).cumsum())
    df['cum_volume'] = df.groupby('date')['volume'].transform(lambda x: x.cumsum())
    df['intraday_vwap'] = df['cum_typical_price_volume'] / df['cum_volume']
    return df


def visualize_vwaps(df, save_path=None):
    plt.figure(figsize=(14, 10))

    # Plot close prices
    plt.plot(df['timestamp'], df['close'], label='Close Price', color='blue', linewidth=0.8)

    # Plot Standard VWAP
    plt.plot(df['timestamp'], df['vwap'], label='Standard VWAP', color='orange', linewidth=0.8)

    # Plot Rolling VWAP
    plt.plot(df['timestamp'], df['rolling_vwap'], label=f'Rolling VWAP', color='green', linewidth=0.8)

    # Plot Intraday VWAP
    plt.plot(df['timestamp'], df['intraday_vwap'], label='Intraday VWAP', color='red', linewidth=0.8)

    # Customize the plot
    plt.title('Close Price and Different VWAPs')
    plt.xlabel('Timestamp')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Show the plot

    # Save or show the plot
    if save_path:
        plt.savefig(save_path)
        print(f"Plot saved as {save_path}")
    else:
        plt.show()
