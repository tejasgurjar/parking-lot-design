from feemodel.intervaltable.validator import IntervalTableValidator


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

        for interval in sorted(intervals_map.keys(), key=lambda e: e[0]):
            table[cls.INTERVALS].append(interval)
            table[cls.VALUES].append(intervals_map[interval])

        return table

    def find_interval(self, value):
        for i, interval in enumerate(self.intervals_table[self.INTERVALS]):
            lo, hi = interval
            if value >= lo:
                if hi is None or value <= hi:
                    return i
        raise Exception(f"Value {value} not found in any interval. Existing intervals: ", self.intervals)

    def get_interval(self, interval_id):
        return self.intervals_table[self.INTERVALS][interval_id]

    def get_value(self, interval_id):
        return self.intervals_table[self.VALUES][interval_id]