from data_pull.data_connection import DataConnection
from bars.bars import VolumeBars

if __name__ == '__main__':
    """
    DATA: Read data_pull from API and create bar
        Input: symbol, history{from, to}/live, time/volume, 1m/1mm
        Methodology: First save data_pull of 1m if not present
                     Create method to either convert to time or volume
        Outputs: iterable object
    """

    # symbol='BTC/USD:BTC', history={"from": None, "to": None}
    # data = DataConnection(exchange="Binance")
    # data.store_exchange_raw_data(from_date="2023-01-01", to_date="2023-12-31")
    # x = data.fetch_raw_data(("2021-01-02", "2021-01-03"))
    data = DataConnection(exchange="Binance")
    volume_bars = VolumeBars()
    iter_data = data.fetch_raw_data(("2019-01-01", "2019-02-01"))
    while True:
        # x = data.fetch_raw_data(1)
        iter_candles = volume_bars.update(next(iter_data)) # 2024-08-10

    x = 0

    # Think how to streamline data from self._data_bar List structure

    """
    FEATURES: Create features
        Input: Data iterable object, features symbol with its param 
        Methodology: Calculate features
        Outputs: iterable object
    """

    # FIND A WAY TO USE SAME BAR CREATE FUNCTION FOR TICK AND FEATURE


    """
    BACKTEST: Backtesting
        Input: Features iterable object
        Methodology: To create validation and train
                     Create 2d array
                     Performance metrics
                     Visualization
        Outputs: 
    
    LIVE:
        Input: Features iterable object
        Methodology: Calculate signals
                     Check its real time performance
        Outputs: 
    """

    pass