import ccxt
import pandas as pd
from backend_app.trading_algo_suite.data.time_converter import get_current_time_iso8601, get_delta_delayed_time_iso8601


class DataAcquisition:

    def __init__(self):
        self.exchange = ccxt.delta()

    def convert_datetime(self, time):
        return self.exchange.parse8601(time)

    def fetch_ohlcv_for_timeframe(self, symbol, timeframe='1m', since=None, limit=None):
        try:
            start_time = self.convert_datetime(since)
            # Fetch OHLCV data
            candles = self.exchange.fetch_ohlcv(symbol, timeframe, start_time, limit)

            # Convert to dataframe
            df = pd.DataFrame(candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

            # Convert timestamp from milliseconds to datetime
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

            # Calculate percentage returns
            df['returns'] = df['close'].pct_change() * 100
            return df

        except ccxt.NetworkError as e:
            print(f"Network error: {e}")
            return f"Network error: {e}"
        except ccxt.ExchangeError as e:
            print(f"Exchange error: {e}")
            return f"Exchange error: {e}"
        except Exception as e:
            print(f"Error: {e}")
            return f"Error: {e}"

    @staticmethod
    def aggregate_ohlcv_for_timeframe(df):
        try:
            json_val = {
                'timestamp': [df.iloc[-1]['timestamp']],
                'open': [df.iloc[0]['open']],
                'high': [df['high'].max()],
                'low': [df['low'].min()],
                'close': [df.iloc[-1]['close']],
                'volume': [df['volume'].sum()],
                'return': [(df.iloc[-1]['close'] - df.iloc[0]['open']) / df.iloc[0]['open'] * 100]
            }
            transformed_df = pd.DataFrame(json_val)
            return transformed_df

        except ccxt.NetworkError as e:
            print(f"Network error: {e}")
            return f"Network error: {e}"
        except ccxt.ExchangeError as e:
            print(f"Exchange error: {e}")
            return f"Exchange error: {e}"
        except Exception as e:
            print(f"Error: {e}")
            return f"Error: {e}"

    # TODO: Upgrade logic
    def fetch_timeframe_for_volume(self, symbol, timeframe, volume_threshold):
        try:
            # Fetch OHLCV data (you may need to adjust the limit based on your volume requirement)
            limit = 1000  # You can adjust this limit based on your needs
            since = None  # Fetch recent data
            ohlcv_data = self.exchange.fetch_ohlcv(symbol, timeframe, since, limit)

            # Create a DataFrame
            df = pd.DataFrame(ohlcv_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

            total_volume = 0
            start_time = None
            end_time = None

            # Iterate through OHLCV data
            for index, row in df.iterrows():
                if start_time is None:
                    start_time = row['timestamp']
                total_volume += row['volume']
                if total_volume >= volume_threshold:
                    end_time = row['timestamp']
                    break

            if start_time and end_time:
                # Calculate the timeframe in minutes
                timeframe_minutes = (end_time - start_time).total_seconds() / 60
                return timeframe_minutes
            else:
                return None
        except ccxt.NetworkError as e:
            print('Network error:', str(e))
            return None
        except ccxt.ExchangeError as e:
            print('Exchange error:', str(e))
            return None
        except Exception as e:
            print('Error:', str(e))
            return None

    # def fetch_open_interest(self, symbol):
    #     # Base URL for Delta Exchange API
    #     base_url = 'https://api.delta.exchange'
    #     try:
    #         # Replace with the correct endpoint for fetching OI data
    #         endpoint = f"{base_url}/futures/v1/historical/open-interest"
    #
    #         # Parameters for the request
    #         params = {
    #             'symbol': symbol,
    #             'period': '1m',  # Example period, adjust as needed
    #         }
    #
    #         response = requests.get(endpoint, params=params)
    #         data = response.json()
    #
    #         if 'result' in data:
    #             return data['result']
    #         else:
    #             return None
    #     except requests.RequestException as e:
    #         print('Network error:', str(e))
    #         return None
    #     except Exception as e:
    #         print('Error:', str(e))
    #         return None


if __name__ == "__main__":
    data = DataAcquisition()

    # candle_1m = data.fetch_ohlcv_for_timeframe('BTC/USD:BTC', '1m', get_delta_delayed_time_iso8601(2))

    # candle_1m = data.fetch_ohlcv_for_timeframe('BTC/USD:BTC', '1m', None)

    # candle_3m = data.fetch_ohlcv_for_timeframe('BTC/USD:BTC', '3m', get_delta_delayed_time_iso8601(60))
    # data.aggregate_ohlcv_for_timeframe(candle_3m)

    timeframe_minutes = data.fetch_timeframe_for_volume('BTC/USD:BTC', '1m', 30000)
    print(timeframe_minutes)
