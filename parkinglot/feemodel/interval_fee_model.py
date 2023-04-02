import constants
from feemodel.fee_model import FeeModel


class HourlyIntervalFeeModel(FeeModel):
    def __init__(self):
        self.rates = None

    def find_interval(self, slot_type, num_of_hours):
        for interval in self.rates[slot_type].keys():
            if interval[0] <= num_of_hours:
                if interval[1] is None or interval[1] > num_of_hours:
                    return interval

        raise Exception("Duration of parking  provided: " + str(num_of_hours) + " but no corresponding time interval slab was defined. Existing intervals are : ",
                        list(self.rates[slot_type].keys()))

    def calculate_fee(self, duration, lot, slot_type):
        hours = duration.seconds/constants.SECONDS_IN_HOUR
        try:
            interval = self.find_interval(slot_type, hours)
            return self.rates[slot_type][interval]
        except Exception as e:
            print("Error in calculation of parking fee:" + str(e))
            raise

