import ccxt

# Initialize the Delta Exchange object
exchange = ccxt.delta()

# List all available API functions
available_functions = exchange.has

# Filter out only the private API functions (those not typically public)
private_api_functions = {key: value for key, value in available_functions.items() if value and not key.startswith('fetch')}

print("List of all private API functions available in Delta Exchange:")
for func in private_api_functions:
    print(func)