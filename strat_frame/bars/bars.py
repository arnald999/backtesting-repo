import datetime
from typing import List

from .raw import Tick, Bar
from strat_frame.constants import OrderBook, BarBook


class TimeBars(Bar):
    def __init__(self, timeframe="5m"):
        super().__init__()
        self._timedelta: int = TimeBars.convert_to_timedelta(timeframe)
        self._last_time: int = 0

    @staticmethod
    def convert_to_timedelta(timeframe: str):
        time_dict = {
            'm': 'minutes',
            's': 'seconds',
            'h': 'hours',
            'd': 'days',
        }

        num, unit = int(timeframe[:-1]), timeframe[-1]
        total_milliseconds = datetime.timedelta(**{time_dict[unit]: num})
        total_milliseconds = int(total_milliseconds.total_seconds() * 1000)

        return total_milliseconds

    def update(self, tick: OrderBook):

        if self.tick.timestamp - self._last_time > self._timedelta:
            self.is_new = True
            self._last_time = self.exchange_timestamp
        else:
            self.is_new = False

        super().update(tick)
        if self.is_new:
            self._data_bar.append(self.book)
        else:
            self._data_bar[-1] = self.book


class VolumeBars(Bar):
    def __init__(self, volume_threshold=20000):
        super().__init__()
        self._volumedelta: int = volume_threshold
        self._bar_volume: float = 0

        self._data_bar: List[BarBook] = [BarBook()]

    def update(self, tick: OrderBook):

        if self._bar_volume > self._volumedelta:
            self.is_new = True
            self._bar_volume = self.tick.tick_volume
        else:
            self.is_new = False
            self._bar_volume += self.tick.tick_volume

        super().update(tick)
        if self.is_new:
            self._data_bar.append(self.book)
        else:
            self._data_bar[-1] = self.book
