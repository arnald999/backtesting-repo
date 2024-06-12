import ccxt

# Initialize the Delta Exchange object
exchange = ccxt.delta()

# List all available API functions
available_functions = exchange.has

# Filter out only the public API functions (typically not requiring authentication)
public_api_functions = {key: value for key, value in available_functions.items() if value and 'fetch' in key}

print("List of all free (public) API functions available in Delta Exchange:")
for func in public_api_functions:
    print(func)