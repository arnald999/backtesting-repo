from strat_frame.data_pull.data_connection import DataAcquisition

if __name__ == '__main__':
    """
    DATA: Read data_pull from API and create bar
        Input: symbol, history{from, to}/live, time/volume, 1m/1mm
        Methodology: First save data_pull of 1m if not present
                     Create method to either convert to time or volume
        Outputs: iterable object
    """

    # symbol='BTC/USD:BTC', history={"from": None, "to": None}
    data = DataAcquisition()

    iter_candles = data.time_bar(bar_count="1m")

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