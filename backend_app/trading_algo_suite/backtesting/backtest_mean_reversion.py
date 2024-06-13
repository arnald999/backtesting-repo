import pandas as pd
import matplotlib.pyplot as plt


def backtest_mean_reversion_strategy(data, initial_balance=10000, amount=1):
    balance = initial_balance
    position = 0
    balance_history = []

    for index, row in data.iterrows():
        if row['position'] == 1 and position == 0:  # Buy signal
            position = amount
            entry_price = row['close']
            balance -= entry_price * amount
        elif row['position'] == -1 and position == amount:  # Sell signal
            position = 0
            exit_price = row['close']
            balance += exit_price * amount

        balance_history.append({'timestamp': index, 'balance': balance + position * row['close']})

    return pd.DataFrame(balance_history)


def plot_balance(backtest_results, save_path=None):
    plt.figure(figsize=(12, 6))
    plt.plot(backtest_results['timestamp'], backtest_results['balance'], label='Balance')
    plt.xlabel('Time')
    plt.ylabel('Balance')
    plt.title('Balance Over Time')
    plt.legend()
    if save_path:
        plt.savefig(save_path)
        print(f"Plot saved as {save_path}")
    else:
        plt.show()