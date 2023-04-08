from feemodel.interval_table.validator import IntervalTableValidator


class OutOfRangeException(Exception):
    def __init__(self):
        super().__init__()


class IntervalTable(object):
    INTERVALS='intervals'
    VALUES='values'

    def __init__(self, intervals_map):
        self.validator = IntervalTableValidator()
        self.validator.validate(intervals_map)
        self.intervals_table = IntervalTable.create_table(intervals_map)

    @classmethod
    def create_table(cls, intervals_map):
        table = dict()
        table[cls.INTERVALS] = []
        table[cls.VALUES] = []

        intervals_sorted = sorted(intervals_map.keys(), key=lambda e: e[0])

        for interval in intervals_sorted:
            # Exclude the infinity interval
            if interval[1] is None:
                continue
            table[cls.INTERVALS].append(interval)
            table[cls.VALUES].append(intervals_map[interval])

        return table

    def get_last_interval(self):
        return len(self.intervals_table[self.INTERVALS])-1

    def get_last_interval_value(self):
        return self.intervals_table[self.INTERVALS][-1]

    def get_max_hi(self):
        return self.get_last_interval_value()[1]

    def find_interval(self, value):

        if value >= self.get_max_hi():
            raise OutOfRangeException()

        for i, interval in enumerate(self.intervals_table[self.INTERVALS]):
            lo, hi = interval
            if value >= lo:
                if hi is None or value < hi:
                    return i
        raise Exception(f"Value {value} not found in any interval. Existing intervals: ", self.intervals)

    def get_interval(self, interval_id):
        return self.intervals_table[self.INTERVALS][interval_id]

    def get_value(self, interval_id):
        return self.intervals_table[self.VALUES][interval_id]