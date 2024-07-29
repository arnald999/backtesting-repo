"""

Methodology:
    - Functions to save data in local (both historical and live) orderbook, 1m
    - Read local data, API data (both historical and live)

Return:
    - Iterable object which returns row data

"""
import os

DIR_PATH = os.path.join(os.path.dirname(__file__))
