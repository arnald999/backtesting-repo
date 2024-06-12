import numpy as np
import matplotlib.pyplot as plt


def calculate_sma(df, window):
    # Calculate Simple Moving Average (SMA)
    df[f'SMA_{window}'] = df['close'].rolling(window=window).mean()
    return df


def calculate_ema(df, window):
    # Calculate Exponential Moving Average (EMA)
    df[f'EMA_{window}'] = df['close'].ewm(span=window, adjust=False).mean()
    return df


def calculate_wma(df, window):
    # Calculate Weighted Moving Average (WMA)
    weights = np.arange(1, window + 1)

    def wma(values):
        return np.dot(values, weights) / weights.sum()

    df[f'WMA_{window}'] = df['close'].rolling(window=window).apply(wma, raw=True)
    return df


def plot_moving_averages(df, moving_averages=[], save_path=None):
    try:
        # Plot Price
        plt.figure(figsize=(12, 8))
        plt.plot(df['timestamp'], df['close'], label='Close Price', color='blue')

        # Plot Moving Averages
        for ma in moving_averages:
            if ma in df.columns:
                plt.plot(df['timestamp'], df[ma], label=ma, alpha=0.8)

        plt.title('Price with Moving Averages')
        plt.xlabel('Timestamp')
        plt.ylabel('Price')
        plt.legend()
        plt.grid(True)

        # Save or Show Plot
        if save_path:
            plt.savefig(save_path)
            print(f"Plot saved as {save_path}")
        else:
            plt.show()

        print("Plot generated successfully")

    except Exception as e:
        print(f"Error plotting: {e}")
