import constants
from feemodel.fee_model import FeeModel
from math import ceil


class DailyFeeModel(FeeModel):
    def __init__(self):
        self.rates =None

    def get_daily_rate(self, slot_type):
        # Use the interval (24, None) to represent daily flat rate
        return self.rates[slot_type][(24, None)]

    def find_interval(self, slot_type, num_of_hours):
        for interval in self.rates[slot_type].keys():
            if interval[0] <= num_of_hours:
                if interval[1] is None or interval[1] > num_of_hours:
                    return interval

        raise Exception("Duration of parking  provided: " +
                        str(num_of_hours) +
                        " but no corresponding time interval slab was defined. Existing intervals are : ",
                        list(self.rates[slot_type].keys()))

    def calculate_flat_daily_rate(self, slot_type, num_of_hours):
        num_of_days = ceil(num_of_hours/constants.HOURS_IN_DAY)
        flat_daily_rate = self.get_daily_rate(slot_type)
        return flat_daily_rate * num_of_days

    def calculate_fee(self, duration, lot, slot_type):
        num_of_hours = duration.seconds/constants.SECONDS_IN_HOUR
        if num_of_hours < constants.HOURS_IN_DAY:
            try:
                interval = self.find_interval(slot_type, num_of_hours)
                return self.rates[slot_type][interval]
            except Exception as e:
                print("Error in calculation of parking fee:" + str(e))
                raise
        else:
            return self.calculate_flat_daily_rate(slot_type, num_of_hours)