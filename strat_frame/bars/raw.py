import math
from typing import List

from strat_frame.constants import OrderBook, BarBook


class Tick(object):
    def __init__(self):
        self._tick_snapshot = OrderBook()
        self._prv_volume = 0

    def __getitem__(self, attr):
        return getattr(self._tick_snapshot, attr)

    def __getattr__(self, attr):
        return getattr(self._tick_snapshot, attr)

    @property
    def tick_volume(self):
        return self._tick_snapshot.volume - self._prv_volume

    def update(self, tick: OrderBook):
        self._prv_volume = self._tick_snapshot.volume

        self._tick_snapshot = tick


class Bar(Tick):
    def __init__(self):
        super().__init__()
        self._data_bar: List[BarBook] = [BarBook()]

        self._high_low = tuple()
        self._first_bar = True
        self._last_bar_close, self._prev_ltp, self._prev_b = math.nan, math.nan, 1

    def _bar_update(self, is_new_bar: bool):
        _timestamp = self.timestamp

        data_bar = self._data_bar
        bar_struct = data_bar[-1]
        high_low = self._high_low

        _ltp = self.close
        _high, _low = self.high, self.low
        _volume = self.tick_volume

        _b = _ltp - self._prev_ltp
        if _b == 0 or math.isnan(_b):
            _b = self._prev_b
        else:
            _b = int(_b / abs(_b))

        if is_new_bar:
            if self._first_bar:
                self._first_bar = False
            else:  # Adding last bar into the list
                ret = math.log10(bar_struct.close / self._last_bar_close)
                bar_struct.log_return = ret
                self._last_bar_close = bar_struct.close
                data_bar.append(BarBook())
                bar_struct = data_bar[-1]

            # Start creating new one
            bar_struct.timestamp = _timestamp
            bar_struct.open, bar_struct.high, bar_struct.low = _ltp, _ltp, _ltp

            if len(high_low) > 0:
                if high_low[0] != _high:
                    bar_struct.high = _high
                elif high_low[1] != _low:
                    bar_struct.low = _low

        else:
            if _ltp > bar_struct.high:
                bar_struct.high = _ltp
            elif _ltp < bar_struct.low:
                bar_struct.low = _ltp

            if len(high_low) > 0:
                if high_low[0] != _high:
                    bar_struct.high = _high
                elif high_low[1] != _low:
                    bar_struct.low = _low

            bar_struct.volume += _volume

        bar_struct.close = _ltp
        self._high_low = (_high, _low)
        self._prev_ltp = _ltp
        self._prev_b = _b


