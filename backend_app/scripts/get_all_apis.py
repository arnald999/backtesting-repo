import ccxt

# Get a list of all available exchanges in ccxt
# exchanges = ccxt.exchanges
exchanges = ["delta"]

# Loop through each exchange and list its methods
for exchange_id in exchanges:
    exchange_class = getattr(ccxt, exchange_id)
    methods = dir(exchange_class)
    print(f"Exchange: {exchange_id}")
    print(f"Number of methods: {len(methods)}")
    print("Methods:")
    for method in methods:
        print(f"- {method}")
    print("=" * 50)