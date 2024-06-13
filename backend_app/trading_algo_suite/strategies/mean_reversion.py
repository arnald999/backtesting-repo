from backend_app.trading_algo_suite.features.trend_indicators.bollinger_bands import calculate_bollinger_bands


def mean_reversion_strategy(data, window=20, std_factor=2):
    data = calculate_bollinger_bands(data, window, std_factor)
    data['position'] = 0
    data['position'] = data.apply(lambda row: -1 if row['close'] > row['Upper Band'] else (1 if row['close'] < row['Lower Band'] else 0), axis=1)
    return data
