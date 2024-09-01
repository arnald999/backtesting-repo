from typing import NamedTuple
from dataclasses import dataclass

# Exchange data columns
exchange_data_columns =\
    ["exchange_timestamp", "open", "high", "low", "close", "volume"]


# Order book/data structure
# TODO: Think better data structure for this

class OrderBook(NamedTuple):
    timestamp: int = 0
    open: float = 0.0
    high: float = 0.0
    low: float = 1e9
    close: float = 0.0
    volume: int = 0


@dataclass
class CandleBook:
    timestamp: int = -1
    open: float = 0.0
    high: float = 0.0
    low: float = 1e9
    close: float = 0.0
    log_return: float = 0


@dataclass
class BarBook(CandleBook):
    volume: float = 0.0
