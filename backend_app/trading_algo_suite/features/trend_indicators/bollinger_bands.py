import matplotlib.pyplot as plt


def calculate_bollinger_bands(df, window=20, num_std_dev=2):
    # Traditional Bollinger Bands using SMA
    df['Middle Band'] = df['close'].rolling(window=window).mean()
    df['Standard Deviation'] = df['close'].rolling(window=window).std()
    df['Upper Band'] = df['Middle Band'] + (df['Standard Deviation'] * num_std_dev)
    df['Lower Band'] = df['Middle Band'] - (df['Standard Deviation'] * num_std_dev)
    return df


def calculate_exponential_bollinger_bands(df, window=20, num_std_dev=2):
    # Bollinger Bands using EMA
    df['Middle Band EMA'] = df['close'].ewm(span=window, adjust=False).mean()
    df['Standard Deviation EMA'] = df['close'].ewm(span=window, adjust=False).std()
    df['Upper Band EMA'] = df['Middle Band EMA'] + (df['Standard Deviation EMA'] * num_std_dev)
    df['Lower Band EMA'] = df['Middle Band EMA'] - (df['Standard Deviation EMA'] * num_std_dev)
    return df


def calculate_percentage_bollinger_bands(df, window=20, percentage=0.1):
    # Percentage Bollinger Bands
    df['Middle Band'] = df['close'].rolling(window=window).mean()
    df['Upper Band Percentage'] = df['Middle Band'] * (1 + percentage)
    df['Lower Band Percentage'] = df['Middle Band'] * (1 - percentage)
    return df


def calculate_asymmetric_bollinger_bands(df, window=20, upper_std_dev=2, lower_std_dev=1.5):
    # Bollinger Bands with different deviations
    df['Middle Band'] = df['close'].rolling(window=window).mean()
    df['Standard Deviation'] = df['close'].rolling(window=window).std()
    df['Upper Band Asymmetric'] = df['Middle Band'] + (df['Standard Deviation'] * upper_std_dev)
    df['Lower Band Asymmetric'] = df['Middle Band'] - (df['Standard Deviation'] * lower_std_dev)
    return df


def plot_multiple_bollinger_bands(df_list, window_list=[20], num_std_list=[2], legend_labels=None, save_path=None):
    try:
        plt.figure(figsize=(12, 8))

        # Plot Price
        plt.plot(df_list[0]['timestamp'], df_list[0]['close'], label='Close Price', color='blue')

        # Plot Bollinger Bands
        for i, df in enumerate(df_list):
            window = window_list[i] if len(window_list) > i else window_list[-1]  # Use last value if not specified
            num_std = num_std_list[i] if len(num_std_list) > i else num_std_list[-1]  # Use last value if not specified
            legend_label = legend_labels[i] if legend_labels and len(
                legend_labels) > i else f'Bollinger Bands ({window}, {num_std} std)'

            rolling_mean = df['close'].rolling(window=window).mean()
            rolling_std = df['close'].rolling(window=window).std()
            upper_band = rolling_mean + (rolling_std * num_std)
            lower_band = rolling_mean - (rolling_std * num_std)

            plt.plot(df['timestamp'], upper_band, label=f'Upper {legend_label}', linestyle='--')
            plt.plot(df['timestamp'], lower_band, label=f'Lower {legend_label}', linestyle='--')

        plt.title('Multiple Bollinger Bands')
        plt.xlabel('Timestamp')
        plt.ylabel('Price')
        plt.legend()
        plt.grid(True)

        # Save or show the plot
        if save_path:
            plt.savefig(save_path)
            print(f"Plot saved as {save_path}")
        else:
            plt.show()

        print("Plot generated successfully")

    except Exception as e:
        print(f"Error plotting: {e}")
