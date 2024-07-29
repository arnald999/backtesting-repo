import os
import re
import ccxt
import datetime
import numpy as np
import pandas as pd
import polars as pl


class DataConnection:
    def __init__(self, exchange: str = "Local", symbol: str = "BTCUSD"):
        assert exchange in ["Local", "Delta", "Binance"]
        self._exchange: str = exchange.lower()
        self._symbol: str = symbol.lower()

    def _local_fetch_ohlcv(self, from_datetime: str, to_datetime: str):
        # from_datetime: "2018-01-01"
        # to_datetime: "2024-01-01"

        from_datetime = int(from_datetime[:4] + from_datetime[6:8] + from_datetime[10:12])
        to_datetime = int(to_datetime[:4] + to_datetime[6:8] + to_datetime[10:12])

        dir_path = os.path.join("data", "ohlcv", self._symbol.lower())
        dir_list = np.array(os.listdir(dir_path)).astype(int)
        dir_list.sort()
        for int_date in dir_list:
            if from_datetime < int_date < to_datetime:
                df = pl.read_parquet(os.path.join(dir_path, f"{int_date}"))

                for row in df.iter_slices():
                    paa

    def fetch_ohlcv(self, *args):
        return getattr(self, f"_{self._exchange}_fetch_ohlcv")(*args)

    def fetch_live_orderbook(self):
        pass


class Local(DataConnection):
    def __init__(self):
        super().__init__()

    def fetch_ohlcv(self, symbol):
        pass


class Delta(DataConnection):
    def __init__(self):
        self.exchange = ccxt.binance()
        xx = self.exchange.fetch_order_book(symbol="BTCUSDT", limit=2)
        s = 0

    def convert_datetime(self, time):
        return self.exchange.parse8601(time)

    def fetch_ohlcv_for_timeframe(self, symbol, timeframe='1m', since=None, limit=None):
        start_time = self.convert_datetime(since)
        # Fetch OHLCV data_pull
        candles = self.exchange.fetch_ohlcv(symbol, timeframe, start_time, limit)

        # Convert to dataframe
        df = pd.DataFrame(candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

        # Convert timestamp from milliseconds to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

        # Calculate percentage returns
        df['returns'] = df['close'].pct_change() * 100
        return df

