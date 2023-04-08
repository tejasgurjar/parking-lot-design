from constants import *


class IntervalTableValidator(object):
    def __init__(self, min_interval_value=0, max_interval_value=HOURS_IN_DAY):
        self.min_interval_value = min_interval_value
        self.max_interval_value = max_interval_value

    def validate(self, interval_map):
        prev_lo, prev_hi = None, None

        for interval in sorted(interval_map.keys(), key=lambda e: e[0]):
            lo, hi = interval
            if prev_hi is not None:
                if lo != prev_hi:
                    raise Exception (f"Interval {interval} does not align with previous interval {prev_lo}, {prev_hi}")

            if lo < self.min_interval_value:
                raise Exception(f"Interval {interval} has illegal lower limit value")

            if hi is not None and hi > self.max_interval_value:
                raise Exception(f"Interval {interval} has illegal upper limit value")

            prev_lo = lo
            prev_hi = hi

        inf_intervals = list(filter(lambda interval: interval[1] is None, interval_map.keys()))
        if len(inf_intervals) != 1:
            raise Exception ("Exactly one interval having 'None' value expected")

        zero_intervals = list(filter(lambda interval: interval[0] == self.min_interval_value, interval_map.keys()))
        if len(zero_intervals) != 1:
            raise Exception(f"Exactly one interval having {self.min_interval_value} expected")

        return True