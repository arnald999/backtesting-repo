import matplotlib.pyplot as plt


def calculate_standard_twap(df):
    df['time_weighted_price'] = df['close']
    df['cum_time_weighted_price'] = df['time_weighted_price'].expanding().mean()
    df['twap'] = df['cum_time_weighted_price']
    return df


def calculate_rolling_twap(df, window):
    df['time_weighted_price'] = df['close']
    df['rolling_twap'] = df['time_weighted_price'].rolling(window=window).mean()
    return df


def calculate_intraday_twap(df):
    df['time_weighted_price'] = df['close']
    df['date'] = df['timestamp'].dt.date
    df['intraday_twap'] = df.groupby('date')['time_weighted_price'].transform(lambda x: x.expanding().mean())
    return df


def visualize_twaps(df, save_path=None):
    """
    Function to visualize different TWAPs on a single plot.

    Parameters:
    df (pandas.DataFrame): DataFrame containing columns 'timestamp', 'close', 'twap', 'rolling_twap', 'intraday_twap'.
    """
    plt.figure(figsize=(14, 10))

    # Plot close prices
    plt.plot(df['timestamp'], df['close'], label='Close Price', color='blue', linewidth=0.8)

    # Plot Standard TWAP
    plt.plot(df['timestamp'], df['twap'], label='Standard TWAP', color='orange', linewidth=0.8)

    # Plot Rolling TWAP
    plt.plot(df['timestamp'], df['rolling_twap'], label=f'Rolling TWAP', color='green', linewidth=0.8)

    # Plot Intraday TWAP
    plt.plot(df['timestamp'], df['intraday_twap'], label='Intraday TWAP', color='red', linewidth=0.8)

    # Customize the plot
    plt.title('Close Price and Different TWAPs')
    plt.xlabel('Timestamp')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
        print(f"Plot saved as {save_path}")
    else:
        plt.show()
