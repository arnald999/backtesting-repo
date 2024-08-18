import datetime

from .raw import Bar
from strat_frame.constants import OrderBook


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
        super().update(tick)

        is_new_bar: bool
        if tick.exchange_timestamp - self._last_time > self._timedelta:
            is_new_bar = True
            self._last_time = tick.exchange_timestamp
        else:
            is_new_bar = False

        self._bar_update(is_new_bar)


class VolumeBars(Bar):
    def __init__(self, volume_threshold=20000):
        super().__init__()
        self._volumedelta: int = volume_threshold
        self._last_time: int = 0
