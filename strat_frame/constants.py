from typing import NamedTuple
from dataclasses import dataclass

# Exchange data columns
exchange_data_columns =\
    ["exchange_timestamp", "open", "high", "low", "close", "volume"]


# Order book/data structure

class OrderBook(NamedTuple):
    exchange_timestamp: int = 0
    open: float = 0.0
    high: float = 0.0
    low: float = 0.0
    close: float = 0.0
    volume: int = 0


@dataclass
class BarBook:
    bar_timestamp: int = 0
    open: float = 0.0
    high: float = 0.0
    low: float = 0.0
    close: float = 0.0
    volume: int = 0
    buy_volume: int = 0
    sell_volume: int = 0
    log_return: float = 0