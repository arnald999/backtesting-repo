import matplotlib.pyplot as plt


def calculate_macd(df, short_window=12, long_window=26, signal_window=9):
    short_window_key = 'EMA_' + str(short_window)
    long_window_key = 'EMA_' + str(long_window)

    # Calculate the short-term EMA
    df[short_window_key] = df['close'].ewm(span=short_window, adjust=False).mean()

    # Calculate the long-term EMA
    df[long_window_key] = df['close'].ewm(span=long_window, adjust=False).mean()

    # Calculate the MACD line
    df['MACD'] = df[short_window_key] - df[long_window_key]

    # Calculate the signal line
    df['Signal Line'] = df['MACD'].ewm(span=signal_window, adjust=False).mean()

    # Calculate the MACD histogram
    df['MACD Histogram'] = df['MACD'] - df['Signal Line']

    return df


def plot_macd(df, save_path=None):
    try:
        # Plot MACD and Signal Line
        plt.figure(figsize=(12, 8))

        plt.subplot(2, 1, 1)
        plt.plot(df['timestamp'], df['close'], label='Close Price', color='blue')
        plt.title('Close Price')
        plt.legend(loc='upper left')

        plt.subplot(2, 1, 2)
        plt.plot(df['timestamp'], df['MACD'], label='MACD', color='red')
        plt.plot(df['timestamp'], df['Signal Line'], label='Signal Line', color='blue')
        plt.bar(df['timestamp'], df['MACD Histogram'], label='MACD Histogram', color='grey', alpha=0.3)
        plt.title('MACD')
        plt.legend(loc='upper left')

        plt.tight_layout()
        if save_path:
            plt.savefig(save_path)
            print(f"MACD plot saved as {save_path}")
        else:
            plt.show()
        print("MACD plot generated successfully")
    except Exception as e:
        print(f"Error plotting MACD: {e}")
