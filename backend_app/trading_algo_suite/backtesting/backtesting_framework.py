import ccxt
import pandas as pd
import numpy as np
import time

# Initialize exchange
exchange = ccxt.delta()

# Symbol and timeframe
symbol = 'BTC/USDT'
timeframe = '1m'

# SMA parameters
pfast = 10
pslow = 30

# Portfolio management
initial_cash = 10000.0
cash = initial_cash
btc_balance = 0


def fetch_live_data(symbol, timeframe, since):
    data = exchange.fetch_ohlcv(symbol, timeframe, since)
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    return df


def calculate_sma(data, period):
    return data['close'].rolling(window=period).mean()


def generate_signals(data):
    data['sma1'] = calculate_sma(data, pfast)
    data['sma2'] = calculate_sma(data, pslow)
    data['signal'] = 0
    data['signal'][pfast:] = np.where(data['sma1'][pfast:] > data['sma2'][pfast:], 1, 0)
    data['position'] = data['signal'].diff()
    return data


def execute_trades(data):
    global cash, btc_balance
    for i in range(len(data)):
        if data['position'].iloc[i] == 1:
            # Buy signal
            amount_to_buy = cash / data['close'].iloc[i]
            btc_balance += amount_to_buy
            cash = 0
            print(f"Bought BTC at {data.index[i]} at price {data['close'].iloc[i]}")
        elif data['position'].iloc[i] == -1:
            # Sell signal
            cash += btc_balance * data['close'].iloc[i]
            btc_balance = 0
            print(f"Sold BTC at {data.index[i]} at price {data['close'].iloc[i]}")


def run_strategy():
    global cash
    # Fetch initial data for initialization
    since = exchange.parse8601('2022-01-01T00:00:00Z')
    df = fetch_live_data(symbol, timeframe, since)

    # Continuous live data fetching
    while True:
        # Fetch the latest data
        since = exchange.parse8601(df.index[-1].strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
        new_df = fetch_live_data(symbol, timeframe, since)

        # Check if there is new data
        if not new_df.empty and new_df.index[-1] > df.index[-1]:
            df = pd.concat([df, new_df]).drop_duplicates()

            # Generate signals
            df = generate_signals(df)

            # Execute trades
            execute_trades(df)

            # Print updated portfolio value
            portfolio_value = cash + btc_balance * df['close'].iloc[-1]
            print(f'Updated Portfolio Value: {portfolio_value:.2f}')

        # Wait for the next interval
        time.sleep(60)  # Sleep for 1 minute (adjust as necessary)


if __name__ == '__main__':
    run_strategy()
