import ccxt
import backtrader as bt
import pandas as pd
import time


# Define a live data feed using CCXT
class LiveData(bt.feeds.PandasData):
    params = (
        ('datetime', None),
        ('open', -1),
        ('high', -1),
        ('low', -1),
        ('close', -1),
        ('volume', -1),
        ('openinterest', -1),
    )


def fetch_live_data(exchange, symbol, timeframe, since):
    data = exchange.fetch_ohlcv(symbol, timeframe, since)
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    return df


class SmaCross(bt.Strategy):
    params = (('pfast', 10), ('pslow', 30),)

    def __init__(self):
        self.sma1 = bt.indicators.SimpleMovingAverage(self.datas[0].close, period=self.params.pfast)
        self.sma2 = bt.indicators.SimpleMovingAverage(self.datas[0].close, period=self.params.pslow)
        self.crossover = bt.indicators.CrossOver(self.sma1, self.sma2)

    def next(self):
        if self.crossover > 0:  # fast crosses slow to the upside
            self.buy()
        elif self.crossover < 0:  # fast crosses slow to the downside
            self.sell()


def run_strategy():
    # Initialize exchange
    exchange = ccxt.delta()

    # Symbol and timeframe
    symbol = 'BTC/USDT'
    timeframe = '1m'

    # Initialize Cerebro engine
    cerebro = bt.Cerebro()
    cerebro.addstrategy(SmaCross)

    # Set initial cash
    cerebro.broker.setcash(10000.0)

    # Fetch initial data for initialization
    since = exchange.parse8601('2022-01-01T00:00:00Z')
    df = fetch_live_data(exchange, symbol, timeframe, since)

    # Create a data feed for Backtrader
    data_feed = LiveData(dataname=df)

    # Add data feed to Cerebro
    cerebro.adddata(data_feed)

    # Print starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run the initial backtest
    cerebro.run()

    # Print final conditions
    print('Ending Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Plot the result
    cerebro.plot()

    # Continuous live data fetching
    while True:
        # Fetch the latest data
        since = exchange.parse8601(df.index[-1].strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
        new_df = fetch_live_data(exchange, symbol, timeframe, since)

        # Check if there is new data
        if not new_df.empty and new_df.index[-1] > df.index[-1]:
            df = pd.concat([df, new_df]).drop_duplicates()
            data_feed = LiveData(dataname=df)
            cerebro.adddata(data_feed)
            cerebro.run()
            print('Updated Portfolio Value: %.2f' % cerebro.broker.getvalue())

        # Wait for the next interval
        time.sleep(60)  # Sleep for 1 minute (adjust as necessary)


if __name__ == '__main__':
    run_strategy()
