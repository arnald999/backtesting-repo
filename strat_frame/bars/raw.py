import math

from strat_frame.constants import OrderBook, CandleBook, BarBook


class Tick(object):
    def __init__(self):
        self._tick_snapshot = OrderBook()
        self._prv_volume = 0

    def __getattr__(self, attr):
        return getattr(self._tick_snapshot, attr)

    @property
    def tick_volume(self):
        return self._tick_snapshot.volume - self._prv_volume

    @property
    def book(self):
        return self._tick_snapshot

    def update(self, tick: OrderBook):
        self._prv_volume = self._tick_snapshot.volume

        self._tick_snapshot = tick


class Candle(object):
    def __init__(self):
        self._tick = Tick()

        self._book = self._curr_book()
        self._prev_candle_close: float = math.nan
        self.is_new: bool = False

    def __getattr__(self, attr):
        return getattr(self._book, attr)

    def _curr_book(self) -> CandleBook:
        return CandleBook()

    def _initialize(self):
        self._book.timestamp = self._tick.timestamp
        self._book.open = self._tick.open
        self._book.high = self._tick.high
        self._book.low = self._tick.low
        self._book.close = self._tick.close

    @property
    def book(self):
        return self._book

    def update(self, tick: OrderBook):
        self._tick.update(tick)

        if self.is_new:
            self._prev_candle_close = self._book.close
            self._initialize()

        self._book.high = max(self._book.high, self._tick.high)
        self._book.low  = min(self._book.low, self._tick.low)
        self._book.close = self._tick.close
        self._book.log_return = self._book.close / self._prev_candle_close


class Bar(Candle):
    def __init__(self):
        super().__init__()

    def _curr_book(self) -> BarBook:
        return BarBook()

    def _initialize(self):
        super()._initialize()
        self._book.volume = 0

    def update(self, tick: OrderBook):
        super().update(tick)

        self._book.volume += self._tick.tick_volume


