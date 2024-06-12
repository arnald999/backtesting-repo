from backend_app.trading_algo_suite.data.acquisition import DataAcquisition
from backend_app.trading_algo_suite.features.vwap import calculate_standard_vwap, calculate_rolling_vwap, \
    calculate_intraday_vwap, visualize_vwaps

if __name__ == "__main__":
    data = DataAcquisition()

    # candle_1m = data.fetch_ohlcv_for_timeframe('BTC/USD:BTC', '1m', get_delta_delayed_time_iso8601(2))

    # candle_1m = data.fetch_ohlcv_for_timeframe('BTC/USD:BTC', '1m', None)

    # candle_3m = data.fetch_ohlcv_for_timeframe('BTC/USD:BTC', '3m', get_delta_delayed_time_iso8601(60))
    # data.aggregate_ohlcv_for_timeframe(candle_3m)

    # timeframe_minutes = data.fetch_timeframe_for_volume('BTC/USD:BTC', '1m', 30000)
    # print(timeframe_minutes)

    # candle_1m = data.fetch_ohlcv_for_timeframe('BTC/USD:BTC', '1m', None)
    # moving_averages = ['SMA_20', 'EMA_20', 'WMA_20']
    # res = calculate_sma(candle_1m, 20)
    # res = calculate_ema(res, 20)
    # res = calculate_wma(res, 20)
    # plot_moving_averages(res, moving_averages, 'mva_plot.png')
    # print(res)

    # candle_1m = data.fetch_ohlcv_for_timeframe('BTC/USD:BTC', '1m', None, 5000)
    # res = calculate_macd(candle_1m)
    # plot_macd(res, 'macd_plot.png')

    # candle_1m = data.fetch_ohlcv_for_timeframe('BTC/USD:BTC', '1m', None, 1000)
    # res1 = calculate_bollinger_bands(candle_1m, 20, 2)
    # res1 = calculate_exponential_bollinger_bands(res1, 20, 2)
    # res1 = calculate_percentage_bollinger_bands(res1, 20, 0.1)
    # res1 = calculate_asymmetric_bollinger_bands(res1, 20, 2, 1.5)
    # res2 = calculate_bollinger_bands(candle_1m, 30, 2.5)
    # res2 = calculate_exponential_bollinger_bands(res2, 30, 2.5)
    # res2 = calculate_percentage_bollinger_bands(res2, 30, 0.1)
    # res2 = calculate_asymmetric_bollinger_bands(res2, 30, 2.5, 1.5)
    # # List of DataFrames containing price data
    # df_list = [res1, res2]
    # # List of window sizes for calculating SMAs
    # window_list = [20, 30]
    # # List of numbers of standard deviations for calculating Bollinger Bands
    # num_std_list = [2, 2.5]
    # # List of legend labels for each set of Bollinger Bands
    # legend_labels = ['Set 1', 'Set 2']
    # plot_multiple_bollinger_bands(df_list, window_list, num_std_list, legend_labels, 'bollinger_bands.png')

    # candle_1m = data.fetch_ohlcv_for_timeframe('BTC/USD:BTC', '1m', None, 5000)
    # df = calculate_traditional_rsi(candle_1m)
    # df = calculate_wilders_rsi(df)
    # df = calculate_modified_rsi(df)
    # plot_rsis(df, 'rsi_plot.png')
    # print(df)

    # candle_1m = data.fetch_ohlcv_for_timeframe('BTC/USD:BTC', '1m', None, 5000)
    # df = calculate_traditional_obv(candle_1m)
    # df = calculate_cumulative_obv(df)
    # df = calculate_smoothed_obv(df)
    # plot_obvs(df, 'obv_plot.png')
    # print(df)

    # candle_1m = data.fetch_ohlcv_for_timeframe('BTC/USD:BTC', '1m', None, 5000)
    # df = calculate_standard_vwap(candle_1m)
    # df = calculate_rolling_vwap(df, 14)
    # df = calculate_intraday_vwap(df)
    # visualize_vwaps(df, 'vwap_plot.png')
    # print(df)
