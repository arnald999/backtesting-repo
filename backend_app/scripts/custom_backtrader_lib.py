import backtrader as bt
import ccxt
import datetime
import time
import pandas as pd

# Custom Indicator
class CustomIndicator(bt.Indicator):
    lines = ('custom',)
    params = (('period', 20),)

    def __init__(self):
        self.addminperiod(self.params.period)

    def next(self):
        self.lines.custom[0] = (self.data.close[0] - self.data.close[-self.params.period]) / self.params.period

# Custom Strategy
class CustomStrategy(bt.Strategy):
    def __init__(self):
        self.custom_indicator = CustomIndicator(self.data)

    def next(self):
        if self.custom_indicator.custom[0] > 0:
            if not self.position:
                self.buy()
        elif self.custom_indicator.custom[0] < 0:
            if self.position:
                self.sell()

# Function to fetch real-time data from Delta Exchange
def fetch_realtime_data(symbol, timeframe='1m', limit=100):
    exchange = ccxt.delta()
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    return bt.feeds.PandasData(dataname=df)

# Function to run the strategy in a live environment
def run_live_strategy():
    cerebro = bt.Cerebro()

    # Add the custom strategy to cerebro
    cerebro.addstrategy(CustomStrategy)

    # Fetch real-time data
    data = fetch_realtime_data('BTC/USDT')
    cerebro.adddata(data)

    # Set the initial cash
    cerebro.broker.set_cash(10000)

    # Print out the starting conditions
    print(f'Starting Portfolio Value: {cerebro.broker.getvalue():.2f}')

    # Run the strategy
    cerebro.run()

    # Print out the final result
    print(f'Final Portfolio Value: {cerebro.broker.getvalue():.2f}')

    # Plot the result
    cerebro.plot()

if __name__ == "__main__":
    run_live_strategy()
