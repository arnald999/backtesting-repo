from data_pull.data_connection import DataConnection

if __name__ == '__main__':
    """
    DATA: Read data_pull from API and create bar
        Input: symbol, history{from, to}/live, time/volume, 1m/1mm
        Methodology: First save data_pull of 1m if not present
                     Create method to either convert to time or volume
        Outputs: iterable object
    """

    # symbol='BTC/USD:BTC', history={"from": None, "to": None}
    data = DataConnection(exchange="Binance")
    data.store_exchange_raw_data(from_date="2021-01-01", to_date="2021-12-31")
    # x = data.fetch_raw_data(("2021-01-02", "2021-01-03"))
    # iter_data = data.fetch_raw_data(("2019-01-01", "2019-02-01"))
    # x = data.fetch_raw_data(1)
    pass
    # iter_candles = data.time_bar(bar_count="1m") 2024-08-10

    """
    FEATURES: Create features
        Input: Data iterable object, features symbol with its param 
        Methodology: Calculate features
        Outputs: iterable object
    """



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