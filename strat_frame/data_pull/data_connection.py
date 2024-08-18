import os
import re
import ccxt
import time
import datetime
import numpy as np
import pandas as pd
import polars as pl
from functools import singledispatchmethod

from . import DIR_PATH
from strat_frame.constants import exchange_data_columns


class DataConnection:
    def __init__(self, exchange: str = "Binance", symbol: str = 'BTCUSD'):
        assert exchange in ["Delta", "Binance"]
        self._exchange: str = exchange.lower()
        self._symbol: str = symbol.lower()
        # always pick 1m data; time or volume bars will create later
        self._timeframe = "1m"
        self._dir_path = os.path.join(DIR_PATH, "data\\ohlcv", self._symbol)
        self._exchange_cols = exchange_data_columns

        # Binance info
        self._binance_symbol = {"btcusd": "BTC/USDT"}

    @staticmethod
    def _exchange_raw_data(exchange, symbol, timeframe, since, limit):
        return exchange.fetch_ohlcv(
            symbol=symbol, timeframe=timeframe, since=since, limit=limit
        )

    def store_exchange_raw_data(self, from_date: str, to_date: str):
        exchange = getattr(ccxt, self._exchange)()
        symbol = eval(f"self._{self._exchange}_symbol")[self._symbol]
        timeframe = self._timeframe
        since_timestamp = exchange.parse8601(f"{from_date} 00:00:00.0")
        to_timestamp = exchange.parse8601(f"{to_date} 00:00:00.0")
        exchange_cols = self._exchange_cols

        # Make lazy dataframe of all the historical data
        # datetime.datetime.fromtimestamp(df[-1][0]/1000, tz=datetime.timezone.utc)
        all_dates = list()
        df = None
        while since_timestamp < to_timestamp:
            _df = DataConnection._exchange_raw_data(
                exchange=exchange, symbol=symbol, since=since_timestamp, timeframe=timeframe, limit=1000
            )
            since_timestamp = _df[-1][0]

            # Add date and time in separate columns
            _df = pd.DataFrame(_df)
            date_time = (pd.to_datetime(_df[0] / 1000, unit="s"))
            _df.columns = exchange_cols
            _df["date"] = date_time.dt.strftime('%Y%m%d').astype("int")

            # Gather unique dates
            print(_df["date"].unique())
            all_dates.extend(list(_df["date"].unique()))

            # Append in lazy dataframe
            _df = pl.DataFrame(_df).lazy()
            df = _df if df is None else pl.concat([df, _df])

            time.sleep(5)

        from_date_int = int(from_date[:4] + from_date[5:7] + from_date[8:10])
        to_date_int = int(to_date[:4] + to_date[5:7] + to_date[8:10])

        dir_path = self._dir_path
        all_dates = set(all_dates)
        for curr_date_int in all_dates:
            if from_date_int <= curr_date_int <= to_date_int:
                _df = df.filter(pl.col("date") == curr_date_int).collect()
                if len(_df) > 0:
                    _df.drop_in_place("date")
                    _df.write_parquet(os.path.join(dir_path, f"{curr_date_int}"))
        pass

    @singledispatchmethod
    def fetch_raw_data(self, arg):
        raise NotImplementedError("Implement historical/live fetch raw data")

    @fetch_raw_data.register
    def _(self, arg: tuple):
        """
        Fetch historical data

        Args:
            arg: ("2018-01-01", "2024-01-01")

        Returns:
            Iterator: Row by row
        """
        print("In")
        from_date, to_date = arg
        from_date_int = int(from_date[:4] + from_date[5:7] + from_date[8:10])
        to_date_int = int(to_date[:4] + to_date[5:7] + to_date[8:10])

        dir_path = self._dir_path
        dir_list = np.array(os.listdir(dir_path)).astype(int)
        dir_list.sort()

        if to_date_int > dir_list[-1]:
            last_available_date = str(dir_list[-1])
            last_available_date = (f"{last_available_date[:4]}-"
                                   f"{last_available_date[4:6]}-"
                                   f"{last_available_date[6:8]}")
            self.store_exchange_raw_data(last_available_date, to_date)

        for curr_date_int in dir_list:
            if from_date_int < curr_date_int < to_date_int:
                _df = pl.read_parquet(os.path.join(dir_path, f"{curr_date_int}"))
                _df = _df.transpose()
                for row in _df.iter_columns():
                    x = 0
                    # yield row.to_numpy(allow_copy=False)

    @fetch_raw_data.register
    def _(self, arg: int):
        """
            Fetch live data
        Args:
            arg: limit = 1
        Returns:
            Iterator: Live data
        """
        limit = arg
        exchange = getattr(ccxt, self._exchange)()
        symbol = eval(f"self._{self._exchange}_symbol")[self._symbol]
        timeframe = self._timeframe

        while True:
            _df = DataConnection._exchange_raw_data(
                exchange=exchange, symbol=symbol, timeframe=timeframe, since=None, limit=limit
            )
            latest_data = np.array(_df[-1])
            # float_timestamp = int(latest_data[0]/1000) + float(latest_data[0] % 1000)/1000
            # latest_timestamp = datetime.datetime.fromtimestamp(float_timestamp)
            # latest_data_date = int(latest_timestamp.date().strftime('%Y%m%d'))
            # latest_data_time = latest_timestamp.time()

            x = 0
            # yield latest_data
            time.sleep(2)

    def fetch_live_orderbook(self):
        pass


