import numpy as np
import matplotlib.pyplot as plt


def calculate_traditional_obv(df):
    try:
        df['OBV'] = (np.sign(df['close'].diff()) * df['volume']).fillna(0).cumsum()
        return df
    except Exception as e:
        print(f"Error calculating Traditional OBV: {e}")
        return None


def calculate_cumulative_obv(df):
    try:
        df['Cumulative_OBV'] = (np.sign(df['close'].diff()) * df['volume']).cumsum()
        return df
    except Exception as e:
        print(f"Error calculating Cumulative OBV: {e}")
        return None


def calculate_smoothed_obv(df, window=14):
    try:
        df['OBV'] = (np.sign(df['close'].diff()) * df['volume']).fillna(0).cumsum()
        df['Smoothed_OBV'] = df['OBV'].ewm(span=window, adjust=False).mean()
        return df
    except Exception as e:
        print(f"Error calculating Smoothed OBV: {e}")
        return None


def plot_obvs(df, save_path=None):
    try:
        plt.figure(figsize=(12, 8))

        # Plot Close Price
        plt.subplot(2, 1, 1)
        plt.plot(df['timestamp'], df['close'], label='Close Price', color='blue')
        plt.title('Close Price and On-Balance Volume (OBV)')
        plt.xlabel('Timestamp')
        plt.ylabel('Close Price')
        plt.legend()
        plt.grid(True)

        # Plot OBVs
        plt.subplot(2, 1, 2)
        plt.plot(df['timestamp'], df['OBV'], label='Traditional OBV', color='orange')
        plt.plot(df['timestamp'], df['Cumulative_OBV'], label='Cumulative OBV', color='green')
        plt.plot(df['timestamp'], df['Smoothed_OBV'], label='Smoothed OBV', color='red')
        plt.xlabel('Timestamp')
        plt.ylabel('OBV')
        plt.legend()
        plt.grid(True)

        # Adjust layout to prevent overlap
        plt.tight_layout()

        # Save or show the plot
        if save_path:
            plt.savefig(save_path)
            print(f"Plot saved as {save_path}")
        else:
            plt.show()

        print("Plot generated successfully")

    except Exception as e:
        print(f"Error plotting: {e}")
