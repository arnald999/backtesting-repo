import matplotlib.pyplot as plt


def calculate_traditional_rsi(df, window=14):
    try:
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        df['Traditional_RSI'] = rsi
        return df
    except Exception as e:
        print(f"Error calculating Traditional RSI: {e}")
        return None


def calculate_wilders_rsi(df, window=14):
    try:
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).ewm(alpha=1 / window, adjust=False).mean()
        loss = (-delta.where(delta < 0, 0)).ewm(alpha=1 / window, adjust=False).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        df['Wilders_RSI'] = rsi
        return df
    except Exception as e:
        print(f"Error calculating Wilder's RSI: {e}")
        return None


def calculate_modified_rsi(df, window=14):
    try:
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).ewm(alpha=1 / window, adjust=False).mean()
        loss = (-delta.where(delta < 0, 0)).ewm(alpha=1 / window, adjust=False).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        smoothed_rsi = rsi.ewm(alpha=1 / window, adjust=False).mean()

        df['Modified_RSI'] = smoothed_rsi
        return df
    except Exception as e:
        print(f"Error calculating Modified RSI: {e}")
        return None


def plot_rsis(df, save_path=None):
    try:
        plt.figure(figsize=(12, 8))

        # Plot Close Price
        plt.plot(df['timestamp'], df['close'], label='Close Price', color='blue')

        # Plot RSI
        plt.plot(df['timestamp'], df['Traditional_RSI'], label='Traditional RSI', color='orange')
        plt.plot(df['timestamp'], df['Wilders_RSI'], label="Wilder's RSI", color='green')
        plt.plot(df['timestamp'], df['Modified_RSI'], label='Modified RSI', color='red')

        plt.title('Relative Strength Index (RSI)')
        plt.xlabel('Timestamp')
        plt.ylabel('Price / RSI')
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
