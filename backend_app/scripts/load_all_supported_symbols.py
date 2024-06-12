import ccxt
import time

# Initialize the Delta Exchange API
exchange = ccxt.delta()

try:
    # Load markets to get the supported symbols
    exchange.load_markets()

    # Search for the symbol containing 'BTC' and 'USD'
    symbol = None
    for market_symbol in exchange.symbols:
        if 'BTC' in market_symbol and 'USD' in market_symbol:
            symbol = market_symbol
            break

    if symbol:
        # Set the timeframe to 1 minute
        timeframe = '1m'

        # Fetch historical candlestick data
        since = exchange.parse8601('2024-06-01T00:00:00Z')  # Start date
        candles = exchange.fetch_ohlcv(symbol, timeframe, since)

        # Calculate time per minute
        if len(candles) > 1:
            time_per_minute = (candles[1][0] - candles[0][0]) / 1000  # Convert milliseconds to seconds
            print(f"Time per minute for {symbol}: {time_per_minute} seconds")
        else:
            print(f"Not enough data available for {symbol} to calculate time per minute.")

    else:
        print("BTC/USD trading pair not found on Delta Exchange.")

except ccxt.NetworkError as e:
    print(f"Network error: {e}")
except ccxt.ExchangeError as e:
    print(f"Exchange error: {e}")
except Exception as e:
    print(f"Error: {e}")