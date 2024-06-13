import ccxt
import time

# Replace with your actual API keys
api_key = 'YOUR_API_KEY'
api_secret = 'YOUR_API_SECRET'

# Initialize the exchange
exchange = ccxt.delta({
    'apiKey': api_key,
    'secret': api_secret,
    'enableRateLimit': True,  # Enabling rate limit handling
    'options': {
        'defaultType': 'future',  # Adjust as needed (future, option)
    },
})


# Fetch account balance
def fetch_balance():
    try:
        balance = exchange.fetch_balance()
        print("Account balance:")
        print(balance)
    except ccxt.BaseError as e:
        print(f"Error fetching balance: {str(e)}")


# Fetch market data
def fetch_market_data(symbol='BTC/USDT'):
    try:
        ticker = exchange.fetch_ticker(symbol)
        print(f"Market data for {symbol}:")
        print(ticker)
    except ccxt.BaseError as e:
        print(f"Error fetching market data: {str(e)}")


# Place a test order (assuming the test environment allows it)
def place_test_order(symbol='BTC/USDT', order_type='limit', side='buy', amount=0.01, price=30000):
    try:
        order = exchange.create_order(symbol, order_type, side, amount, price)
        print("Order placed:")
        print(order)
    except ccxt.BaseError as e:
        print(f"Error placing order: {str(e)}")


# Cancel an order
def cancel_order(order_id, symbol='BTC/USDT'):
    try:
        result = exchange.cancel_order(order_id, symbol)
        print(f"Order {order_id} cancelled:")
        print(result)
    except ccxt.BaseError as e:
        print(f"Error cancelling order: {str(e)}")


# Fetch open orders
def fetch_open_orders(symbol='BTC/USDT'):
    try:
        open_orders = exchange.fetch_open_orders(symbol)
        print(f"Open orders for {symbol}:")
        print(open_orders)
    except ccxt.BaseError as e:
        print(f"Error fetching open orders: {str(e)}")


# Main function to demonstrate the API usage
def main():
    fetch_balance()
    fetch_market_data()
    place_test_order()
    time.sleep(5)  # Wait for a while before fetching open orders
    fetch_open_orders()


# Run the main function
if __name__ == "__main__":
    main()
