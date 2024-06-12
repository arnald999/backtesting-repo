import requests
import pandas as pd


def fetch_open_interest(symbol):
    # Base URL for Delta Exchange API
    base_url = 'https://api.delta.exchange'
    try:
        # Replace with the correct endpoint for fetching OI data
        endpoint = f"{base_url}/v2/tickers/{symbol}"

        # Parameters for the request
        params = {
            'symbol': symbol,
            'period': '1m',  # Example period, adjust as needed
        }

        response = requests.get(endpoint, params=params)
        data = response.json()

        if 'result' in data:
            return data['result']
        else:
            return None
    except requests.RequestException as e:
        print('Network error:', str(e))
        return None
    except Exception as e:
        print('Error:', str(e))
        return None


def main():
    # Example usage: Fetch Open Interest data for BTCUSD trading pair
    symbol = 'USD'

    oi_data = fetch_open_interest(symbol)

    if oi_data:
        # Convert to DataFrame
        df = pd.DataFrame(oi_data)
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')  # Adjust according to the actual data format
        print(df)
    else:
        print("Failed to fetch Open Interest data.")


if __name__ == "__main__":
    main()
