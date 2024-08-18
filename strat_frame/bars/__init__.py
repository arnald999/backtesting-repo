"""
Input: Takes iterable data object

Methodology:
    - Functions to create any data type ( orderbook, 1m) to time bars or volume bars
    - Read local data, API data (both historical and live)

Return:
    - Return iterable time/volume candles

"""

import os

DIR_PATH = os.path.join(os.path.dirname(__file__))